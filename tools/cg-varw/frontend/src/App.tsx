import { useState } from "react";
import type { ReviewMode } from "./types/cgVarw";
import { R0RawReviewPage } from "./pages/R0RawReviewPage";
import { R1SplitReviewPage } from "./pages/R1SplitReviewPage";
import { R2ProjectReviewPage } from "./pages/R2ProjectReviewPage";

export default function App() {
  const [mode, setMode] = useState<ReviewMode>("R0");

  return (
    <>
      <nav className="mode-switcher" aria-label="review layer switcher">
        {(["R0", "R1", "R2"] as ReviewMode[]).map((item) => (
          <button key={item} className={mode === item ? "active" : ""} onClick={() => setMode(item)}>
            {item === "R0" ? "Raw review" : item === "R1" ? "Split review" : "Project review"}
          </button>
        ))}
      </nav>
      {mode === "R0" && <R0RawReviewPage />}
      {mode === "R1" && <R1SplitReviewPage />}
      {mode === "R2" && <R2ProjectReviewPage />}
    </>
  );
}
