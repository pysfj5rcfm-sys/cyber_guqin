#!/usr/bin/env python3
"""Register XWC MVP pilot raw audio without transforming source files."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path


SESSION_ID = "RS_XWC_001_MVP_PILOT"
RECORDING_ID = "RS_XWC_001"
PIECE_ID = "XWC"
PIECE_TITLE = "仙翁操"
QINIST_ID = "QINIST_001"
QINIST_NAME = "三曼"
QIN_ID = "QIN_A"
QIN_NAME = "主测琴"
TUNING_ID = "ZHENG_DIAO"
TUNING_NAME = "正调"
ASSET_CLASS = "mvp_experimental_raw"
PRODUCTION_GRADE = "false"
EXPECTED_BATCHES = [f"batch{i:02d}.m4a" for i in range(1, 8)]

USAGE_SCOPE = [
    "MVP pipeline experiment",
    "rough segmentation test",
    "sample selection prototype",
    "render feasibility test",
    "listening workflow test",
]
NOT_FOR = [
    "final production sample library",
    "long-term Sanman standard sample archive",
    "ML training baseline",
]

RAW_SESSION_DIR = Path("02_recordings/raw_audio/QINIST_001/XWC") / SESSION_ID
RAW_DIR = RAW_SESSION_DIR / "raw"
NORMALIZED_DIR = RAW_SESSION_DIR / "normalized"
SESSION_MANIFEST = RAW_SESSION_DIR / "session_manifest.yaml"
SESSION_MANIFEST_COPY = Path("02_recordings/session_manifests") / f"{SESSION_ID}_session_manifest.yaml"
RAW_INVENTORY = RAW_SESSION_DIR / "raw_audio_inventory.csv"
SESSION_README = RAW_SESSION_DIR / "README.md"
NORMALIZED_README = NORMALIZED_DIR / "README.md"
SESSION_NOTES = Path("02_recordings/session_notes") / f"{SESSION_ID}_notes.md"
QC_NOTE = Path("02_recordings/qc_notes") / f"{SESSION_ID}_qc.md"
REGISTRATION_REPORT = Path("reports/mvp_pilot_raw_audio_registration.md")
REPORT_INVENTORY = Path("reports/mvp_pilot_raw_audio_inventory.csv")
REPORT_QC_NOTE = Path("reports/mvp_pilot_qc_note.md")
PROPOSED_ROW = Path("reports/mvp_pilot_recording_sessions_proposed_row.csv")
MISSING_INPUT_REPORT = Path("reports/mvp_pilot_raw_audio_missing_input.md")

INVENTORY_FIELDS = [
    "file_id",
    "recording_session_id",
    "recording_id",
    "piece_id",
    "qinist_id",
    "qin_id",
    "tuning_id",
    "batch_id",
    "original_filename",
    "stored_path",
    "sha256",
    "file_size_bytes",
    "extension",
    "detected_format",
    "codec",
    "duration_s",
    "sample_rate",
    "channels",
    "bit_rate",
    "asset_class",
    "production_grade",
    "usage_scope",
    "not_for",
    "qc_status",
    "notes",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-dir",
        default=f"_incoming_audio/{SESSION_ID}",
        help="Directory containing batch01.m4a through batch07.m4a.",
    )
    parser.add_argument("--session-id", default=SESSION_ID)
    parser.add_argument("--dry-run", action="store_true", help="Validate only; do not write archive outputs.")
    parser.add_argument("--execute", action="store_true", help="Copy raw audio and write registration outputs.")
    return parser.parse_args()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def probe_audio(path: Path, ffprobe_path: str | None) -> dict[str, str]:
    if not ffprobe_path:
        return {
            "detected_format": "unknown",
            "codec": "unknown",
            "duration_s": "unknown",
            "sample_rate": "unknown",
            "channels": "unknown",
            "bit_rate": "unknown",
        }

    command = [
        ffprobe_path,
        "-v",
        "error",
        "-show_entries",
        "format=format_name,duration,bit_rate:stream=codec_name,sample_rate,channels",
        "-of",
        "json",
        str(path),
    ]
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        data = json.loads(result.stdout)
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        return {
            "detected_format": "unknown",
            "codec": "unknown",
            "duration_s": "unknown",
            "sample_rate": "unknown",
            "channels": "unknown",
            "bit_rate": "unknown",
        }

    audio_stream = next((stream for stream in data.get("streams", []) if stream.get("codec_name")), {})
    format_data = data.get("format", {})
    return {
        "detected_format": format_data.get("format_name") or "unknown",
        "codec": audio_stream.get("codec_name") or "unknown",
        "duration_s": format_data.get("duration") or "unknown",
        "sample_rate": audio_stream.get("sample_rate") or "unknown",
        "channels": str(audio_stream.get("channels") or "unknown"),
        "bit_rate": format_data.get("bit_rate") or "unknown",
    }


def check_inputs(input_dir: Path) -> list[Path]:
    return [input_dir / filename for filename in EXPECTED_BATCHES if not (input_dir / filename).is_file()]


def write_missing_report(input_dir: Path, missing: list[Path]) -> None:
    MISSING_INPUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    missing_lines = "\n".join(str(path) for path in missing)
    expected_lines = "\n".join(EXPECTED_BATCHES)
    MISSING_INPUT_REPORT.write_text(
        f"""# MVP Pilot Raw Audio Missing Input

