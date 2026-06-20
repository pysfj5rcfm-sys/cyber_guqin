import type {
  ListeningReview,
  MarkerReviewStatus,
  PhraseDefinition,
  PhraseMarker,
  R2IssueType,
  RenderPhraseAlignment,
  Section,
  Severity,
} from "../types/cgVarw";

export type R2PreviewTable = {
  file: string;
  columns: string[];
  rows: Record<string, string>[];
};

export type R2ListeningReviewDraft = {
  phrase_id: string;
  version_id: string;
  issue_type: R2IssueType[];
  severity: Severity;
  quick_judgement?: "good" | "usable" | "needs_revision" | "bad";
  comment: string;
  suggested_revision: string;
  reviewer: string;
  reviewed_at: string;
  updated_at?: string;
};

type PreferredVersionByPhrase = Record<string, string>;
type ListeningReviewByKey = Record<string, R2ListeningReviewDraft>;

type BuildR2PreviewTablesInput = {
  sections: Section[];
  phrases: PhraseDefinition[];
  alignments: RenderPhraseAlignment[];
  markers: PhraseMarker[];
  review: ListeningReview;
  preferredVersionByPhrase?: PreferredVersionByPhrase;
  listeningReviewByKey?: ListeningReviewByKey;
  activePhraseId: string;
  activeVersionId: string;
  preferredVersionId?: string;
  boundaryStatus: MarkerReviewStatus;
};

const draftColumns = [
  "review_status",
  "gpt_review_pending",
  "e_revision_plan_generated",
  "e_generated",
  "experimental_render",
  "review_only",
  "production_grade",
];

const draftFlags = {
  review_status: "draft",
  gpt_review_pending: "true",
  e_revision_plan_generated: "false",
  e_generated: "false",
  experimental_render: "true",
  review_only: "true",
  production_grade: "false",
};

export function buildR2PreviewTables({
  sections,
  phrases,
  alignments,
  markers,
  review,
  preferredVersionByPhrase,
  listeningReviewByKey,
  activePhraseId,
  activeVersionId,
  preferredVersionId,
  boundaryStatus,
}: BuildR2PreviewTablesInput): Record<string, R2PreviewTable> {
  const activePhrase = phrases.find((phrase) => phrase.phrase_id === activePhraseId) ?? phrases[0];
  const activeSection = sections.find((section) => section.section_id === activePhrase?.section_id) ?? sections[0];
  const reviewDrafts = Object.values(listeningReviewByKey ?? {});
  const listeningRows = reviewDrafts.length > 0 ? reviewDrafts : [{
    phrase_id: activePhraseId,
    version_id: activeVersionId,
    issue_type: review.issue_type,
    severity: review.severity,
    quick_judgement: undefined,
    comment: review.comment,
    suggested_revision: review.suggested_revision ?? "",
    reviewer: review.reviewer,
    reviewed_at: review.reviewed_at,
    updated_at: review.reviewed_at,
  }];
  const listeningColumns = [
    "review_id",
    "render_set_id",
    "phrase_id",
    "section_id",
    "event_range",
    "active_version_id",
    "preferred_version_id",
    "quick_judgement",
    "issue_type",
    "severity",
    "comment",
    "suggested_revision",
    ...draftColumns,
  ];
  const listeningPreviewRows = listeningRows.map((item) => {
    const phrase = phraseFor(phrases, item.phrase_id, activePhrase);
    return {
      review_id: `R2_REVIEW_${item.phrase_id}_${item.version_id}`,
      render_set_id: review.render_set_id,
      phrase_id: item.phrase_id,
      section_id: phrase?.section_id ?? "",
      event_range: phrase?.event_range ?? "",
      active_version_id: item.version_id,
      preferred_version_id: preferredVersionByPhrase?.[item.phrase_id] ?? (item.phrase_id === activePhraseId ? preferredVersionId ?? "" : ""),
      quick_judgement: item.quick_judgement ?? "",
      issue_type: JSON.stringify(item.issue_type),
      severity: item.severity,
      comment: item.comment,
      suggested_revision: item.suggested_revision,
      ...draftFlags,
    };
  });

  return {
    "phrase_structure_review.yaml": buildPhraseStructureReviewYaml(sections, phrases, markers),
    "phrase_boundary_decision.csv": buildPhraseBoundaryDecisionCsv(alignments),
    "render_phrase_alignment.csv": buildRenderPhraseAlignmentCsv(alignments),
    "listening_review.csv": {
      file: "listening_review.csv",
      columns: listeningColumns,
      rows: listeningPreviewRows,
    },
    "listening_review.yaml": {
      file: "listening_review.yaml",
      columns: listeningColumns,
      rows: listeningPreviewRows,
    },
    "issue_list.csv": buildIssueListCsv(listeningRows, phrases, activePhrase),
    "render_revision_log.yaml": buildRenderRevisionLogYaml({
      renderSetId: review.render_set_id,
      phrases,
      activePhrase,
      listeningRows,
      preferredVersionByPhrase,
      activePhraseId,
      preferredVersionId,
    }),
    "preferred_version_summary.csv": buildPreferredVersionSummaryCsv({
      renderSetId: review.render_set_id,
      sections,
      phrases,
      activeSection,
      activePhraseId,
      activeVersionId,
      preferredVersionByPhrase,
    }),
  };
}

