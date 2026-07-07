# CG-LXY P1-A Grammar Contract v0.1

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

## 1. P1-A Scope

P1-A only designs the Phase 1 Grammar Parser MVP contract for already recognized and normalized component token sequences. It defines parser input shape, lexical component types, semantic slot roles, local production rule families, parse status, ambiguity handling, D3A guard use, and output shape.

This document is a design input for later P1-B fixtures and P1-C executable parser work. It is not parser code, not a runtime schema, not a repo contract, and not any kind of Dapu IR or score-event authority.

## 2. Phase Boundary

P1 starts from a known component sequence and does not touch images. P1-A designs a single notation-unit and local marker grammar. P1-B may later turn this design into fixtures. P1-C may later implement an executable parser only after explicit authorization.

P2 owns visual component candidate detection. P3 owns parser plus lattice top-k integration. P4 owns line-level unit streams and coverage ledgers. P5 owns phrase-level reconstruction, state spans, and cross-unit context. P6 owns human-review-driven proposal material. P1-A must not enter any of those phases.

## 3. D1 / D2 / D3A Read Relationship

Generation-side grammar design may read D1 component references, D1 alias normalization policy, D2 construction templates, and D3A scoped guardrails. It must not read D3B phrase-level oracle answers.

D1 answers what a component is as reference evidence. D2 answers which local component patterns may form a legal construction. D3A prevents known scoped failures, but it does not provide the target phrase answer.

## 4. Lexical Type vs Semantic Slot

Lexical component type describes the component itself. Semantic slot role describes the role assigned by a grammar parse.

For example, a numeric component such as `七` is only `NUMERIC_COMPONENT` during tokenization. It may later become `hui_position`, `string_number`, `range_start`, `range_end`, `count`, or `unknown_numeric_role`, depending on the matched production, neighboring tokens, and context.

Therefore:

```text
lexical_component_type != semantic_slot_role
```

No tokenizer may hard-code a number as hui or string. No lexical category may by itself promote a component into a sounding unit.

## 5. Parser Input Lifecycle

The parser receives a `token_sequence` of already normalized v0.2 primary component tokens. Required Phase 1 fields are token identity, order, v0.2 component id, Chinese label, lexical component type, source category, normalization status, optional traceability ids, optional semantic hints, optional local relations, input confidence, and metadata.

Phase 1 may accept:

- pure component sequence;
- component sequence plus optional local relation fields;
- component sequence plus optional semantic role hint, treated as non-authoritative;
- incomplete sequence;
- repeated components;
- unknown component placeholders;
- legacy id input only before parse normalization;
- v0.1 source component id input only before parse normalization.

Phase 1 must not require image fields such as `bbox`, `image_path`, `visual_similarity`, or `pixel_coordinates`.

## 6. Normalization Lifecycle

Primary parse ids must be category-based v0.2 ids. Legacy `COMP-001..038` and v0.1 source `COMP-100..273` ids may appear only as traceability inputs. They must be normalized to v0.2 primary ids before grammar matching.

If a legacy or source id cannot be normalized, the parser response must use `COMPONENT_ID_NORMALIZATION_GAP`. The parser may still report unresolved items, but it must not silently parse unnormalized ids as primary ids.

## 7. Grammar Matching Lifecycle

P1-A grammar matching is local and bounded:

```text
input tokens
-> normalized tokens
-> structured slots
-> semantic resolution
-> surface reading candidate
```

`structured_parse` / semantic slots are the primary parser result. `surface_reading_candidate` is derived from `structured_parse` as non-authority display text and must never overwrite, repair, or backfill slots. `literal_component_gloss` preserves the direct gloss of input components before semantic slot resolution.

P1-A allows local marker sequences, but it does not reconstruct full phrase spans. State span handling such as `STATE_START + unit* + STATE_END` is reserved for P5. P1-A may classify state markers and validate local legality only.

## 8. Locked Decision: RH_ACTION + STRING_NUMBER

`RH_ACTION + STRING_NUMBER` must not default to `VALID_COMPLETE`.

Stable status policy:

- no explicit sound-state evidence and no explicit context: `VALID_AMBIGUOUS`;
- ambiguity may carry an open-string interpretation candidate and an inherited-context interpretation candidate;
- explicit scattered/open-string evidence or caller-declared `no_inherited_context`: `VALID_COMPLETE`;
- valid caller-provided `inherited_context`: `VALID_WITH_CONTEXT`;
- caller declares context is required but omits `context_ref` / `inherited_context`: `INCOMPLETE` with a missing context requirement.

The parser must not infer `sound_type_candidate=散` from `RH_ACTION + STRING_NUMBER` alone. Sound type metadata is:

```text
sound_type_candidate: 散 | 按 | 泛 | null
sound_type_resolution_status: RESOLVED | AMBIGUOUS | CONTEXT_REQUIRED | UNRESOLVED
```

`sound_type_resolution_status` is not a sound type. The only sound types remain `散`、`按`、`泛`.

## 9. Locked Decision: Explicit Context Only

P1 does not perform implicit historical search.

```text
implicit_backward_scan_depth = 0
accepted context inputs = context_ref, inherited_context
```

