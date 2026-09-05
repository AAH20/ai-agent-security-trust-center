import json
import tempfile
import unittest
from pathlib import Path

from agent_trust.core import build_bundle, calculate_score, validate_profile, verify_bundle
from agent_trust.render import render_profile


ROOT = Path(__file__).parents[1]
PROFILE = ROOT / "examples/procurement-agent/agent-assurance.json"
EVIDENCE = ROOT / "examples/procurement-agent/evidence-summary.json"


class TrustCenterTests(unittest.TestCase):
    def setUp(self):
        self.profile = json.loads(PROFILE.read_text())

    def test_reference_profile_is_valid(self):
        self.assertEqual(validate_profile(self.profile), [])

    def test_weighted_score(self):
        self.assertEqual(calculate_score(self.profile)["score"], 77.5)

    def test_untested_gate_prevents_verified_status(self):
        self.profile["assurance"]["status"] = "VERIFIED"
        result = calculate_score(self.profile)
        self.assertEqual(result["effective_status"], "REVIEW_REQUIRED")

    def test_failed_gate_overrides_high_score(self):
        for key in self.profile["assurance"]["scores"]:
            self.profile["assurance"]["scores"][key] = 100
        self.profile["assurance"]["mandatory_gates"]["approval_enforcement"] = "FAIL"
        result = calculate_score(self.profile)
        self.assertEqual(result["score"], 100)
        self.assertEqual(result["effective_status"], "RESTRICTED")

    def test_bundle_detects_tampering(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            profile = target / PROFILE.name
            evidence = target / EVIDENCE.name
            profile.write_bytes(PROFILE.read_bytes())
            evidence.write_bytes(EVIDENCE.read_bytes())
            bundle = target / "bundle.json"
            build_bundle(profile, [evidence], bundle)
            self.assertEqual(verify_bundle(bundle, target), [])
            evidence.write_text("tampered")
            self.assertIn("content hash mismatch", verify_bundle(bundle, target)[0])

    def test_static_trust_center_renders(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "index.html"
            render_profile(PROFILE, output)
            content = output.read_text()
            self.assertIn("Example Procurement Assistant", content)
            self.assertIn("REVIEW_REQUIRED", content)


if __name__ == "__main__":
    unittest.main()
