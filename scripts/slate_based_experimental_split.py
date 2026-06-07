#!/usr/bin/env python3
"""Slate-based experimental split sandbox for Cyber Guqin recordings.

This script is intentionally reusable:

- take-plan adapters normalize source-specific rows into one internal schema;
- raw-audio inventory loading is independent of batch count;
- split logic operates on derived working WAV files and normalized takes.

Implemented adapter:

- legacy_xwc_preview: reads reports/xwc_legacy_take_manifest_preview.csv.

Reserved future adapter:

- dapu_event_ir_recording_plan: will accept canon-backed recording plans emitted
  from the guqin-dapu-parser -> Dapu Event IR pipeline.

The outputs are experimental only. They are not production samples and are never
written to 03_samples or V1 runtime paths.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import math
import os
import re
import shutil
import statistics
import subprocess
import sys
import wave
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


SESSION_RECORDING_ID = "RS_XWC_001"
PIECE_ID = "XWC"
EXPERIMENTAL_SEGMENT_PREFIX = "SEG_XWC_PILOT"
DETECTION_METHOD = "energy_sequential_alignment"

TAKE_PLAN_FIELDS = [
    "recording_take_no",
    "batch_take_no",
    "script_id",
    "event_id",
    "event_range",
    "gesture_id",
    "normalized_name",
    "expected_sample_type",
    "realization_variant",
    "realization_pre_action",
    "notes",
]

MANIFEST_FIELDS = [
    "experimental_segment_id",
    "recording_session_id",
    "recording_id",
    "recording_take_no",
    "batch_take_no",
    "batch_id",
    "source_file_id",
    "source_raw_file",
    "source_sha256",
    "derived_working_file",
    "script_id",
    "event_id",
    "event_range",
    "gesture_id",
    "normalized_name",
    "expected_sample_type",
    "realization_variant",
    "realization_pre_action",
    "start_time_s",
    "end_time_s",
    "attack_marker_ms",
    "release_tail_ms",
    "segment_file_path",
    "segment_filename",
    "slate_detection_method",
    "split_confidence",
    "confidence_level",
    "needs_manual_review",
    "review_reason",
    "qc_status",
    "quality_status",
    "selected_for_mvp_render",
    "experimental_only",
    "production_grade",
    "not_standard_sample_library",
    "notes",
]

BOUNDARY_FIELDS = [
    "review_row_id",
    "experimental_segment_id",
    "recording_take_no",
    "batch_take_no",
    "script_id",
    "batch_id",
    "source_raw_file",
    "segment_file_path",
    "segment_filename",
    "event_id",
    "event_range",
    "gesture_id",
    "normalized_name",
    "expected_sample_type",
    "realization_variant",
    "confidence_level",
    "split_confidence",
    "review_reason",
    "current_start_time_s",
    "current_end_time_s",
    "recommended_action",
    "review_decision",
    "review_adjusted_start_time_s",
    "review_adjusted_end_time_s",
    "review_note",
]

SLATE_FIELDS = [
    "batch_id",
    "source_raw_file",
    "derived_working_file",
    "detected_window_no",
    "assigned_recording_take_no",
    "assigned_script_id",
    "window_start_time_s",
    "window_end_time_s",
    "slate_region_start_s",
    "slate_region_end_s",
    "performance_region_start_s",
    "performance_region_end_s",
    "detection_method",
    "detection_confidence",
    "notes",
]

DERIVED_INVENTORY_FIELDS = [
    "batch_id",
    "source_file_id",
    "source_raw_file",
    "source_sha256",
    "derived_working_file",
    "working_wav_source",
    "conversion_status",
    "converter",
    "converter_profile",
    "conversion_command",
    "experimental_only",
    "production_grade",
    "source_format",
    "notes",
]


@dataclass
class TakePlanRow:
    recording_session_id: str
    recording_id: str
    recording_take_no: str
    batch_take_no: str
    script_id: str
    event_id: str
    event_range: str
    gesture_id: str
    normalized_name: str
    expected_sample_type: str
    realization_variant: str
    realization_pre_action: str
    notes: str


@dataclass
class RawAudioItem:
    batch_id: str
    source_file_id: str
    source_raw_file: Path
    source_sha256: str
    original_filename: str


@dataclass(frozen=True)
class Converter:
    name: str
    executable: str


@dataclass(frozen=True)
class ConverterProfile:
    converter: Converter
    profile_name: str
    output_suffix: str
    command_template: tuple[str, ...]
    usable_for_wav_split: bool


@dataclass
class ProbeResult:
    converter: str
    profile_name: str
    command: list[str]
    exit_code: int
    stderr_summary: str
    output_exists: bool
    output_size: int
    probe_status: str
    output_path: Path
    usable_for_wav_split: bool


@dataclass
class AudioWindow:
    start: float
    end: float
    slate_start: float
    slate_end: float
    performance_start: float
    performance_end: float
    confidence: float
    notes: str = ""


@dataclass
class SegmentResult:
    take: TakePlanRow
    raw: RawAudioItem
    working_wav: Path
    window: AudioWindow
    start_time_s: float
    end_time_s: float
    segment_file: Path
    split_confidence: float
    confidence_level: str
    review_reasons: list[str] = field(default_factory=list)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create experimental slate-based split sandbox outputs."
    )
    parser.add_argument("--session-id", required=True)
    parser.add_argument("--raw-audio-dir", required=True, type=Path)
    parser.add_argument("--raw-inventory", required=True, type=Path)
    parser.add_argument("--working-wav-dir", type=Path)
    parser.add_argument("--take-plan", required=True, type=Path)
    parser.add_argument(
        "--take-plan-kind",
        required=True,
        choices=["legacy_xwc_preview", "dapu_event_ir_recording_plan"],
    )
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--expected-count", type=int, required=True)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", default=True)
    mode.add_argument("--execute", action="store_true")
    convert = parser.add_mutually_exclusive_group()
    convert.add_argument("--convert-working-wav", action="store_true", default=False)
    convert.add_argument("--no-convert-working-wav", action="store_true")
    split = parser.add_mutually_exclusive_group()
    split.add_argument("--auto-split", action="store_true", default=False)
    split.add_argument("--no-auto-split", action="store_true")
    parser.add_argument("--converter-probe-only", action="store_true", default=False)
    parser.add_argument("--pre-roll-s", type=float, default=0.08)
    parser.add_argument("--min-tail-s", type=float, default=1.2)
    parser.add_argument("--default-tail-s", type=float, default=2.0)
    parser.add_argument("--max-segment-s", type=float, default=8.0)
    parser.add_argument("--min-segment-s", type=float, default=0.3)
    args = parser.parse_args()
    if args.execute:
        args.dry_run = False
    if args.no_convert_working_wav:
        args.convert_working_wav = False
    if args.no_auto_split:
        args.auto_split = False
    return args


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        return [dict(row) for row in csv.DictReader(f)]


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_take_plan(kind: str, path: Path, session_id: str) -> list[TakePlanRow]:
    if kind == "dapu_event_ir_recording_plan":
        raise SystemExit(
            "take-plan adapter dapu_event_ir_recording_plan is reserved for a "
            "future Dapu Event IR recording plan; no formal adapter is enabled "
            "in this experimental pilot."
        )
    if kind != "legacy_xwc_preview":
        raise SystemExit(f"Unsupported take plan kind: {kind}")

    rows = []
    for raw in read_csv(path):
        gesture_id = (raw.get("gesture_id") or "UNKNOWN_GESTURE").strip()
        rows.append(
            TakePlanRow(
                recording_session_id=(raw.get("recording_session_id") or session_id).strip(),
                recording_id=(raw.get("recording_id") or SESSION_RECORDING_ID).strip(),
                recording_take_no=(raw.get("recording_take_no") or "").strip(),
                batch_take_no=(raw.get("batch_take_no") or "").strip(),
                script_id=(raw.get("script_id") or "").strip(),
                event_id=(raw.get("event_id") or "").strip(),
                event_range=(raw.get("event_range") or "").strip(),
                gesture_id=gesture_id,
                normalized_name=(raw.get("normalized_name") or "").strip(),
                expected_sample_type=(raw.get("expected_sample_type") or "").strip(),
                realization_variant=(raw.get("realization_variant") or "").strip(),
                realization_pre_action=(raw.get("realization_pre_action") or "").strip(),
                notes=(raw.get("notes") or "").strip(),
            )
        )
    return sorted(rows, key=lambda r: int(r.recording_take_no or 0))


def load_raw_inventory(path: Path, raw_audio_dir: Path) -> list[RawAudioItem]:
    items: list[RawAudioItem] = []
    for row in read_csv(path):
        stored = Path((row.get("stored_path") or "").strip())
        source = stored if stored.is_absolute() else Path.cwd() / stored
        if not source.exists():
            fallback = raw_audio_dir / (row.get("original_filename") or "")
            source = fallback if fallback.exists() else source
        sha = (row.get("sha256") or "").strip()
        if source.exists() and (not sha or sha == "unknown"):
            sha = sha256_file(source)
        items.append(
            RawAudioItem(
                batch_id=(row.get("batch_id") or source.stem).strip(),
                source_file_id=(row.get("file_id") or "").strip(),
                source_raw_file=source,
                source_sha256=sha,
                original_filename=(row.get("original_filename") or source.name).strip(),
            )
        )
    return sorted(items, key=lambda item: item.batch_id)


def ensure_output_dirs(output_dir: Path) -> dict[str, Path]:
    dirs = {
        "output": output_dir,
        "working": output_dir / "working_wav",
        "segments": output_dir / "segment_candidates",
        "logs": output_dir / "logs",
    }
    for path in dirs.values():
        path.mkdir(parents=True, exist_ok=True)
    return dirs


def safe_part(value: str, fallback: str) -> str:
    text = (value or fallback).strip()
    text = text.replace(" ", "_")
    text = re.sub(r"[^A-Za-z0-9_.-]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("._")
    return text or fallback


def segment_filename(take: TakePlanRow) -> str:
    take_no = safe_part(take.recording_take_no, "000")
    script_id = safe_part(take.script_id, f"TAKE_{take_no}")
    gesture_id = safe_part(take.gesture_id or "UNKNOWN_GESTURE", "UNKNOWN_GESTURE").upper()
    variant = safe_part(take.realization_variant or "unknown", "unknown")
    return f"{EXPERIMENTAL_SEGMENT_PREFIX}_T{take_no}_{script_id}_{gesture_id}_{variant}.wav"


def ffmpeg_command_for_conversion(ffmpeg: str, source: Path, output: Path) -> list[str]:
    return [
        ffmpeg,
        "-y",
        "-i",
        str(source),
        "-acodec",
        "pcm_s16le",
        str(output),
    ]


def afconvert_command_for_conversion(afconvert: str, source: Path, output: Path) -> list[str]:
    return [
        afconvert,
        "-f",
        "WAVE",
        "-d",
        "LEI16",
        str(source),
        str(output),
    ]


def available_converters(which=shutil.which) -> dict[str, Converter]:
    converters: dict[str, Converter] = {}
    ffmpeg = which("ffmpeg")
    if ffmpeg:
        converters["ffmpeg"] = Converter(name="ffmpeg", executable=ffmpeg)
    afconvert = which("afconvert")
    if afconvert:
        converters["afconvert"] = Converter(name="afconvert", executable=afconvert)
    return converters


def select_converter(which=shutil.which) -> Converter | None:
    converters = available_converters(which)
    return converters.get("ffmpeg") or converters.get("afconvert")


def converter_profiles(converters: dict[str, Converter]) -> list[ConverterProfile]:
    profiles: list[ConverterProfile] = []
    if "ffmpeg" in converters:
        profiles.append(
            ConverterProfile(
                converter=converters["ffmpeg"],
                profile_name="ffmpeg_pcm_s16le_wav",
                output_suffix=".wav",
                command_template=(
                    "{exe}",
                    "-y",
                    "-i",
                    "{input}",
                    "-acodec",
                    "pcm_s16le",
                    "{output}",
                ),
                usable_for_wav_split=True,
            )
        )
    if "afconvert" in converters:
        af = converters["afconvert"]
        profiles.extend(
            [
                ConverterProfile(af, "afconvert_wav_LEI16_48000_positional", ".wav", ("{exe}", "{input}", "{output}", "-f", "WAVE", "-d", "LEI16@48000"), True),
                ConverterProfile(af, "afconvert_wav_LEI16_44100_positional", ".wav", ("{exe}", "{input}", "{output}", "-f", "WAVE", "-d", "LEI16@44100"), True),
                ConverterProfile(af, "afconvert_wav_I16_48000_positional", ".wav", ("{exe}", "{input}", "{output}", "-f", "WAVE", "-d", "I16@48000"), True),
                ConverterProfile(af, "afconvert_wav_I16_44100_positional", ".wav", ("{exe}", "{input}", "{output}", "-f", "WAVE", "-d", "I16@44100"), True),
                ConverterProfile(af, "afconvert_wav_LEI16_48000_options_first", ".wav", ("{exe}", "-f", "WAVE", "-d", "LEI16@48000", "{input}", "{output}"), True),
                ConverterProfile(af, "afconvert_wav_LEI16_44100_options_first", ".wav", ("{exe}", "-f", "WAVE", "-d", "LEI16@44100", "{input}", "{output}"), True),
                ConverterProfile(af, "afconvert_aiff_BEI16_48000_diagnostic", ".aiff", ("{exe}", "{input}", "{output}", "-f", "AIFF", "-d", "BEI16@48000"), False),
                ConverterProfile(af, "afconvert_caf_LEI16_48000_diagnostic", ".caf", ("{exe}", "{input}", "{output}", "-f", "caff", "-d", "LEI16@48000"), False),
            ]
        )
    return profiles


def profile_command(profile: ConverterProfile, source: Path, output: Path) -> list[str]:
    replacements = {
        "{exe}": profile.converter.executable,
        "{input}": str(source),
        "{output}": str(output),
    }
    return [replacements.get(part, part) for part in profile.command_template]


def conversion_command(converter: Converter, source: Path, output: Path) -> list[str]:
    if converter.name == "ffmpeg":
        return ffmpeg_command_for_conversion(converter.executable, source, output)
    if converter.name == "afconvert":
        return afconvert_command_for_conversion(converter.executable, source, output)
    raise ValueError(f"Unsupported converter: {converter.name}")


def probe_converters(raw_items: list[RawAudioItem], logs_dir: Path) -> tuple[list[ProbeResult], ConverterProfile | None]:
    if not raw_items:
        return [], None
    probe_dir = logs_dir / "converter_probe_outputs"
    probe_dir.mkdir(parents=True, exist_ok=True)
    source = raw_items[0].source_raw_file
    results: list[ProbeResult] = []
    selected: ConverterProfile | None = None
    for profile in converter_profiles(available_converters()):
        output = probe_dir / f"{source.stem}_{profile.profile_name}{profile.output_suffix}"
        if output.exists():
            output.unlink()
        command = profile_command(profile, source, output)
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        output_exists = output.exists()
        output_size = output.stat().st_size if output_exists else 0
        status = "success" if result.returncode == 0 and output_exists and output_size > 0 else "failed"
        probe_result = ProbeResult(
            converter=profile.converter.name,
            profile_name=profile.profile_name,
            command=command,
            exit_code=result.returncode,
            stderr_summary=(result.stderr or result.stdout or "").strip().replace("\n", " ")[:500],
            output_exists=output_exists,
            output_size=output_size,
            probe_status=status,
            output_path=output,
            usable_for_wav_split=profile.usable_for_wav_split,
        )
        results.append(probe_result)
        if status == "success" and profile.usable_for_wav_split and selected is None:
            selected = profile
    return results, selected


def write_audio_probe_report(
    logs_dir: Path,
    raw_items: list[RawAudioItem],
    probe_results: list[ProbeResult],
    selected_profile: ConverterProfile | None,
) -> None:
    afinfo = shutil.which("afinfo")
    lines = [
        "# Audio Probe Report",
        "",
        f"- ffmpeg_available: {str(bool(shutil.which('ffmpeg'))).lower()}",
        f"- afconvert_available: {str(bool(shutil.which('afconvert'))).lower()}",
        f"- afinfo_available: {str(bool(afinfo)).lower()}",
        f"- selected_wav_converter_profile: {selected_profile.profile_name if selected_profile else 'none'}",
        "",
        "## Converter Probe Matrix",
        "",
        "| converter | profile | command | exit_code | output_exists | output_size | status | stderr_summary |",
        "| --- | --- | --- | ---: | --- | ---: | --- | --- |",
    ]
    if probe_results:
        for result in probe_results:
            stderr = result.stderr_summary.replace("|", "/")
            command = " ".join(result.command).replace("|", "/")
            lines.append(
                f"| {result.converter} | {result.profile_name} | `{command}` | {result.exit_code} | "
                f"{str(result.output_exists).lower()} | {result.output_size} | "
                f"{result.probe_status} | {stderr} |"
            )
    else:
        lines.append("| none | none |  |  | false | 0 | not_run | no converter available |")
    lines.extend(["", "## afinfo Diagnostics", ""])
    for item in raw_items:
        lines.append(f"### {item.batch_id}: `{rel(item.source_raw_file)}`")
        if not afinfo:
            lines.append("")
            lines.append("afinfo unavailable; diagnostic skipped.")
            lines.append("")
            continue
        result = subprocess.run([afinfo, str(item.source_raw_file)], capture_output=True, text=True, check=False)
        lines.append("")
        lines.append("```text")
        lines.append((result.stdout or result.stderr or "").strip()[:2500])
        lines.append("```")
        lines.append("")
    (logs_dir / "audio_probe_report.md").write_text("\n".join(lines), encoding="utf-8")


def find_provided_working_wav(working_wav_dir: Path, item: RawAudioItem) -> Path | None:
    candidates = [
        working_wav_dir / f"{item.batch_id}_working.wav",
        working_wav_dir / f"{item.source_raw_file.stem}_working.wav",
        working_wav_dir / f"{item.batch_id}.wav",
        working_wav_dir / f"{item.source_raw_file.stem}.wav",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    matches = sorted(working_wav_dir.glob(f"{item.batch_id}*.wav"))
    return matches[0] if matches else None


def ffmpeg_command_for_segment(
    ffmpeg: str, source: Path, start: float, end: float, output: Path
) -> list[str]:
    return [
        ffmpeg,
        "-y",
        "-ss",
        f"{start:.3f}",
        "-to",
        f"{end:.3f}",
        "-i",
        str(source),
        "-acodec",
        "pcm_s16le",
        str(output),
    ]


def convert_working_wavs(
    raw_items: list[RawAudioItem],
    working_dir: Path,
    execute: bool,
    convert_enabled: bool,
    selected_profile: ConverterProfile | None,
    working_wav_dir: Path | None = None,
) -> tuple[list[dict[str, str]], dict[str, Path], Converter | None]:
    converter = selected_profile.converter if selected_profile else None
    rows: list[dict[str, str]] = []
    working_by_batch: dict[str, Path] = {}

    for item in raw_items:
        provided = find_provided_working_wav(working_wav_dir, item) if working_wav_dir else None
        working = provided or working_dir / f"{safe_part(item.batch_id, item.source_raw_file.stem)}_working.wav"
        working_by_batch[item.batch_id] = working
        command = (
            " ".join(profile_command(selected_profile, item.source_raw_file, working))
            if selected_profile
            else ""
        )
        status = "not_requested"
        notes = "conversion disabled; derived WAV not created"
        working_source = "conversion"

        if provided:
            status = "provided"
            command = ""
            working_source = "provided"
            notes = (
                "working WAV was supplied via --working-wav-dir; it is a working "
                "copy only, not a raw master or production source"
            )
        elif working_wav_dir:
            status = "missing_provided"
            command = ""
            working_source = "provided"
            notes = (
                "no matching working WAV was found in --working-wav-dir for this "
                "raw batch; no working WAV was fabricated"
            )
        elif convert_enabled and not selected_profile:
            status = "skipped_no_converter"
            notes = (
                "no usable WAV converter profile was found; no working WAV was "
                "generated; source remains M4A/AAC experimental raw; provide "
                "preconverted working WAV via --working-wav-dir"
            )
        elif convert_enabled and execute and selected_profile:
            if working.exists():
                status = "reused_existing"
                notes = (
                    "working WAV already existed; source sha256 recorded for "
                    "traceability; derived file remains experimental-only and "
                    "does not change the M4A/AAC source into a production source"
                )
            else:
                result = subprocess.run(
                    profile_command(selected_profile, item.source_raw_file, working),
                    capture_output=True,
                    text=True,
                    check=False,
                )
                if result.returncode == 0 and working.exists():
                    status = "created"
                    notes = (
                        "derived working WAV created for experimental split only; "
                        "source remains M4A/AAC experimental raw, not production source"
                    )
                else:
                    status = "failed"
                    notes = (
                        result.stderr
                        or result.stdout
                        or f"{converter.name} failed"
                    ).strip()[-500:]
        elif convert_enabled and not execute:
            status = "planned_dry_run"
            notes = "dry-run only; conversion command not executed"

        rows.append(
            {
                "batch_id": item.batch_id,
                "source_file_id": item.source_file_id,
                "source_raw_file": rel(item.source_raw_file),
                "source_sha256": item.source_sha256,
                "derived_working_file": rel(working),
                "working_wav_source": working_source,
                "conversion_status": status,
                "converter": selected_profile.converter.name if selected_profile else "",
                "converter_profile": selected_profile.profile_name if selected_profile else "",
                "conversion_command": command,
                "experimental_only": "true",
                "production_grade": "false",
                "source_format": "m4a_aac",
                "notes": notes,
            }
        )
    return rows, working_by_batch, converter


def rel(path: Path | str) -> str:
    path = Path(path)
    try:
        return str(path.relative_to(Path.cwd()))
    except ValueError:
        return str(path)


def read_wav_windows(path: Path, min_segment_s: float) -> tuple[list[AudioWindow], float]:
    with wave.open(str(path), "rb") as wav:
        channels = wav.getnchannels()
        sample_width = wav.getsampwidth()
        sample_rate = wav.getframerate()
        frame_count = wav.getnframes()
        duration = frame_count / sample_rate if sample_rate else 0.0
        if sample_width != 2:
            return [], duration

        frame_step = max(1, int(sample_rate * 0.02))
        energies: list[tuple[float, float]] = []
        for index in range(0, frame_count, frame_step):
            raw = wav.readframes(frame_step)
            if not raw:
                break
            sample_count = len(raw) // 2
            if sample_count == 0:
                continue
            total = 0
            for offset in range(0, len(raw) - 1, 2):
                value = int.from_bytes(raw[offset : offset + 2], "little", signed=True)
                total += value * value
            rms = math.sqrt(total / sample_count) / 32768.0
            energies.append((index / sample_rate, rms))

    if not energies:
        return [], duration

    values = [energy for _, energy in energies]
    peak = max(values)
    if peak <= 0:
        return [], duration
    median = statistics.median(values)
    threshold = max(median * 4.0, peak * 0.08, 0.002)
    active_regions = energy_regions(energies, threshold)
    active_regions = merge_regions(active_regions, max_gap_s=0.18)
    active_regions = [(s, e) for s, e in active_regions if e - s >= 0.08]
    windows = merge_regions(active_regions, max_gap_s=0.85)

    audio_windows: list[AudioWindow] = []
    for start, end in windows:
        if end - start < min_segment_s:
            continue
        inner = [(s, e) for s, e in active_regions if s >= start - 0.001 and e <= end + 0.001]
        slate_start = start
        slate_end = min(end, start + 0.45)
        perf_start = start
        perf_end = end
        notes = "single active group; slate boundary estimated"
        if len(inner) >= 2 and inner[0][1] - inner[0][0] <= 1.3:
            slate_start = inner[0][0]
            slate_end = inner[0][1]
            perf_start = inner[1][0]
            notes = "first short active region treated as spoken slate"
        confidence = 0.78 if len(inner) >= 2 else 0.58
        audio_windows.append(
            AudioWindow(
                start=start,
                end=end,
                slate_start=slate_start,
                slate_end=slate_end,
                performance_start=perf_start,
                performance_end=perf_end,
                confidence=confidence,
                notes=notes,
            )
        )
    return audio_windows, duration


def write_wav_segment(source: Path, start: float, end: float, output: Path) -> bool:
    with wave.open(str(source), "rb") as src:
        params = src.getparams()
        frame_rate = src.getframerate()
        start_frame = max(0, int(start * frame_rate))
        end_frame = max(start_frame, int(end * frame_rate))
        src.setpos(min(start_frame, src.getnframes()))
        data = src.readframes(max(0, min(end_frame, src.getnframes()) - start_frame))
    with wave.open(str(output), "wb") as dst:
        dst.setparams(params)
        dst.writeframes(data)
    return output.exists() and output.stat().st_size > 0


def energy_regions(
    energies: list[tuple[float, float]], threshold: float
) -> list[tuple[float, float]]:
    regions: list[tuple[float, float]] = []
    start: float | None = None
    last_t = 0.0
    for t, energy in energies:
        last_t = t
        if energy >= threshold and start is None:
            start = t
        elif energy < threshold and start is not None:
            regions.append((start, t))
            start = None
    if start is not None:
        regions.append((start, last_t + 0.02))
    return regions


def merge_regions(regions: list[tuple[float, float]], max_gap_s: float) -> list[tuple[float, float]]:
    if not regions:
        return []
    merged = [regions[0]]
    for start, end in regions[1:]:
        prev_start, prev_end = merged[-1]
        if start - prev_end <= max_gap_s:
            merged[-1] = (prev_start, max(prev_end, end))
        else:
            merged.append((start, end))
    return merged


def classify_segment(
    take: TakePlanRow,
    window: AudioWindow | None,
    start: float | None,
    end: float | None,
    min_segment_s: float,
    max_segment_s: float,
) -> tuple[float, str, list[str]]:
    reasons: list[str] = []
    gesture_upper = (take.gesture_id or "").upper()
    normalized = take.normalized_name or ""

    if not take.gesture_id or take.gesture_id == "UNKNOWN_GESTURE":
        reasons.append("missing_gesture_id")
    if take.expected_sample_type == "context" or take.realization_variant == "context":
        reasons.append("context_take")
    if take.realization_pre_action == "zhu" or take.realization_variant == "zhu":
        reasons.append("zhu_special_item")
    if "QIAQI" in gesture_upper or "掐起" in normalized:
        reasons.append("qiaqi_special_item")
    if "ZHUANG" in gesture_upper or "撞" in normalized:
        reasons.append("zhuang_special_item")
    if take.script_id == "RS_XWC_001_060" and not take.event_range:
        reasons.append("missing_event_range_context_take")

    if start is None or end is None or window is None:
        reasons.append("missing_segment")
        return 0.0, "forced_review", reasons

    duration = end - start
    allowed_max = 15.0 if take.expected_sample_type == "context" else max_segment_s
    if duration < min_segment_s:
        reasons.append("duration_too_short")
    if duration > allowed_max:
        reasons.append("duration_too_long")
    if window.confidence < 0.65:
        reasons.append("uncertain_slate_performance_boundary")

    if reasons and any(
        reason
        in {
            "missing_gesture_id",
            "context_take",
            "zhu_special_item",
            "qiaqi_special_item",
            "zhuang_special_item",
            "missing_event_range_context_take",
            "missing_segment",
        }
        for reason in reasons
    ):
        return min(0.55, window.confidence if window else 0.0), "forced_review", reasons
    if reasons:
        return min(0.72, window.confidence), "medium", reasons
    return max(0.86, window.confidence), "high", reasons


def split_segments(
    take_plan: list[TakePlanRow],
    raw_items: list[RawAudioItem],
    working_by_batch: dict[str, Path],
    segment_dir: Path,
    ffmpeg: str | None,
    args: argparse.Namespace,
) -> tuple[list[SegmentResult], list[dict[str, object]], list[dict[str, object]], list[TakePlanRow]]:
    if not args.execute or not args.auto_split:
        return [], [], [], take_plan

    segment_results: list[SegmentResult] = []
    slate_rows: list[dict[str, object]] = []
    assigned = 0

    for raw in raw_items:
        working = working_by_batch.get(raw.batch_id)
        if not working or not working.exists():
            continue
        windows, _duration = read_wav_windows(working, args.min_segment_s)
        for window_no, window in enumerate(windows, start=1):
            if assigned >= len(take_plan):
                break
            take = take_plan[assigned]
            assigned += 1
            next_window_start = (
                windows[window_no].start if window_no < len(windows) else None
            )
            start = max(0.0, window.performance_start - args.pre_roll_s)
            end = window.performance_end + max(args.min_tail_s, args.default_tail_s)
            if next_window_start is not None:
                end = min(end, max(window.performance_end, next_window_start - 0.08))
            allowed_max = 15.0 if take.expected_sample_type == "context" else args.max_segment_s
            if end - start > allowed_max:
                end = start + allowed_max
            confidence, level, reasons = classify_segment(
                take, window, start, end, args.min_segment_s, args.max_segment_s
            )
            filename = segment_filename(take)
            segment_file = segment_dir / filename
            if ffmpeg:
                result = subprocess.run(
                    ffmpeg_command_for_segment(ffmpeg, working, start, end, segment_file),
                    capture_output=True,
                    text=True,
                    check=False,
                )
                extract_ok = result.returncode == 0 and segment_file.exists()
            else:
                extract_ok = write_wav_segment(working, start, end, segment_file)
            if not extract_ok:
                reasons.append("segment_extract_failed")
                confidence = 0.0
                level = "forced_review"
            segment_results.append(
                SegmentResult(
                    take=take,
                    raw=raw,
                    working_wav=working,
                    window=window,
                    start_time_s=start,
                    end_time_s=end,
                    segment_file=segment_file,
                    split_confidence=confidence,
                    confidence_level=level,
                    review_reasons=reasons,
                )
            )
            slate_rows.append(
                {
                    "batch_id": raw.batch_id,
                    "source_raw_file": rel(raw.source_raw_file),
                    "derived_working_file": rel(working),
                    "detected_window_no": window_no,
                    "assigned_recording_take_no": take.recording_take_no,
                    "assigned_script_id": take.script_id,
                    "window_start_time_s": f"{window.start:.3f}",
                    "window_end_time_s": f"{window.end:.3f}",
                    "slate_region_start_s": f"{window.slate_start:.3f}",
                    "slate_region_end_s": f"{window.slate_end:.3f}",
                    "performance_region_start_s": f"{window.performance_start:.3f}",
                    "performance_region_end_s": f"{window.performance_end:.3f}",
                    "detection_method": DETECTION_METHOD,
                    "detection_confidence": f"{window.confidence:.2f}",
                    "notes": window.notes,
                }
            )
    missing = take_plan[assigned:]
    return segment_results, slate_rows, [], missing


def manifest_row(result: SegmentResult, session_id: str) -> dict[str, object]:
    take = result.take
    return {
        "experimental_segment_id": f"EXP_{session_id}_T{take.recording_take_no}",
        "recording_session_id": session_id,
        "recording_id": take.recording_id,
        "recording_take_no": take.recording_take_no,
        "batch_take_no": take.batch_take_no,
        "batch_id": result.raw.batch_id,
        "source_file_id": result.raw.source_file_id,
        "source_raw_file": rel(result.raw.source_raw_file),
        "source_sha256": result.raw.source_sha256,
        "derived_working_file": rel(result.working_wav),
        "script_id": take.script_id,
        "event_id": take.event_id,
        "event_range": take.event_range,
        "gesture_id": take.gesture_id,
        "normalized_name": take.normalized_name,
        "expected_sample_type": take.expected_sample_type,
        "realization_variant": take.realization_variant,
        "realization_pre_action": take.realization_pre_action,
        "start_time_s": f"{result.start_time_s:.3f}",
        "end_time_s": f"{result.end_time_s:.3f}",
        "attack_marker_ms": "0",
        "release_tail_ms": f"{max(0.0, result.end_time_s - result.window.performance_end) * 1000:.0f}",
        "segment_file_path": rel(result.segment_file),
        "segment_filename": result.segment_file.name,
        "slate_detection_method": DETECTION_METHOD,
        "split_confidence": f"{result.split_confidence:.2f}",
        "confidence_level": result.confidence_level,
        "needs_manual_review": str(result.confidence_level != "high").lower(),
        "review_reason": ";".join(result.review_reasons),
        "qc_status": "auto_split_candidate",
        "quality_status": "pending",
        "selected_for_mvp_render": "false",
        "experimental_only": "true",
        "production_grade": "false",
        "not_standard_sample_library": "true",
        "notes": take.notes,
    }


def boundary_row_from_result(
    index: int, result: SegmentResult, session_id: str
) -> dict[str, object]:
    row = manifest_row(result, session_id)
    return {
        "review_row_id": f"BR_{index:03d}",
        "experimental_segment_id": row["experimental_segment_id"],
        "recording_take_no": row["recording_take_no"],
        "batch_take_no": row["batch_take_no"],
        "script_id": row["script_id"],
        "batch_id": row["batch_id"],
        "source_raw_file": row["source_raw_file"],
        "segment_file_path": row["segment_file_path"],
        "segment_filename": row["segment_filename"],
        "event_id": row["event_id"],
        "event_range": row["event_range"],
        "gesture_id": row["gesture_id"],
        "normalized_name": row["normalized_name"],
        "expected_sample_type": row["expected_sample_type"],
        "realization_variant": row["realization_variant"],
        "confidence_level": row["confidence_level"],
        "split_confidence": row["split_confidence"],
        "review_reason": row["review_reason"],
        "current_start_time_s": row["start_time_s"],
        "current_end_time_s": row["end_time_s"],
        "recommended_action": recommended_action(str(row["review_reason"])),
        "review_decision": "",
        "review_adjusted_start_time_s": "",
        "review_adjusted_end_time_s": "",
        "review_note": "",
    }


def boundary_row_from_missing(
    index: int, take: TakePlanRow, session_id: str
) -> dict[str, object]:
    reasons = ["missing_segment"]
    _, _level, take_reasons = classify_segment(take, None, None, None, 0.3, 8.0)
    reasons.extend(reason for reason in take_reasons if reason not in reasons)
    return {
        "review_row_id": f"BR_{index:03d}",
        "experimental_segment_id": f"EXP_{session_id}_T{take.recording_take_no}",
        "recording_take_no": take.recording_take_no,
        "batch_take_no": take.batch_take_no,
        "script_id": take.script_id,
        "batch_id": "",
        "source_raw_file": "",
        "segment_file_path": "",
        "segment_filename": "",
        "event_id": take.event_id,
        "event_range": take.event_range,
        "gesture_id": take.gesture_id,
        "normalized_name": take.normalized_name,
        "expected_sample_type": take.expected_sample_type,
        "realization_variant": take.realization_variant,
        "confidence_level": "forced_review",
        "split_confidence": "0.00",
        "review_reason": ";".join(reasons),
        "current_start_time_s": "",
        "current_end_time_s": "",
        "recommended_action": recommended_action(";".join(reasons)),
        "review_decision": "",
        "review_adjusted_start_time_s": "",
        "review_adjusted_end_time_s": "",
        "review_note": "",
    }


def recommended_action(review_reason: str) -> str:
    if "missing_segment" in review_reason:
        return "install ffmpeg or use macOS afconvert/provide working WAV, then rerun auto split; manually mark boundaries if needed"
    if "missing_event_range_context_take" in review_reason:
        return "human confirm context event_range; possible candidate is XWC_P09_N01_to_N02, do not auto-write it"
    if "context_take" in review_reason:
        return "human review context boundaries before sample candidate selection"
    if "missing_gesture_id" in review_reason:
        return "repair take-plan gesture_id before downstream use"
    return "audition and adjust boundary if needed"


def summarize(
    take_plan: list[TakePlanRow],
    manifest_rows: list[dict[str, object]],
    boundary_rows: list[dict[str, object]],
    conversion_rows: list[dict[str, str]],
    missing_rows: list[TakePlanRow],
    converter: Converter | None,
    asr_used: bool = False,
) -> dict[str, object]:
    levels = {"high": 0, "medium": 0, "low": 0, "forced_review": 0}
    for row in manifest_rows:
        level = str(row.get("confidence_level", ""))
        if level in levels:
            levels[level] += 1
    levels["forced_review"] += len(missing_rows)
    reasons = ";".join(str(row.get("review_reason", "")) for row in manifest_rows)
    reasons += ";" + ";".join(str(row.get("review_reason", "")) for row in boundary_rows)
    filenames_ok = all(
        not row.get("segment_filename")
        or str(row.get("gesture_id") or "") in str(row.get("segment_filename") or "")
        for row in manifest_rows
    )
    unknown_gesture = sum(
        1 for row in manifest_rows if row.get("gesture_id") == "UNKNOWN_GESTURE"
    )
    conversion_created = sum(
        1
        for row in conversion_rows
        if row["conversion_status"] in {"created", "reused_existing", "provided"}
    )
    converter_names = sorted({row.get("converter", "") for row in conversion_rows if row.get("converter", "")})
    converter_profiles_used = sorted({row.get("converter_profile", "") for row in conversion_rows if row.get("converter_profile", "")})
    converter_name = converter.name if converter else (",".join(converter_names) if converter_names else "")
    return {
        "expected_count": len(take_plan),
        "segments_created": len(manifest_rows),
        "missing_count": len(missing_rows),
        "high": levels["high"],
        "medium": levels["medium"],
        "low": levels["low"],
        "forced_review": levels["forced_review"],
        "boundary_review_count": len(boundary_rows),
        "context_count": sum(1 for t in take_plan if t.expected_sample_type == "context"),
        "zhu_count": sum(
            1
            for t in take_plan
            if t.realization_pre_action == "zhu" or t.realization_variant == "zhu"
        ),
        "qiaqi_count": sum(
            1 for t in take_plan if "QIAQI" in t.gesture_id.upper() or "掐起" in t.normalized_name
        ),
        "event_range_gap_count": sum(
            1 for t in take_plan if t.script_id == "RS_XWC_001_060" and not t.event_range
        ),
        "retake_suspected_count": reasons.count("retake_suspected"),
        "missing_gesture_id_count": sum(
            1 for t in take_plan if not t.gesture_id or t.gesture_id == "UNKNOWN_GESTURE"
        )
        + unknown_gesture,
        "filenames_include_gesture_id": filenames_ok,
        "unknown_gesture_count": unknown_gesture,
        "working_wav_count": conversion_created,
        "converter": converter_name,
        "converter_profile": ",".join(converter_profiles_used),
        "ffmpeg_available": converter_name == "ffmpeg" or bool(shutil.which("ffmpeg")),
        "afconvert_available": converter_name == "afconvert" or bool(shutil.which("afconvert")),
        "converter_available": bool(converter_name),
        "asr_used": asr_used,
    }


def write_markdown_outputs(
    output_dir: Path,
    reports_dir: Path,
    summary: dict[str, object],
    conversion_rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> None:
    if summary["converter"]:
        if summary["working_wav_count"]:
            converter_note = (
                f"{summary['converter']} was used for working WAV conversion"
                f"{' with ' + summary['converter_profile'] if summary.get('converter_profile') else ''}. "
                "The source files remain M4A/AAC experimental raw material and do "
                "not become production sources."
            )
        else:
            converter_note = (
                f"{summary['converter']} was selected and attempted for working "
                "WAV conversion, but no derived WAV was generated. The source "
                "files remain M4A/AAC experimental raw material and do not "
                "become production sources."
            )
    else:
        if summary["afconvert_available"] or summary["ffmpeg_available"]:
            converter_note = (
                "Converter binaries were available, but no usable WAV converter "
                "profile was found. See `logs/audio_probe_report.md`; provide "
                "preconverted working WAV via `--working-wav-dir` or continue "
                "Phase 1B-3E-A converter/input repair."
            )
        else:
            converter_note = (
                "Neither ffmpeg nor afconvert was available on PATH, so no derived "
                "working WAV or segment candidate files were created."
            )
    next_step = (
        "Stay in Phase 1B-3E-A converter/input repair because no working WAV "
        "files were generated; do not enter 1B-3E-B yet."
        if summary["working_wav_count"] == 0
        else "Stay in Phase 1B-3E-A auto-split diagnosis because working WAVs "
        "exist but no segment candidates were produced; do not enter 1B-3E-B yet."
        if summary["segments_created"] == 0
        else "If coverage is acceptable after audition, proceed to Phase 1B-3E-C "
        "Experimental Sample Candidate Set; otherwise run 1B-3E-B boundary repair."
    )
    scope_lines = [
        "- This run is experimental auto split only.",
        "- This run did not write `03_samples`.",
        "- This run did not write `sample_assets`.",
        "- This run did not create `recording_items_enriched`.",
        "- This run did not modify raw master audio.",
        "- This run did not modify V1 runtime.",
        "- This run did not modify legacy recording scripts.",
        "- Next step is determined by whether segment candidates exist; this is not production sample ingest.",
    ]

    confidence_report = f"""# Slate-Based Experimental Split Confidence Report

