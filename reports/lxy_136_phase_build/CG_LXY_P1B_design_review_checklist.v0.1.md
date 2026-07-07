# CG-LXY P1-B Design Review Checklist v0.1

Status labels:

- P1B_FIXTURE_DESIGN_DRAFT
- NEEDS_USER_REVIEW
- NOT_EXECUTABLE_TEST
- NOT_PARSER_IMPLEMENTATION
- NOT_RUNTIME_SCHEMA
- NOT_REPO_CONTRACT
- NOT_CANON_AUTHORITY
- NOT_DAPU_IR_AUTHORITY
- NOT_SCORE_EVENT_AUTHORITY
- NOT_SAMPLE_INGEST
- NOT_ML_TRAINING_DATA
- NOT_RENDER_OUTPUT

Allowed checklist states:

- PASS
- FAIL
- NEEDS_USER_DECISION
- NOT_APPLICABLE

## A. Repo Context Checks

| Check | Status | Evidence |
| --- | --- | --- |
| Branch is `main` | PASS | Initial gate checked with `git branch --show-current`. |
| HEAD is `3a4084a4ece64346baf151ddf00b9d103488de35` | PASS | Initial gate checked with `git rev-parse HEAD`. |
| Worktree was clean before write | PASS | Initial gate checked with `git status --short --untracked-files=all`. |
| No pull/stash/reset/restore/clean performed | PASS | Only read commands and allowed new-file writes were used. |

## B. Directory Gate Checks

| Check | Status | Evidence |
| --- | --- | --- |
| `reports/lxy_136_phase_build/` exists | PASS | Verified before write. |
| `tests/fixtures/cyber_guqin/component_guided_transcription/` exists | PASS | Verified before write. |
| No directory creation performed | PASS | No `mkdir` used. |

## C. P1-A Contract Consistency

| Check | Status | Evidence |
| --- | --- | --- |
| `structured_parse` remains primary | PASS | Fixture assertions bind slots before surface text. |
| `surface_reading_candidate` remains derived | PASS | Surface assertions are local and non-authoritative. |
| `literal_component_gloss` boundary preserved | PASS | Inputs retain raw component labels and trace fields. |
| `implicit_backward_scan_depth=0` preserved | PASS | Context fixtures assert explicit context only. |
| `INPUT_CONTRACT_INVALID` included | PASS | Abstract cases P1B-ABS-001 through P1B-ABS-008. |

## D. Abstract Fixture Coverage

| Check | Status | Evidence |
| --- | --- | --- |
| Input contract validation covered | PASS | 8 abstract schema-failure cases. |
| RH_ACTION + STRING_NUMBER branches covered | PASS | P1B-ABS-009 through P1B-ABS-013. |
| Motion host requirements covered | PASS | P1B-ABS-025 through P1B-ABS-028. |
| Marker non-sounding behavior covered | PASS | State/timing/generic marker cases. |
| Unknown fallback behavior covered | PASS | P1B-ABS-036 through P1B-ABS-038. |

## E. Real-ID Fixture Coverage

| Check | Status | Evidence |
| --- | --- | --- |
| Primary v0.2 IDs used | PASS | P1B-REAL-001 and related cases. |
| Registry labels/types are traceable | PASS | Manifest real-id trace records selected IDs. |
| At least 8 production families covered | PASS | Real fixture covers RH string, context, state start/end, timing, generic, special, pre-motion, LF/HUI/RH/string, unknown fallback. |
| Surface assertions are local-only | PASS | Real fixture uses `LOCAL_NOTATION_UNIT_ONLY`. |

## F. Normalization Coverage

| Check | Status | Evidence |
| --- | --- | --- |
| Primary v0.2 input covered | PASS | P1B-REAL-001. |
| Legacy alias normalization covered | PASS | P1B-REAL-002 and P1B-REAL-011. |
| Source v0.1 normalization covered | PASS | P1B-REAL-003, 005, 006, 007, 008, 009, 010, 012. |
| Normalization gap covered | PASS | P1B-REAL-004 and P1B-ABS-042. |

