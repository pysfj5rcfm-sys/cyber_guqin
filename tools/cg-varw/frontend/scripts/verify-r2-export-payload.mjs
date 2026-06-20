import assert from "node:assert/strict";
import { mkdtemp, readFile, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import ts from "typescript";

const modulePath = new URL("../src/utils/r2ExportPayload.ts", import.meta.url);
const source = await readFile(modulePath, "utf8");
const compiled = ts.transpileModule(source, {
  compilerOptions: {
    target: ts.ScriptTarget.ES2022,
    module: ts.ModuleKind.ES2022,
    moduleResolution: ts.ModuleResolutionKind.Bundler,
    importsNotUsedAsValues: ts.ImportsNotUsedAsValues.Remove,
  },
  fileName: "r2ExportPayload.ts",
}).outputText;
const tempDir = await mkdtemp(join(tmpdir(), "r2-export-payload-"));
const tempModule = join(tempDir, "r2ExportPayload.mjs");
await writeFile(tempModule, compiled, "utf8");

const { buildR2PreviewTables } = await import(`file://${tempModule}`);

const versions = ["A_LITERAL", "B_PHRASE", "C_QINIST_STYLE", "D_TEACHING_DIAGNOSTIC"];
const phrases = Array.from({ length: 10 }, (_, index) => {
  const order = index + 1;
  return {
    phrase_id: `XWC_PHRASE_${String(order).padStart(2, "0")}`,
    section_id: order <= 5 ? "XWC_SEC_01" : "XWC_SEC_02",
    phrase_label: `第${order}句`,
    phrase_role: "score_phrase",
    event_range: `XWC_P${String(order).padStart(2, "0")}_N01_to_N04`,
    start_event_id: `EVT_${order}_001`,
    end_event_id: `EVT_${order}_004`,
    phrase_order: order,
  };
});
const sections = [
  { section_id: "XWC_SEC_01", section_label: "上段", section_order: 1, phrase_count: 5 },
  { section_id: "XWC_SEC_02", section_label: "下段", section_order: 2, phrase_count: 5 },
];
const alignments = phrases.flatMap((phrase, phraseIndex) => versions.map((versionId, versionIndex) => {
  const start = phraseIndex * 5 + versionIndex * 0.05;
  const nextAttack = phraseIndex < phrases.length - 1 ? (phraseIndex + 1) * 5 + versionIndex * 0.05 : undefined;
  return {
    render_set_id: "R2_TEST_RENDER_SET",
    version_id: versionId,
    phrase_id: phrase.phrase_id,
    section_id: phrase.section_id,
    event_range: phrase.event_range,
    start_s: start,
    end_s: start + 4.8,
    phrase_play_start_s: start + 0.02,
    phrase_play_end_s: nextAttack ? nextAttack - 0.03 : start + 4.75,
    phrase_tail_end_s: start + 4.8,
    next_phrase_first_attack_s: nextAttack,
    phrase_end_policy: nextAttack ? "next_phrase_first_attack_minus_epsilon" : "last_phrase_safe_tail",
    breath_points_s: [start + 1.2, start + 2.5],
    cadence_point_s: start + 4.5,
    boundary_source: "score_phrase_lock",
    boundary_confidence: "provisional",
    review_status: "candidate",
  };
}));

const listeningReviewByKey = Object.fromEntries([
  ...phrases.map((phrase, index) => [`${phrase.phrase_id}:B_PHRASE`, {
    phrase_id: phrase.phrase_id,
    version_id: "B_PHRASE",
    issue_type: index % 2 === 0 ? ["wrong_breath"] : [],
    severity: "medium",
    quick_judgement: "needs_revision",
    comment: `第${index + 1}句听评`,
    suggested_revision: `第${index + 1}句修订建议`,
    reviewer: "human",
    reviewed_at: "2026-06-20T00:00:00.000Z",
  }]),
  ["COMMENT_ONLY:A_LITERAL", {
    phrase_id: phrases[0].phrase_id,
    version_id: "A_LITERAL",
    issue_type: [],
    severity: "low",
    comment: "只有评论，没有修订建议",
    suggested_revision: "",
    reviewer: "human",
    reviewed_at: "2026-06-20T00:00:00.000Z",
  }],
]);

const tables = buildR2PreviewTables({
  sections,
  phrases,
  alignments,
  markers: [],
  review: {
    review_id: "R2_REVIEW_ACTIVE",
    render_set_id: "R2_TEST_RENDER_SET",
    phrase_id: phrases[0].phrase_id,
    section_id: phrases[0].section_id,
    event_range: phrases[0].event_range,
    active_version_id: "B_PHRASE",
    preferred_version_id: "B_PHRASE",
    quick_judgement: "needs_revision",
    issue_type: ["wrong_breath"],
    severity: "medium",
    comment: "active review",
    suggested_revision: "active revision",
    reviewer: "human",
    reviewed_at: "2026-06-20T00:00:00.000Z",
    review_only: true,
    production_grade: false,
  },
  preferredVersionByPhrase: Object.fromEntries(phrases.map((phrase) => [phrase.phrase_id, "B_PHRASE"])),
  listeningReviewByKey,
  activePhraseId: phrases[0].phrase_id,
  activeVersionId: "B_PHRASE",
  preferredVersionId: "B_PHRASE",
  boundaryStatus: "candidate",
});

assert.equal(tables["render_phrase_alignment.csv"].rows.length, 40, "render_phrase_alignment.csv should include full score phrases x ABCD");
assert.equal(tables["phrase_boundary_decision.csv"].rows.length, 40, "phrase_boundary_decision.csv should include full score phrases x ABCD");
assert.equal(tables["render_revision_log.yaml"].rows.length, 10, "render_revision_log.yaml should include every non-empty suggested_revision only");
assert.equal(tables["render_revision_log.yaml"].rows.some((row) => row.reason === "只有评论，没有修订建议"), false, "comment-only reviews must not become revision rows");
assert.equal(tables["preferred_version_summary.csv"].rows.length, 10, "preferred_version_summary.csv should still cover all phrases");
assert.equal(tables["phrase_structure_review.yaml"].rows.length, 10, "phrase_structure_review.yaml should still cover all phrases");

for (const [file, table] of Object.entries(tables)) {
  for (const flag of ["gpt_review_pending", "e_revision_plan_generated", "e_generated", "experimental_render", "production_grade"]) {
    assert.ok(table.columns.includes(flag), `${file} should keep ${flag}`);
  }
  const csv = toCsv(table);
  const csvRows = parseCsv(csv);
  assert.equal(csvRows.length, table.rows.length + 1, `${file} CSV text should parse back to header + rows`);
  const yaml = toYaml(table);
  assert.equal((yaml.match(/^  -$/gm) ?? []).length, table.rows.length, `${file} YAML text should expose each row`);
}

console.log("R2 export payload verification passed");

function toCsv(table) {
  return `${[table.columns.join(","), ...table.rows.map((row) => table.columns.map((column) => csvCell(row[column] ?? "")).join(","))].join("\n")}\n`;
}

function csvCell(value) {
  const text = String(value);
  if (!/[",\n]/.test(text)) return text;
  return `"${text.replace(/"/g, '""')}"`;
}

function parseCsv(text) {
  const rows = [];
  let row = [];
  let cell = "";
  let quoted = false;
  for (let index = 0; index < text.length; index += 1) {
    const char = text[index];
    if (quoted) {
      if (char === '"' && text[index + 1] === '"') {
        cell += '"';
        index += 1;
      } else if (char === '"') {
        quoted = false;
      } else {
        cell += char;
      }
    } else if (char === '"') {
      quoted = true;
    } else if (char === ",") {
      row.push(cell);
      cell = "";
    } else if (char === "\n") {
      row.push(cell);
      if (row.length > 1 || row[0] !== "") rows.push(row);
      row = [];
      cell = "";
    } else {
      cell += char;
    }
  }
  return rows;
}

function toYaml(table) {
  const lines = [`file: ${JSON.stringify(table.file)}`, "rows:"];
  for (const row of table.rows) {
    lines.push("  -");
    for (const column of table.columns) lines.push(`      ${column}: ${JSON.stringify(row[column] ?? "")}`);
  }
  return `${lines.join("\n")}\n`;
}
