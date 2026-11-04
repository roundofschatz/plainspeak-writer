"""Tests for the career-writing rules added in 1.10: "supported" as a career
verb (R12), the timing brag that ends in "existed" (R21), naming what the
writer lacks (R49) and a claim hung on leaving a job (R50).

Each rule gets sentences that should trip it and near-misses that shouldn't.
Run from the repository root:

    python3 tests/test_career_rules.py

Standard library only, like the checker.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import check_voice as cv  # noqa: E402

RULES = cv.HARD + cv.WARN


def ids(text, surface):
    """The rule IDs that fire on this text, on this surface."""
    return {label.split(" ", 1)[0] for _ln, label, _hit, _note in cv.scan(text, RULES, surface)}


class RuleCase(unittest.TestCase):
    rule = None
    surface = "resume"
    hits = ()
    misses = ()      # (text, surface) pairs

    def test_hits(self):
        for text in self.hits:
            with self.subTest(text=text):
                self.assertIn(self.rule, ids(text, self.surface), f"{self.rule} should fire")

    def test_misses(self):
        for text, surface in self.misses:
            with self.subTest(text=text, surface=surface):
                self.assertNotIn(self.rule, ids(text, surface), f"{self.rule} should not fire")


class SupportedAsCareerVerb(RuleCase):
    """1: "Supported" reads as helping, not doing (R12)."""
    rule = "R12"
    surface = "resume"
    hits = (
        "Supported the brand team on three launches.",
        "- Supported the CMO through a rebrand of 40 stores.",
        "I supported the sales team during the Q3 push.",
        "Led the audit. Supported two product launches in 2024.",
        "I also supported the regional managers on hiring.",
        "* Supported launch planning for the Denver office.",
    )
    misses = (
        ("The program supported 40 schools in its first year.", "resume"),
        ("Supported by a $2M grant, the pilot reached 900 homes.", "resume"),
        ("The grant supported three new clinics.", "letter"),
        ("Our team supported the rollout in Ohio.", "letter"),
        ("The data supported the decision to close the site.", "linkedin"),
        ("Supported the brand team on three launches.", "general"),
    )


class TimingBragExisted(RuleCase):
    """2: the timing brag that ends in "existed" (R21)."""
    rule = "R21"
    surface = "letter"
    hits = (
        "I built this before AI tools existed.",
        "I was mapping guest journeys before the term existed.",
        "We ran remote workshops before the category even existed.",
        "Built a booking model before the platform existed.",
        "My team shipped the first version before the market existed.",
    )
    misses = (
        ("The tool existed before I joined.", "letter"),
        ("Before I joined, the tool existed only on paper.", "letter"),
        ("Records from before the county existed are kept in Ohio.", "general"),
        ("The trail existed before the park did.", "general"),
        ("Nobody knew the backlog existed before the audit.", "letter"),
    )


class NamingWhatYouLack(RuleCase):
    """3: the writer naming what they lack (R49)."""
    rule = "R49"
    surface = "letter"
    hits = (
        "I haven't led a team that size.",
        "I'd have to learn Salesforce.",
        "No formal experience in healthcare, but I learn fast.",
        "I have never managed a budget over $1M.",
        "I lack a CPA, but I've run the books for six years.",
        "On paper, I'm not the obvious fit for this role.",
        "I don't have direct experience in public health.",
        "I could learn your CRM in two weeks.",
        "I don't come from the software world.",
    )
    misses = (
        ("I haven't seen a cleaner model.", "linkedin"),
        ("I haven't seen this before.", "general"),
        ("The workshop needs no prior experience.", "letter"),
        ("We moved every permit from paper to a shared drive.", "letter"),
        ("The teams need to learn the new code by May.", "general"),
        ("I learned Salesforce in two weeks at Acme.", "letter"),
        ("No prior experience is needed to join the group.", "blurb"),
    )


class ClaimHungOnLeaving(RuleCase):
    """4: a claim hung on leaving a job (R50)."""
    rule = "R50"
    surface = "letter"
    hits = (
        "After I left, the system kept running.",
        "The model is still in use two years after I left.",
        "After my departure, the team kept using the playbook.",
        "Three clients stayed on since I left.",
        "The program ran for three more years after I moved on.",
    )
    misses = (
        ("Acme, Brand Manager, 2021 to 2025. Left the firm in 2025.", "resume"),
        ("Since I left Acme, I've run my own practice.", "letter"),
        ("After I left the meeting, I wrote the brief that night.", "letter"),
        ("The pilot kept running after the grant ended.", "letter"),
        ("After I left, the system kept running.", "general"),
    )


class RulesListedEverywhere(unittest.TestCase):
    """Every rule the checker runs is written out in full-check.md."""

    def test_full_check_lists_new_rules(self):
        here = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(here, "..", "references", "full-check.md"), encoding="utf-8") as fh:
            text = fh.read()
        for rid in ("R49", "R50"):
            with self.subTest(rule=rid):
                self.assertIn(f"- {rid} (", text)


if __name__ == "__main__":
    unittest.main(verbosity=1)