function buildPhraseStructureReviewYaml(
  sections: Section[],
  phrases: PhraseDefinition[],
  markers: PhraseMarker[],
): R2PreviewTable {
  return {
    file: "phrase_structure_review.yaml",
    columns: ["section_id", "section_label", "phrase_id", "phrase_label", "event_range", "marker_count", ...draftColumns],
    rows: phrases.map((phrase) => {
      const section = sections.find((item) => item.section_id === phrase.section_id);
      return {
        section_id: phrase.section_id,
        section_label: section?.section_label ?? "",
        phrase_id: phrase.phrase_id,
        phrase_label: phrase.phrase_label,
        event_range: phrase.event_range,
        marker_count: String(markers.filter((marker) => marker.phrase_id === phrase.phrase_id).length),
        ...draftFlags,
      };
    }),
  };
}

export function buildPhraseBoundaryDecisionCsv(alignments: RenderPhraseAlignment[]): R2PreviewTable {
  return {
    file: "phrase_boundary_decision.csv",
    columns: [
      "render_set_id",
      "version_id",
      "phrase_id",
      "section_id",
      "boundary_status",
      "phrase_start_s",
      "phrase_end_s",
      "phrase_play_start_s",
      "phrase_play_end_s",
      "phrase_tail_end_s",
      "next_phrase_first_attack_s",
      "phrase_end_policy",
      "breath_points_s",
      "cadence_point_s",
      ...draftColumns,
    ],
    rows: alignments.map((alignment) => ({
      render_set_id: alignment.render_set_id,
      version_id: alignment.version_id,
      phrase_id: alignment.phrase_id,
      section_id: alignment.section_id,
      boundary_status: alignment.review_status,
      phrase_start_s: seconds(alignment.start_s),
      phrase_end_s: seconds(alignment.end_s),
      phrase_play_start_s: seconds(alignment.phrase_play_start_s ?? alignment.start_s),
      phrase_play_end_s: seconds(alignment.phrase_play_end_s ?? alignment.end_s),
      phrase_tail_end_s: seconds(alignment.phrase_tail_end_s ?? alignment.end_s),
      next_phrase_first_attack_s: alignment.next_phrase_first_attack_s === undefined || alignment.next_phrase_first_attack_s === null ? "" : seconds(alignment.next_phrase_first_attack_s),
      phrase_end_policy: alignment.phrase_end_policy ?? "playback_safe_fallback",
      breath_points_s: alignment.breath_points_s.map(seconds).join(";"),
      cadence_point_s: alignment.cadence_point_s === undefined ? "" : seconds(alignment.cadence_point_s),
      ...draftFlags,
    })),
  };
}

export function buildRenderPhraseAlignmentCsv(alignments: RenderPhraseAlignment[]): R2PreviewTable {
  return {
    file: "render_phrase_alignment.csv",
    columns: [
      "render_set_id",
      "version_id",
      "phrase_id",
      "section_id",
      "event_range",
      "start_s",
      "end_s",
      "phrase_play_start_s",
      "phrase_play_end_s",
      "phrase_tail_end_s",
      "next_phrase_first_attack_s",
      "phrase_end_policy",
      "boundary_source",
      ...draftColumns,
    ],
    rows: alignments.map((alignment) => ({
      render_set_id: alignment.render_set_id,
      version_id: alignment.version_id,
      phrase_id: alignment.phrase_id,
      section_id: alignment.section_id,
      event_range: alignment.event_range,
      start_s: seconds(alignment.start_s),
      end_s: seconds(alignment.end_s),
      phrase_play_start_s: seconds(alignment.phrase_play_start_s ?? alignment.start_s),
      phrase_play_end_s: seconds(alignment.phrase_play_end_s ?? alignment.end_s),
      phrase_tail_end_s: seconds(alignment.phrase_tail_end_s ?? alignment.end_s),
      next_phrase_first_attack_s: alignment.next_phrase_first_attack_s === undefined || alignment.next_phrase_first_attack_s === null ? "" : seconds(alignment.next_phrase_first_attack_s),
      phrase_end_policy: alignment.phrase_end_policy ?? "playback_safe_fallback",
      boundary_source: alignment.boundary_source,
      ...draftFlags,
    })),
  };
}

