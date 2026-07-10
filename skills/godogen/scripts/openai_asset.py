#!/usr/bin/env python3
"""Generate one staged game image with the OpenAI Python SDK and record provenance."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def safe_name(value: str) -> str:
    allowed = [character.lower() if character.isalnum() else "-" for character in value]
    compact = "-".join(part for part in "".join(allowed).split("-") if part)
    if not compact:
        raise ValueError("asset name must contain letters or numbers")
    return compact


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def append_manifest(path: Path, entry: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict) or not isinstance(payload.get("assets"), list):
            raise ValueError(f"invalid asset manifest: {path}")
    else:
        payload = {"schema_version": 1, "assets": []}
    payload["assets"].append(entry)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", required=True, help="Stable descriptive asset name")
    parser.add_argument("--prompt", help="Prompt text. Prefer --prompt-file for durable work")
    parser.add_argument("--prompt-file", help="UTF-8 file containing the approved prompt")
    parser.add_argument("--model", default=os.environ.get("OPENAI_IMAGE_MODEL"), help="Image model name or OPENAI_IMAGE_MODEL")
    parser.add_argument("--size", default="1024x1024")
    parser.add_argument("--quality", default="auto")
    parser.add_argument("--background", choices=["auto", "transparent", "opaque"], default="auto")
    parser.add_argument("--output-dir", default="artifacts/godogen/asset-staging")
    parser.add_argument("--manifest", default="artifacts/godogen/asset-manifest.json")
    parser.add_argument("--intended-use", required=True)
    parser.add_argument("--approved-budget", required=True, help="Human-readable approved limit, for example USD 1.00")
    return parser.parse_args()


def load_prompt(args: argparse.Namespace) -> tuple[str, str | None]:
    if bool(args.prompt) == bool(args.prompt_file):
        raise ValueError("provide exactly one of --prompt or --prompt-file")
    if args.prompt_file:
        prompt_path = Path(args.prompt_file).expanduser().resolve()
        return prompt_path.read_text(encoding="utf-8").strip(), str(prompt_path)
    return args.prompt.strip(), None


def main() -> int:
    args = parse_args()
    if not os.environ.get("OPENAI_API_KEY"):
        print("error: OPENAI_API_KEY is not set", file=sys.stderr)
        return 2
    if not args.model:
        print("error: provide --model or set OPENAI_IMAGE_MODEL", file=sys.stderr)
        return 2
    try:
        prompt, prompt_file = load_prompt(args)
        name = safe_name(args.name)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if not prompt:
        print("error: prompt is empty", file=sys.stderr)
        return 2

    try:
        from openai import OpenAI
    except ImportError:
        print("error: install the optional SDK with: python -m pip install openai", file=sys.stderr)
        return 2

    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output = output_dir / f"{name}-{timestamp}.png"

    client = OpenAI()
    request: dict[str, Any] = {
        "model": args.model,
        "prompt": prompt,
        "size": args.size,
        "quality": args.quality,
        "n": 1,
    }
    if args.background != "auto":
        request["background"] = args.background

    try:
        response = client.images.generate(**request)
        item = response.data[0]
        encoded = getattr(item, "b64_json", None)
        if not encoded:
            raise RuntimeError("provider response did not contain base64 image data")
        output.write_bytes(base64.b64decode(encoded))
    except Exception as exc:
        print(f"OpenAI image generation failed: {exc}", file=sys.stderr)
        return 1

    entry = {
        "id": f"{name}-{timestamp}",
        "provider": "OpenAI",
        "tool_or_model": args.model,
        "source": "api-generation",
        "prompt": prompt if prompt_file is None else None,
        "prompt_file": prompt_file,
        "requested_size": args.size,
        "quality": args.quality,
        "transparent_background": args.background == "transparent",
        "staging_path": str(output),
        "runtime_path": None,
        "sha256": sha256(output),
        "approved_budget": args.approved_budget,
        "estimated_cost": None,
        "actual_cost": None,
        "manual_edits": [],
        "approved": False,
        "intended_use": args.intended_use,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    append_manifest(Path(args.manifest).expanduser().resolve(), entry)
    print(json.dumps(entry, indent=2, sort_keys=True))
    print("Asset remains staged and unapproved until it is inspected in the game.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
