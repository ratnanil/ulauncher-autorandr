# ulauncher-autorandr

A [Ulauncher](https://ulauncher.io) extension to load display profiles managed by [autorandr](https://github.com/phillipberndt/autorandr).

## Usage

Type the keyword (default: `display`) in Ulauncher to list all saved profiles. Optionally filter by name, then select one to apply it.

## Adding a new profile

Set up your displays the way you want (resolution, position, primary, on/off), then run:

```bash
autorandr --save <profile-name>
```

The profile will automatically appear in Ulauncher next time you use the extension — no configuration needed.

## Requirements

- [`autorandr`](https://github.com/phillipberndt/autorandr) — install via `sudo apt install autorandr`
