# Changelog

Every change to this skill is logged here: what was added, changed or removed, and why. Nothing comes out without a line saying so. Newest first.

## 1.3.1 · Public repository
- Changed: the clone command in the README now points at `github.com/roundofschatz/plainspeak-writer` instead of a placeholder owner.
- Changed: two lines in SKILL.md that called the user "him" and "he" now say "the user", since the skill is for anyone.
- Changed: the copyright line in LICENSE now names "The Plainspeak Writer contributors", to match the 1.3 rename.

## 1.3 · Renamed to Plainspeak Writer
- Renamed: the skill from `writer` to `plainspeak-writer`, in the folder, the `name` field, the titles, the checker and the README. The folder and the `name` field must match.
- Moved: the README and the MIT license into the skill folder, so every copy includes its documentation and its license notice, which MIT requires. The repository and the skill are now one folder.
- Added: `license: MIT` to the SKILL.md frontmatter.

## 1.2 · Hanging phrases
- Added back as a general rule: R42 blocks the hanging phrases "gave/give the hours/time back", "the work that wins" and "what wins". It's in `scripts/check_voice.py` and in the full check in tells.md, alongside the hanging-reference row in the tells table.
- Left out on purpose: rules about leaving a job, firm ownership, naming gaps, one writer's method names and system vocabulary, one letter header, one resume lead-in and two retired lines. They fit one writer's career documents, not a general writing tool. The letter guide still advises against naming gaps in a letter, as guidance rather than a pattern rule.

## 1.1 · Five tells back in as general rules
- Added back as general rules, because each one is common AI phrasing for any writer: R11 ("authored" and "architected" as verbs), R28 ("at once" as filler), R30 ("the more X, the more Y"), R39 ("carry" as a verb for an abstraction) and R46 ("read" as a noun). They're in `scripts/check_voice.py`, in the full check in tells.md, and in the tells table.
- Changed: five lines of the skill's own text that the new rules flagged, in voice.md (two), samples.md (two) and formats/linkedin.md (one).

## 1.0 · First public release
- Changed: `scripts/check_voice.py` skips fenced code blocks and inline code, so command-line flags like `--surface` no longer read as dashes. The choppiness checks (V02, V03, V04) now count only prose, leaving out headings, list items, quotes and tables. The full check in tells.md says the same.
- Changed: one line in formats/linkedin.md that the check flagged ("fairly" read as a hedge).
- The repository adds a README, an MIT license and a .gitignore around the skill folder.

## 0.9 · General tool only
- Removed: the personal voice profile, the example brand file, the worked examples from one writer's portfolio in samples.md, and the 14 rules that applied to one writer only. The skill is a general tool for specific outputs, not a personalization skill, so no personal details, clients or private work stay in any file.
- Removed: the `--profile` switch from `scripts/check_voice.py`.
- Replaced: every example drawn from one writer's work, in voice.md and the format guides, with a neutral example that teaches the same move.
- Changed: users now supply their own samples or a voice or brand guide in the conversation. The skill follows it there and never saves it.
- Rewrote: earlier changelog entries, to remove personal details. What each build changed stays on record.

## 0.8 · General core
- Added: P12 blocks "leverage", except in its finance sense (debt, financial and operating leverage, highly leveraged, over-leveraged, leverage ratio, leveraged buyout).
- Changed: SKILL.md, voice.md, samples.md, tells.md and the format guides to general wording, and the source section numbers came out of the text.
- Generalized: R05 catches "My name is..." for anyone, R12 catches "supported" after any pronoun, and R07 keeps only the general "Through X years..." lead-in.

## 0.7 · Restored what earlier rewrites dropped
- Restored: "Own the work", "A provocation without the objection reads as a rant", "Say each point once and trust the reader", and "The same voice comes out short and flat for a CFO and looser for peers".
- Restored to the checker: "could potentially" as a weak claim, exclamation marks as a warning, and "landscape" as a warning that skips "landscape architect" and "landscape architecture".
- Added: this changelog and the "Changing the skill" rule in SKILL.md.

## 0.6 · Self-contained
- Added: every rule written out in plain words in tells.md under "The full check", so the check runs by reading with no tools.
- Added: `scripts/check_voice.py`, one optional checker with all the rules and a `general` surface.
- Rulings: wrap-up words block (S02), chatbot stock phrases block (S03), and colon reveals are limited to one per piece, with any second one blocking (S04).
- Removed: the two earlier scripts, replaced by check_voice.py with every rule kept, and every reference to outside files and tools.

## 0.5 · A full voice system
- Added: references/voice.md (where the voice sits, twelve patterns for how it works, the moves to reach for with how each fails, seven modes, and the edit-pass checks).
- Added to tells.md: terminal abstractions, empty bridges, defensive meta-statements, symmetrical negation, urgency codas, endings anchored in the person or the organization, repeated sentence shapes, compression tells and the sentence shapes that invite em dashes.
- Added: mode sequences in every format guide, plus formats/brand-narrative.md and formats/workshop.md.
- Changed: semicolon and ellipsis warnings removed, the metaphor rule replaced by the removal test, and three-item lists and short-sentence runs allowed when the items are specific or stack proof points.

## 0.4 · More formats
- Added: formats/proposal.md, formats/letter.md (including referral blurbs) and formats/think-piece.md.

## 0.3 · The full tells table
- Added: the four root causes on every row of the tells table, a row for em dashes, colon reveals and one-line paragraphs, the full drift fix (sections, a fresh chat, a separate edit pass), and colon reveal and signposting checks.

## 0.2 · After a choppy draft
- Added: the rule to connect sentences, the empty assertion, restating rhetorical question and intensifier label tells, the read-aloud step and a choppiness check.

## 0.1 · First build
- Added: SKILL.md (why AI writing sounds like AI, the seven steps, the four questions, the voice rules), references/tells.md, references/samples.md (public-domain passages and described writers), formats/linkedin.md and a first checker script.
