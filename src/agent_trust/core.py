from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping


SCORE_WEIGHTS = {
    "identity_authorization": 25,
    "tool_data_security": 20,
    "adversarial_resilience": 20,
    "operational_reliability": 15,
    "governance_evidence": 20,
}
MANDATORY_GATES = (
    "approval_enforcement",
    "cross_tenant_isolation",
    "audit_log_completeness",
    "rollback_or_safe_failure",
)
STATUSES = {"VERIFIED", "REVIEW_REQUIRED", "RESTRICTED", "EXPIRED"}


class ProfileError(ValueError):
    pass


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def validate_profile(profile: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    required = ("schema_version", "agent_id", "name", "version", "owner", "purpose", "autonomy_level", "tools", "data_classes", "authorization", "assurance")
    for field in required:
        if field not in profile:
            errors.append(f"missing required field: {field}")
    level = profile.get("autonomy_level")
    if not isinstance(level, int) or not 0 <= level <= 5:
        errors.append("autonomy_level must be an integer from 0 to 5")
    if not isinstance(profile.get("tools", []), list):
        errors.append("tools must be an array")
    if not isinstance(profile.get("data_classes", []), list):
        errors.append("data_classes must be an array")
    assurance = profile.get("assurance", {})
    if not isinstance(assurance, Mapping):
        errors.append("assurance must be an object")
        return errors
    if assurance.get("status") not in STATUSES:
        errors.append("assurance.status must be VERIFIED, REVIEW_REQUIRED, RESTRICTED, or EXPIRED")
    scores = assurance.get("scores", {})
    for dimension in SCORE_WEIGHTS:
        value = scores.get(dimension) if isinstance(scores, Mapping) else None
        if not isinstance(value, (int, float)) or not 0 <= value <= 100:
            errors.append(f"assurance.scores.{dimension} must be between 0 and 100")
    gates = assurance.get("mandatory_gates", {})
    if not isinstance(gates, Mapping):
        errors.append("assurance.mandatory_gates must be an object")
    else:
        for gate in MANDATORY_GATES:
            if gates.get(gate) not in {"PASS", "FAIL", "NOT_TESTED"}:
                errors.append(f"mandatory gate {gate} must be PASS, FAIL, or NOT_TESTED")
    return errors


def calculate_score(profile: Mapping[str, Any]) -> dict[str, Any]:
    errors = validate_profile(profile)
    if errors:
        raise ProfileError("; ".join(errors))
    assurance = profile["assurance"]
    scores = assurance["scores"]
    weighted = round(sum(float(scores[key]) * weight for key, weight in SCORE_WEIGHTS.items()) / sum(SCORE_WEIGHTS.values()), 2)
    gates = assurance["mandatory_gates"]
    failed = sorted(gate for gate in MANDATORY_GATES if gates[gate] == "FAIL")
    untested = sorted(gate for gate in MANDATORY_GATES if gates[gate] == "NOT_TESTED")
    status = assurance["status"]
    if failed:
        status = "RESTRICTED"
        why = f"mandatory gates failed: {', '.join(failed)}"
    elif untested and status == "VERIFIED":
        status = "REVIEW_REQUIRED"
        why = f"mandatory gates not tested: {', '.join(untested)}"
    else:
        why = "declared status is consistent with mandatory gates"
    valid_until = assurance.get("valid_until")
    if valid_until:
        try:
            expiry = datetime.fromisoformat(valid_until.replace("Z", "+00:00"))
            if expiry < datetime.now(timezone.utc):
                status, why = "EXPIRED", "assurance validity period has ended"
        except ValueError:
            raise ProfileError("assurance.valid_until must be ISO 8601")
    return {"score": weighted, "effective_status": status, "reason": why, "failed_gates": failed, "untested_gates": untested}


def build_bundle(profile_path: Path, evidence_paths: list[Path], output: Path) -> dict[str, Any]:
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    score = calculate_score(profile)
    files = []
    for item in [profile_path, *evidence_paths]:
        content = item.read_bytes()
        files.append({"path": item.name, "sha256": sha256(content), "bytes": len(content)})
    manifest = {
        "bundle_version": "1.0",
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "agent_id": profile["agent_id"],
        "agent_version": profile["version"],
        "assurance": score,
        "files": files,
        "signature": {"status": "UNSIGNED", "reason": "Attach a Sigstore or organizational signature before external reliance"},
    }
    envelope = {"manifest": manifest, "manifest_sha256": sha256(canonical_json(manifest))}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(envelope, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return envelope


def verify_bundle(bundle_path: Path, source_dir: Path) -> list[str]:
    envelope = json.loads(bundle_path.read_text(encoding="utf-8"))
    errors: list[str] = []
    manifest = envelope.get("manifest", {})
    if envelope.get("manifest_sha256") != sha256(canonical_json(manifest)):
        errors.append("manifest hash mismatch")
    for entry in manifest.get("files", []):
        item = source_dir / entry["path"]
        if not item.is_file():
            errors.append(f"missing bundle source: {entry['path']}")
        elif sha256(item.read_bytes()) != entry["sha256"]:
            errors.append(f"content hash mismatch: {entry['path']}")
    return errors
