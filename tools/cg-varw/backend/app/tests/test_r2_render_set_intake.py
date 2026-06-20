import unittest
from os import environ
from pathlib import Path
from unittest.mock import patch

from app.services import r2_mock_store as store


REPO_ROOT = Path(__file__).resolve().parents[5]
R2_RENDER_ROOT = REPO_ROOT / "04_outputs" / "XWC" / "RS_XWC_002_BAIYA_PILOT" / "abcd_experimental_render"
R2_INTAKE_ROOT = R2_RENDER_ROOT / "r2_review_intake"


class R2RenderSetIntakeTests(unittest.TestCase):
    def test_loads_xwc_abcd_render_set_intake_when_present(self):
        with patch.dict(environ, {"CG_VARW_R2_RENDER_ROOT": str(R2_RENDER_ROOT), "CG_VARW_R2_INTAKE_ROOT": str(R2_INTAKE_ROOT)}):
            render_sets = store.list_render_sets()

            self.assertEqual(["R2_XWC_BAIYA_ABCD_EXPERIMENTAL_354811e"], [item.render_set_id for item in render_sets])
            self.assertTrue(render_sets[0].review_only)
            self.assertFalse(render_sets[0].production_grade)

            versions = store.list_versions(render_sets[0].render_set_id)
            self.assertEqual(
                ["A_LITERAL", "B_PHRASE", "C_QINIST_STYLE", "D_TEACHING_DIAGNOSTIC", "E_REVIEWED", "F_FINAL_REVIEWED"],
                [item.version_id for item in versions],
            )
            e_version = next(item for item in versions if item.version_id == "E_REVIEWED")
            f_version = next(item for item in versions if item.version_id == "F_FINAL_REVIEWED")
            self.assertFalse(e_version.mock_render)
            self.assertTrue(e_version.playable)
            self.assertEqual("review_ready", e_version.status)
            self.assertTrue(e_version.alignment_available)
            self.assertTrue(e_version.audio_path.endswith("XWC_BAIYA_E_REVIEWED.wav"))
            self.assertTrue(f_version.playable)
            self.assertEqual("final_ready", f_version.status)
            self.assertTrue(f_version.audio_path.endswith("XWC_BAIYA_F_FINAL_REVIEWED.wav"))
            self.assertTrue(f_version.alignment_available)
            self.assertFalse(f_version.generation_allowed)
            self.assertEqual("f_final_reviewed_generation", f_version.source)
            self.assertTrue(all(not item.mock_render for item in versions))
            self.assertTrue(all(item.audio_path.endswith(".wav") for item in versions if item.playable))

            alignments = store.list_alignments(render_sets[0].render_set_id)
            self.assertEqual(60, len(alignments))
            self.assertEqual(10, len([item for item in alignments if item.version_id == "E_REVIEWED"]))
            self.assertEqual(10, len([item for item in alignments if item.version_id == "F_FINAL_REVIEWED"]))
            p09_c = next(item for item in alignments if item.phrase_id == "XWC_P09_LOCAL_PHRASE" and item.version_id == "C_QINIST_STYLE")
            self.assertEqual("imported", p09_c.boundary_source)
            self.assertEqual("candidate", p09_c.review_status)
            self.assertGreater(p09_c.end_s, p09_c.start_s)

    def test_resolves_real_r2_version_audio_path(self):
        with patch.dict(environ, {"CG_VARW_R2_RENDER_ROOT": str(R2_RENDER_ROOT), "CG_VARW_R2_INTAKE_ROOT": str(R2_INTAKE_ROOT)}):
            self.assertEqual(R2_INTAKE_ROOT, store.get_r2_intake_root())
            self.assertEqual(R2_RENDER_ROOT, store.get_r2_render_root())
            audio_path = store.resolve_version_audio_path("R2_XWC_BAIYA_ABCD_EXPERIMENTAL_354811e", "A_LITERAL")
            e_audio_path = store.resolve_version_audio_path("R2_XWC_BAIYA_ABCD_EXPERIMENTAL_354811e", "E_REVIEWED")
            f_audio_path = store.resolve_version_audio_path("R2_XWC_BAIYA_ABCD_EXPERIMENTAL_354811e", "F_FINAL_REVIEWED")

        self.assertTrue(audio_path.exists())
        self.assertEqual("XWC_BAIYA_A_LITERAL.wav", audio_path.name)
        self.assertTrue(e_audio_path.exists())
        self.assertEqual("XWC_BAIYA_E_REVIEWED.wav", e_audio_path.name)
        self.assertTrue(f_audio_path.exists())
        self.assertEqual("XWC_BAIYA_F_FINAL_REVIEWED.wav", f_audio_path.name)

    def test_prefers_playback_safe_phrase_alignment_seed(self):
        with patch.dict(environ, {"CG_VARW_R2_RENDER_ROOT": str(R2_RENDER_ROOT), "CG_VARW_R2_INTAKE_ROOT": str(R2_INTAKE_ROOT)}):
            self.assertEqual(R2_INTAKE_ROOT / "r2_phrase_alignment_seed.playback_safe.csv", store.get_r2_alignment_seed_path())
            alignments = store.list_alignments("R2_XWC_BAIYA_ABCD_EXPERIMENTAL_354811e")

        self.assertEqual(60, len(alignments))
        non_final = [item for item in alignments if item.next_phrase_first_attack_s is not None]
        self.assertEqual(54, len(non_final))
        self.assertTrue(all(item.phrase_play_end_s <= item.next_phrase_first_attack_s for item in non_final))
        self.assertTrue(all(item.phrase_tail_end_s >= item.phrase_play_end_s for item in non_final))


if __name__ == "__main__":
    unittest.main()
