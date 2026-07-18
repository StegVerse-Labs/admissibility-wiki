# Decision Authority Governance Compatibility Procedure

## Scope

This procedure binds the internal `decision-authority` ecosystem record to the six mandatory governance-compatibility case families. It evaluates the public wiki vocabulary mapping to canonical ST-004 authority values without treating the mapping as an external implementation, runtime observation, certification, or grant of authority.

## Artifacts

- Source page: `docs/external-frameworks/decision-authority.md`
- Fixture: `tests/fixtures/external-frameworks/decision-authority-governance-compatibility-cases.v1.json`
- Evaluator: `scripts/run_decision_authority_governance_compatibility.py`
- Receipt: `reports/external-frameworks/decision-authority/decision-authority-stegverse-governance-compatibility-receipt.json`

## Required cases

The deterministic fixture covers positive alignment, negative or denied result, authority or delegation failure, stale or missing evidence, malformed or runtime-error input, and semantic-divergence protection.

## Evaluation boundary

A mapped `allowed` value can produce a simulated StegVerse `ALLOW` only when current policy, delegation, and evidence are present. `denied` produces `DENY`. Missing evidence, malformed input, unknown vocabulary, or any claim that the vocabulary mapping itself grants execution authority produces `FAIL_CLOSED`.

Decision vocabulary compatibility is evidence only. It does not create standing, prove transition admissibility, authorize execution, certify a runtime, or replace a current commitment-candidate review.

## Observation posture

The contract is authored with deterministic local simulation. Native runtime execution and independent reproduction are not observed. General compatibility claims remain prohibited. The canonical workflow owns future validation and publication observation.

## Automation ownership

`manual_tasks_required: []`

`user_action_required: false`