Session: `{args.session_id}`

## Summary

- Expected takes: {summary['expected_count']}
- Segment candidates created: {summary['segments_created']}
- Missing segments: {summary['missing_count']}
- high: {summary['high']}
- medium: {summary['medium']}
- low: {summary['low']}
- forced_review: {summary['forced_review']}
- Boundary review rows: {summary['boundary_review_count']}

## Risk Counts

- context takes: {summary['context_count']}
- zhu items: {summary['zhu_count']}
- qiaqi items: {summary['qiaqi_count']}
- RS_XWC_001_060 event_range gap: {summary['event_range_gap_count']}
- retake suspected: {summary['retake_suspected_count']}
- missing gesture_id: {summary['missing_gesture_id_count']}

## Filename Rule

- All generated segment filenames include gesture_id: {str(summary['filenames_include_gesture_id']).lower()}
- UNKNOWN_GESTURE filenames: {summary['unknown_gesture_count']}

## Method

- Slate detection method: `{DETECTION_METHOD}`
- ASR used: {str(summary['asr_used']).lower()}
- Converter status: {converter_note}

## RS_XWC_001_060 Note

`RS_XWC_001_060` is recognized as a forced-review context take with a missing
`event_range`. The script does not patch legacy source files and does not
auto-write `XWC_P09_N01_to_N02`; that value remains only a human review
possibility if this row is confirmed as 撞到掐起 context.

