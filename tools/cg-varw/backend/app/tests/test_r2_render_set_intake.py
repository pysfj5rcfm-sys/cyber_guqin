import unittest

from app.services import r2_mock_store as store


class R2RenderSetIntakeTests(unittest.TestCase):
    def test_loads_xwc_abcd_render_set_intake_when_present(self):
        render_sets = store.list_render_sets()

        self.assertEqual(["R2_XWC_BAIYA_ABCD_EXPERIMENTAL_354811e"], [item.render_set_id for item in render_sets])
        self.assertTrue(render_sets[0].review_only)
        self.assertFalse(render_sets[0].production_grade)

        versions = store.list_versions("R2_XWC_BAIYA_ABCD_EXPERIMENTAL_354811e")
        self.assertEqual(
            ["A_LITERAL", "B_PHRASE", "C_QINIST_STYLE", "D_TEACHING_DIAGNOSTIC"],
            [item.version_id for item in versions],
        )
        self.assertNotIn("E_REVIEWED", [item.version_id for item in versions])
        self.assertTrue(all(not item.mock_render for item in versions))
        self.assertTrue(all(item.audio_path.endswith(".wav") for item in versions))

        alignments = store.list_alignments("R2_XWC_BAIYA_ABCD_EXPERIMENTAL_354811e")
        self.assertEqual(40, len(alignments))
        p09_c = next(item for item in alignments if item.phrase_id == "XWC_P09_LOCAL_PHRASE" and item.version_id == "C_QINIST_STYLE")
        self.assertEqual("imported", p09_c.boundary_source)
        self.assertEqual("candidate", p09_c.review_status)
        self.assertGreater(p09_c.end_s, p09_c.start_s)

    def test_resolves_real_r2_version_audio_path(self):
        audio_path = store.resolve_version_audio_path("R2_XWC_BAIYA_ABCD_EXPERIMENTAL_354811e", "A_LITERAL")

        self.assertTrue(audio_path.exists())
        self.assertEqual("XWC_BAIYA_A_LITERAL.wav", audio_path.name)


if __name__ == "__main__":
    unittest.main()
