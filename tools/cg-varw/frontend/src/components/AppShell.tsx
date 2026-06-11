import type { ReactNode } from "react";
import type { ReviewMode } from "../types/cgVarw";
import { TopBar } from "./TopBar";

type Slots = {
  left: ReactNode;
  main: ReactNode;
  right: ReactNode;
  bottom: ReactNode;
};

export function AppShell({
  mode,
  left,
  main,
  right,
  bottom,
  children,
  statusText = "就绪",
  detailText = "review_only=true · production_grade=false",
}: {
  mode: ReviewMode;
  left?: ReactNode;
  main?: ReactNode;
  right?: ReactNode;
  bottom?: ReactNode;
  children?: Slots;
  statusText?: string;
  detailText?: string;
}) {
  const slots = children ?? { left, main, right, bottom };

  return (
    <div className="app-shell">
      <TopBar mode={mode} />
      <div className="workspace-grid">
        <aside className="side-panel left-panel">{slots.left}</aside>
        <main className="main-panel">{slots.main}</main>
        <aside className="side-panel right-panel">{slots.right}</aside>
        <section className="bottom-panel">{slots.bottom}</section>
      </div>
      <footer className="statusbar">
        <span><i className="status-dot" /> {statusText}</span>
        <span>{detailText}</span>
      </footer>
    </div>
  );
}