P1 may validate caller-provided context compatibility, but it must not search the previous notation unit, previous phrase, previous line, or arbitrary historical units. Phrase-level context discovery and span reconstruction belong to P5.

## 10. Ambiguity Handling

P1 must not assume one input has one answer. It returns n-best candidates with deterministic heuristic grammar scores. These scores are not calibrated visual probabilities.

Sorting policy:

1. invalid and hard guard rejected attempts do not enter `accepted_candidates`;
2. complete required slots outrank incomplete parses;
3. higher specificity outranks generic rules;
4. fewer context dependencies outrank more context dependencies;
5. fewer unresolved tokens outrank more unresolved tokens;
6. higher consumed-token coverage outranks lower coverage;
7. rule priority is the final grammar tie-break;
8. candidate id is the deterministic final tie-break.

## 11. Guard Application

D3A guardrails are scoped. A guard applies only when its component, template, or declared local context matches. A forbidden literal is not a global ban.

Guard action enum:

```text
HARD_REJECT
SOFT_PENALTY
FORCE_UNRESOLVED
NEEDS_CONTEXT
NEEDS_HUMAN_REVIEW
NOT_APPLICABLE
```

Default mapping:

- impossible lexical-type / slot binding -> `HARD_REJECT`;
- marker-as-sounding -> `HARD_REJECT`;
- scoped forbidden parse with complete scope match -> `HARD_REJECT`;
- known confusable component with remaining legal interpretation -> `SOFT_PENALTY`;
- component conflict or insufficient evidence -> `FORCE_UNRESOLVED`;
- missing inherited context -> `NEEDS_CONTEXT`;
- human confirmation only -> `NEEDS_HUMAN_REVIEW`;
- scope mismatch -> `NOT_APPLICABLE`.

P1-A must preserve `scoped_component_or_template_context` semantics and must not treat D3A as an answer oracle.

## 12. Output Lifecycle

The parser response contains input tokens, normalization summary, parse status, accepted candidates, rejected candidates, unconsumed tokens, context requirements, guard summary, input contract errors, and authority flags.

Accepted candidates contain candidate id, rank, `structured_parse`, `surface_reading_candidate`, `literal_component_gloss`, parse type, status, consumed and unconsumed token ids, slots, applied rules, applied guards, context requirements, unresolved items, sound type candidate / resolution status, score, score type, score breakdown, reason, and authority flags.

Rejected candidates contain attempted rule id, consumed tokens, rejection status, rejection reason, guard ids, recoverability, and suggested next action.

Input contract failures use `INPUT_CONTRACT_INVALID`. This status is reserved for empty input, required field missing, duplicate `token_id`, duplicate or invalid `sequence_index`, invalid field type, malformed component ID, and schema-level input failure. These are not `INVALID_TYPE_COMBINATION`.

## 13. Authority Boundary

Every P1-A output remains:

```text
not_repo_contract=true
not_canon_authority=true
not_dapu_ir_authority=true
not_score_event_authority=true
not_sample_ingest=true
not_ml_training_data=true
not_render_output=true
needs_human_review=true
```

P1-A must not modify canon, Dapu IR, score facts, component registry, construction templates, goldsets, forbidden fixtures, skills, sample ingest, ML, render, R0/R1/R2/E/F, or accepted F artifacts.

## 14. P1-B Handoff

P1-B may create fixtures only after explicit authorization. It must use two fixture tracks:

A. abstract fixtures:

- validate grammar logic;
- avoid dependency on a concrete piece;
- prevent LXY overfitting.

B. sanitized real-ID fixtures:

- validate D1 registry, alias normalization, and D2 integration;
- use general atlas component ids;
- must not carry LXY phrase id, complete reading, `source_report`, or oracle.

It should use this contract to create answer-blind cases for:

- valid right-hand plus string constructions;
- pressed left-finger plus hui plus right-hand plus string constructions;
- context-required constructions;
- non-sounding marker classifications;
- incomplete and unresolved sequences;
- invalid order and invalid type-combination rejection;
- scoped D3A guard behavior.

P1-B must not copy phrase-level oracle readings into generation fixtures.

## 15. P1-C Handoff

P1-C may implement an executable parser only after a later task opens code and tests. The implementation should keep tokenizer normalization, lexical typing, rule matching, guard application, n-best scoring, and output rendering as separable units.

P1-C is not authorized by this document.

## 16. Design Decisions Locked

The following user decisions are locked:

- `P1A-DEC-001-DUAL-OUTPUT`
- `P1A-DEC-002-RH-STRING-AMBIGUITY`
- `P1A-DEC-003-EXPLICIT-CONTEXT-ONLY`
- `P1A-DEC-004-D3A-GUARD-ACTIONS`
- `P1A-DEC-005-DUAL-FIXTURE-STRATEGY`

The following corrections are locked:

- `P1A-COR-001-INPUT-CONTRACT-INVALID`
- `P1A-COR-002-UNKNOWN-FALLBACK-ONLY`
- `P1A-COR-003-GENERIC-MARKER-WHITELIST`

`unresolved_user_decisions` is now empty for P1-B design readiness. P1-C implementation remains not authorized.
