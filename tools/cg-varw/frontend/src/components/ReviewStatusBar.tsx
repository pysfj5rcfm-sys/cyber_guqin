export function PlaybackBar({
  time,
  total,
  backLabel,
  sequenceLabel,
  isPlaying = false,
  playbackRate = 1,
  loopAuditionEnabled = false,
  onPlayPause,
  onBack,
  onToggleLoop,
  onRateChange,
}: {
  time: string;
  total: string;
  backLabel: string;
  sequenceLabel?: string;
  isPlaying?: boolean;
  playbackRate?: number;
  loopAuditionEnabled?: boolean;
  onPlayPause?: () => void;
  onBack?: () => void;
  onToggleLoop?: () => void;
  onRateChange?: (rate: number) => void;
}) {
  return (
    <div className="playback-bar">
      <button className="play-button" onClick={onPlayPause}>{isPlaying ? "暂停" : "播放"}<span>{isPlaying ? "播放" : "暂停"}</span></button>
      <button onClick={onBack}>{backLabel}</button>
      <button className={loopAuditionEnabled ? "active" : ""} onClick={onToggleLoop}>循环试听</button>
      {sequenceLabel && <button>{sequenceLabel}</button>}
      <strong className="clock">{time}<small>/ {total}</small></strong>
      <span className="speed-label">播放速度</span>
      {[0.5, 1, 1.5].map((rate) => (
        <button key={rate} className={playbackRate === rate ? "active" : ""} onClick={() => onRateChange?.(rate)}>
          {rate}x
        </button>
      ))}
    </div>
  );
}