## G. Status Coverage

| Check | Status | Evidence |
| --- | --- | --- |
| 11 parser status values covered | PASS | Verified across the four fixture JSON files. |
| Ambiguous vs incomplete vs unresolved vs invalid separated | PASS | Numeric-alone, missing-slot, incompatible-context, invalid-order/type cases. |

## H. Production-Rule Coverage

| Check | Status | Evidence |
| --- | --- | --- |
| 11 production families covered | PASS | Matrix and manifest count all P1-A production families. |
| PR-UNKNOWN fallback only | PASS | P1B-ABS-038 and P1B-REAL-012. |
| PR-GENERIC-MARKER whitelist/subtype boundary | PASS | P1B-ABS-029 through P1B-ABS-031. |

## I. Guard-Action Coverage

| Check | Status | Evidence |
| --- | --- | --- |
| Six D3A actions covered | PASS | Guard fixture includes two cases per action. |
| Scope mismatch maps to NOT_APPLICABLE | PASS | P1B-GUARD-011 and P1B-GUARD-012. |
| Literal forbidden string is not global blacklist | PASS | Guard fixture assertions require scope match. |

## J. Ranking Coverage

| Check | Status | Evidence |
| --- | --- | --- |
| Eight ranking criteria covered | PASS | P1B-RANK-001 through P1B-RANK-008. |
| Floating micro-difference not required | PASS | Ranking fixture uses deterministic criterion order and candidate id final tie-break. |

## K. Invalid-Matrix Traceability

| Check | Status | Evidence |
| --- | --- | --- |
| 24 invalid matrix rows referenced | PASS | Matrix and manifest include full row coverage. |
| Schema failures stay schema-level | PASS | P1B-ABS-001 through P1B-ABS-008. |
| Partial consumption records unconsumed token | PASS | P1B-ABS-041. |

## L. Anti-Overfit Checks

| Check | Status | Evidence |
| --- | --- | --- |
| Abstract fixtures do not depend on real component IDs | PASS | Abstract cases use `ABS-*` IDs. |
| Real-ID fixtures vary component IDs per production | PASS | Real fixture uses distinct right-hand, marker, state, special and motion IDs. |
| Ranking fixtures are synthetic and local | PASS | Ranking cases use candidate sets, not score facts. |

## M. Anti-Oracle Checks

| Check | Status | Evidence |
| --- | --- | --- |
| D3B goldset not read | PASS | Not used as source. |
| Old candidate/answer reports not read | PASS | Not used as source. |
| No score image or crop read | PASS | Not used as source. |
| No complete reading oracle encoded | PASS | Fixture assertions are local notation-unit or abstract. |

## N. Authority Checks

| Check | Status | Evidence |
| --- | --- | --- |
| Not canon authority | PASS | Every fixture carries non-authority labels. |
| Not Dapu IR authority | PASS | Every fixture carries non-authority labels. |
| Not runtime schema | PASS | Every fixture carries draft labels only. |
| Not sample ingest / ML / render | PASS | Every fixture carries boundary labels. |

## O. P1-C Readiness

| Check | Status | Evidence |
| --- | --- | --- |
| Ready for P1-C implementation design review | PASS | Fixtures and matrix define input/output cases. |
| Ready for direct P1-C code | FAIL | User review and explicit implementation authorization still required. |
| Unresolved user decisions | PASS | `[]`. |

## P. P1-C Code-Not-Yet-Authorized Checks

| Check | Status | Evidence |
| --- | --- | --- |
| No parser code written | PASS | No Python/parser files created. |
| No Python tests written | PASS | Only JSON/CSV/Markdown design artifacts created. |
| No pytest/unittest run | PASS | Not executed. |
| Commit not performed | PASS | No commit was requested or made. |
