# Quantum-Resilient Execution Security Simulation

This directory contains a deterministic illustrative model comparing inherited execution authority with state-bound execution authority.

## Run

```bash
python simulations/quantum_execution_security_model.py
```

Expected terminal marker:

```text
QUANTUM EXECUTION SECURITY MODEL: PASS
```

## What the model demonstrates

The model issues one capability from an initial valid state, then evaluates unchanged state, policy drift, delegation drift, stale evidence, and target-state drift.

The inherited-authority model executes in every case because possession of the earlier capability is treated as sufficient. The state-bound model re-evaluates current policy, delegation, evidence freshness, target state, and consumption state immediately before commit and blocks each drifted case.

## Boundaries

This is not a cryptographic benchmark, formal proof, deployment test, or security certification. It isolates one architectural property: whether stale authority is allowed to cross a changed state boundary.
