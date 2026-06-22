# Self-Contained Reproduction Toolchain Report

- Task: `CG-XWC-MVP-P1F_SELF_CONTAINED_REPRODUCTION_TOOLCHAIN`
- Phase: `Phase 1F-XWC-MVP Passed / Sweep & Review`
- Scope: generic / manifest-driven / dry-run-first reproduction toolchain for XWC F engineering-path replay.

## 1. Scope Result

This round built a self-contained repo workflow for dry-run reproduction of the XWC `F_FINAL_REVIEWED` engineering path. It did not enter the second piece, did not run a real render, did not read real audio binary, did not overwrite accepted `F_FINAL_REVIEWED`, and did not write sample ingest artifacts.

## 2. Added / Modified Files

Added:

- `scripts/cyber_guqin_reproduction_lib.py`
- `scripts/generate_recording_plan_from_dapu_ir.py`
- `scripts/render_abcd_from_manifest.py`
- `tools/cg-varw/backend/scripts/generate_final_reviewed_render.py`
- `tools/cg-varw/backend/scripts/verify_r2_render_manifest.py`
- `docs/cyber_guqin/XWC_F_REPRODUCTION_RUNBOOK.md`
- `docs/cyber_guqin/SCRIPT_REGISTRY.md`
- `examples/cyber_guqin/xwc_recording_plan_config.yaml`
- `examples/cyber_guqin/xwc_dapu_ir_minimal_fixture.jsonl`
- `examples/cyber_guqin/xwc_abcd_render_manifest.yaml`
- `examples/cyber_guqin/xwc_final_render_manifest.yaml`
- `examples/cyber_guqin/xwc_r2_render_verify_manifest.yaml`
- `tests/test_self_contained_reproduction_toolchain.py`
- `reports/self_contained_reproduction_toolchain_report.md`

Modified:

- `README.md`

## 3. Generic Scripts

| Script | Role | Default | Execute behavior |
| --- | --- | --- | --- |
| `scripts/generate_recording_plan_from_dapu_ir.py` | Dapu IR + recording config -> take plan, batch plan, gap report, human checklist, manifest | dry-run | writes 5 planning artifacts only to caller output root |
| `scripts/render_abcd_from_manifest.py` | ABCD manifest -> planned A/B/C/D output paths and alignment metadata | dry-run | writes sandbox metadata/alignment plan only; no real audio render |
| `tools/cg-varw/backend/scripts/generate_final_reviewed_render.py` | final render manifest + canonical latest/input snapshot -> authority summary and sandbox final plan | dry-run | writes sandbox metadata/alignment/validation/report/input snapshot only; no real audio render |
| `tools/cg-varw/backend/scripts/verify_r2_render_manifest.py` | read-only canonical R2/latest + render manifest verifier | read-only | no write mode |

## 4. Runbook / Registry / Examples

- Runbook: `docs/cyber_guqin/XWC_F_REPRODUCTION_RUNBOOK.md`
- Script registry: `docs/cyber_guqin/SCRIPT_REGISTRY.md`
- Examples: `examples/cyber_guqin/*`

The runbook starts from the workflow skill, confirms R2 authority, runs verifier dry-run, recording-plan dry-run, ABCD dry-run, final reviewed dry-run, and lists optional sandbox execute commands.

## 5. XWC F Reproduction Coverage

Covered:

- R2 latest JSON authority check.
- Derived CSV/YAML non-authority guard.
- Forbidden authority guard for Downloads, browser Blob, restore zip, and derived CSV/YAML as source.
- Recording plan dry-run from Dapu IR fixture and config.
- ABCD render path dry-run from manifest.
- Final reviewed render path dry-run from canonical latest JSON.
- Sandbox output-root requirement for execute.
- Accepted `F_FINAL_REVIEWED` baseline refusal.
- Help text for fresh-user entry.

Not covered by design:

- Real audio render.
- Human listening acceptance.
- Sample ingest.
- ML training.
- Arrangement Mode.
- Second-piece execution.

## 6. Old Script Safety

- `scripts/generate_baiya_recording_plan.py` was read-only reference only.
- It was not modified, committed, deleted, moved, archived, or run.
- Current SHA256 observed by tests: `34ee60f94f64e7f14161f583fd29ac8ddbe256055e00fe12439e03c7b167d7de`.
- `tools/cg-varw/backend/scripts/refresh_xwc_r1_full_tail_and_regenerate_f.py` remains `historical_only` and was not parameterized as a workflow entry.
- `scripts/render_xwc_abcd_from_planning.py` and `tools/cg-varw/backend/scripts/generate_xwc_f_final_reviewed.py` remain historical/template references, not new entry points.

## 7. CLI Usage Summary

```bash
python3 tools/cg-varw/backend/scripts/verify_r2_render_manifest.py \
  --review-state 04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/latest/r2_review_state.latest.json \
  --render-manifest examples/cyber_guqin/xwc_r2_render_verify_manifest.yaml \
  --dry-run
```