Phase: Cyber Guqin v1 Phase 1B-2A - Register MVP Pilot Raw Audio

Status: stopped before registration

The required input directory or one or more required files were not found:

```text
{input_dir}/
```

Per the Phase 1B-2A constraints, no partial session archive, raw audio folder, session manifest, inventory, QC note, or proposed `recording_sessions.csv` row was created.

## Missing Files

```text
{missing_lines}
```

## Required Filenames

```text
{expected_lines}
```

## Guardrails Preserved

- Did not scan the whole disk.
- Did not import files from non-accepted locations.
- Did not copy or modify raw audio.
- Did not create normalized audio.
- Did not create or update recording segments.
- Did not create or update sample assets.
- Did not create `recording_items_enriched.jsonl`.
- Did not modify `02_recordings/recording_sessions.csv`.
""",
        encoding="utf-8",
    )


def build_inventory_rows(input_dir: Path, ffprobe_path: str | None) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for filename in EXPECTED_BATCHES:
        source_path = input_dir / filename
        batch_id = filename.removesuffix(".m4a")
        stored_path = RAW_DIR / filename
        metadata = probe_audio(source_path, ffprobe_path)
        rows.append(
            {
                "file_id": f"{SESSION_ID}_{batch_id}",
                "recording_session_id": SESSION_ID,
                "recording_id": RECORDING_ID,
                "piece_id": PIECE_ID,
                "qinist_id": QINIST_ID,
                "qin_id": QIN_ID,
                "tuning_id": TUNING_ID,
                "batch_id": batch_id,
                "original_filename": filename,
                "stored_path": str(stored_path),
                "sha256": sha256_file(source_path),
                "file_size_bytes": str(source_path.stat().st_size),
                "extension": ".m4a",
                **metadata,
                "asset_class": ASSET_CLASS,
                "production_grade": PRODUCTION_GRADE,
                "usage_scope": ";".join(USAGE_SCOPE),
                "not_for": ";".join(NOT_FOR),
                "qc_status": "registered_for_mvp_experiment",
                "notes": "raw preserved; not segmented; not sample asset; M4A/AAC experimental source",
            }
        )
    return rows


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def manifest_text(rows: list[dict[str, str]]) -> str:
    sample_rates = sorted({row["sample_rate"] for row in rows if row["sample_rate"] != "unknown"})
    channels = sorted({row["channels"] for row in rows if row["channels"] != "unknown"})
    sample_rate_value = sample_rates[0] if len(sample_rates) == 1 else "unknown"
    channel_count_value = channels[0] if len(channels) == 1 else "unknown"
    return f"""recording_session_id: {SESSION_ID}
