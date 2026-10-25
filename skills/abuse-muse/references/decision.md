# Decision

## Severity to action

| Severity | Example | Action |
|---|---|---|
| None | Public facts, invented placeholders | Send (green) |
| Low | One indirect clue that redaction or generalization removes | Generalize, then send after the user confirms (yellow) |
| Medium | Several indirect clues, or public material behind a login | Generalize and confirm (yellow); block if the task can't survive generalizing |
| High | Direct identifiers, secrets, private data | Redact; block if anything survives the re-scan (red) |
| Critical | Whole private collections, or clues that together single out the user | Block (red) |
| Unknown | Can't tell | Block (red). When unsure, block. |

Redact first and block as a fallback, so a draft isn't blocked when redaction can save it.

## Green, yellow, red

- **Green:** only public material or invented placeholders, with no real person, account, location, or payment, and no clues that narrow down who the user is.
- **Yellow:** at least one indirect clue (age range, job, city, hobby, routine, or public material behind a login), and the draft can be generalized without losing the task.
- **Red:** direct identifiers, secrets, private data, a whole private collection, or clues that together single out the user.

## Pipeline

1. Scan the draft for direct values, indirect clues, and secret patterns.
2. Redact direct values to typed placeholders, and generalize indirect clues to broader categories.
3. Re-scan the redacted draft against the mapping file, which also catches encoded and reformatted copies.
4. Decide with the table above, and show the decision to the user before sending.
5. Treat a tool call (connecting a source, publishing, sharing) as an action that needs the user's approval, not as free text.
6. Send only the redacted draft, and scan the reply before reusing it.
7. Restore placeholders locally, and log only types and counts.