## Next Step

{next_step}
"""
    (output_dir / "split_confidence_report.md").write_text(confidence_report, encoding="utf-8")

    readme = f"""# Experimental Split Sandbox

Session: `{args.session_id}`

This directory contains only non-production experimental split artifacts for
the MVP pilot. It is not a formal sample library and does not register segment
candidates into `03_samples`.

{converter_note}
"""
    (output_dir / "README.md").write_text(readme, encoding="utf-8")

    split_plan = f"""# Slate-Based Split Plan

## Input Strategy

The `legacy_xwc_preview` adapter reads the 71-row legacy take preview and
normalizes each row to the reusable take-plan schema:

`{', '.join(TAKE_PLAN_FIELDS)}`

Future formal sampling should replace this adapter with
`dapu_event_ir_recording_plan`, fed by guqin-dapu-parser, Dapu Event IR, and a
canon-backed recording plan.

## Split Strategy

Derived working WAV files are scanned for energy windows. Windows are aligned
sequentially to expected takes across raw batch order. Spoken slate text is not
invented; without ASR, the method is `{DETECTION_METHOD}`.

## Parameters

- pre_roll_s: {args.pre_roll_s}
- min_tail_s: {args.min_tail_s}
- default_tail_s: {args.default_tail_s}
- min_segment_s: {args.min_segment_s}
- max_segment_s: {args.max_segment_s}
"""
    (output_dir / "split_plan.md").write_text(split_plan, encoding="utf-8")

    conversion_notes = "# Conversion Notes\n\n"
    conversion_notes += f"{converter_note}\n\n"
    conversion_notes += "Converter probe details are in `logs/audio_probe_report.md`.\n\n"
    conversion_notes += "All derived WAVs, if generated, are experimental_only=true and production_grade=false.\n"
    for row in conversion_rows:
        conversion_notes += (
            f"- {row['batch_id']}: {row['conversion_status']}; "
            f"converter={row.get('converter', '')}; source_sha256={row['source_sha256']} -> "
            f"`{row['derived_working_file']}`\n"
            f"  - command: `{row['conversion_command']}`\n"
        )
    (output_dir / "conversion_notes.md").write_text(conversion_notes, encoding="utf-8")

    qc_note = f"""# Experimental Split QC Note

