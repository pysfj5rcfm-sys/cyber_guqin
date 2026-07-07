# CG-LXY P1-C Implementation Report v0.1

Task ID: `CG-LXY-136-P1C-EXECUTABLE-GRAMMAR-PARSER-MVP-v0.1`

Status labels:

- P1_GRAMMAR_PARSER_MVP
- GPT_TRANSCRIPTION_DRAFT
- REFERENCE_COMPONENT_ATLAS_GUIDED
- NEEDS_HUMAN_REVIEW
- NOT_REPO_CONTRACT
- NOT_CANON_AUTHORITY
- NOT_DAPU_IR_AUTHORITY
- NOT_SCORE_EVENT_AUTHORITY
- NOT_SAMPLE_INGEST
- NOT_ML_TRAINING_DATA
- NOT_RENDER_OUTPUT

## 1. Implementation Scope

P1-C implements an executable local grammar parser for already supplied component token sequences. It does not read images, perform visual recognition, reconstruct phrases, search prior context, generate Dapu IR, touch runtime score facts, run render/sample/ML workflows, or modify P1-A/P1-B source artifacts.

## 2. Module Architecture

- `scripts/cyber_guqin_grammar_parser.py`: stable public API, token validation, D1 normalization, local production handlers, guard evaluation, ranking, surface rendering, and combinatorial smoke generation.
- `scripts/run_cyber_guqin_grammar_fixtures.py`: dynamic P1-B fixture discovery and post-parse assertion runner.
- `references/qxby_component_atlas/p1_grammar_runtime_contract.v0.1.json`: executable reference projection derived from frozen P1-A and D2 metadata.
- `references/qxby_component_atlas/p1_generation_safe_guards.v0.1.json`: generation-safe D3A guard projection.

## 3. Runtime Contract Projection

The runtime contract is `DERIVED_EXECUTABLE_REFERENCE`, hash `b838347cc570095a01eeac18d07bc5ce9380d566c3c0622d4e115f7b6ab7d21d`. It contains lexical types, parser statuses, semantic slots, production rules, rule ordering, ambiguity policy, partial-consumption policy, context policy, sound-type policy, surface rendering policy, and authority boundary. It excludes LXY phrase ids, phrase readings, source reports, `expected_continuous_reading`, `must_include`, and phrase integration oracle fields.

## 4. Guard Projection

The guard projection hash is `d27f2aed92e630bde1ed37d1c8225f5381a00a0acb039f5e74927b1ec25d2e50`. It keeps only generation-safe fields: guard/case id, component ids, labels, forbidden output, reason, expected guard, allowed-elsewhere flag, authority boundary, evaluation rule, and primary component refs. Phrase scope and oracle-style fields are excluded.

## 5. Public API

`GrammarParser.from_repo_root(repo_root, allow_abstract_component_ids=False)` loads only runtime projection, D1 registry/alias/crosswalk, and generation-safe guard projection. `parse(tokens, context_input=None, options=None)` returns normalization summary, parse status, accepted/rejected candidates, slot bindings, guard summary, unresolved items, and authority flags. `load_default_parser(repo_root)` is provided for default production mode.

## 6. Normalization

The parser supports v0.2 primary ids, legacy alias ids, source v0.1 ids, normalization gaps, and explicit abstract ids only when `allow_abstract_component_ids=True`. Default mode rejects abstract ids as normalization gaps.

## 7. Production Engine

All 11 P1-A production families are implemented: PR-RH-STRING, PR-LF-HUI-RH-STRING, PR-RH-STRING-CONTEXT, PR-STATE-START, PR-STATE-END, PR-TIMING, PR-PRE-MOTION, PR-POST-MOTION, PR-SPECIAL-TECHNIQUE, PR-GENERIC-MARKER, and PR-UNKNOWN. `PR-UNKNOWN` remains fallback/review-only and does not create a valid complete accepted parse.

## 8. Context Isolation

`implicit_backward_scan_depth=0` is enforced. The parser accepts only explicit `context_ref`, `inherited_context`, `no_inherited_context`, and `context_required` inputs. Repeated calls do not share session state.

## 9. Guard Evaluator

The guard evaluator supports HARD_REJECT, SOFT_PENALTY, FORCE_UNRESOLVED, NEEDS_CONTEXT, NEEDS_HUMAN_REVIEW, and NOT_APPLICABLE. Literal forbidden strings are not treated as global bans; scope mismatch stays `NOT_APPLICABLE`.

## 10. Ranking

