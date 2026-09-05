from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .core import ProfileError, build_bundle, calculate_score, validate_profile, verify_bundle
from .render import render_profile


def main() -> None:
    parser = argparse.ArgumentParser(prog="agent-trust", description="Validate and publish AI agent security assurance profiles")
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("validate", "score"):
        cmd = commands.add_parser(name)
        cmd.add_argument("profile", type=Path)
    bundle = commands.add_parser("bundle")
    bundle.add_argument("profile", type=Path)
    bundle.add_argument("--evidence", type=Path, action="append", default=[])
    bundle.add_argument("--output", type=Path, required=True)
    verify = commands.add_parser("verify")
    verify.add_argument("bundle", type=Path)
    verify.add_argument("--source-dir", type=Path, required=True)
    render = commands.add_parser("render")
    render.add_argument("profile", type=Path)
    render.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "validate":
            errors = validate_profile(json.loads(args.profile.read_text(encoding="utf-8")))
            if errors:
                print("\n".join(errors), file=sys.stderr)
                raise SystemExit(1)
            print("profile valid")
        elif args.command == "score":
            print(json.dumps(calculate_score(json.loads(args.profile.read_text(encoding="utf-8"))), indent=2))
        elif args.command == "bundle":
            print(json.dumps(build_bundle(args.profile, args.evidence, args.output), indent=2))
        elif args.command == "verify":
            errors = verify_bundle(args.bundle, args.source_dir)
            if errors:
                print("\n".join(errors), file=sys.stderr)
                raise SystemExit(1)
            print("bundle hashes verified; cryptographic signature status is separate")
        else:
            render_profile(args.profile, args.output)
            print(args.output)
    except (ProfileError, json.JSONDecodeError, OSError) as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(2)


if __name__ == "__main__":
    main()
