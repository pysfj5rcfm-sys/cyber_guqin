import assert from "node:assert/strict";
import { mkdtemp, readFile, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import ts from "typescript";

const pagePath = new URL("../src/pages/R2ProjectReviewPage.tsx", import.meta.url);
const panelPath = new URL("../src/components/R2ExportPreviewPanel.tsx", import.meta.url);
const adapterPath = new URL("../src/utils/r2ReviewDraftState.ts", import.meta.url);
const latestPath = new URL("../../../../04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/latest/r2_review_state.latest.json", import.meta.url);

const pageSource = await readFile(pagePath, "utf8");
const panelSource = await readFile(panelPath, "utf8");

const forbiddenBrowserSuccess = "draft 已保存" + "到浏览器";
assert.equal(pageSource.includes(forbiddenBrowserSuccess), false, "browser-only save must not be phrased as draft save success");
assert.ok(pageSource.includes("saveR2ReviewDraftToProject"), "R2 page must call project-directory save API");
assert.ok(pageSource.includes("saveDraft={saveProjectDraft}"), "right-panel default save must use project-directory save");
assert.ok(panelSource.includes("临时保存到浏览器"), "browser fallback button must be explicitly temporary");
assert.ok(panelSource.includes("保存草稿到工程目录"), "project-directory save action must be visible");

const source = await readFile(adapterPath, "utf8");
const compiled = ts.transpileModule(source, {
  compilerOptions: {
    target: ts.ScriptTarget.ES2022,
    module: ts.ModuleKind.ES2022,
    moduleResolution: ts.ModuleResolutionKind.Bundler,
    importsNotUsedAsValues: ts.ImportsNotUsedAsValues.Remove,
  },
  fileName: "r2ReviewDraftState.ts",
}).outputText;
const tempDir = await mkdtemp(join(tmpdir(), "r2-review-draft-state-"));
const tempModule = join(tempDir, "r2ReviewDraftState.mjs");
await writeFile(tempModule, compiled, "utf8");
const { adaptR2ProjectDraftState } = await import(`file://${tempModule}`);
const latest = JSON.parse(await readFile(latestPath, "utf8"));
const adapted = adaptR2ProjectDraftState(latest, {
  versions: [
    { version_id: "A_LITERAL" },
    { version_id: "B_PHRASE" },
    { version_id: "C_QINIST_STYLE" },
    { version_id: "D_TEACHING_DIAGNOSTIC" },
  ],
  phrases: Array.from({ length: 10 }, (_, index) => ({ phrase_id: `XWC_P${String(index + 1).padStart(2, "0")}_LOCAL_PHRASE` })),
});

assert.equal(Object.keys(adapted.listeningReviewByKey).length, 28, "latest draft adapter should restore 28 reviews");
assert.equal(Object.keys(adapted.preferredVersionByPhrase).length, 10, "latest draft adapter should restore 10 preferred versions");
assert.equal(adapted.draftSource, "restored_from_exports", "latest draft should preserve restored_from_exports source");
assert.equal(adapted.e_generated, false, "adapter must keep E disabled");
assert.equal(adapted.e_revision_plan_generated, false, "adapter must not generate e revision plan");

console.log("R2 persistence UI verification passed");