Candidate ids are deterministic hashes over rule ids, consumed tokens, slots, status, and sound type. Ranking is deterministic and excludes hard-rejected candidates from accepted candidates. Scores are `HEURISTIC_GRAMMAR_SCORE` and `calibrated_probability=false`.

## 11. Renderer

`surface_reading_candidate` is derived from structured slots and normalized labels. `literal_component_gloss` preserves raw token labels. Surface text never backfills slot semantics.

## 12. Dynamic Fixture Loading

Runner discovery uses glob `p1b_*_fixtures.v*.json`; no fixture file count, case count, or case id is hardcoded. Discovered fixture files: ['p1b_abstract_grammar_fixtures.v0.1.json', 'p1b_deterministic_ranking_fixtures.v0.1.json', 'p1b_guard_action_fixtures.v0.1.json', 'p1b_sanitized_real_id_fixtures.v0.1.json']. Discovered cases: 75.

## 13. Extensibility Proof

The property test builds a temporary fixture directory, appends a new case id, and confirms discovery/execution without parser or runner edits.

## 14. Property Tests

`tests.test_cyber_guqin_grammar_parser_properties` passed. Covered determinism, token conservation, unknown safety, marker safety, sound-type closure, context isolation, token-id renaming invariance, invalid permutation safety, fixture independence, abstract-mode isolation, dynamic discovery, and combinatorial smoke.

## 15. Metamorphic Tests

`tests.test_cyber_guqin_grammar_parser_metamorphic` passed all 8 required transformations: remove string, remove RH, replace RH with timing marker, add unknown token, add explicit context, declare no inherited context, reverse motion attachment, and scope-mismatched guard.

## 16. Combinatorial Smoke

Generated cases: 19. Rule-family coverage: ['PR-GENERIC-MARKER', 'PR-LF-HUI-RH-STRING', 'PR-PRE-MOTION', 'PR-RH-STRING', 'PR-RH-STRING-CONTEXT', 'PR-STATE-START', 'PR-TIMING']. Invariant failures: [].

## 17. Fixture Baseline Results

Fixture runner result: 75 pass / 0 fail. Coverage by production: `{"PR-GENERIC-MARKER": 7, "PR-LF-HUI-RH-STRING": 8, "PR-POST-MOTION": 3, "PR-PRE-MOTION": 3, "PR-RH-STRING": 21, "PR-RH-STRING-CONTEXT": 8, "PR-SPECIAL-TECHNIQUE": 6, "PR-STATE-END": 2, "PR-STATE-START": 3, "PR-TIMING": 6, "PR-UNKNOWN": 9}`. Coverage by status: `{"COMPONENT_ID_NORMALIZATION_GAP": 2, "FORBIDDEN_GUARD_REJECTED": 3, "INCOMPLETE": 9, "INPUT_CONTRACT_INVALID": 8, "INVALID_ORDER": 1, "INVALID_TYPE_COMBINATION": 2, "UNRESOLVED": 11, "UNSUPPORTED": 3, "VALID_AMBIGUOUS": 8, "VALID_COMPLETE": 22, "VALID_WITH_CONTEXT": 6}`. Coverage by guard action: `{"FORCE_UNRESOLVED": 8, "HARD_REJECT": 8, "NEEDS_CONTEXT": 10, "NEEDS_HUMAN_REVIEW": 6, "NOT_APPLICABLE": 40, "SOFT_PENALTY": 3}`.

## 18. Known Limitations

P1-C starts from caller-provided component tokens; it does not detect glyphs, segment lines, build a lattice, reconstruct phrases, infer missing context, or create score authority. P1-B practical token fixtures omit some P1-A audit fields such as `source_category` and `confidence_input`; P1-C validates the core executable fields and keeps those audit fields optional unless present.

## 19. Authority Boundary

All outputs remain draft parser evidence only: not repo contract, not canon authority, not Dapu IR authority, not score-event authority, not sample ingest, not ML training data, not render output, and still need human review.

## 20. P1 Completion Conclusion

P1 Grammar Parser MVP is executable and passes the current dynamic P1-B fixture baseline. It preserves `structured_parse` as primary and `surface_reading_candidate` as derived display.

## 21. P2 Readiness

Ready for P2 design discussion. Not ready for P2 code by this task; visual component detection/top-k/lattice work needs a separate authorization gate.

## 22. Unresolved Issues

No blocking P1-C fixture contradiction remains. The only documented limitation is the P1-A required-audit-field vs P1-B minimal-token fixture mismatch, handled as optional audit metadata in P1-C runtime validation.
