---
title: AI-Led Radiology Execution-Boundary Admissibility
---

# AI-Led Radiology Execution-Boundary Admissibility

## Status

`PUBLIC_CONCEPTUAL_FORMALISM / EXECUTABLE_FIXTURES_INSTALLED / NON_CLINICAL_AUTHORITY`

This formalism distinguishes assistive imaging use from a transfer of diagnostic execution authority. It does not certify clinical performance, authorize autonomous diagnosis, evaluate any named hospital, or replace medical regulation, professional judgment, or patient-specific care.

## Core distinction

Three operating modes must not be treated as equivalent:

1. **Human-led diagnosis with AI assistance** — a qualified human remains responsible for reviewing the study and forming the diagnostic disposition.
2. **AI-first review with mandatory human review** — AI may prioritize or draft findings, but a qualified human must review the study before disposition binds.
3. **Autonomous negative clearance** — an unflagged study may bind as normal without human review.

The transition from the first or second mode to the third is a transfer of execution authority. It is not merely a productivity improvement.

## Execution boundary

The consequence-binding boundary is the point at which an imaging study is permitted to become a final clinical disposition, downstream treatment decision, discharge input, screening result, or no-follow-up outcome.

At that boundary, admissibility requires current evidence for:

- patient and study identity;
- model and version identity;
- approved indication and population;
- modality, protocol, body region, and image-series completeness;
- image quality and out-of-distribution assessment;
- relevant clinical context and prior-study availability;
- uncertainty and escalation posture;
- qualified human review obligations;
- policy and delegation references;
- durable provenance for model output, review, override, and final disposition.

## Decision classes

- `ADMIT_ASSISTIVE_USE` — AI output may assist, but does not independently bind disposition.
- `ADMIT_AI_FIRST_WITH_MANDATORY_HUMAN_REVIEW` — AI may lead triage or draft interpretation only when qualified review remains mandatory before binding.
- `REVIEW_REQUIRED` — evidence is sufficient to continue only through explicit human review or escalation.
- `DENY_AUTONOMOUS_CLEARANCE` — autonomous negative clearance is prohibited for the presented state.
- `FAIL_CLOSED` — required evidence is absent, contradictory, stale, or unverifiable.

## Fail-closed rules

A study cannot be autonomously cleared solely because the model emitted no flag. Missing priors, incomplete series, low image quality, unapproved use, unresolved model-version drift, or absent policy/delegation evidence must produce `FAIL_CLOSED` or `REVIEW_REQUIRED`.

## Negative clearance sampling

A policy may require human sampling of apparently normal studies even when AI performance is otherwise accepted. Sampling is an oversight control and does not convert an AI-only disposition into human-reviewed diagnosis.

## Longitudinal comparison

When prior imaging is clinically required, absence of the prior study prevents an autonomous final disposition. Temporal change cannot be inferred from a single current study merely because the current image appears normal.

## Automation-bias control

Human review is not meaningful when the reviewer is shown only the model conclusion, is prevented from independently inspecting source images, or is operationally pressured to accept AI output without adequate time and authority. Such a posture requires review escalation and cannot be represented as independent verification.

## Reconstructability

The final disposition must be reconstructable from durable evidence including:

- model/version and configuration;
- input-study identifiers and integrity references;
- model output and uncertainty;
- applicable policy and delegation;
- human reviewer identity, role, review scope, and timestamp;
- overrides and reasons;
- final disposition and downstream action.

## Publication boundary

This page makes no claim that any specific hospital has deployed autonomous radiology, that any named AI system is unsafe, or that StegVerse certifies medical devices or clinical outcomes. It defines a governance distinction between assistance and execution-authority transfer.