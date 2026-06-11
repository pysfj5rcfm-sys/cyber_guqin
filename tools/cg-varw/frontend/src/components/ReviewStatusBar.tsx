export function PlaybackBar({
  time,
  total,
  backLabel,
  sequenceLabel,
}: {
  time: string;
  total: string;
  backLabel: string;
  sequenceLabel?: string;
}) {
  return (
    <div className="playback-bar">
      <button className="play-button">Play<span>Pause</span></button>
      <button>{backLabel}</button>
      <button>Loop audition</button>
      {sequenceLabel && <button>{sequenceLabel}</button>}
      <strong className="clock">{time}<small>/ {total}</small></strong>
      <span className="speed-label">Speed</span>
      <button>0.5x</button>
      <button className="active">1x</button>
      <button>1.5x</button>
    </div>
  );
}
