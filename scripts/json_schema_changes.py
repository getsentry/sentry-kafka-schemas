from typing import (
    Any,
    Callable,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
    Tuple,
)

import sys
import subprocess
import tempfile
import json
import pkg_resources
import urllib.request


from sentry_kafka_schemas.sentry_kafka_schemas import (
    TopicData,
    _list_topics,
    _get_topic,
)

Change = Mapping[str, Any]


def _build_schema_to_topic_mapping() -> Mapping[str, TopicData]:
    rv = {}

    for topic_name in _list_topics():
        topic_data = _get_topic(topic_name)
        for schema in topic_data["schemas"]:
            filename = f"schemas/{schema['resource']}"
            rv[filename] = topic_data

    return rv


_SCHEMA_FILE_TO_TOPIC: Mapping[str, TopicData] = _build_schema_to_topic_mapping()

FileName = str
Repo = str
Version = Tuple[int, int, int]


def main() -> None:
    process_output = subprocess.check_output(
        [
            "git",
            "diff",
            "--diff-filter=M",
            "--name-only",
            "origin/main",
            "--",
            "./schemas",
        ],
    )
    lines = process_output.decode("utf8").splitlines()

    if not lines:
        return

    breaking_changes: MutableMapping[FileName, MutableSequence[Change]] = {}
    non_breaking_changes: MutableMapping[FileName, MutableSequence[Change]] = {}
    consumers: MutableMapping[Repo, MutableSequence[FileName]] = {}
    producers: MutableMapping[Repo, MutableSequence[FileName]] = {}

    for filename in lines:
        for consumer in _SCHEMA_FILE_TO_TOPIC[filename]["services"]["consumers"]:
            consumers.setdefault(consumer, []).extend(filename)
        for producer in _SCHEMA_FILE_TO_TOPIC[filename]["services"]["producers"]:
            producers.setdefault(producer, []).extend(filename)

        with tempfile.NamedTemporaryFile() as old_file:
            old_file_contents = subprocess.check_output(
                ["git", "show", f"origin/main:{filename}"]
            )
            old_file.write(old_file_contents)
            old_file.flush()

            for raw_change in subprocess.check_output(
                ["json-schema-diff", old_file.name, filename]
            ).splitlines():

                change: Change = json.loads(raw_change)
                if change["is_breaking"]:
                    breaking_changes.setdefault(filename, []).append(change)
                else:
                    non_breaking_changes.setdefault(filename, []).append(change)

    check_for_outdated_repos(consumers, producers)

    if breaking_changes:
        print(
            "<details><summary><strong>changes considered breaking</strong></summary>"
        )
        print_files_and_changes(breaking_changes)
        print("</details>")

    if non_breaking_changes:
        print("<details><summary><strong>benign changes</strong></summary>")
        print_files_and_changes(non_breaking_changes)
        print("</details>")

    if not non_breaking_changes and not breaking_changes:
        print(
            """\
There were changes to the JSON schema file, but we couldn't categorize any of
them. Therefore we don't know whether this change is safe to make.

This might be a gap in linting. Want to take a look at
https://github.com/getsentry/json-schema-diff/ and figure it out?"""
        )
        if "--no-exit-code" not in sys.argv:
            sys.exit(2)

    elif breaking_changes:
        print(
            """
⚠️ **This PR contains breaking changes.** Normally you should avoid that and make
your consumer backwards-compatible (meaning that updated consumers can still
accept old messages). There are a few exceptions:

* If consumers already require these invariants in practice, and you're
  just adjusting the JSON schema to reality, ignore this warning.

* If you know what you are doing, this change could potentially be rolled out
  to **producers** first, but that's not a flow we support.
"""
        )
        if "--no-exit-code" not in sys.argv:
            sys.exit(2)
    else:
        newline = "\n"
        print(
            f"""
✅ This PR should be safe to roll out to **consumers** first. Make sure to bump
the library in the following repos first:

```
{newline.join(consumers)}
```

...then in the other repos:

```
{newline.join(producers)}
```

Take a look at the README for how to release a new version of sentry-kafka-schemas.
        """
        )


def print_files_and_changes(file_to_changes: Mapping[str, Sequence[Change]]) -> None:
    print()
    for filename, changes in file_to_changes.items():
        print(f"**{filename}**")
        for change in changes:
            print_change(change)
    print()


