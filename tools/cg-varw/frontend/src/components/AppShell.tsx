import type { ReactNode } from "react";
import type { ReviewMode } from "../types/cgVarw";
import { TopBar } from "./TopBar";

export function AppShell({
  mode,
  left,
  main,
  right,
  bottom,
}: {
  mode: ReviewMode;
  left: ReactNode;
  main: ReactNode;
  right: ReactNode;
  bottom: ReactNode;
}) {
  return (
    <div className="app-shell">
      <TopBar mode={mode} />
      <div className="workspace-grid">
        <aside className="side-panel left-panel">{left}</aside>
        <main className="main-panel">{main}</main>
        <aside className="side-panel right-panel">{right}</aside>
        <section className="bottom-panel">{bottom}</section>
      </div>
      <footer className="statusbar">
        <span><i className="status-dot" /> 就绪</span>
        <span>mock only · not written</span>
      </footer>
    </div>
  );
}
