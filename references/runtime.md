# Runtime and delivery contract

## Required

- Python 3 with the standard library.
- A Scene JSON file that passes `scripts/validate_scene.py`.
- A renderer supplied by the active agent environment when SVG/PNG generation
  is requested. This repository contains the schema and examples; it does not
  silently assume a particular renderer.

Run `scripts/doctor.sh --json` before choosing an output path.

## Delivery states

- `validated`: Scene JSON passed structural validation.
- `generated`: local SVG or PNG exists and passed visual inspection.
- `inserted_unverified`: Feishu write returned but remote readback is missing.
- `verified`: the target document was read back and the board is at the intended
  paragraph anchor.

Never collapse these states into a single “done” claim.
