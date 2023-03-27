import re
from pathlib import Path


def test_codeowner() -> None:
    topic_pattern = re.compile(r"^\/topics\/([a-zA-Z0-9\-\_]+.yaml)")

    with open("CODEOWNERS") as f:
        topics_covered = set()
        for li in f.read().split("\n"):
            match = topic_pattern.match(li)
            if match:
                topics_covered.add(match.group(1))

    topics_dir = Path.joinpath(Path(__file__).parents[2], "topics")
    all_topics = {filename.name for filename in topics_dir.iterdir()}

    assert topics_covered == all_topics, "All topics have defined codeowners!"
