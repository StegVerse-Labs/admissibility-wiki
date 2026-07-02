# Governed LLM Demonstration Verification

This page describes how to verify the governed LLM demonstrator.

## Adapter verification

```bash
python scripts/run_end_to_end_demo.py --fixture examples/end_to_end/simple_query.json
python scripts/replay_demo.py --session-report reports/simple_query.session.json
python scripts/reconstruct_demo.py --session-report reports/simple_query.session.json
pytest tests/test_end_to_end_demo.py -v
```

## SDK verification

```bash
python scripts/smoke_governed_llm_sdk.py
python scripts/verify_governed_llm_demo_packet.py
pytest tests/test_governed_llm_demo_packet.py -v
```

## Wiki verification

```bash
python scripts/check_governed_llm_pages.py
python scripts/check_governed_llm_demo_docs.py
npm run build
```

## Boundary

The verification path confirms documentation and deterministic fixture behavior only. It does not create provider governance, execution authority, master-record persistence, or public deployment confirmation.
