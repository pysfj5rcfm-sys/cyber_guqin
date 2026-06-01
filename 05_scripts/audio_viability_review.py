from pathlib import Path
import csv
import wave

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

FIELDS = ["check_id","candidate_id","status","message"]

def wav_duration(path):
    with wave.open(str(path), "rb") as wav:
        frames = wav.getnframes()
        rate = wav.getframerate()
        return frames / rate

def main():
    score = read_csv(SCORE); require_score_count(score)
    templates = load_templates()
    render_path = REPORT_DIR / "render_events.csv"
    rows = []
    overall = "pass"
    def add(cid, status, message, candidate=""):
        nonlocal overall
        rows.append({"check_id": cid, "candidate_id": candidate, "status": status, "message": message})
        if status == "fail": overall = "fail"
        elif status == "warning" and overall == "pass": overall = "warning"
    if not render_path.exists():
        add("render_events_exists", "fail", "render_events.csv missing")
        render_events = []
    else:
        render_events = read_csv(render_path)
        add("render_events_exists", "pass", "render_events.csv exists")
    durations = {}
    for cid in ["A_even", "B_phrase", "C_sanban", "D_teaching"]:
        wav_path = RENDER_DIR / f"{cid}.wav"
        if not wav_path.exists() or wav_path.stat().st_size == 0:
            add("wav_exists", "fail", "wav missing or empty", cid); continue
        try:
            durations[cid] = wav_duration(wav_path)
            add("wav_readable", "pass", f"wav readable duration={durations[cid]:.2f}s", cid)
        except wave.Error as exc:
            add("wav_readable", "fail", f"wave read error: {exc}", cid)
        rhythm = read_csv(RHYTHM_DIR / f"{cid}.csv")
        add("rhythm_coverage", "pass" if len(rhythm) == 51 else "fail", f"rhythm rows={len(rhythm)}", cid)
        rendered = [r for r in render_events if r["candidate_id"] == cid]
        add("render_coverage", "pass" if len(rendered) == 51 else "fail", f"render rows={len(rendered)}", cid)
        missing = [r for r in rendered if not r["sample_id"]]
        add("missing_sample", "pass" if not missing else "fail", f"missing samples={len(missing)}", cid)
        prev = None
        repeats = 0
        for r in rendered:
            key = (r["gesture_id"], r["sample_id"])
            if key == prev:
                repeats += 1
            prev = key
        add("repeat_sample", "pass" if repeats == 0 else "warning", f"consecutive same gesture/sample repeats={repeats}", cid)
    if len({round(v, 1) for v in durations.values()}) > 1:
        add("duration_difference", "pass", "A/B/C/D total durations differ")
    else:
        add("duration_difference", "warning", "A/B/C/D total durations too similar")
    score_by_id = {r["event_id"]: r for r in score}
    for r in render_events:
        event = score_by_id[r["event_id"]]
        template = templates[event["gesture_id"]]
        if event["notation_pre_action"] == "zhu" and r["render_note"] not in {"zhu", "fallback"}:
            add("explicit_zhu", "warning", f"{r['event_id']} did not use zhu or fallback", r["candidate_id"])
        if template["primary_sound_type"] == "按音" and event["notation_pre_action"] == "none" and template["gesture_family"] != "left_hand_sound" and r["render_note"] not in {"chuo", "fallback"}:
            add("default_chuo", "warning", f"{r['event_id']} did not use chuo or fallback", r["candidate_id"])
        if template["gesture_family"] == "left_hand_sound" and r["render_note"] != "context":
            add("qiaqi_context", "warning", f"{r['event_id']} qiaqi did not use context", r["candidate_id"])
    md = ["# Audio Viability Report", "", f"Overall status: {overall}", ""]
    for r in rows:
        md.append(f"- [{r['status']}] {r['candidate_id']} {r['check_id']}: {r['message']}")
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / "audio_viability_report.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    write_csv(REPORT_DIR / "audio_viability_report.csv", FIELDS, rows)
    print(f"Audio viability status: {overall}")

if __name__ == "__main__":
    main()
