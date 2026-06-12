import type { ReviewMode } from "../types/cgVarw";

const modeLabels: Record<ReviewMode, string> = {
  R0: "R0 Raw 校验",
  R1: "R1 Split 审校",
  R2: "R2 句读听评",
};

export function TopBar({ mode }: { mode: ReviewMode }) {
  return (
    <header className="topbar">
      <div className="brand">
        <button className="icon-button" aria-label="菜单">☰</button>
        <strong>赛博古琴 · Visual Anchor Review Workbench</strong>
      </div>
      <div className="topbar-actions">
        <span className="badge badge-cyan">{modeLabels[mode]}</span>
        <span className="badge badge-blue">review_only=true</span>
        <span className="badge badge-gold">production_grade=false</span>
        <button className="window-button" aria-label="最小化">−</button>
        <button className="window-button" aria-label="最大化">□</button>
        <button className="window-button" aria-label="关闭">×</button>
      </div>
    </header>
  );
}
