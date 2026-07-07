# CG-LXY P1-A Design Review Checklist v0.1

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

Review marks allowed for each item:

```text
PASS
FAIL
NEEDS_USER_DECISION
NOT_APPLICABLE
```

## A. Architecture Checks

| item | mark | note |
| --- | --- | --- |
| P1-A stays design-only and non-executable. | PASS | No parser code is authorized. |
| P1-A starts from normalized component sequence, not images. | PASS | Image fields are reserved only. |
| P1-A remains single notation-unit / local marker grammar. | PASS | Phrase spans reserved for P5. |
| Design decisions are locked for P1-B design readiness. | PASS | Five decision IDs and three correction IDs are recorded. |

## B. D1 / D2 / D3 Boundary Checks

| item | mark | note |
| --- | --- | --- |
| D1 is component reference, not score-event authority. | PASS | Registry authority flags remain false for Dapu/sample/ML/render. |
| D2 is construction grammar input, not an answer bank. | PASS | Production examples are abstract. |
| D3A is scoped guard material only. | PASS | No oracle reading is used. |

## C. Anti-Oracle Leakage Checks

| item | mark | note |
| --- | --- | --- |
| Goldset oracle file was not read. | PASS | User-forbidden goldset path was avoided. |
| Old LXY candidate reports were not read. | PASS | No old reports were opened. |
| No complete P1-P6 phrase reading was written as example. | PASS | Contract uses abstract notation-unit patterns. |

## D. Token Type Checks

| item | mark | note |
| --- | --- | --- |
| Lexical component type is separate from semantic slot role. | PASS | Numeric components are not pre-bound to hui/string. |
| Legacy and v0.1 ids require normalization. | PASS | Gap status is defined. |
| Phase 1 image fields are not required. | PASS | Visual fields are reserved for P2/P3. |

## E. Slot Checks

| item | mark | note |
| --- | --- | --- |
| Sounding unit required slots are explicit. | PASS | RH action and string are required for basic sounding units. |
| Context inheritance is modeled explicitly. | PASS | Source context is recorded. |
| Marker slots remain non-sounding by default. | PASS | State/timing/generic markers do not create independent sound. |
| Sound type boundary remains散/按/泛. | PASS | Special techniques do not become a fourth sound type. |

## F. Production Rule Checks

| item | mark | note |
| --- | --- | --- |
| Required production families are represented. | PASS | RH, pressed, context, marker, motion, special, unknown families included. |
| Priority and specificity ordering is deterministic. | PASS | Tie-break policy is defined. |
| Recursion and state spans are bounded. | PASS | Full spans reserved for P5. |

## G. Ambiguity Checks

| item | mark | note |
| --- | --- | --- |
| N-best output is required. | PASS | `max_candidates`, rank, and score breakdown are defined. |
| Scores are heuristic, not calibrated probability. | PASS | `calibrated_probability=false`. |
| Unresolved and incomplete are preserved. | PASS | They are not collapsed into invalid. |

## H. Invalid Combination Checks

| item | mark | note |
| --- | --- | --- |
| Matrix covers required 20 case families. | PASS | See CSV matrix. |
| Incomplete cases are not over-rejected. | PASS | RH alone and numeric alone are not blanket invalid. |
| Context inheritance source missing is explicit. | PASS | Covered as unresolved/context gap. |

## I. Output Contract Checks

| item | mark | note |
| --- | --- | --- |
| Top-level parser response fields are defined. | PASS | See parse output contract JSON. |
| Accepted and rejected candidate fields are defined. | PASS | Both are present. |
| Authority flags are carried by response and candidates. | PASS | All non-authority flags are true. |
| Dual output contract is defined. | PASS | `structured_parse` is primary; `surface_reading_candidate` is derived; `literal_component_gloss` preserves input gloss. |
| Surface reading cannot overwrite slots. | PASS | Contract states one-way derivation from structured slots to display text. |

## J. Authority Checks

| item | mark | note |
| --- | --- | --- |
| Not repo contract. | PASS | Labeled throughout. |
| Not canon authority. | PASS | Labeled throughout. |
| Not Dapu IR / score-event authority. | PASS | Labeled throughout. |
| Not sample ingest, ML, or render output. | PASS | Labeled throughout. |

## K. P1-B Readiness

| item | mark | note |
| --- | --- | --- |
| Fixture design inputs are clear enough for later P1-B. | PASS | Abstract cases and status model are defined. |
| P1-B dual fixture strategy is locked. | PASS | Abstract fixtures plus sanitized real-ID fixtures; no LXY phrase id, complete reading, source_report, or oracle. |
| Fixture creation is not performed in this task. | PASS | No tests or fixtures are written. |

## L. P1-C Not-Yet-Authorized Checks

| item | mark | note |
| --- | --- | --- |
| Parser implementation is not written. | PASS | No Python is created. |
| Runtime schema is not claimed. | PASS | JSON files are design contracts only. |
| Tests are not created or run. | PASS | Validation is limited to generated artifact checks. |
| P1-C implementation is not authorized by the freeze. | PASS | `ready_for_p1c_implementation=false` in manifest. |
