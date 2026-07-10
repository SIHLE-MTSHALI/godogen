# Asset creation with GodoGen

GodoGen can use existing assets, procedural placeholders, user-provided files, ChatGPT-created images, OpenAI API image generation, local tools and approved third-party providers.

## Asset priority

Use the least expensive and least disruptive source that can satisfy the task:

1. existing repository assets;
2. procedural placeholders;
3. user-provided assets;
4. manual ChatGPT image creation;
5. approved local tools such as Blender or ComfyUI;
6. OpenAI image API;
7. Gemini, xAI, Tripo3D or another approved provider.

Paid generation requires explicit approval or an existing repository policy with a spending limit.

## Before generating anything

Define an asset brief containing:

- asset type, such as icon, sprite, texture, portrait, background or concept reference;
- exact use in the game;
- target dimensions in pixels;
- transparent or opaque background;
- camera angle and perspective;
- visual style and palette constraints;
- animation or tiling requirements;
- expected file format;
- required safe margins;
- whether text is allowed;
- whether the result must match an existing character or environment reference.

Do not request a vague "cool asset" and then force the game to fit an unsuitable result.

## Manual ChatGPT workflow

Use this path when a person is available to generate and download an image from ChatGPT.

1. Prepare the asset brief.
2. In ChatGPT, request the image with exact dimensions, composition and background requirements.
3. When consistency matters, upload approved reference images and describe what must remain unchanged.
4. Review the generated image for unwanted text, incorrect anatomy, inconsistent perspective, poor silhouettes, clipped content and background contamination.
5. Download the approved image.
6. Place it in:

```text
artifacts/godogen/asset-staging/
```

7. Rename it descriptively, for example:

```text
player_portrait_v01.png
plasma_rifle_icon_v02.png
forest_ground_tile_v01.png
```

8. Tell Codex the staging path, intended runtime path and use.
9. GodoGen validates size, alpha channel, format, import result and in-game appearance.
10. Move the approved asset into the project’s runtime asset directory only after validation.

### Example ChatGPT request

```text
Create a single 512 x 512 pixel inventory icon for a compact science-fiction mining scanner. Three-quarter view, strong readable silhouette, brushed dark metal, small amber sensor window, no lettering, no border, transparent background, centred with 48 pixel safe margins. Match the attached approved UI icon style. The result will be displayed at 64 x 64 pixels in a Godot inventory grid.
```

## OpenAI API workflow

Use this path when the repository has an approved API key and generation budget.

### Secret handling

Store the API key in an environment variable. Never put it in source code, `project.godot`, `AGENTS.md`, a committed `.env` file or an issue comment.

Windows PowerShell for the current session:

```powershell
$env:OPENAI_API_KEY = "your-key"
```

Linux or macOS for the current shell:

```bash
export OPENAI_API_KEY="your-key"
```

### Required policy before a request

Record:

- provider: OpenAI;
- approved maximum spend;
- number of requested variations;
- intended dimensions and quality;
- whether edits or references are required;
- destination staging directory;
- stop condition for retries.

GodoGen should not repeatedly regenerate an asset without comparing each result to explicit acceptance criteria.

### Provider adapter expectations

An OpenAI asset adapter should:

- read the API key only from the environment;
- accept the brief as structured input;
- save raw outputs into the staging directory;
- retain the final prompt and relevant parameters;
- calculate a content hash;
- avoid overwriting earlier variations;
- emit a manifest entry;
- report provider errors without exposing secrets;
- stop when the approved retry or budget limit is reached.

The exact OpenAI model name should be configurable rather than hardcoded permanently because available image models can change.

## Asset manifest

Record generated and imported assets in `artifacts/godogen/asset-manifest.json` or the project’s existing asset registry.

Example entry:

```json
{
  "id": "plasma-rifle-icon-v02",
  "provider": "OpenAI",
  "tool_or_model": "configured-image-model",
  "source": "api-generation",
  "prompt_file": "artifacts/godogen/prompts/plasma-rifle-icon-v02.txt",
  "requested_size": "512x512",
  "transparent_background": true,
  "staging_path": "artifacts/godogen/asset-staging/plasma_rifle_icon_v02.png",
  "runtime_path": "assets/ui/items/plasma_rifle_icon.png",
  "sha256": "64-character-hash",
  "estimated_cost": null,
  "actual_cost": null,
  "manual_edits": [],
  "approved": true,
  "notes": "Validated at 64 x 64 pixels in inventory UI"
}
```

## Godot import validation

After placing an asset in the runtime directory:

1. run Godot import;
2. check import warnings and errors;
3. inspect the generated resource in the editor;
4. confirm filter, mipmap, repeat and compression settings;
5. test the asset at its real display size;
6. check transparency edges and colour shifts;
7. confirm materials and texture coordinates when used in 3D;
8. capture the asset in the running game;
9. reject or revise it when it does not meet the brief.

## Common asset-specific requirements

### UI icons

- Use a readable silhouette.
- Avoid tiny details that disappear at runtime size.
- Keep safe margins consistent.
- Test against actual UI backgrounds.

### 2D sprites

- Specify frame dimensions and animation order.
- Keep the character centred consistently.
- Remove unintended background pixels.
- Validate pivots and collision shapes separately.

### Seamless textures

- Require tileable edges.
- Test a repeated 3 x 3 grid.
- Check normal, roughness and height maps for consistent orientation.

### Character references

- Preserve face, clothing, proportions and colour identifiers.
- Store approved references.
- Do not accept near-matches when continuity matters.

### 3D generation

- Treat generated models as source material, not automatically production-ready assets.
- Validate topology, scale, origin, rig, materials, collision and performance.
- Keep original generation inputs and conversion history.

## Alternative providers

GodoGen may use Gemini, xAI, Tripo3D, local Blender workflows, ComfyUI or other approved tools. Every provider follows the same rules for approval, secrets, staging, provenance, cost tracking, import validation and runtime proof.

## Completion criteria

An asset task is complete only when:

- the file exists in the intended runtime location;
- the manifest is updated;
- Godot imports it successfully;
- it looks correct in the actual game context;
- performance and dimensions are acceptable;
- the source, prompt and edits are traceable;
- no secret or unapproved paid request appears in the repository.
