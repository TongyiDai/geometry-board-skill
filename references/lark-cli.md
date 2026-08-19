# Feishu delivery contract

Feishu insertion is optional. Generate and validate the local Scene JSON and
SVG first.

```bash
lark-cli auth status --json --verify
```

Before writing, resolve the live document, account/tenant, paragraph anchor,
and existing board positions. Preserve existing structure. After writing, read
back the outline and the text before and after each board. A successful CLI
response without readback is `inserted_unverified`.

Never publish real profile identifiers, document tokens, Base tokens, internal
URLs, or private document titles in examples.