function buildIssueListCsv(
  listeningRows: R2ListeningReviewDraft[],
  phrases: PhraseDefinition[],
  activePhrase?: PhraseDefinition,
): R2PreviewTable {
  return {
    file: "issue_list.csv",
    columns: ["review_id", "phrase_id", "version_id", "section_id", "issue_type", "severity", ...draftColumns],
    rows: listeningRows.flatMap((item) => item.issue_type.map((issue) => ({
      review_id: `R2_REVIEW_${item.phrase_id}_${item.version_id}`,
      phrase_id: item.phrase_id,
      version_id: item.version_id,
      section_id: phraseFor(phrases, item.phrase_id, activePhrase)?.section_id ?? "",
      issue_type: issue,
      severity: item.severity,
      ...draftFlags,
    }))),
  };
}

export function buildRenderRevisionLogYaml({
  renderSetId,
  phrases,
  activePhrase,
  listeningRows,
  preferredVersionByPhrase,
  activePhraseId,
  preferredVersionId,
}: {
  renderSetId: string;
  phrases: PhraseDefinition[];
  activePhrase?: PhraseDefinition;
  listeningRows: R2ListeningReviewDraft[];
  preferredVersionByPhrase?: PreferredVersionByPhrase;
  activePhraseId: string;
  preferredVersionId?: string;
}): R2PreviewTable {
  return {
    file: "render_revision_log.yaml",
    columns: ["revision_id", "render_set_id", "from_version_id", "to_version_id", "phrase_id", "section_id", "event_range", "change_type", "reason", ...draftColumns],
    rows: listeningRows
      .filter((item) => item.suggested_revision.trim().length > 0)
      .map((item) => {
        const phrase = phraseFor(phrases, item.phrase_id, activePhrase);
        return {
          revision_id: `R2_REVISION_${item.phrase_id}_${item.version_id}`,
          render_set_id: renderSetId,
          from_version_id: item.version_id,
          to_version_id: preferredVersionByPhrase?.[item.phrase_id] ?? (item.phrase_id === activePhraseId ? preferredVersionId ?? "" : ""),
          phrase_id: item.phrase_id,
          section_id: phrase?.section_id ?? "",
          event_range: phrase?.event_range ?? "",
          change_type: "other",
          reason: item.suggested_revision.trim(),
          ...draftFlags,
        };
      }),
  };
}

function buildPreferredVersionSummaryCsv({
  renderSetId,
  sections,
  phrases,
  activeSection,
  activePhraseId,
  activeVersionId,
  preferredVersionByPhrase,
}: {
  renderSetId: string;
  sections: Section[];
  phrases: PhraseDefinition[];
  activeSection?: Section;
  activePhraseId: string;
  activeVersionId: string;
  preferredVersionByPhrase?: PreferredVersionByPhrase;
}): R2PreviewTable {
  return {
    file: "preferred_version_summary.csv",
    columns: ["render_set_id", "phrase_id", "section_id", "section_label", "preferred_version_id", "active_version_id", ...draftColumns],
    rows: phrases.map((phrase) => {
      const section = sections.find((item) => item.section_id === phrase.section_id) ?? activeSection;
      return {
        render_set_id: renderSetId,
        phrase_id: phrase.phrase_id,
        section_id: phrase.section_id,
        section_label: section?.section_label ?? "",
        preferred_version_id: preferredVersionByPhrase?.[phrase.phrase_id] ?? "",
        active_version_id: phrase.phrase_id === activePhraseId ? activeVersionId : "",
        ...draftFlags,
      };
    }),
  };
}

function phraseFor(phrases: PhraseDefinition[], phraseId: string, fallback?: PhraseDefinition) {
  return phrases.find((candidate) => candidate.phrase_id === phraseId) ?? fallback;
}

function seconds(value: number) {
  return value.toFixed(3);
}
