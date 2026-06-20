type DraftRecord = Record<string, unknown>;

export type R2AdaptedProjectDraftState = {
  activePhraseId: string;
  activeVersionId: string;
  selectedMarkerId: string;
  boundaryStatusByKey: DraftRecord;
  listeningReviewByKey: DraftRecord;
  preferredVersionByPhrase: DraftRecord;
  markersByKey: DraftRecord;
  draftSource: "engineering_dir_latest" | "restored_from_exports";
  savedAt: string;
  path: string;
  e_generated: boolean;
  e_revision_plan_generated: boolean;
};

export function adaptR2ProjectDraftState(rawDraft: DraftRecord, context: {
  versions: { version_id: string }[];
  phrases: { phrase_id: string }[];
}): R2AdaptedProjectDraftState {
  const provenance = readRecord(rawDraft.provenance) ?? {};
  const listeningReviews = normalizeReviewDrafts(
    readRecord(rawDraft.listeningReviewByKey) ?? readRecord(rawDraft.listening_review_by_key) ?? {},
    context,
  );
  return {
    activePhraseId: phraseIdInList(readString(rawDraft.active_phrase_id) || readString(rawDraft.selected_phrase_id), context.phrases),
    activeVersionId: versionIdInList(readString(rawDraft.active_version_id) || readString(rawDraft.selected_version_id), context.versions),
    selectedMarkerId: readString(rawDraft.selected_marker_id),
    boundaryStatusByKey: normalizeKeyedRecord(readRecord(rawDraft.boundaryStatusByKey) ?? readRecord(rawDraft.boundary_status_by_key) ?? {}),
    listeningReviewByKey: listeningReviews,
    preferredVersionByPhrase: readRecord(rawDraft.preferredVersionByPhrase) ?? readRecord(rawDraft.preferred_version_by_phrase) ?? {},
    markersByKey: normalizeKeyedRecord(readRecord(rawDraft.markersByKey) ?? readRecord(rawDraft.markers_by_key) ?? {}),
    draftSource: provenance.restored_from_exports === true ? "restored_from_exports" : "engineering_dir_latest",
    savedAt: readString(rawDraft.saved_at) || readString(provenance.restored_at) || readString(provenance.saved_at),
    path: readString(rawDraft.path),
    e_generated: rawDraft.e_generated === true,
    e_revision_plan_generated: rawDraft.e_revision_plan_generated === true,
  };
}

function readString(value: unknown) {
  return typeof value === "string" ? value : "";
}

function readRecord(value: unknown) {
  return value && typeof value === "object" && !Array.isArray(value) ? value as DraftRecord : undefined;
}

function normalizeReviewDrafts(value: DraftRecord, context: { versions: { version_id: string }[]; phrases: { phrase_id: string }[] }) {
  const result: DraftRecord = {};
  Object.entries(value).forEach(([rawKey, rawReview]) => {
    const review = readRecord(rawReview);
    if (!review) return;
    const phraseId = phraseIdInList(readString(review.phrase_id) || phraseIdFromKey(rawKey), context.phrases);
    const versionId = versionIdInList(readString(review.version_id) || readString(review.active_version_id) || versionIdFromKey(rawKey), context.versions);
    if (!phraseId || !versionId) return;
    result[frontendPhraseVersionKey(phraseId, versionId)] = {
      ...review,
      phrase_id: phraseId,
      version_id: versionId,
      issue_type: normalizeIssueType(review.issue_type),
      severity: readString(review.severity) || "low",
      comment: readString(review.comment),
      suggested_revision: readString(review.suggested_revision),
      reviewer: readString(review.reviewer) || "human",
      reviewed_at: readString(review.reviewed_at),
      updated_at: readString(review.updated_at) || readString(review.reviewed_at),
    };
  });
  return result;
}

function normalizeKeyedRecord(value: DraftRecord) {
  const result: DraftRecord = {};
  Object.entries(value).forEach(([rawKey, item]) => {
    const phraseId = phraseIdFromKey(rawKey);
    const versionId = versionIdFromKey(rawKey);
    result[phraseId && versionId ? frontendPhraseVersionKey(phraseId, versionId) : rawKey] = item;
  });
  return result;
}

function phraseIdFromKey(value: string) {
  if (value.includes("::")) return value.split("::", 1)[0] ?? "";
  if (value.includes(":")) return value.split(":", 1)[0] ?? "";
  return "";
}

function versionIdFromKey(value: string) {
  if (value.includes("::")) return value.split("::")[1] ?? "";
  if (value.includes(":")) return value.split(":")[1] ?? "";
  return "";
}

function frontendPhraseVersionKey(phraseId: string, versionId: string) {
  return `${phraseId}::${versionId}`;
}

function normalizeIssueType(value: unknown) {
  if (Array.isArray(value)) return value.map((item) => String(item)).filter(Boolean);
  const text = readString(value).trim();
  if (!text || text === "[]") return [];
  try {
    const parsed = JSON.parse(text) as unknown;
    if (Array.isArray(parsed)) return parsed.map((item) => String(item)).filter(Boolean);
  } catch {
    // Fall back to delimiter parsing below.
  }
  return text.split(/[;,]/).map((item) => item.trim()).filter(Boolean);
}

function phraseIdInList(value: string, phrases: { phrase_id: string }[]) {
  return phrases.some((phrase) => phrase.phrase_id === value) ? value : phrases[0]?.phrase_id ?? "";
}

function versionIdInList(value: string, versions: { version_id: string }[]) {
  return versions.some((version) => version.version_id === value) ? value : versions[0]?.version_id ?? "";
}