Session: `{args.session_id}`

## QC Status

- Segment candidates created: {summary['segments_created']}
- Missing segments: {summary['missing_count']}
- Boundary review rows: {summary['boundary_review_count']}
- Working WAV files generated/reused: {summary['working_wav_count']}

## Scope

{os.linesep.join(scope_lines)}

## Converter

{converter_note}
"""
    (output_dir / "experimental_split_qc_note.md").write_text(qc_note, encoding="utf-8")

    next_step_doc = f"""# Next Step: Phase 1B-3E-C Sample Candidate Plan

This sandbox can feed a non-production experimental sample candidate set only
after boundary review. It must not be promoted directly to `sample_assets` or
formal `recording_segments`.

Recommended next step: {next_step}
"""
    (output_dir / "next_step_1b3e_c_sample_candidate_plan.md").write_text(
        next_step_doc, encoding="utf-8"
    )

    report = f"""# MVP Slate Auto Split Report

## Scope

{os.linesep.join(scope_lines)}

## Results

- Expected takes: {summary['expected_count']}
- Segment candidates created: {summary['segments_created']}
- Missing segments: {summary['missing_count']}
- high: {summary['high']}
- medium: {summary['medium']}
- low: {summary['low']}
- forced_review: {summary['forced_review']}
- Working WAV generated/reused: {summary['working_wav_count']}
- Converter used: {summary['converter'] or 'none'}
- Converter profile: {summary.get('converter_profile') or 'none'}
- ASR used: {str(summary['asr_used']).lower()}
- Detection method: `{DETECTION_METHOD}`
- RS_XWC_001_060 event_range gap recognized: {str(summary['event_range_gap_count'] > 0).lower()}
- Segment filenames include gesture_id: {str(summary['filenames_include_gesture_id']).lower()}
- UNKNOWN_GESTURE count: {summary['unknown_gesture_count']}

