from pathlib import Path
import csv
import wave
import struct

ROOT = Path(__file__).resolve().parents[1]
SCORE = ROOT / "01_pieces" / "xianwengcao" / "score_events.csv"
TEMPLATES = ROOT / "00_global" / "gesture_templates.csv"
SAMPLE_ASSETS = ROOT / "03_samples" / "sample_assets.csv"
RHYTHM_DIR = ROOT / "01_pieces" / "xianwengcao" / "rhythm_candidates"
RENDER_DIR = ROOT / "04_outputs" / "xianwengcao" / "renders"
REPORT_DIR = ROOT / "04_outputs" / "xianwengcao" / "reports"

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

FIELDS = ["render_id","candidate_id","event_id","gesture_id","sample_id","realization_variant","start_time","attack_align_time","gain_db","time_stretch","render_note"]
SR = 44100

def read_wav(path):
    with wave.open(str(path), "rb") as wav:
        if wav.getnchannels() != 1 or wav.getsampwidth() != 2 or wav.getframerate() != SR:
            raise ValueError(f"Unsupported wav format: {path}")
        frames = wav.readframes(wav.getnframes())
    return [v[0] for v in struct.iter_unpack("<h", frames)]

def write_wav(path, samples):
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1); wav.setsampwidth(2); wav.setframerate(SR)
        wav.writeframes(b"".join(struct.pack("<h", max(-32768, min(32767, int(v)))) for v in samples))

def choose_sample(event, template, assets, counters):
    gid = event["gesture_id"]
    candidates = [a for a in assets if a["gesture_id"] == gid]
    def pick(filtered, note):
        if not filtered:
            return None
        key = (gid, note)
        idx = counters.get(key, 0) % len(filtered)
        counters[key] = counters.get(key, 0) + 1
        return filtered[idx], note
    if template["gesture_family"] == "left_hand_sound":
        got = pick([a for a in candidates if a["sample_type"] == "context"], "context")
        if got: return got
    if event["notation_pre_action"] == "zhu":
        got = pick([a for a in candidates if a["realization_pre_action"] == "zhu"], "zhu")
        if got: return got
    if event["notation_pre_action"] == "chuo":
        got = pick([a for a in candidates if a["realization_pre_action"] == "chuo"], "chuo")
        if got: return got
    if template["primary_sound_type"] == "按音" and event["notation_pre_action"] == "none":
        got = pick([a for a in candidates if a["realization_pre_action"] == "chuo"], "chuo")
        if got: return got
    got = pick([a for a in candidates if a["realization_variant"] == "straight"], "straight")
    if got: return got
    got = pick(candidates, "fallback")
    if got: return got
    return None, "missing sample"

def main():
    score = read_csv(SCORE)
    require_score_count(score)
    score_by_id = {row["event_id"]: row for row in score}
    templates = load_templates()
    validate_score_templates(score, templates)
    assets = read_csv(SAMPLE_ASSETS)
    rows = []
    counters = {}
    for rhythm_path in sorted(RHYTHM_DIR.glob("*.csv")):
        rhythm = read_csv(rhythm_path)
        if len(rhythm) != 51:
            raise ValueError(f"{rhythm_path} must cover 51 events, got {len(rhythm)}")
        candidate_id = rhythm_path.stem
        end_time = max(float(r["event_start"]) + float(r["total_duration"]) + 2.0 for r in rhythm)
        mix = [0] * int(end_time * SR)
        for idx, r in enumerate(rhythm, start=1):
            event = score_by_id[r["event_id"]]
            template = templates[event["gesture_id"]]
            sample, note = choose_sample(event, template, assets, counters)
            if not sample:
                rows.append({"render_id": f"{candidate_id}_{idx:03d}", "candidate_id": candidate_id, "event_id": event["event_id"], "gesture_id": event["gesture_id"], "sample_id": "", "realization_variant": "", "start_time": r["event_start"], "attack_align_time": r["attack_time"], "gain_db": "0", "time_stretch": "1.0", "render_note": note})
                continue
            data = read_wav(Path(sample["file_path"]))
            start = float(r["attack_time"]) - (float(sample["attack_marker_ms"]) / 1000.0)
            offset = max(0, int(start * SR))
            for i, value in enumerate(data):
                pos = offset + i
                if pos >= len(mix): break
                mix[pos] += value
            rows.append({"render_id": f"{candidate_id}_{idx:03d}", "candidate_id": candidate_id, "event_id": event["event_id"], "gesture_id": event["gesture_id"], "sample_id": sample["sample_id"], "realization_variant": sample["realization_variant"], "start_time": f"{start:.3f}", "attack_align_time": r["attack_time"], "gain_db": "0", "time_stretch": "1.0", "render_note": note})
        write_wav(RENDER_DIR / f"{candidate_id}.wav", mix)
        print(f"Rendered {candidate_id}.wav")
    write_csv(REPORT_DIR / "render_events.csv", FIELDS, rows)
    print("Generated render_events.csv")

if __name__ == "__main__":
    main()