_CHANGE_PRINTERS: MutableMapping[str, Callable[[Change], str]] = {}
ChangePrinter = Callable[[Change], str]


def _add_change_printer(f: ChangePrinter) -> ChangePrinter:
    _CHANGE_PRINTERS[f.__name__] = f
    return f


@_add_change_printer
def TypeRemove(change: Change) -> str:
    return f"Restricted the type of `{change['path']}`, as `{change['change']['TypeRemove']['removed']}` is no longer allowed"


@_add_change_printer
def PropertyRemove(change: Change) -> str:
    first_sentence = f"Removed a property `{change['change']['PropertyRemove']['removed']}` from `{change['path']}`"
    if change["change"]["PropertyRemove"]["lhs_additional_properties"]:
        return f"{first_sentence}, but it is still accepted via `additionalProperties=true`"
    else:
        return f"{first_sentence}, so it is no longer accepted. Maybe use `additionalProperties`?"


@_add_change_printer
def PropertyAdd(change: Change) -> str:
    if change["change"]["PropertyRemove"]["lhs_additional_properties"]:
        return f"Added a new property, but the consumer has been ignoring additional properties so far. This is probably still fine, but please double-check that the producer does not already send this property with a different type in practice than you defined in this schema."
    else:
        return "Added a new property."


def print_change(change: Change) -> None:
    change = dict(change)
    change.pop("is_breaking")

    printer = _CHANGE_PRINTERS.get(next(iter(change["change"])))
    print("- ", end="")
    if printer:
        print(f"{printer(change)}")
        print()
        print("  ", end="")

    print("```")
    print(f"  {json.dumps(change)}")
    print("  ```")
    print()


def parse_version(string: str) -> Version:
    constraints = []
    for constraint in string.split(","):
        if " " in constraint:
            operator, version = constraint.split(" ", 1)
        else:
            version = constraint
            operator = ""

        constraints.append((version, operator))

    constraints.sort(
        key=lambda version_and_operator: version_and_operator[1] in (">", ">=")
    )
    version, _ = constraints[0]
    x, y, z = map(int, version.split("."))
    return x, y, z


def format_version(version: Version) -> str:
    return ".".join(map(str, version))


def check_for_outdated_repos(
    consumers: Mapping[Repo, Sequence[FileName]],
    producers: Mapping[Repo, Sequence[FileName]],
) -> None:
    latest_version = parse_version(
        pkg_resources.get_distribution("sentry-kafka-schemas").version
    )

    sboms = {}
    for repo in {*consumers, *producers}:
        with urllib.request.urlopen(
            f"https://api.github.com/repos/{repo}/dependency-graph/sbom"
        ) as f:
            sboms[repo] = json.load(f)

    used_versions: MutableMapping[Repo, MutableMapping[str, Version]] = {}
    for repo, sbom in sboms.items():
        repo_used_versions = used_versions[repo] = {}

        for package in sbom["sbom"]["packages"]:
            name = package["name"]
            if name not in ("pip:sentry-kafka-schemas", "rust:sentry-kafka-schemas"):
                continue

            version = parse_version(package["versionInfo"])

            # for some reason, github's SBOM (for sentry, relay, snuba)
            # contains all versions of the package ever used of the past. only
            # consider the latest one.
            if name not in repo_used_versions or repo_used_versions[name] < version:
                repo_used_versions[name] = version

    print("**versions in use:**")
    print()
    print(
        "*The following repositories use one of the schemas you are editing. "
        "It is recommended to roll out schema changes in small PRs, meaning "
        "that if those used versions lag behind the latest, it is probably "
        "best to update those services before rolling out your change.*"
    )

    for repo, package_to_version in used_versions.items():
        for package, version in package_to_version.items():
            print(
                f"- {repo}: `{package}=={format_version(version)}`"
                f"{upgrade_button(latest_version, version, repo)}"
            )

    print()
    print(f"**latest version:** {format_version(latest_version)}")
    print()


def upgrade_button(latest_version: Version, version: Version, repo: Repo) -> str:
    if latest_version == version:
        return ""

    return f" ([upgrade](https://github.com/{repo}/actions/workflows/bump-version.yml))"


if __name__ == "__main__":
    main()
