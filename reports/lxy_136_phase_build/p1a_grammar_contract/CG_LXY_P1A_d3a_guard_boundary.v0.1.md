# CG-LXY P1-A D3A Guard Boundary v0.1

Status labels:

```text
P1A_GRAMMAR_DESIGN_DRAFT
NEEDS_USER_REVIEW
NOT_EXECUTABLE_PARSER
NOT_RUNTIME_SCHEMA
NOT_REPO_CONTRACT
NOT_CANON_AUTHORITY
NOT_DAPU_IR_AUTHORITY
NOT_SCORE_EVENT_AUTHORITY
NOT_SAMPLE_INGEST
NOT_ML_TRAINING_DATA
NOT_RENDER_OUTPUT
```

## Purpose

This document defines how P1-A grammar design may use D3A generation-safe guardrails without reading or copying D3B phrase-level oracle material.

## Generation-Safe D3A Reads

P1 Generation / grammar design may read scoped guard material only when it is used as guardrail evidence, not as a target answer. Allowed D3A categories are:

- scoped component guards;
- scoped label guards;
- `must_not_read_as`;
- known invalid type binding;
- known component split error;
- known marker-as-sounding error.

The guard may refer to matched component ids, matched labels, matched template ids, local construction context, or scoped phrase ids as scope metadata. It must not be promoted into a phrase reading source.

## Forbidden D3B Reads

P1 Generation / grammar design must not read or use:

- `expected_continuous_reading`;
- `must_include`;
- `phrase_integration_cases`;
- `source_report`;
- old phrase report references;
- complete P1-P6 readings;
- any phrase-level oracle.

If a file mixes D3A and D3B fields, P1-A must treat the D3B fields as unavailable. Later implementation should prefer a sanitized D3A view.

## Guard Effects

D3A guard application must use this enum:

```text
HARD_REJECT
SOFT_PENALTY
FORCE_UNRESOLVED
NEEDS_CONTEXT
NEEDS_HUMAN_REVIEW
NOT_APPLICABLE
```

| guard action | default trigger | meaning |
| --- | --- |
| `HARD_REJECT` | impossible lexical-type / slot binding; marker-as-sounding; scoped forbidden parse with complete scope match | Grammar could form a candidate, but the scoped guard forbids that parse attempt. |
| `SOFT_PENALTY` | known confusable component but at least one legal interpretation remains | Candidate remains reviewable but receives guard penalty and explanation. |
| `FORCE_UNRESOLVED` | component conflict or insufficient evidence | Parser must emit unresolved rather than choose a risky parse. |
| `NEEDS_CONTEXT` | missing inherited context | Candidate requires caller-provided `context_ref` or `inherited_context`; P1 must not search history. |
| `NEEDS_HUMAN_REVIEW` | human confirmation is the only missing gate | Candidate can be shown only as review-needed draft. |
| `NOT_APPLICABLE` | scope mismatch | Guard scope does not match; no penalty or rejection applies. |

Literal forbidden strings are not global forbidden words.

## Scoped Literal Policy

A literal forbidden string is not a global forbidden word. It is only invalid when the guard scope matches. Legal component labels and legal readings elsewhere must remain legal outside the guard scope.

Required parser behavior:

1. read guard scope first;
2. compare scope to current component ids, template ids, and local rule context;
3. apply the guard only on scope match;
4. record `applied_guard_ids` or `skipped_guard_ids`;
5. explain scope mismatch when a guard is not applied;
6. use `NOT_APPLICABLE` for scope mismatch rather than a global literal scan.

## Parser Boundary

D3A guards are not grammar production rules. They run after a candidate parse attempt has enough structure to compare scope, but before accepted candidate ranking is finalized.

D3A cannot:

- create a new parse by itself;
- fill a missing required slot;
- supply phrase-level context;
- override D1 component normalization;
- override D2 grammar legality;
- authorize Dapu IR or score facts.

## Human Review Boundary

When a guard blocks an otherwise plausible candidate, the parser response should keep a rejected candidate record and a suggested next action such as:

```text
review_component_identity
review_template_scope
review_context_source
add_learning_mode_proposal_after_user_review
```

No guard-triggered repair may update references, tests, skills, canon, or runtime data in P1-A.
