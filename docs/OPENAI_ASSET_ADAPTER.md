# OpenAI asset adapter

GodoGen includes an optional script at:

```text
skills/godogen/scripts/openai_asset.py
```

It generates one image per command, saves the raw result in the asset staging directory and appends a provenance entry to `artifacts/godogen/asset-manifest.json`.

## 1. Install the optional OpenAI SDK

From PowerShell:

```powershell
python -m pip install --upgrade openai
```

Verify the package imports:

```powershell
python -c "from openai import OpenAI; print('OpenAI SDK ready')"
```

## 2. Set the API key for the current PowerShell session

```powershell
$env:OPENAI_API_KEY = "your-key"
```

The key exists only in the current PowerShell window. Close the window to remove it from the session.

Do not paste the key into source files, GitHub issues, pull requests, screenshots or committed `.env` files.

## 3. Select the current image model

The adapter deliberately does not hardcode a permanent model name. Supply the model explicitly:

```powershell
$env:OPENAI_IMAGE_MODEL = "CURRENT_IMAGE_MODEL_NAME"
```

Use the model available to your OpenAI account and current OpenAI documentation.

## 4. Create a durable prompt file

Create the prompt directory:

```powershell
New-Item -ItemType Directory -Path artifacts\godogen\prompts -Force
notepad artifacts\godogen\prompts\scanner-icon.txt
```

Paste a complete brief and save it. Example:

```text
Create a single 512 x 512 pixel inventory icon for a compact science-fiction mining scanner. Three-quarter view, strong readable silhouette, brushed dark metal, small amber sensor window, no lettering, no border, transparent background, centred with 48 pixel safe margins. The result will be displayed at 64 x 64 pixels in a Godot inventory grid.
```

## 5. Generate one staged image

When using the installed user skill:

```powershell
python "$HOME\.codex\skills\godogen\scripts\openai_asset.py" `
  --name "mining-scanner-icon" `
  --prompt-file "artifacts\godogen\prompts\scanner-icon.txt" `
  --model "$env:OPENAI_IMAGE_MODEL" `
  --size "1024x1024" `
  --quality "auto" `
  --background "transparent" `
  --intended-use "Inventory icon displayed at 64 x 64 pixels" `
  --approved-budget "USD 1.00"
```

The exact supported size, quality and background values depend on the selected model. Provider validation errors are returned without exposing the key.

## 6. Inspect generated outputs

List staged files:

```powershell
Get-ChildItem artifacts\godogen\asset-staging
```

Open `artifacts/godogen/asset-manifest.json` and confirm the new entry contains:

- provider;
- model;
- prompt file;
- dimensions;
- background choice;
- approved budget;
- intended use;
- SHA-256 hash;
- staged file path.

The adapter marks new assets as unapproved. Generation alone does not move an image into the game.

## 7. Ask Codex to validate and import it

```text
$godogen review the newly staged OpenAI asset for the intended inventory use. Check the manifest, dimensions, transparency, silhouette and visual consistency. Import it using the project’s existing asset conventions, test it at the real UI size in the running game, update the manifest with the runtime path and approval result, and keep the original staged output and prompt traceable.
```

## Command options

```powershell
python "$HOME\.codex\skills\godogen\scripts\openai_asset.py" --help
```

Important options:

| Option | Meaning |
|---|---|
| `--name` | Stable descriptive name used in the output filename |
| `--prompt` | Prompt supplied directly on the command line |
| `--prompt-file` | Recommended durable prompt file |
| `--model` | Current OpenAI image model name |
| `--size` | Requested image size supported by the selected model |
| `--quality` | Requested quality value supported by the selected model |
| `--background` | `auto`, `transparent` or `opaque` |
| `--intended-use` | Exact use inside the game |
| `--approved-budget` | Human-readable spending approval |
| `--output-dir` | Staging output directory |
| `--manifest` | Asset manifest path |

Provide exactly one of `--prompt` or `--prompt-file`.

## Failure behaviour

The command exits without generating when:

- `OPENAI_API_KEY` is missing;
- no model is supplied;
- both prompt methods or neither prompt method are supplied;
- the OpenAI SDK is missing;
- the provider rejects the request;
- the response does not contain image data;
- the existing manifest has an invalid structure.

It does not print the API key and does not overwrite previous variations because every output filename includes a UTC timestamp.
