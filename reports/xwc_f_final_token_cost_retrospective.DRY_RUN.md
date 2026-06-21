# XWC F Final Token Cost Retrospective DRY RUN

- Scope: retrospective only. No render, no code edit, no report sync regeneration.
- Basis: task sheet constraints plus file-level inventory; no repository-wide content deep scan was performed.

## Why first F-final generation likely consumed high token

- F-final combined acceptance semantics, render inputs, validation evidence, and provenance reporting in one pass.
- Large audio/output trees forced repeated path verification and careful must_keep separation from historical variants.
- The task required preserving final artifacts while distinguishing old R2 exports, E variants, and F snapshots; that increased reasoning overhead even without reading binary contents.

## Why full_tail regeneration consumed high token

- Full-tail work touches phrase tails, split previews, render alignment, and final validation together.
- The file tree shows final F plus `full_tail_preview_refresh_manifest.csv`, `full_tail_refresh_audit.json`, and a before-fix F snapshot, which implies regeneration had to preserve both current accepted output and rollback evidence.
- Audio binaries were large and numerous, so verification had to rely on path/existence/metadata rather than content reads.

## R2 latest JSON vs exported CSV/YAML confusion

- The canonical current path is `r2_review_drafts/latest/r2_review_state.latest.json`, while many CSV/YAML exports exist beside it and in quarantine/archive paths.
- When exported CSV/YAML and latest JSON are treated as equivalent authority, verification has to prove which one is source of truth before any render or report claim.
- Future tasks should state whether `r2_review_state.latest.json` is canonical and treat exports as derived unless explicitly promoted.

## Report sync + render generation combined cost

- Combining report synchronization with render generation multiplies checks: audio output, alignment CSV, validation JSON, revision plan, and doc consistency all need independent proof.
- A safer split is: render/generate first, validate canonical outputs second, sync human report third, then run a narrow git/status audit.

## full_tail / safe_trim_smart_fade diagnosis cost

- Tail diagnosis is cross-cutting: it depends on split preview boundaries, render alignment, fade/trim behavior, and subjective playback acceptance.
- The inventory shows many split preview wavs and R1/R2 support files; path-level evidence alone cannot prove tail quality, so prior runs likely spent tokens triangulating from reports, manifests, and validation files.

## Future task constraints to reduce cost

- Use `canonical_authority` first: current handoff/instructions if present, canonical latest R2 state, final F output directory, and alignment/validation files.
- Keep `allowed_read_paths` narrow and explicitly forbid Downloads, restore zips, browser Blob downloads, raw-master binary reads, and old exports as source of truth.
- Run dry-run-first for cleanup/archive tasks; produce archive index before touching files.
- Split tasks into: inventory, user review, archive execution, validation, and retrospective/report sync.
- Keep R0 recovery separate until `LEGACY_R0_DRAFT_LOAD_NOT_VERIFIED` is explicitly opened; do not archive R0 drafts/exports by convenience.