## Converter

{converter_note}

## Next Step

{next_step}
"""
    (reports_dir / "mvp_slate_auto_split_report.md").write_text(report, encoding="utf-8")

    next_steps = f"""# MVP Slate Auto Split Next Steps

{next_step}

This is not production sample ingest. Do not write `03_samples`, `sample_assets`,
or `recording_items_enriched` from these artifacts.
"""
    (reports_dir / "mvp_slate_auto_split_next_steps.md").write_text(
        next_steps, encoding="utf-8"
    )

    confidence_rows = [
        {"metric": "expected_count", "value": summary["expected_count"]},
        {"metric": "segments_created", "value": summary["segments_created"]},
        {"metric": "missing_count", "value": summary["missing_count"]},
        {"metric": "high", "value": summary["high"]},
        {"metric": "medium", "value": summary["medium"]},
        {"metric": "low", "value": summary["low"]},
        {"metric": "forced_review", "value": summary["forced_review"]},
        {"metric": "boundary_review_count", "value": summary["boundary_review_count"]},
        {"metric": "working_wav_count", "value": summary["working_wav_count"]},
        {"metric": "converter", "value": summary["converter"] or "none"},
        {"metric": "converter_profile", "value": summary.get("converter_profile") or "none"},
        {"metric": "ffmpeg_available", "value": str(summary["ffmpeg_available"]).lower()},
        {"metric": "afconvert_available", "value": str(summary["afconvert_available"]).lower()},
        {"metric": "asr_used", "value": str(summary["asr_used"]).lower()},
        {
            "metric": "filenames_include_gesture_id",
            "value": str(summary["filenames_include_gesture_id"]).lower(),
        },
        {"metric": "unknown_gesture_count", "value": summary["unknown_gesture_count"]},
    ]
    write_csv(
        reports_dir / "mvp_slate_auto_split_confidence_summary.csv",
        ["metric", "value"],
        confidence_rows,
    )


def run(args: argparse.Namespace) -> int:
    take_plan = load_take_plan(args.take_plan_kind, args.take_plan, args.session_id)
    raw_items = load_raw_inventory(args.raw_inventory, args.raw_audio_dir)

    if len(take_plan) != args.expected_count:
        print(
            f"WARNING: expected {args.expected_count} takes, loaded {len(take_plan)}",
            file=sys.stderr,
        )

    if args.dry_run:
        ffmpeg = shutil.which("ffmpeg")
        afconvert = shutil.which("afconvert")
        afinfo = shutil.which("afinfo")
        converter = select_converter()
        print("Dry run: no files will be written.")
        print(f"session_id={args.session_id}")
        print(f"take_plan_kind={args.take_plan_kind}")
        print(f"loaded_takes={len(take_plan)}")
        print(f"loaded_raw_batches={len(raw_items)}")
        print(f"ffmpeg_available={str(bool(ffmpeg)).lower()}")
        print(f"afconvert_available={str(bool(afconvert)).lower()}")
        print(f"afinfo_available={str(bool(afinfo)).lower()}")
        print(f"selected_converter={converter.name if converter else 'none'}")
        print(f"working_wav_dir={args.working_wav_dir or ''}")
        print(f"converter_probe_only={str(args.converter_probe_only).lower()}")
        print(f"convert_working_wav_requested={str(args.convert_working_wav).lower()}")
        print(f"auto_split_requested={str(args.auto_split).lower()}")
        print("future_adapter_reserved=dapu_event_ir_recording_plan")
        return 0

    dirs = ensure_output_dirs(args.output_dir)
    reports_dir = Path("reports")
    probe_results: list[ProbeResult] = []
    selected_profile: ConverterProfile | None = None
    if args.converter_probe_only or args.convert_working_wav:
        probe_results, selected_profile = probe_converters(raw_items, dirs["logs"])
    write_audio_probe_report(dirs["logs"], raw_items, probe_results, selected_profile)

    conversion_rows, working_by_batch, converter = convert_working_wavs(
        raw_items,
        dirs["working"],
        execute=args.execute,
        convert_enabled=args.convert_working_wav,
        selected_profile=selected_profile,
        working_wav_dir=args.working_wav_dir,
    )
    segment_ffmpeg = shutil.which("ffmpeg")

    can_split = (
        args.execute
        and args.auto_split
        and any(Path(path).exists() for path in working_by_batch.values())
        and not args.converter_probe_only
    )
    if not can_split:
        segment_results: list[SegmentResult] = []
        slate_rows: list[dict[str, object]] = []
        missing_takes = take_plan
    else:
        segment_results, slate_rows, _split_notes, missing_takes = split_segments(
            take_plan, raw_items, working_by_batch, dirs["segments"], segment_ffmpeg, args
        )

    manifest_rows = [manifest_row(result, args.session_id) for result in segment_results]
    boundary_rows = [
        boundary_row_from_result(index, result, args.session_id)
        for index, result in enumerate(
            [r for r in segment_results if r.confidence_level != "high"], start=1
        )
    ]
    next_index = len(boundary_rows) + 1
    boundary_rows.extend(
        boundary_row_from_missing(index, take, args.session_id)
        for index, take in enumerate(missing_takes, start=next_index)
    )

    write_csv(dirs["output"] / "derived_audio_inventory.csv", DERIVED_INVENTORY_FIELDS, conversion_rows)
    write_csv(dirs["output"] / "experimental_segment_manifest.csv", MANIFEST_FIELDS, manifest_rows)
    write_csv(dirs["output"] / "boundary_review_sheet.csv", BOUNDARY_FIELDS, boundary_rows)
    write_csv(dirs["output"] / "slate_detection_report.csv", SLATE_FIELDS, slate_rows)

    summary = summarize(
        take_plan, manifest_rows, boundary_rows, conversion_rows, missing_takes, converter
    )
    write_markdown_outputs(dirs["output"], reports_dir, summary, conversion_rows, args)

    write_csv(
        reports_dir / "mvp_slate_auto_split_manifest.csv",
        MANIFEST_FIELDS,
        manifest_rows,
    )
    write_csv(
        reports_dir / "mvp_slate_auto_split_boundary_review_sheet.csv",
        BOUNDARY_FIELDS,
        boundary_rows,
    )

    print(f"expected_takes={summary['expected_count']}")
    print(f"segment_candidates={summary['segments_created']}")
    print(f"missing_segments={summary['missing_count']}")
    print(f"working_wav_count={summary['working_wav_count']}")
    print(
        "confidence_counts="
        f"high:{summary['high']},medium:{summary['medium']},"
        f"low:{summary['low']},forced_review:{summary['forced_review']}"
    )
    print(f"boundary_review_rows={summary['boundary_review_count']}")
    print(f"converter={summary['converter'] or 'none'}")
    if not converter and args.convert_working_wav:
        print("conversion_status=skipped_no_converter")
    return 0


def main() -> int:
    return run(parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
