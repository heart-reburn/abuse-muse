#!/usr/bin/env python3
"""Local redaction helper for abuse-muse.

Run this on your own machine before pasting material to Muse. It never
makes network requests and never prints a matched value.

  redact.py redact  input.txt redacted.txt mapping.json
  redact.py scan    redacted.txt [mapping.json]
  redact.py restore reply.txt restored.txt mapping.json

redact   writes a redacted copy and a mapping file (owner-only permissions).
scan     reports finding types and counts. With a mapping file it also checks
         that no original value survived, including lowercased, spaced-out,
         URL-encoded, base64, and hex forms. Exits 1 if anything is found.
restore  puts the original values back into a reply, locally.

The mapping file holds the original values. Keep it local, never send it
to Muse, and delete it when the task is done.
"""
import base64
import json
import os
import re
import sys
import urllib.parse
from pathlib import Path

# Order matters: multi-line and specific secrets first, so a generic number
# pattern does not split a key that contains digits.
PATTERNS = [
    ("PRIVATE_KEY", r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?(?:-----END [A-Z ]*PRIVATE KEY-----|\Z)"),
    ("EMAIL", r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    ("API_KEY", r"\b(?:sk-[A-Za-z0-9_-]{8,}|AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9]{20,}|xox[baprs]-[A-Za-z0-9-]{10,}|AIza[0-9A-Za-z_-]{35})\b"),
    ("BEARER", r"Bearer [A-Za-z0-9._\-]{10,}"),
    ("JWT", r"\beyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\b"),
    ("URL_WITH_TOKEN", r"https?://[^\s]*?(?:token|key|secret|password)=[^\s&]+"),
    ("SSN", r"\b\d{3}-\d{2}-\d{4}\b"),
    ("NUMBER", r"(?<![\w.])(?:\d[ -]?){12,18}\d(?![\w.])"),  # cards pass a Luhn check -> CREDIT_CARD
    ("IP", r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
    ("PHONE", r"(?<![\w+])(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}(?!\w)"),
]
PLACEHOLDER = re.compile(r"\[[A-Z_]+_\d+\]")


def luhn(digits):
    total = 0
    for i, d in enumerate(reversed(digits)):
        n = int(d)
        if i % 2:
            n = n * 2 - 9 if n > 4 else n * 2
        total += n
    return total % 10 == 0


def label_for(label, value):
    if label == "NUMBER":
        digits = re.sub(r"\D", "", value)
        return "CREDIT_CARD" if luhn(digits) else "LONG_NUMBER"
    return label


def find(text):
    """Yield (label, value) for every match, skipping existing placeholders."""
    masked = PLACEHOLDER.sub(lambda m: " " * len(m.group(0)), text)
    for label, pattern in PATTERNS:
        for m in re.finditer(pattern, masked, re.S):
            yield label_for(label, m.group(0)), m.group(0)
            masked = masked[:m.start()] + " " * (m.end() - m.start()) + masked[m.end():]


def variants(value):
    """Forms a value can survive in after reformatting."""
    compact = re.sub(r"[\s.\-()]", "", value)
    raw = value.encode()
    forms = {value, value.lower(), compact, urllib.parse.quote(value), raw.hex(),
             base64.b64encode(raw).decode().rstrip("=")}
    return {f for f in forms if len(f) >= 6}


def write_private(path, data):
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(data)
    os.chmod(path, 0o600)


def redact(src, dst, mapping_path):
    text = Path(src).read_text(encoding="utf-8", errors="ignore")
    mapping, counters = {}, {}
    for label, value in find(text):
        if value in mapping.values():
            continue
        counters[label] = counters.get(label, 0) + 1
        mapping[f"[{label}_{counters[label]}]"] = value
    for placeholder, value in sorted(mapping.items(), key=lambda kv: -len(kv[1])):
        text = text.replace(value, placeholder)
    Path(dst).write_text(text, encoding="utf-8")
    write_private(mapping_path, json.dumps(mapping, indent=2))
    print(f"Redacted {len(mapping)} values. Types: {', '.join(sorted(counters)) or 'none'}")
    print("The mapping file holds the original values. Keep it local and never send it to Muse.")
    print("Pattern matching misses plain names and street addresses. Read the redacted file before sending.")
    return 0


def scan(path, mapping_path=None):
    text = Path(path).read_text(encoding="utf-8", errors="ignore")
    counts = {}
    for label, _ in find(text):
        counts[label] = counts.get(label, 0) + 1
    if mapping_path:
        mapping = json.loads(Path(mapping_path).read_text(encoding="utf-8"))
        lowered = text.lower()
        for value in mapping.values():
            if any(form.lower() in lowered for form in variants(value)):
                counts["SURVIVED_REDACTION"] = counts.get("SURVIVED_REDACTION", 0) + 1
    if not counts:
        print("Clean: no findings. Still read it by eye for names and addresses.")
        return 0
    for label, n in sorted(counts.items()):
        print(f"{label}: {n}")
    print("Blocked: fix the findings above before sending.")
    return 1


def restore(src, dst, mapping_path):
    text = Path(src).read_text(encoding="utf-8", errors="ignore")
    mapping = json.loads(Path(mapping_path).read_text(encoding="utf-8"))
    for placeholder, value in mapping.items():
        text = text.replace(placeholder, value)
    write_private(dst, text)
    print(f"Restored {len(mapping)} placeholders into {dst}. Keep it local.")
    return 0


def main(argv):
    commands = {"redact": (redact, 3, 3), "scan": (scan, 1, 2), "restore": (restore, 3, 3)}
    if len(argv) < 2 or argv[1] not in commands:
        print(__doc__)
        return 2
    func, lo, hi = commands[argv[1]]
    args = argv[2:]
    if not lo <= len(args) <= hi:
        print(__doc__)
        return 2
    return func(*args)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
