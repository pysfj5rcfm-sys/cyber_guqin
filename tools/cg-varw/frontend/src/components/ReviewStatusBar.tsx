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
      <button className="play-button">▶<span>播放/暂停</span></button>
      <button>{backLabel}</button>
      <button>循环试听</button>
      {sequenceLabel && <button>{sequenceLabel}</button>}
      <strong className="clock">{time}<small>/ {total}</small></strong>
      <span className="speed-label">播放速度</span>
      <button>0.5x</button>
      <button className="active">1x</button>
      <button>1.5x</button>
    </div>
  );
}
