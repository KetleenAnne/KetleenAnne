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
    allb = [(s["title"], b) for s in sections for b in s["books"]]
    read = [x for x in allb if x[1]["status"] == "read"]
    now = [x for x in allb if x[1]["status"] == "reading"]
    todo = [s for s in sections if any(b["status"] == "todo" for b in s["books"])]
    out = [f"📊 **{len(read)} read · lidos** &nbsp;|&nbsp; **{len(now)} reading · lendo** "
           f"&nbsp;|&nbsp; **{sum(1 for x in allb if x[1]['status']=='todo')} to read · na fila**", ""]
    out.append("**✅ Read · Lidos**")
    out += [item(b, False) for _, b in read] or ["- _Nothing yet — the first check ✔️ is coming! · Ainda nada — o primeiro ✔️ vem aí!_"]
    out += ["", "**📖 Reading now · Lendo agora**"]
    out += [item(b) for _, b in now] or ["- _—_"]
    out += ["", "**🔖 To read · Na fila**"]
    for s in todo:
        out += ["", f"_{s['title']}_"]
        out += [item(b) for b in s["books"] if b["status"] == "todo"]
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
