from pathlib import Path
import csv
import math
import struct
import wave

ROOT = Path(__file__).resolve().parents[1]
SCORE = ROOT / "01_pieces" / "xianwengcao" / "score_events.csv"
TEMPLATES = ROOT / "00_global" / "gesture_templates.csv"
SAMPLE_ASSETS = ROOT / "03_samples" / "sample_assets.csv"

def read_csv(path):
    with Path(path).open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def write_csv(path, fieldnames, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def require_score_count(rows):
    if len(rows) != 51:
        raise ValueError(f"score_events.csv must contain 51 data rows, got {len(rows)}")

def load_templates():
    return {row["gesture_id"]: row for row in read_csv(TEMPLATES)}

def validate_score_templates(score_rows, templates):
    missing = sorted({row["gesture_id"] for row in score_rows if row["gesture_id"] not in templates})
    if missing:
        raise ValueError("gesture_id missing from gesture_templates.csv: " + ", ".join(missing))

FIELDS = ["sample_id","qinist_id","gesture_id","realization_variant","realization_pre_action","realization_vibrato","qin_id","tuning_id","dynamic","take","sample_type","file_path","sample_rate","bit_depth","attack_marker_ms","perceptual_offset_ms","tail_ms","quality_status","source_type","source_recording_id","source_segment_id","source_event_id","source_event_range","extraction_method","notes"]
SAMPLE_RATE = 44100

def write_wav(path, frequency, seconds, amplitude=0.28):
    path.parent.mkdir(parents=True, exist_ok=True)
    frames = int(SAMPLE_RATE * seconds)
    payload = bytearray()
    # Build the whole buffer once; per-frame writeframes is far slower on Windows.
    for i in range(frames):
        t = i / SAMPLE_RATE
        decay = math.exp(-2.2 * t / max(seconds, 0.1))
        sample = amplitude * decay * (math.sin(2 * math.pi * frequency * t) + 0.25 * math.sin(2 * math.pi * frequency * 2.01 * t))
        payload.extend(struct.pack("<h", max(-32767, min(32767, int(sample * 32767)))))
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        wav.writeframes(payload)

def make_row(sample_id, gid, variant, pre_action, take, sample_type, rel_path):
    return {
        "sample_id": sample_id, "qinist_id": "QINIST_001", "gesture_id": gid,
        "realization_variant": variant, "realization_pre_action": pre_action,
        "realization_vibrato": "none", "qin_id": "QIN_A", "tuning_id": "ZHENG_DIAO",
        "dynamic": "mp", "take": str(take), "sample_type": sample_type,
        "file_path": rel_path, "sample_rate": "44100", "bit_depth": "16",
        "attack_marker_ms": "50", "perceptual_offset_ms": "600", "tail_ms": "500",
        "quality_status": "good", "source_type": "dummy", "source_recording_id": "",
        "source_segment_id": "", "source_event_id": "", "source_event_range": "",
        "extraction_method": "generated", "notes": "Phase 0.1 generated dummy sample",
    }

def main():
    score = read_csv(SCORE)
    require_score_count(score)
    templates = load_templates()
    validate_score_templates(score, templates)
    zhu_gestures = {row["gesture_id"] for row in score if row["notation_pre_action"] == "zhu"}
    rows = []
    for idx, (gid, template) in enumerate(templates.items(), start=1):
        base = 180 + idx * 17
        variants = []
        if template["gesture_family"] == "left_hand_sound":
            variants = [("atomic", "none", "atomic", 1), ("context", "none", "context", 1)]
        elif template["primary_sound_type"] in {"散音", "泛音"}:
            variants = [("straight", "none", "atomic", 1), ("straight", "none", "atomic", 2)]
        elif gid in zhu_gestures:
            variants = [("straight", "none", "atomic", 1), ("straight", "none", "atomic", 2), ("zhu", "zhu", "atomic", 1), ("zhu", "zhu", "atomic", 2)]
        else:
            variants = [("straight", "none", "atomic", 1), ("straight", "none", "atomic", 2), ("chuo", "chuo", "atomic", 1), ("chuo", "chuo", "atomic", 2)]
        for variant, pre_action, sample_type, take in variants:
            sample_id = f"SMP_{gid}_{variant}_{take:02d}"
            duration = 1.05 + (idx % 5) * 0.12 + (0.25 if sample_type == "context" else 0.0)
            frequency = base + (take * 3) + (19 if variant == "chuo" else 31 if variant == "zhu" else 47 if variant == "context" else 0)
            rel_path = f"03_samples/QIN_A/ZHENG_DIAO/{gid}/{sample_id}.wav"
            write_wav(ROOT / rel_path, frequency, duration)
            rows.append(make_row(sample_id, gid, variant, pre_action, take, sample_type, rel_path))
    write_csv(SAMPLE_ASSETS, FIELDS, rows)
    print(f"Generated {SAMPLE_ASSETS} with {len(rows)} dummy samples.")

if __name__ == "__main__":
    main()
