import type { PhraseDefinition, RenderPhraseAlignment, RenderSet, RenderVersion, Section } from "../types/cgVarw";

export const apiBase = import.meta.env.VITE_CG_VARW_API_BASE ?? "http://127.0.0.1:8788";

type R2RenderSetsResponse = {
  render_sets: RenderSet[];
};

type R2VersionsResponse = {
  versions: RenderVersion[];
};

type R2PhrasesResponse = {
  sections: Section[];
  phrases: PhraseDefinition[];
};

type R2AlignmentsResponse = {
  phrase_alignments: RenderPhraseAlignment[];
};

async function getJson<T>(path: string): Promise<T> {
  const response = await fetch(`${apiBase}${path}`);
  if (!response.ok) throw new Error(`${response.status} ${response.statusText}`);
  return response.json() as Promise<T>;
}

export async function loadR2RenderSets() {
  const data = await getJson<R2RenderSetsResponse>("/api/r2/render-sets");
  return data.render_sets;
}

export async function loadR2Versions(renderSetId: string) {
  const data = await getJson<R2VersionsResponse>(`/api/r2/render-sets/${encodeURIComponent(renderSetId)}/versions`);
  return data.versions.map((version) => ({
    ...version,
    audio_url: version.mock_render ? undefined : r2VersionAudioUrl(renderSetId, version.version_id),
  }));
}

export async function loadR2Phrases(renderSetId: string) {
  return getJson<R2PhrasesResponse>(`/api/r2/render-sets/${encodeURIComponent(renderSetId)}/phrases`);
}

export async function loadR2PhraseAlignments(renderSetId: string) {
  const data = await getJson<R2AlignmentsResponse>(`/api/r2/render-sets/${encodeURIComponent(renderSetId)}/phrase-alignments`);
  return data.phrase_alignments;
}

export function r2VersionAudioUrl(renderSetId: string, versionId: string) {
  return `${apiBase}/api/r2/render-sets/${encodeURIComponent(renderSetId)}/versions/${encodeURIComponent(versionId)}/audio`;
}
