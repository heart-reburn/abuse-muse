---
name: abuse-muse
description: Checks a prompt, file, or task before it goes to Meta's Muse assistant, so no personal, secret, work, or indirectly identifying data is sent. Scans, redacts, re-scans, and gives a send, pause, or block decision. Use only when the user mentions sending, pasting, or asking something in Muse and the content might contain personal data, secrets, or clues to who they are. Not for ordinary tasks that don't involve Muse.
---

# abuse-muse

A privacy check for Muse. Use Muse freely for public and invented material, and keep everything personal on your own machine.

## Where this runs

- **Best: in a local agent, before Muse sees anything.** Run the check in an agent on your own machine (or another assistant you trust), then paste only the cleared draft into Muse. This is the only mode that actually protects data.
- **Inside Muse: reminders only.** If this skill is installed in Muse itself, Muse has already received the draft by the time the skill runs. There it can only warn you, advise on what to share next, and stop Muse from connecting extra sources or publishing. Say so to the user. Do not use the revealed-clues tracker inside Muse.

## Working assumptions

- Assume everything sent to Muse in a regular session (prompts, files, images, tool results) may be logged and reviewed by Meta for safety, security, debugging, and product improvement, even with AI training turned off.
- If Muse offers a more private mode, treat it as a separate environment, and check what it actually promises before relying on it.
- Never promise that data sent to Muse is private, deleted, or used only for the task.
- Assume anything sent is permanent and may be matched with other data later.
- Metadata counts as data: timing, device, language, the order of questions, and writing style can identify a person even when every fact is generic.
- Settings can change or reset. Check them, but act as if review may happen anyway.

## The idea

- If a task needs real identity, money, health, or work files, don't send it to Muse.
- If a task only needs public material or invented examples, Muse is great for it.
- Work locally first, send the minimum, and delete local originals and mappings when done.
- Keep domains (work, health, location, personal) separate. Don't mix them in one account, session, or invented persona; a reused persona becomes a fingerprint of its own.
- A new session on the same machine is weak separation: the same device, network, account, and timing can link sessions. For a sensitive domain, use a separate machine.

## The check, every time

Run it before sending, never after.

1. **Scan** the draft for direct identifiers, secrets, and indirect clues.
2. **Read the tracker** of clue types already revealed (local mode only; see below).
3. **Redact** with `scripts/redact.py redact`, and generalize indirect clues.
4. **Re-scan** with `scripts/redact.py scan redacted.txt mapping.json`. Block if anything survived.
5. **Decide** green, yellow, or red (below), and show the decision and the cleared draft to the user.
6. **Send** only after the user confirms. If the decision is unclear, block. Unknown counts as red.
7. **Check the reply** before reusing it, since it can echo a value that was redacted. Restore placeholders locally with `scripts/redact.py restore`.
8. **Update the tracker** after the user confirms sending.

Keep the original, the mapping file, and the restored result local. For a new kind of task, do a dry run: show the redacted draft and the decision without sending.

## Green, yellow, red

See `references/decision.md` for the full table.

- **Green: send.** Only public material or invented placeholders. No real person, account, location, or payment, and no clues that narrow down who the user is.
- **Yellow: pause and generalize.** The draft has at least one indirect clue (age range, job, city, hobby, routine). Name the clues, show a generalized version, and send only if the user confirms.
- **Red: never send to Muse.** Direct identifiers, secrets, private data, a whole private collection, or clues that together single out the user. Offer a local alternative.

## Indirect clues and the tracker

See `references/indirect-identity.md` for the clue types and how to generalize them, and `references/revealed-clues.md` for the tracker.

- One indirect clue is yellow. Clues that together single out the user are red.
- The tracker records clue *types* already sent (such as "job" or "city"), never values. It lives at `~/.abuse-muse/revealed-clues-tracker.md`, outside any skill folder. If it doesn't exist, copy `revealed-clues-tracker.template.md` there.
- A draft with no indirect clues is unaffected by the tracker.

## Red list

See `references/stop-list.md`. Block secrets, direct identifiers, financial, health, business, and customer data, and whole private collections. Block any task that connects email, calendar, contacts, banking, health, photo, or location sources when it can be done without them.

## Redaction

See `references/redaction.md`. `scripts/redact.py` replaces matched values with typed placeholders such as `[EMAIL_1]`, never prints a value, and writes the mapping file readable only by you. It misses plain names and street addresses, so always read the draft yourself.

## Green uses

See `references/green-categories.md`. Classify a green task by its main intent: learn, build, or create.

## How to present the result

- Green: the prompt exactly as the user can paste it, with nothing personal in it. Stop there: no extra warnings or reminders for a plainly public task.
- Yellow: the clues found, the generalized version, and a safer alternative.
- Red: the type of data at risk and the local alternative.
- Don't repeat restricted details the user didn't include.
- Remind the user to delete chats, files, and artifacts they no longer need, and that deleting a memory doesn't delete every record.
- Log only types and counts, never values, file contents, or full prompts.

## Limits

- This is a checklist, not a security boundary. It cannot guarantee a prompt is safe.
- It does not help get around quotas, rate limits, or terms of service.
- The tracker only knows about prompts that went through the check.
