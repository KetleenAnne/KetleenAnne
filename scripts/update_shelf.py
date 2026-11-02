#!/usr/bin/env python3
"""Rebuilds the bookshelf block in README.md from data/books.md (stdlib only)."""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC, README = ROOT / "data" / "books.md", ROOT / "README.md"
START, END = "<!-- SHELF:START -->", "<!-- SHELF:END -->"
LINE = re.compile(r"^- \[( |x|X)\]\s+(.*)$")


def parse(text):
    sections, cur = [], None
    for raw in text.splitlines():
        if raw.startswith("## "):
            cur = {"title": raw[3:].strip(), "books": []}
            sections.append(cur)
            continue
        m = LINE.match(raw.strip())
        if not m or cur is None:
            continue
        done = m.group(1).lower() == "x"
        parts = [p.strip() for p in m.group(2).split("|")]
        title = parts[0]
        reading = bool(re.search(r"\((lendo|reading)\)\s*$", title, re.I))
        title = re.sub(r"\s*\((lendo|reading)\)\s*$", "", title, flags=re.I)
        if not title:
            continue
        cur["books"].append({
            "title": title,
            "author": parts[1] if len(parts) > 1 else "",
            "why": parts[2] if len(parts) > 2 else "",
            "status": "read" if done else ("reading" if reading else "todo"),
        })
    return sections


def item(b, with_why=True):
    s = f"_{b['title']}_" + (f" — {b['author']}" if b["author"] else "")
    if with_why and b["why"]:
        s += f" · {b['why']}"
    return f"- {s}"


def build(sections):
    allb = [b for s in sections for b in s["books"]]
    read = [b for b in allb if b["status"] == "read"]
    now = [b for b in allb if b["status"] == "reading"]
    todo = [b for b in allb if b["status"] == "todo"]
    out = ["**\U0001F4D6 Reading now \u00b7 Lendo agora**"]
    out += [item(b, False) for b in now] or ["- _\u2014_"]
    out += ["", "**\U0001F516 Next up \u00b7 Pr\u00f3ximos**"]
    out += [item(b) for b in todo[:5]] or ["- _\u2014_"]
    if read:
        out += ["", f"**\u2705 Read \u00b7 Lidos ({len(read)})**"]
        out += [item(b, False) for b in read[-5:]]
    out += ["", f"\U0001F4DA [Full list \u00b7 Lista completa ({len(allb)} books)](data/books.md)"]
    return "\n".join(out)


def main():
    block = build(parse(SRC.read_text(encoding="utf-8")))
    text = README.read_text(encoding="utf-8")
    if START not in text or END not in text:
        sys.exit("markers not found in README.md")
    pre, rest = text.split(START, 1)
    _, post = rest.split(END, 1)
    new = f"{pre}{START}\n\n{block}\n\n{END}{post}"
    if new != text:
        README.write_text(new, encoding="utf-8")
        print("README updated")
    else:
        print("no changes")


if __name__ == "__main__":
    main()