recording_id: {RECORDING_ID}
piece_id: {PIECE_ID}
piece_title: {PIECE_TITLE}
qinist_id: {QINIST_ID}
qinist_name: {QINIST_NAME}
qin_id: {QIN_ID}
qin_name: {QIN_NAME}
tuning_id: {TUNING_ID}
tuning_name: {TUNING_NAME}

asset_class: {ASSET_CLASS}
production_grade: false
source_format: m4a_aac
recording_mode: continuous_batch

recording_date: unknown
location: unknown
recorder: unknown
microphone: unknown
audio_interface: unknown
sample_rate: {sample_rate_value}
bit_depth: unknown_or_not_applicable_for_aac
channel_count: {channel_count_value}

source_script:
  script_type: legacy_v1_recording_script
  recording_batches: 01_pieces/xianwengcao/recording_batches.md
  recording_script_human: 01_pieces/xianwengcao/recording_script_human.csv
  recording_script: 01_pieces/xianwengcao/recording_script.csv

legacy_bridge:
  bridge_plan: reports/xwc_legacy_recording_bridge_plan.md
  take_manifest_preview: reports/xwc_legacy_take_manifest_preview.csv
  bridge_map: reports/xwc_legacy_recording_bridge_map.json

audio_files:
  inventory: 02_recordings/raw_audio/QINIST_001/XWC/{SESSION_ID}/raw_audio_inventory.csv

raw_audio_policy:
  preserve_raw: true
  no_destructive_editing: true
  no_transcoding_in_this_phase: true
  normalized_copy_allowed_later: true

usage_scope:
  - MVP pipeline experiment
  - rough segmentation test
  - sample selection prototype
  - render feasibility test
  - listening workflow test

not_for:
  - final production sample library
  - long-term Sanman standard sample archive
  - ML training baseline

qc_summary:
  status: registered_for_mvp_experiment
  production_grade: false
  known_issues:
    - lossy_m4a_aac_source
    - not_standard_wav_capture
    - possible_hot_level_based_on_manual_review
    - possible_stereo_imbalance_based_on_manual_review

next_allowed_phase:
  - experimental_split_sandbox

next_forbidden_without_new_phase:
  - production_sample_ingest
  - formal_recording_segments_update
  - sample_assets_update
  - machine_learning_training

review_status: registered
notes:
  - "MVP pilot raw audio only."
  - "Not production-grade Sanman sample source."
  - "本批录音可用于 MVP 真实音频链路实验。"
  - "本批录音不得标记为 production-grade。"
  - "本批录音不得作为最终三曼标准采样库。"
  - "MVP 成功后，应按 WAV / controlled gain / standardized mic placement 全量重录标准采样。"
"""


def normalized_readme_text() -> str:
    return f"""# Normalized Working Copy Placeholder

This directory is reserved for a future normalized working copy for `{SESSION_ID}`.

No normalized audio is generated in Phase 1B-2A.

Rules:

- Do not overwrite files in `../raw/`.
- Do not place transformed audio here during raw registration.
- Create normalized copies only in the Experimental Split Sandbox phase.
- The current raw source is M4A/AAC MVP experimental source audio.
"""


def session_readme_text() -> str:
    return f"""# {SESSION_ID}

Session ID: `{SESSION_ID}`

Asset class: `{ASSET_CLASS}`

Production grade: `false`

This folder preserves the first MVP pilot raw audio batch for 《{PIECE_TITLE}》 by {QINIST_NAME}. The original M4A files are stored in `raw/` with filenames unchanged from `batch01.m4a` through `batch07.m4a`.

This session is registered only as MVP experimental raw audio.

