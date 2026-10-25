# Redaction

## Rules

- Redact a copy; never overwrite the original.
- Never print or log a matched value. Report only types and counts.
- Give the agent access only to the folders the task needs.
- Pattern matching misses plain names and street addresses, so read the draft yourself after the scan.

## Commands

All local, no network.

```
python3 scripts/redact.py redact  input.txt redacted.txt mapping.json
python3 scripts/redact.py scan    redacted.txt mapping.json
python3 scripts/redact.py restore reply.txt restored.txt mapping.json
```

- `redact` writes the redacted copy and a mapping file readable only by you.
- `scan` reports finding types and counts, and with the mapping file it checks whether any original value survived in plain, lowercased, spaced-out, URL-encoded, base64, or hex form. It exits with an error if anything is found; block the draft until it's fixed.
- `restore` puts the original values back into the reply, locally.

Delete the redacted copy, the mapping file, and the restored file when the task is done.

## Placeholders

- Each value becomes a typed placeholder such as `[EMAIL_1]`, `[PHONE_1]`, or `[API_KEY_1]`.
- The same value gets the same placeholder within one draft, so the draft stays readable.
- Numbering restarts for each draft, so placeholders can't be linked across drafts.
- Long numbers that pass a card checksum are labelled `CREDIT_CARD`; others are `LONG_NUMBER`.

## Re-scan

- Re-scan every redacted draft with the mapping file before sending.
- Scan the reply before reusing it, and redact any value it echoes back.
