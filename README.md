# abuse-muse

A privacy check for prompts you send to Muse, Meta's AI assistant. Use Muse hard for public and invented material; keep anything personal on your own machine.

> **Not affiliated with Meta.** This is an independent, unofficial project. "Muse" and "Meta" are trademarks of their owners. The name is a joke about using Muse to the fullest, not a guide to misusing it: this skill does not help get around quotas, rate limits, or terms of service.

## What it does

Before anything goes to Muse, the agent:

1. Scans the draft for secrets, direct identifiers, and indirect clues (job, city, hobby, routine).
2. Redacts with a local script, and generalizes indirect clues.
3. Re-scans to make sure nothing survived, including encoded copies.
4. Decides: **green** (send), **yellow** (generalize and confirm), or **red** (keep it local).
5. Tracks, locally and by type only, which kinds of clues you've already revealed, so it can warn when a new one would complete a fingerprint.

## Where to run it

- **In a local agent, before Muse (recommended).** Install it in Claude Code or another agent on your own machine, run the check there, and paste only the cleared draft into Muse. This is the mode that actually protects data.
- **Inside Muse (reminders only).** Muse has already received your draft when the skill runs there, so it can only warn and advise. Don't keep the clue tracker inside Muse. `skills/abuse-muse/skill.yaml` is the metadata file Muse's custom-skills folder uses.

## Install

Claude Code, as a plugin:

```
/plugin marketplace add heart-reburn/abuse-muse
/plugin install abuse-muse@abuse-muse
```

Or copy the skill folder:

```
cp -R skills/abuse-muse ~/.claude/skills/
```

Then create your private tracker, outside any skill folder:

```
mkdir -p ~/.abuse-muse
cp skills/abuse-muse/revealed-clues-tracker.template.md ~/.abuse-muse/revealed-clues-tracker.md
```

## Redaction script

Python 3, standard library only, no network.

```
python3 skills/abuse-muse/scripts/redact.py redact  draft.txt redacted.txt mapping.json
python3 skills/abuse-muse/scripts/redact.py scan    redacted.txt mapping.json
python3 skills/abuse-muse/scripts/redact.py restore reply.txt restored.txt mapping.json
```

It catches emails, API keys, bearer tokens, JWTs, private keys, URLs with tokens, SSNs, card and long numbers, IPs, and phone numbers. It does **not** catch plain names or street addresses; always read the draft yourself. The mapping file holds your real values; it is written readable only by you and should be deleted after the task.

## Example

> **You:** Can Muse help with this? "I'm a 34-year-old accountant in Denver, I climb on weekends, plan my training around tax season."
>
> **Agent:** Yellow. Clues: age, job, city, hobby. Together they narrow you down a lot. Generalized: "I'm an adult with a desk job and a busy season in spring; plan climbing training around it." Send that?

## Limits

This is a checklist, not a security boundary. It cannot guarantee a prompt is safe, and the tracker only knows about prompts that went through it.

## Credits

The decision and redaction design borrows ideas (not code) from Arcjet's guard rules, PromptGuard-style severity scoring, and DataFog's scan-before-read approach.

## License

MIT. See [LICENSE](LICENSE).