```bash
python3 scripts/generate_recording_plan_from_dapu_ir.py \
  --piece-id XWC \
  --session-id RS_XWC_002_BAIYA_PILOT \
  --recording-id RS_XWC_002 \
  --qinist-id QINIST_002 \
  --qinist-name Baiya \
  --dapu-ir examples/cyber_guqin/xwc_dapu_ir_minimal_fixture.jsonl \
  --recording-config examples/cyber_guqin/xwc_recording_plan_config.yaml \
  --output-root 04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/reproduction_runs/DRY_RUN_ONLY/recording_plan \
  --dry-run
```

```bash
python3 scripts/render_abcd_from_manifest.py \
  --render-manifest examples/cyber_guqin/xwc_abcd_render_manifest.yaml \
  --output-root 04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/reproduction_runs/DRY_RUN_ONLY/abcd \
  --dry-run
```

```bash
python3 tools/cg-varw/backend/scripts/generate_final_reviewed_render.py \
  --final-render-manifest examples/cyber_guqin/xwc_final_render_manifest.yaml \
  --output-root 04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/reproduction_runs/DRY_RUN_ONLY/final \
  --dry-run
```

## 8. Manifest / Config Schema Summary

Recording config requires:

- `max_batch_size`
- `tail_policy`
- `context_take_policy`
- `output_settings`

Dapu IR rows require:

- `event_id`, `phrase_id`, `score_order`, `sound_type`, `string`, `hui_position`
- `technique`, `gesture_family`, `special_technique`
- `needs_context_take`, `needs_long_tail`, `needs_retake`
- `source_confidence`, `needs_review`

ABCD manifest requires:

- `piece_id`, `session_id`, `qinist_id`, `render_set_id`
- `source_map`, `phrase_plan`, `version_policy`, `output_versions`
- `tail_policy`, `context_take_policy`, `output_root`
- `dry_run_default`, `forbid_overwrite_accepted_baseline`

Final manifest requires:

- `source_review_state`, `source_version`, `target_version`, `render_set_id`
- `input_snapshot_policy`, `phrase_revision_policy`, `tail_policy`
- `forbidden_authority`, `sample_safety_rules`
- `dry_run_default`, `forbid_overwrite_accepted_baseline`, `reproduction_sandbox_required`

## 9. Tests

RED evidence:

- `python3 -m unittest tests.test_self_contained_reproduction_toolchain`
- Initial result: failed because the new scripts/docs/examples did not exist yet.

GREEN targeted test:

```text
python3 -m unittest tests.test_self_contained_reproduction_toolchain
Ran 16 tests in 0.456s
OK
```

Coverage map:

- Recording plan dry-run no writes.
- Recording plan execute writes 5 outputs to temp dir.
- max batch size 10.
- context policy without take hardcode.
- long-tail/full-tail policy.
- missing required fields fail clearly.
- manifest row counts.
- slate text.
- ABCD dry-run no audio.
- missing source/version policy fail.
- manifest-driven output paths.
- no generic XWC/Baiya/take hardcode.
- execute refuses accepted baseline.
- final dry-run no writes.
- forbidden authority fail.
- latest/input authority required.
- manifest target/source/output root.
- no final generic phrase/take hardcode.
- final execute refuses accepted baseline and requires sandbox.
- verifier accepts canonical latest.
- verifier rejects derived-only authority.
- verifier checks forbidden authority and required fields.
- runbook dry-run commands and stop rules.
- registry includes new generic scripts and old historical scripts.
- examples parse successfully.
- old Baiya script SHA256 unchanged.
- full-tail repair script remains historical-only.

## 10. Self-Replay Validation

Entry documents used:

- `.agents/skills/cyber_guqin_mvp_workflow/SKILL.md`
- `docs/cyber_guqin/XWC_F_REPRODUCTION_RUNBOOK.md`
- `docs/cyber_guqin/SCRIPT_REGISTRY.md`
- `examples/cyber_guqin/*`
- new script `--help`

Replay command results:

| Command | Result |
| --- | --- |
| `git status --short --untracked-files=all` | PASS; showed new files plus pre-existing untracked `scripts/generate_baiya_recording_plan.py` |
| `python3 tools/cg-varw/backend/scripts/verify_r2_render_manifest.py ... --dry-run` | PASS; canonical latest JSON accepted, derived CSV/YAML non-authority noted |
| `python3 scripts/generate_recording_plan_from_dapu_ir.py ... --dry-run` | PASS; printed 5 planned takes, 1 batch, 2 coverage gaps, expected paths |
| `python3 scripts/render_abcd_from_manifest.py ... --dry-run` | PASS; printed A/B/C/D planned paths, no audio written |
| `python3 tools/cg-varw/backend/scripts/generate_final_reviewed_render.py ... --dry-run` | PASS; printed authority hash, phrase/review counts, planned target files |
| examples standard-library parse command | PASS; 4 manifest/config files and 5 Dapu rows parsed |
| four new script `--help` commands | PASS; usage text printed for each |
| dry-run output root absence check | PASS; `reproduction_runs/DRY_RUN_ONLY` was not created |
| sample ingest absence checks | PASS; no root `sample_assets.csv`, `recording_segments.csv`, or `recording_items_enriched.jsonl` |

