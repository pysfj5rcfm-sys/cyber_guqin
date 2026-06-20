export const markerNudgeDeltasMs = [-500, -50, -5, 5, 50, 500] as const;

export function MarkerNudgeControls({
  nudgeTotalMs,
  onNudge,
}: {
  nudgeTotalMs: number;
  onNudge: (deltaMs: number) => void;
}) {
  return (
    <>
      <div className="nudge-grid">
        {markerNudgeDeltasMs.map((delta) => (
          <button key={delta} onClick={() => onNudge(delta)}>{delta > 0 ? "+" : ""}{delta}ms</button>
        ))}
      </div>
      <small className="nudge-total">累计微调：{nudgeTotalMs > 0 ? "+" : ""}{nudgeTotalMs}ms</small>
    </>
  );
}
