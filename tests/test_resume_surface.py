#!/usr/bin/env python3
"""The resume surface (1.10): a resume's bullets are one sentence and full of
lists by convention, and resume guides spell contractions out, so V04, V01 and
R41 don't run there, and "contributed to" warns instead of blocking.

    python tests/test_resume_surface.py
"""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

CHECK = Path(__file__).resolve().parent.parent / "scripts" / "check_voice.py"


def check(text, surface):
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(text)
    r = subprocess.run([sys.executable, str(CHECK), "--surface", surface, f.name],
                       capture_output=True, text=True)
    return r.stdout


class ResumeSurface(unittest.TestCase):
    def test_one_sentence_bullets_dont_warn_v04(self):
        bullets = "\n\n".join(f"- Ran site {i} for 40 staff and cut dock time 12%." for i in range(10))
        self.assertNotIn("V04", check("# Experience\n\n" + bullets + "\n", "resume"))

    def test_long_forms_dont_warn_r41_on_a_resume(self):
        text = ("Ran the yard at 3 sites and did not add staff. Cut costs 12% at 3 sites, and there is "
                "room for 40 trucks. Built the plan, and it is the plan the county runs. Trained 14 "
                "leads, and they are running the yard. Wrote the scorecard, and it is still in use.\n")
        self.assertNotIn("R41", check(text, "resume"))
        self.assertIn("R41", check(text, "letter"))

    def test_contributed_to_warns_on_a_resume_and_blocks_on_a_letter(self):
        text = "Contributed to the county trails plan, adopted in 2023.\n"
        resume = check(text, "resume")
        self.assertIn("R12W", resume)
        self.assertNotIn("HARD FAIL", resume)
        self.assertIn("HARD FAIL", check(text, "letter"))


if __name__ == "__main__":
    unittest.main()
