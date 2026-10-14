import argparse
import json
import re
from pathlib import Path


YEAR_START = 2021
YEAR_END = 2026
QUERY = (
    '(("sentiment" AND ("analysis" OR "classification")) OR "opinion mining") '
    'AND ("stock market*" OR "financial market*" OR "stock price*" OR "stock return*") '
    'AND (predict* OR forecast*) '
    'AND ("X" OR Twitter OR tweet* OR microblog*)'
)


def matches_query(text):
    return bool(
        (
            (
                re.search(r"\bsentiment\b", text, re.I)
                and re.search(r"\b(?:analysis|classification)\b", text, re.I)
            )
            or re.search(r"\bopinion\s+mining\b", text, re.I)
        )
        and re.search(
            r"\b(?:stock\s+market\w*|financial\s+market\w*|stock\s+price\w*|stock\s+return\w*)",
            text,
            re.I,
        )
        and re.search(r"\b(?:predict\w*|forecast\w*)", text, re.I)
        and re.search(r"\b(?:x|twitter|tweet\w*|microblog\w*)\b", text, re.I)
    )


def matches_language(language):
    # Missing ACL metadata stays for manual language screening.
    return language is None or language.lower().startswith(("en", "eng", "pt", "por"))


def plain_text(value):
    if value is None:
        return ""
    return value.as_text() if hasattr(value, "as_text") else str(value)


def search(anthology_dir):
    from acl_anthology import Anthology

    anthology = Anthology(datadir=str(Path(anthology_dir) / "data"))
    records = []
    for paper in anthology.papers():
        title = plain_text(paper.title)
        abstract = plain_text(paper.abstract)
        year = int(paper.year)
        if not (YEAR_START <= year <= YEAR_END):
            continue
        if not matches_language(paper.language):
            continue
        if not matches_query(f"{title}\n{abstract}"):
            continue

        events = paper.get_events()
        records.append(
            {
                "source": "ACL Anthology",
                "year": year,
                "language": paper.language,
                "title": title,
                "authors": [
                    f"{author.first} {author.last}".strip()
                    for author in paper.authors
                    if author.first or author.last
                ],
                "venue": str(events[0].title) if events else "",
                "doi": paper.doi or "",
                "url": paper.web_url,
                "abstract": abstract,
            }
        )
    return records


def main():
    parser = argparse.ArgumentParser(description=f"Busca ACL: {QUERY}")
    parser.add_argument("--anthology-dir", default="acl-anthology")
    parser.add_argument("--output", default="results/acl.json")
    args = parser.parse_args()

    records = search(args.anthology_dir)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{len(records)} registros gravados em {output}")


if __name__ == "__main__":
    main()

