import sys
import subprocess
import tempfile
import json
from typing import Any, Callable, Mapping, MutableMapping, MutableSequence, Sequence

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

    breaking_changes: MutableMapping[str, MutableSequence[Change]] = {}
    non_breaking_changes: MutableMapping[str, MutableSequence[Change]] = {}
    consumers: MutableSequence[str] = []
    producers: MutableSequence[str] = []

    if not lines:
        return

    for filename in lines:
        consumers.extend(_SCHEMA_FILE_TO_TOPIC[filename]["services"]["consumers"])
        producers.extend(_SCHEMA_FILE_TO_TOPIC[filename]["services"]["producers"])

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

    if breaking_changes:
        print("**changes considered breaking:**")
        print_files_and_changes(breaking_changes)

    if non_breaking_changes:
        print("<details><summary>benign changes:</summary>")
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
            """\
**This PR contains breaking changes.** Normally you should avoid that and make
your consumer forwards-compatible (meaning that updated consumers can still
accept old messages).

If you know what you are doing, this change could potentially be rolled out
to **producers**
first.
"""
        )
        if "--no-exit-code" not in sys.argv:
            sys.exit(2)
    else:
        print(
            f"""\
This PR should be safe to roll out to **consumers** first. Make sure to bump
the library in the following repos first:

```
{json.dumps(consumers)}
```

...then in the other repos:

```
{json.dumps(producers)}
```

Take a look at the README for how to release a new version of sentry-kafka-schemas.
        """
        )

    # Manually add comment marker that is still expected by action-migrations.
    print("<!-- This PR has a migration; here is the generated SQL for `json-schema-changes` () -->")


def print_files_and_changes(file_to_changes: Mapping[str, Sequence[Change]]) -> None:
    print("```")
    for filename, changes in file_to_changes.items():
        print(f"### {filename}")
        for change in changes:
            print_change(change)
    print("```")


_CHANGE_PRINTERS: MutableMapping[str, Callable[[Change], str]] = {}
ChangePrinter = Callable[[Change], str]


def _add_change_printer(f: ChangePrinter) -> ChangePrinter:
    _CHANGE_PRINTERS[f.__name__] = f
    return f


@_add_change_printer
def TypeRemove(change: Change) -> str:
    return f"Restricted the type of {change['path']}, as {change['change']['TypeRemove']['removed']} is no longer allowed"


@_add_change_printer
def PropertyRemove(change: Change) -> str:
    first_sentence = f"Removed a property {change['change']['PropertyRemove']['removed']} from {change['path']}"
    if change["change"]["PropertyRemove"]["lhs_additional_properties"]:
        return (
            f"{first_sentence}, but it is still accepted via additionalProperties=true"
        )
    else:
        return f"{first_sentence}, so it is no longer accepted. Maybe use additionalProperties?"


def print_change(change: Change) -> None:
    change = dict(change)
    change.pop("is_breaking")

    printer = _CHANGE_PRINTERS.get(next(iter(change["change"])))
    if printer:
        print(f"## {printer(change)}")

    print(json.dumps(change))
    print()


if __name__ == "__main__":
    main()
