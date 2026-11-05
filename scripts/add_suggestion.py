#!/usr/bin/env python3
"""Adds an approved book suggestion (a GitHub issue form) to data/books.md.

The issue text comes from visitors, so it is treated as untrusted data:
it is read from environment variables (never interpolated into shell code),
stripped of characters that would break the list format or inject markup,
and length-limited.
"""
import os
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BOOKS = ROOT / "data" / "books.md"
SECTION_BY_TOPIC = {"tecnologia": "## 🧑‍💻", "mente": "## 🌱", "ficção": "## 🐱", "ficcao": "## 🐱"}


def field(body, heading_start):
    m = re.search(r"^###\s*" + re.escape(heading_start) + r"[^\n]*\n+(.*?)(?=^###\s|\Z)", body, re.M | re.S)
    if not m:
        return ""
    value = m.group(1).strip()
    return "" if value == "_No response_" else value


def clean(text, limit):
    text = re.sub(r"[\r\n\t]+", " ", text)
    text = re.sub(r"[|<>`\[\]\\]", "", text)      # keep the "title | author | why" format intact, no markup
    text = re.sub(r"\s{2,}", " ", text).strip()
    return text[:limit].rstrip()


def main():
    body = os.environ.get("ISSUE_BODY", "")
    user = re.sub(r"[^A-Za-z0-9-]", "", os.environ.get("ISSUE_USER", ""))[:39]
    title = clean(field(body, "Título"), 90)
    author = clean(field(body, "Autor"), 80)
    topic = clean(field(body, "Tema"), 60).lower()
    why = clean(field(body, "Por que"), 140)
    if not title or not author:
        sys.exit("missing title or author")

    section = next((h for key, h in SECTION_BY_TOPIC.items() if key in topic), "## 🐱")
    note = f"{why} (sugestão de {user})" if why else f"sugestão de {user}"
    line = f"- [ ] {title} | {author} | {note}"

    text = BOOKS.read_text(encoding="utf-8")
    if re.search(r"^- \[[ xX]\]\s+" + re.escape(title) + r"(\s*\(lendo\))?\s*\|", text, re.M | re.I):
        print("already on the list:", title)
        return
    lines = text.split("\n")
    start = next(i for i, l in enumerate(lines) if l.startswith(section))
    end = start + 1
    while end < len(lines) and not lines[end].startswith("## "):
        end += 1
    last_book = max((i for i in range(start, end) if lines[i].startswith("- [")), default=start)
    lines.insert(last_book + 1, line)
    BOOKS.write_text("\n".join(lines), encoding="utf-8")
    print("added:", line)


if __name__ == "__main__":
    main()
