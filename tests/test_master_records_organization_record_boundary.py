import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_llm_free_tier_trust_chain.py"


def _load():
    spec = importlib.util.spec_from_file_location("check_llm_free_tier_trust_chain", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestMasterRecordsOrganizationRecordBoundary(unittest.TestCase):
    def test_new_name_is_read(self):
        m = _load()
        out = m.normalize_organization_record_boundary({m.ORGANIZATION_RECORD_BOUNDARY: False})
        self.assertIs(out[m.ORGANIZATION_RECORD_BOUNDARY], False)

    def test_legacy_name_is_read(self):
        m = _load()
        out = m.normalize_organization_record_boundary({m.LEGACY_ORGANIZATION_RECORD_BOUNDARY: False})
        self.assertIs(out[m.ORGANIZATION_RECORD_BOUNDARY], False)

    def test_new_name_wins_over_legacy(self):
        m = _load()
        out = m.normalize_organization_record_boundary(
            {m.ORGANIZATION_RECORD_BOUNDARY: False, m.LEGACY_ORGANIZATION_RECORD_BOUNDARY: True}
        )
        self.assertIs(out[m.ORGANIZATION_RECORD_BOUNDARY], False)

    def test_published_status_emits_only_new_name(self):
        m = _load()
        data = json.loads(m.REFERENCES.read_text(encoding="utf-8"))
        self.assertIn(m.ORGANIZATION_RECORD_BOUNDARY, data["boundaries"])
        self.assertNotIn(m.LEGACY_ORGANIZATION_RECORD_BOUNDARY, data["boundaries"])

    def test_checker_passes(self):
        cp = subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, text=True, capture_output=True)
        self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)


if __name__ == "__main__":
    unittest.main()
