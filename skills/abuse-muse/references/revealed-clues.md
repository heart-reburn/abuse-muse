# Revealed clues

How abuse-muse remembers which kinds of clues were already sent to Meta, without becoming a profile itself.

## Where the tracker lives

- At `~/.abuse-muse/revealed-clues-tracker.md` on the user's own machine, created from `revealed-clues-tracker.template.md`. One file, shared by every local agent that runs the check.
- Never inside the skill folder, a git repo, cloud sync, or anywhere in Muse (memory, chats, artifacts, workspace). A tracker Muse can read hands Meta the profile the skill is trying to prevent.
- If the skill is running inside Muse, don't use the tracker at all.

## What is stored

- Stored: clue types as ticked boxes, and domain names (work, health, location, personal).
- Never stored: values (accountant, New York, hiking), names, places, dates, prompts, or chats.
- Allowed clue types: gender, age_group, job, industry, city, school, hobby, course, schedule, commute, language, health_hint, income_range, family, routine.

## Decision rule

1. List the clue types in the new draft.
2. If there are none, the tracker doesn't change the decision.
3. Otherwise, count the distinct types: those already ticked plus those in the draft.
   - 1 or 2: yellow. Generalize, show the user how the new clue adds to what was already sent, and send only if they confirm.
   - 3 or more, or job + city + hobby together in any mix: red. Don't send unless the clue is generalized away or the user explicitly accepts that fingerprint.
4. Show the count to the user every time.
5. After the user confirms sending, tick the new types and mark the domain. Never update the tracker for blocked drafts.

## Limits

- The tracker only knows about prompts that went through the check. If the user sent something to Muse directly, say the record is incomplete, and add only the types the user reports.
- Nothing enforces the rules automatically. Read the file every time.
- Even a type-only list tells someone with access to the file what kinds of clues were shared. Keep it local, and clear it when it's no longer needed.