Guardrails:

- Do not slice these files in this phase.
- Do not transcode these files in this phase.
- Do not write `sample_assets` rows from this batch.
- Do not treat this batch as the final Sanman standard sample library.
- Do not use this batch as an ML training baseline.

The next allowed phase is Experimental Split Sandbox. If the MVP succeeds, standard sampling should be repeated as WAV with controlled gain and standardized mic placement.
"""


def session_notes_text() -> str:
    return f"""# {SESSION_ID} Session Notes

1. This session is an MVP pilot.
2. This session uses the legacy 71 XWC recording tasks as source-script context.
3. `batch01.m4a` through `batch07.m4a` are raw audio recorded by batch.
4. Original files are not cut, transcoded, overwritten, denoised, resampled, or loudness-normalized.
5. This session does not create a real take manifest in this phase.
6. This session does not create `recording_segments`.
7. This session does not create `sample_assets`.
8. Later slicing must enter Experimental Split Sandbox.
9. After MVP success, standard sampling should be re-recorded as WAV with controlled gain and standardized mic placement.

Policy statement:

- 本批录音可用于 MVP 真实音频链路实验。
- 本批录音不得标记为 production-grade。
- 本批录音不得作为最终三曼标准采样库。
- MVP 成功后，应按 WAV / controlled gain / standardized mic placement 全量重录标准采样。
"""


def qc_note_text() -> str:
    return f"""# {SESSION_ID} QC Note

QC classification: MVP experimental only

Production grade: false

Accepted for: MVP pipeline experiment

Rejected for: standard Sanman sample library

## Known Issues

- Source files are M4A/AAC, not WAV.
- Lossy compression may affect guqin tail, harmonic detail, slide detail, and transient fidelity.
- Prior manual review indicated possible hot level / near full-scale peaks in some batches.
- Prior manual review indicated possible stereo imbalance.
- Therefore this batch should not be used as final production sample source.

## Experimental Value

- This batch is not rejected as an experiment.
- This batch is useful for pipeline validation.
- This batch is useful for rough segmentation test.
- This batch is useful for first real-audio render feasibility test.
- Standard sampling should be repeated after MVP success.

## Scope

Asset class: `{ASSET_CLASS}`

Not for:

- final production sample library
- long-term Sanman standard sample archive
- ML training baseline
"""


def write_proposed_row() -> None:
    PROPOSED_ROW.parent.mkdir(parents=True, exist_ok=True)
    with PROPOSED_ROW.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["recording_id", "qinist_id", "piece_id", "qin_id", "tuning_id", "date", "status", "notes"])
        writer.writerow(
            [
                SESSION_ID,
                QINIST_ID,
                PIECE_ID,
                QIN_ID,
                TUNING_ID,
                "unknown",
                "registered_mvp_pilot",
                f"manifest=02_recordings/session_manifests/{SESSION_ID}_session_manifest.yaml; production_grade=false; asset_class={ASSET_CLASS}",
            ]
        )


def write_registration_report(rows: list[dict[str, str]], ffprobe_path: str | None) -> None:
    total_size = sum(int(row["file_size_bytes"]) for row in rows)
    known_durations = [float(row["duration_s"]) for row in rows if row["duration_s"] != "unknown"]
    total_duration = f"{sum(known_durations):.3f}" if len(known_durations) == len(rows) else "unknown"
    files = "\n".join(f"- `{row['original_filename']}` -> `{row['stored_path']}`" for row in rows)
    metadata_note = (
        "ffprobe was available; technical metadata was read opportunistically."
        if ffprobe_path
        else "ffprobe was not available; duration, codec, sample rate, channels, bitrate, and detected format are recorded as `unknown`."
    )
    REGISTRATION_REPORT.parent.mkdir(parents=True, exist_ok=True)
    REGISTRATION_REPORT.write_text(
        f"""# MVP Pilot Raw Audio Registration

