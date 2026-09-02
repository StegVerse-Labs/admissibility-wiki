import copy, json, unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from check_volatile_memory_evidence_contract import validate

BASE=json.loads((Path(__file__).resolve().parents[1]/"data/forensics/volatile-memory-reference-manifest.json").read_text())

class TestVolatileMemoryEvidence(unittest.TestCase):
    def test_reference_passes(self):
        self.assertTrue(validate(copy.deepcopy(BASE)))
    def test_missing_authorization_fails(self):
        m=copy.deepcopy(BASE); del m["authorization"]["authorization_ref"]
        with self.assertRaises(ValueError): validate(m)
    def test_missing_machine_identity_fails(self):
        m=copy.deepcopy(BASE); m["target"]["machine_identity"]=""
        with self.assertRaises(ValueError): validate(m)
    def test_bad_evidence_hash_fails(self):
        m=copy.deepcopy(BASE); m["evidence_object"]["sha256"]="bad"
        with self.assertRaises(ValueError): validate(m)
    def test_stream_gap_fails(self):
        m=copy.deepcopy(BASE); m["evidence_object"]["chunks"][0]["index"]=1
        with self.assertRaises(ValueError): validate(m)
    def test_admissibility_claim_fails(self):
        m=copy.deepcopy(BASE); m["authority"]["claims_admissibility"]=True
        with self.assertRaises(ValueError): validate(m)

if __name__=="__main__":
    unittest.main()