Intervention log:

| Failure command | Failure reason | Fix type | Code involved | Real data impact | Replay after fix |
| --- | --- | --- | --- | --- | --- |
| `python3 -m unittest tests.test_self_contained_reproduction_toolchain` | target scripts/docs/examples missing during RED | implementation | yes | no | PASS |
| `python3 -m unittest tests.test_self_contained_reproduction_toolchain` | recording plan test expected slate alias; ABCD rejected `.yaml` phrase plan as derived authority | validation/script output | yes | no | PASS |

Self-replay judgement:

| Check | Result |
| --- | --- |
| `REPRODUCTION_DRY_RUN_SELF_CONTAINED` | PASS |
| `NO_CODE_INTERVENTION_REQUIRED` | PASS for final self-replay after implementation; initial RED/GREEN fixes were development work |
| `ACCEPTED_BASELINE_PROTECTED` | PASS |
| `NO_REAL_RENDER_RUN` | PASS |
| `NO_AUDIO_BINARY_READ` | PASS |
| User can run without Codex explanation | PASS |
| Steps still needing human judgment | Human listening gate and any future execute/render acceptance |

## 11. Boundary Checklist

| Boundary | Result |
| --- | --- |
| Modified old untracked `generate_baiya_recording_plan.py` | No |
| Entered second piece | No |
| Ran real render | No |
| Read real audio binary | No |
| Wrote real R0/R1/R2/F data | No |
| Covered accepted F baseline | No overwrite; protected |
| Wrote sample ingest | No |
| Generated G/F2 | No |
| Auto commit | No |

## 12. Final Verification

Targeted unittest:

```text
python3 -m unittest tests.test_self_contained_reproduction_toolchain
Ran 16 tests in 0.479s
OK
```

Diff whitespace check:

```text
git diff --check
PASS: no output
```

Source compile check:

```text
python3 -c "compile selected new scripts/tests"
compile PASS 6
```

Note: direct `python3 -m py_compile ...` was not used as final evidence because this macOS Python tried to write `.pyc` under `/Users/chenyulin/Library/Caches/...` and hit a cache permission error. The replacement check compiles source in memory and does not write cache files.

Hardcode guard checks:

```text
rg -n "RS_XWC_002_BAIYA_PILOT|XWC_P09|T060|T071|Baiya|白牙" scripts/render_abcd_from_manifest.py
PASS: no matches

rg -n "T008|T014|XWC_P02|XWC_P09|RS_XWC_002_BAIYA_PILOT|白牙" tools/cg-varw/backend/scripts/generate_final_reviewed_render.py
PASS: no matches
```

Dry-run no-write checks:

```text
test ! -e 04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/reproduction_runs/DRY_RUN_ONLY
PASS

test ! -e sample_assets.csv
PASS

test ! -e recording_segments.csv
PASS

test ! -e recording_items_enriched.jsonl
PASS
```

Old script hash check:

```text
scripts/generate_baiya_recording_plan.py sha256
34ee60f94f64e7f14161f583fd29ac8ddbe256055e00fe12439e03c7b167d7de
PASS: unchanged against test baseline
```

Final git status:

```text
 M README.md
?? docs/cyber_guqin/SCRIPT_REGISTRY.md
?? docs/cyber_guqin/XWC_F_REPRODUCTION_RUNBOOK.md
?? examples/cyber_guqin/xwc_abcd_render_manifest.yaml
?? examples/cyber_guqin/xwc_dapu_ir_minimal_fixture.jsonl
?? examples/cyber_guqin/xwc_final_render_manifest.yaml
?? examples/cyber_guqin/xwc_r2_render_verify_manifest.yaml
?? examples/cyber_guqin/xwc_recording_plan_config.yaml
?? reports/self_contained_reproduction_toolchain_report.md
?? scripts/cyber_guqin_reproduction_lib.py
?? scripts/generate_baiya_recording_plan.py
?? scripts/generate_recording_plan_from_dapu_ir.py
?? scripts/render_abcd_from_manifest.py
?? tests/test_self_contained_reproduction_toolchain.py
?? tools/cg-varw/backend/scripts/generate_final_reviewed_render.py
?? tools/cg-varw/backend/scripts/verify_r2_render_manifest.py
```

`scripts/generate_baiya_recording_plan.py` remains the pre-existing untracked historical template and was not staged or modified.

## 13. Recommendation

If final verification remains green, this round is ready for user review. Suggested commit message if the user later chooses to commit:

```text
feat(tools): add self-contained XWC F reproduction toolchain
```

Next step after acceptance: P1-G second-piece small-piece startup preparation, limited to piece selection, score authority, piece/session/qinist config, Dapu IR preparation, and generic tools dry-run.
