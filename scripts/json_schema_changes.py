# this script currently runs without any dependencies installed. that can be
# changed easily, but right now we don't need anything like rapidjson over
# json, so CI is slightly faster
import sys
import subprocess
import tempfile
import json
from typing import Any, Callable, Mapping


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

    breaking_changes = []
    non_breaking_changes = []

    for filename in lines:
        print(f"# {filename}")
        print()

        with tempfile.NamedTemporaryFile() as old_file:
            old_file_contents = subprocess.check_output(
                ["git", "show", f"origin/main:{filename}"]
            )
            old_file.write(old_file_contents)
            old_file.flush()

            for raw_change in subprocess.check_output(
                ["json-schema-diff", old_file.name, filename]
            ).splitlines():

                change = json.loads(raw_change)
                if change["is_breaking"]:
                    breaking_changes.append(change)
                else:
                    non_breaking_changes.append(change)

    if breaking_changes:
        print("!!! WARNING: changes considered breaking:")
        print()
        for change in breaking_changes:
            print_change(change)

        print()

        if non_breaking_changes:
            print("other changes:")

    if non_breaking_changes:
        print()

    for change in non_breaking_changes:
        print_change(change)

    if not non_breaking_changes and not breaking_changes:
        print("""\
There were changes to the JSON schema file, but we couldn't categorize any of
them. Therefore we don't know whether this change is safe to make.

This might be a gap in linting. Want to take a look at
https://github.com/getsentry/json-schema-diff/ and figure it out?""")
        if "--no-exit-code" not in sys.argv:
            sys.exit(2)

    if breaking_changes and "--no-exit-code" not in sys.argv:
        sys.exit(2)


Change = Mapping[str, Any]


_CHANGE_PRINTERS: Mapping[str, Callable[[Change], str]] = {
    "TypeRemove": lambda change: f"Restricted the type of {change['path']}, as {change['change']['TypeRemove']['removed']} is no longer allowed",
    "PropertyRemove": lambda change: f"Removed the property {change['path']}, so it is no longer accepted. Maybe use additionalProperties?",
}


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
