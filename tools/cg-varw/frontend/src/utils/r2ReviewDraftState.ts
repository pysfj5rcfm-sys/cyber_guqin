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
  return {
    activePhraseId: phraseIdInList(readString(rawDraft.active_phrase_id) || readString(rawDraft.selected_phrase_id), context.phrases),
    activeVersionId: versionIdInList(readString(rawDraft.active_version_id) || readString(rawDraft.selected_version_id), context.versions),
    selectedMarkerId: readString(rawDraft.selected_marker_id),
    boundaryStatusByKey: readRecord(rawDraft.boundaryStatusByKey) ?? readRecord(rawDraft.boundary_status_by_key) ?? {},
    listeningReviewByKey: readRecord(rawDraft.listeningReviewByKey) ?? readRecord(rawDraft.listening_review_by_key) ?? {},
    preferredVersionByPhrase: readRecord(rawDraft.preferredVersionByPhrase) ?? readRecord(rawDraft.preferred_version_by_phrase) ?? {},
    markersByKey: readRecord(rawDraft.markersByKey) ?? readRecord(rawDraft.markers_by_key) ?? {},
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

function phraseIdInList(value: string, phrases: { phrase_id: string }[]) {
  return phrases.some((phrase) => phrase.phrase_id === value) ? value : phrases[0]?.phrase_id ?? "";
}

function versionIdInList(value: string, versions: { version_id: string }[]) {
  return versions.some((version) => version.version_id === value) ? value : versions[0]?.version_id ?? "";
}
