# CG-LXY P2 Visual Component Layer Implementation Report v0.1

Task ID: `CG-LXY-136-P2-IMPLEMENTATION-MVP-v0.1`

## Repo Context Gate

Preflight was checked before implementation:

- `git status --short --untracked-files=all`: clean
- `git branch --show-current`: `main`
- `git rev-parse HEAD`: `ccc5377c75d56e9f8f013bf0c1cd1a914fb3f9c5`
- Recent commits include:
  - `ccc5377 feat(lxy): implement phase2 component matcher mvp`
  - `6996767 docs(lxy): define phase2 visual component candidate design`
  - `51598da feat(lxy): implement phase1 grammar parser mvp`

This satisfies the P1-C, P2-B, and P2 design commit gate.

## Implemented Runtime Modules

`scripts/component_visual_index.py`

- Builds `component_visual_runtime_index.v0.1.json` from the D1 registry through the existing P2-B image index builder.
- Preserves `component_id`, label, component category, reference path, image hash, image dimensions, and normalized reference metadata.
- Keeps extension behavior registry-driven: a new component with an image can be added to the registry and included by rebuilding the index without editing matcher code.

`scripts/component_matcher_runtime.py`

- Exposes `class ComponentMatcher.match(crop, top_k=5, crop_id=None, grammar_context=None)`.
- Returns deterministic `MATCHED`, `AMBIGUOUS`, or `UNKNOWN_COMPONENT` results.
- Produces multiple candidates with `visual_score`, zero-based `rank`, evidence, lexical type, and score breakdown.
- Uses no random model, no training, and no external model download.

`scripts/component_candidate_lattice.py`

- Exposes `class CandidateLattice.build(component_candidates, grammar_context=None)`.
- Builds deterministic `nodes`, `edges`, `ranking`, and `unresolved` fields.
- Does not call `GrammarParser.parse()` and does not produce phrase readings, sentence readings, score events, or Dapu IR.

## Scoring

Runtime candidates include this breakdown:

```json
{
  "visual": 0.72,
  "lexical": 1.0,
  "grammar": 0.6,
  "uncertainty_penalty": 0.0,
  "final": 0.75
}
```

The final rank score is not pure visual:

```text
0.68*visual + 0.18*lexical + 0.14*grammar - uncertainty_penalty
```

Lexical compatibility is derived from component category. Grammar compatibility is a hook-level compatibility check using caller-provided context such as `allowed_lexical_types`, `allowed_component_ids`, or slot ids. P2 does not call the full P1 parser.

## Unknown Policy

`UNKNOWN_COMPONENT` is returned without minting a component id when:

- no matchable image reference exists;
- input image decoding fails;
- the crop has no ink;
- top visual support is below the configured threshold.

Unknown state is recorded in `unknown_component_state`, `coverage_ledger`, and lattice `unresolved`.

## Boundary Evidence

Implementation remained component-candidate only:

- no phrase reading output;
- no sentence reading output;
- no score event output;
- no Dapu IR output;
- no goldset dependency;
- no old candidate dependency;
- no LXY special-case rule;
- no training or sample ingest.

The runtime index generated from the current registry contains:

- `component_index_count`: 186
- `image_reference_count`: 174
- `source_image_missing_count`: 12

## Validation Notes

Fresh validation evidence:

- `python3 -m json.tool` passed for the runtime index, implementation manifest, and eval result JSON files.
- `python3 -m compileall` passed for the three new runtime modules and the new test file with bytecode redirected to `/tmp/cyber_guqin_p2_pycache`.
- `python3 -m unittest tests.test_component_visual_layer` passed: 10 tests.
- Relevant regression set passed: 43 tests across `test_component_visual_layer`, `test_component_matcher`, and the P1 grammar parser test modules.
- Bare `python3 -m unittest` exited 0 but discovered 0 tests in this repo layout.
- Full `python3 -m unittest discover -s tests -p 'test*.py'` ran 59 tests and had one pre-existing unrelated failure in `test_self_contained_reproduction_toolchain.py`: `BAIYA_PLAN_SCRIPT.exists()` was false. This is outside the allowed P2 write paths and was not modified.

## Readiness

```json
{
  "ready_for_P3_visual_grammar_fusion": true,
  "ready_for_LXY_phrase_reading": false,
  "ready_for_training_model": false
}
```