Session ID: `{SESSION_ID}`

Asset class: `{ASSET_CLASS}`

Production grade: `false`

QC status: `registered_for_mvp_experiment`

## Registered Files

{files}

File count: {len(rows)}

Total size: {total_size} bytes

Total duration: {total_duration}

Metadata note: {metadata_note}

## Outputs

- Session manifest: `{SESSION_MANIFEST}`
- Session manifest index copy: `{SESSION_MANIFEST_COPY}`
- Raw inventory: `{RAW_INVENTORY}`
- QC note: `{QC_NOTE}`
- Proposed recording_sessions row: `{PROPOSED_ROW}`

## Scope Confirmation

- This batch is MVP experimental raw audio only.
- This batch is not production-grade.
- This batch is not for final production sample library.
- This batch is not for long-term Sanman standard sample archive.
- This batch is not for ML training baseline.
- This phase did not slice audio.
- This phase did not transcode audio.
- This phase did not create normalized audio.
- This phase did not write `sample_assets`.
- This phase did not create `recording_items_enriched`.
- This phase did not modify `02_recordings/recording_sessions.csv`.

## Next Step

Proceed to Phase 1B-3E Experimental Split Sandbox before any segmentation experiment. Do not proceed directly to production sample ingest.
""",
        encoding="utf-8",
    )


def write_outputs(rows: list[dict[str, str]], ffprobe_path: str | None) -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    NORMALIZED_DIR.mkdir(parents=True, exist_ok=True)
    SESSION_MANIFEST_COPY.parent.mkdir(parents=True, exist_ok=True)
    SESSION_NOTES.parent.mkdir(parents=True, exist_ok=True)
    QC_NOTE.parent.mkdir(parents=True, exist_ok=True)

    write_csv(RAW_INVENTORY, INVENTORY_FIELDS, rows)
    write_csv(REPORT_INVENTORY, INVENTORY_FIELDS, rows)

    manifest = manifest_text(rows)
    SESSION_MANIFEST.write_text(manifest, encoding="utf-8")
    SESSION_MANIFEST_COPY.write_text(manifest, encoding="utf-8")
    NORMALIZED_README.write_text(normalized_readme_text(), encoding="utf-8")
    SESSION_README.write_text(session_readme_text(), encoding="utf-8")
    SESSION_NOTES.write_text(session_notes_text(), encoding="utf-8")
    qc_text = qc_note_text()
    QC_NOTE.write_text(qc_text, encoding="utf-8")
    REPORT_QC_NOTE.write_text(qc_text, encoding="utf-8")
    write_proposed_row()
    write_registration_report(rows, ffprobe_path)


def copy_raw_files(input_dir: Path) -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    for filename in EXPECTED_BATCHES:
        shutil.copy2(input_dir / filename, RAW_DIR / filename)


def main() -> int:
    args = parse_args()
    if args.session_id != SESSION_ID:
        print(f"error: this registrar is fixed to {SESSION_ID}; got {args.session_id}", file=sys.stderr)
        return 2

    input_dir = Path(args.input_dir)
    missing = check_inputs(input_dir)
    if missing:
        write_missing_report(input_dir, missing)
        print(f"missing input; wrote {MISSING_INPUT_REPORT}")
        return 1

    ffprobe_path = shutil.which("ffprobe")
    rows = build_inventory_rows(input_dir, ffprobe_path)

    if not args.execute:
        print(f"dry-run ok: found {len(rows)} files for {SESSION_ID}")
        if not ffprobe_path:
            print("ffprobe unavailable: technical metadata will be recorded as unknown")
        return 0

    copy_raw_files(input_dir)
    write_outputs(rows, ffprobe_path)
    print(f"registered {len(rows)} raw audio files for {SESSION_ID}")
    print(f"raw archive: {RAW_DIR}")
    print(f"inventory: {RAW_INVENTORY}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
