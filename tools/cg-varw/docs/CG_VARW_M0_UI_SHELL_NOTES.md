# CG-VARW M0 UI Shell Notes

- R0 shows raw marker review for `slate_start`, `slate_end`, `guqin_start`, `tail_end`, and `next_slate_start`.
- R1 edits only split-level markers: `pre_idle_end`, `gesture_start`, `render_anchor`, and `tail_end`.
- R2 is phrase-aligned by `phrase_id`, `section_id`, and `event_range`; it does not switch A/B/C/D/E by one absolute timestamp.
- All data is mock data with `review_only=true` and `production_grade=false`.
- Export rows are visual placeholders and do not write files.
