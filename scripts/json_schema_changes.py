# this script currently runs without any dependencies installed. that can be
# changed easily, but right now we don't need anything like rapidjson over
# json, so CI is slightly faster
import sys
import subprocess
import tempfile
import json


def main():
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
    changes = []

    for filename in lines:
        print(f"# {filename}")
        print()

        with tempfile.NamedTemporaryFile() as old_file:
            old_file_contents = subprocess.check_output(
                ["git", "show", f"main:{filename}"]
            )
            old_file.write(old_file_contents)
            old_file.flush()

            for change in subprocess.check_output(
                ["json-schema-diff", old_file.name, filename]
            ).splitlines():

                change = json.loads(change)
                if change["is_breaking"]:
                    breaking_changes.append(change)
                changes.append(change)

    if not breaking_changes:
        print("no breaking changes found")
    else:
        print("!!! WARNING: changes considered breaking:")
        print()
        for change in breaking_changes:
            print_change(change)

        print()
        print("other changes:")

    print()

    for change in changes:
        print_change(change)

    if breaking_changes:
        sys.exit(2)


def print_change(change):
    change = dict(change)
    change.pop("is_breaking")
    print(json.dumps(change))


if __name__ == "__main__":
    main()
