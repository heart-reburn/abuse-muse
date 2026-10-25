# Red list

Block a prompt that contains any item below, and offer a local or redacted alternative instead.

## Secrets

- Passwords, API keys, tokens, session cookies, bearer tokens, JWTs, private keys, and PEM files.

- Credentials in code, logs, environment files, screenshots, and configuration files.

## Direct identity

- Full name combined with address, date of birth, government identifier, phone number, or email address.

- Biometric data, precise location, and data about children.

## Money and work

- Card numbers, bank account numbers, routing numbers, and full financial statements.

- Tax documents, pay information, employment records, and internal business records.

- Customer data, trade secrets, contracts, and internal documents.

## Health and private collections

- Health records, medical notes, and health data from a device or app.

- A full inbox, a full vault, a full drive, a full photo library, or a full business dataset.

- Photos, screenshots, or documents with faces, addresses, or other identifying details that cannot be removed.

## Connections

- A task that connects email, calendar, contacts, banking, health, photo, or location sources when the task can be done without them.

- A task that publishes an artifact, creates a public link, or shares content through feedback or troubleshooting without a clear need.

## Note on detection limits

- Pattern matching can miss plain names and street addresses, so a clean scan does not prove a draft is safe.

- Review the draft by eye after the scan, especially for names, places, and unique combinations.
