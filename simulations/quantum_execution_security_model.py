#!/usr/bin/env python3
"""Deterministic comparison of inherited and state-bound execution authority.

This model is illustrative. It does not benchmark cryptographic performance or
prove production security. It models whether execution occurs after policy,
delegation, evidence, or state drift between authorization and commit.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Iterable


@dataclass(frozen=True)
class TransitionState:
    policy_version: int
    delegation_version: int
    evidence_fresh: bool
    target_state: str


@dataclass(frozen=True)
class Capability:
    actor: str
    action: str
    target: str
    policy_version: int
    delegation_version: int
    target_state: str
    consumed: bool = False


@dataclass(frozen=True)
class Result:
    model: str
    executed: bool
    safe: bool
    reason: str


def issue_capability(actor: str, action: str, target: str, state: TransitionState) -> Capability:
    if not state.evidence_fresh:
        raise ValueError("cannot issue capability from stale evidence")
    return Capability(
        actor=actor,
        action=action,
        target=target,
        policy_version=state.policy_version,
        delegation_version=state.delegation_version,
        target_state=state.target_state,
    )


def canonical_admissibility(capability: Capability, current: TransitionState) -> tuple[bool, str]:
    if capability.consumed:
        return False, "capability_already_consumed"
    if not current.evidence_fresh:
        return False, "evidence_stale"
    if capability.policy_version != current.policy_version:
        return False, "policy_drift"
    if capability.delegation_version != current.delegation_version:
        return False, "delegation_drift"
    if capability.target_state != current.target_state:
        return False, "target_state_drift"
    return True, "admissible"


def inherited_authority(capability: Capability, current: TransitionState) -> Result:
    """Traditional model: possession of a previously issued capability executes."""
    safe, reason = canonical_admissibility(capability, current)
    return Result(
        model="inherited_authority",
        executed=True,
        safe=safe,
        reason="executed_with_" + reason,
    )


def state_bound_authority(capability: Capability, current: TransitionState) -> Result:
    """StegVerse model: current state is re-evaluated immediately before commit."""
    admissible, reason = canonical_admissibility(capability, current)
    if not admissible:
        return Result(
            model="state_bound_authority",
            executed=False,
            safe=True,
            reason="blocked_" + reason,
        )
    return Result(
        model="state_bound_authority",
        executed=True,
        safe=True,
        reason="executed_admissible",
    )


def scenarios(base: TransitionState) -> Iterable[tuple[str, TransitionState]]:
    yield "unchanged", base
    yield "policy_drift", replace(base, policy_version=base.policy_version + 1)
    yield "delegation_drift", replace(base, delegation_version=base.delegation_version + 1)
    yield "stale_evidence", replace(base, evidence_fresh=False)
    yield "target_state_drift", replace(base, target_state="changed")


def run() -> list[dict[str, object]]:
    base = TransitionState(
        policy_version=1,
        delegation_version=1,
        evidence_fresh=True,
        target_state="ready",
    )
    capability = issue_capability("agent-1", "commit", "target-1", base)
    rows: list[dict[str, object]] = []

    for scenario_name, current in scenarios(base):
        for evaluator in (inherited_authority, state_bound_authority):
            result = evaluator(capability, current)
            rows.append(
                {
                    "scenario": scenario_name,
                    "model": result.model,
                    "executed": result.executed,
                    "safe": result.safe,
                    "reason": result.reason,
                }
            )
    return rows


def validate(rows: list[dict[str, object]]) -> None:
    inherited_unsafe = [
        row
        for row in rows
        if row["model"] == "inherited_authority" and row["executed"] and not row["safe"]
    ]
    state_bound_unsafe = [
        row
        for row in rows
        if row["model"] == "state_bound_authority" and row["executed"] and not row["safe"]
    ]
    state_bound_blocks = [
        row
        for row in rows
        if row["model"] == "state_bound_authority" and not row["executed"]
    ]

    assert len(inherited_unsafe) == 4, inherited_unsafe
    assert not state_bound_unsafe, state_bound_unsafe
    assert len(state_bound_blocks) == 4, state_bound_blocks


if __name__ == "__main__":
    output = run()
    validate(output)
    for row in output:
        print(
            f"{row['scenario']:22} {row['model']:24} "
            f"executed={str(row['executed']):5} safe={str(row['safe']):5} {row['reason']}"
        )
    print("QUANTUM EXECUTION SECURITY MODEL: PASS")
