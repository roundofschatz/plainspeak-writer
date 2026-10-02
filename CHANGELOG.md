# Changelog

Every change to this skill is logged here: what was added, changed or removed, and why. Nothing comes out without a line saying so. Newest first.

## 1.4.1 · A list of four isn't a list of three
Why: V01 counted the last three items of a longer list as a list of three. Its pattern only refused a match that started right after a comma, so a list of four or more still matched from partway through an item: "roads, bike lanes, bus shelters, and street trees" counted from "lanes". On October 1, 2026, a 498-word test letter got five V01 hits, 10.0 per 1,000 words, and a warning. A reader counts three lists of three in it, 6.0 per 1,000, which is under the limit of 8.

- Changed: V01 no longer counts the last three items of a list of four or more. The script reads back to the comma before the three items, and when a plain item sits on each side of that comma, the list is longer than three. The three still count when that comma closes an opening phrase ("In March,", "When I joined,", "However,", "Last year,", "Founded in 1920,"), when the words after it start a clause or a phrase ("and", "which", "we", "in", "showing") or when six or more words run from it to the list's first comma. The pattern is the same, so every hit 1.4.1 reports, 1.4 reported too. The test letter now gets three hits and no warning.
- Left out on purpose: the shorter fix, dropping every hit that has a comma before it. Of V01's 4,691 hits on the 944,440 words of human writing, 1,924 have one, and most of them follow an opening phrase or a new clause ("In March, we shipped apples, pears, and plums"). 1.4.1 drops 321.
- Unchanged: V01's limit of 8 per 1,000 words. On the human writing, V01's hits fell from 4,691 to 4,370, and the pieces above the limit fell from 34 of 358 to 22. The limit was set at the rate nine in ten human pieces stay under. That rate is now 7.6, so 8 is a little looser than it was.
- Unchanged: what the script still can't read. A longer list still counts when an item opens with an -ing or -ed word ("hiring plans") or a preposition ("in Ohio, in Maine, in Iowa, or in Texas"), since the same words open a phrase that leads into a real list of three ("showing wit, sparkle and aplomb"). A list of three after a name between commas ("My manager, Dana, likes...") is missed. The full check in tells.md says both go by reading.
- Changed: the V01 entry in the full check in tells.md, to match the script, and the checker's version to 1.4.1.
- Added: cases that check V01's hit count, in the red-team folder (`checker/count_cases/lists.jsonl`, run by `checker/run_count_cases.py`): six longer lists that count nothing, seven lists of three that still count, and the three limits above.

## 1.4 · The check reads like a reader
Why: a red-team test of 1.3.1 (`phase1.md` in the red-team results) ran the check on 113 test cases and on 944,440 words of edited human writing: presidential speeches from 1945 to 2021 and the Brown Corpus. The check blocked good writing more often than it caught AI writing. 88% of 500-word stretches of human writing hit a block, 41 of 51 good sentences got blocked, and none of the 46 AI tells that weren't controls got a block. In 1.4 a rule blocks only when good human writing trips it less than once per 10,000 words and its hits are mostly the misuse it targets. Everything else warns.

How the check reads a draft:
- Changed: lines that wrap inside a paragraph or a list item are joined before checking, so a tell split by a line break no longer gets through. In 1.3.1, none of six split tells got the block they got on one line.
- Changed: words inside quotation marks and block quotes are skipped, because a writer can't change what a source said. Quoted examples in the skill's own files no longer trip the check either.
- Changed: a capitalized word in the middle of a sentence is read as a name and skipped, and so is a capitalized pair at the start of a sentence. Foster + Partners, Seamless, Synergy Health and Google Drive all got blocked in 1.3.1. A word in capitals, a hyphenated word and a word ending in -ed or -ing are never read as names, so "Spearheaded Salesforce rollout" still blocks.
- Changed: R01 counts every dash character: the en dash, the figure dash, the minus sign, the two-em and three-em dashes, the small em dash, a spaced hyphen, and a double or triple hyphen. In 1.3.1 five of them got through, including the spaced en dash Word inserts. An en dash in a number range passes, and so does a command flag like `--surface`.
- Changed: label lines ("Budget: $40K.") no longer count as colon reveals under S04, and neither does a colon that opens a quote or a numbered list.
- Changed: R09 (hedge words), R41 (long forms), P10 ("just"), V01 (lists of three) and V02 (runs of short sentences) warn once per draft, and only when the draft has at least two hits and runs above the rate that more than nine in ten pieces of human writing stay under. R41 averaged 11 warnings per 1,000 words of formal human writing and V01 about 5, so a warning on every hit asked writers to justify normal prose. Two hits are the minimum because one use in a short post says nothing about a habit.
- Changed: a run without `--surface` uses `general`. In 1.3.1 it used `letter`, which checked posts and proposals against letter rules.
- Added: `--skip` turns off a rule that the user's own instructions, samples or guide allow, like `--skip R01` for a writer whose house style uses dashes.

Rules that block, narrowed or moved:
- Changed: R02 splits in two. "Not just X, but Y", "not merely" and "not simply" still block. "Not only X, but Y" warns under R02W, since it's 229 of 312 human hits, Kennedy's inaugural address among them.
- Changed: R04 lets a follow-up letter open on thanks for a specific meeting or call.
- Changed: R08 checks the draft's first line only and blocks a self-description there ("Experienced product manager", "I am a passionate designer"). "As a result", "As an example" and "As a rule" pass, and so do "Proven reserves fell 4%" and "Experienced riders take the north loop".
- Changed: R09 moves from a block to a rate warning. "Very" meaning "exact" ("the very first permit"), "fairly" meaning "justly" and "or rather" pass. A booster before a superlative ("truly one of the best") still blocks under R37, with one human use in 944,440 words.
- Changed: R11 allows "authored a bill" and other legislation, which is standard in government writing.
- Changed: R12 runs on letters, resumes, LinkedIn and blurbs only, where it's about career claims. Removed: "supported", which blocked plain sentences like "We supported 1,200 households last winter."
- Changed: R20 blocks "Actually" only at the start of a sentence. Inside a sentence it warns under R20W, since most of its 93 human uses mean "in fact".
- Removed: "before... existed" from R21, which fired on "before there existed a 3-to-3 deadlock".
- Changed: R22 blocks "stood up" only before a, an or the, since bare "stood up" meant standing in every human hit. "Land with" now blocks only as a verb ("lands with", "will land with"), since every human hit was the noun ("the same land with", "many lands with").
- Changed: R26 matches "synergy", not "synergism" or the pharmacology term "synergistic".
- Changed: R28 blocks only the filler form, "at once X and Y". "Left at once" and "went off at once" pass.
- Changed: R39 ("carry") and R40 ("That is the...") move to warnings. Most of 305 human uses of "carry" are literal, and long forms already warn under R41.
- Changed: R48 matches "seasoned" only before a person, so "seasoned to taste" passes.
- Changed: P01's two-sentence form ("This isn't a pricing problem. It's a trust problem.") goes in as a warning, U10, until there's evidence of how often AI drafts use it. A looser pattern hit human writing 25 times.
- Changed: P02 ("simply", "literally") moves to a warning, since "simply because" is plain English.
- Changed: P03 splits in two. "Robust" and "seamless" still block, and statistics terms like "robust standard errors" pass. "Significant", "powerful" and "comprehensive" warn under P03W, since their human uses are plain meanings and terms of art ("statistically significant", "a comprehensive metabolic panel").
- Changed: P04 lets "foster" pass before home, care, parent or child, "elevated" pass for height and measurements ("an elevated boardwalk", "elevated blood pressure") and "elevate" pass for a body part.
- Changed: P06 checks the start of a sentence only.
- Changed: P08 blocks only when the writer, the firm or the product is the subject ("we can help", "our platform can help"). "A mother can help a child adapt" passes.
- Changed: P12 blocks "leverage" as a verb only. The noun for bargaining power passes ("our negotiating leverage"), and the finance sense still does.
- Changed: S02 splits in two. "In summary", "In conclusion", "To sum up" and "Overall," still block. "Moreover", "furthermore" and "ultimately" warn under S02W, since inside a sentence "ultimately" usually means "in the end".
- Changed: S03 adds "deep dive" and keeps "delve", "testament to", "let's dive" and "rich tapestry". Removed: bare "tapestry" and "dive into", which fired on real tapestries and real dives.
- Unchanged: R06, R07, R16, R31 and R32 are under review, because each may fit one writer's drafts more than general writing. They stay as they are until the review decides. R01 stays a block as the skill's house style.

Rules added:
- Added, as blocks: S05 "I hope this email finds you well" (letters), S06 engagement bait such as "Agree?" and "Drop a comment" (LinkedIn), S07 "Thrilled to announce" and "excited to share" (LinkedIn), S08 "humbled" (LinkedIn), S09 "proven approach" and "rigorous process", S10 chatbot closers such as "I hope this helps", S11 "Certainly!", S12 "Let that sink in" and "At its core", S13 "arguably", S14 "Notably," at the start of a sentence, S15 "multifaceted", "transformative" and "valuable insights", S16 question reveals ("The result? A 40% drop") and S17 "It's not just". Each one got past the 1.3.1 check as an AI tell, and none appears more than 0.06 times per 10,000 words of the human writing.
- Added, as warnings: U05 "we'll aim to", U06 "Additionally," at the start of a sentence, U07 "notes that" in place of "says", U08 "meticulously", "innovative", "groundbreaking" and "showcase", U09 "underscore", "intricate" and "vibrant", U10 "This isn't X. It's Y.", U11 "in many ways" and "to some extent", U12 "less X, more Y", U13 a trailing phrase that states the lesson (", highlighting the value of..."), U14 "when it comes to" and "at the end of the day", and U15 "enhance" and "unprecedented". Human writers use each of these now and then, so they warn until there's evidence that AI drafts use them far more.

Instructions and files:
- Added: "When instructions conflict" to SKILL.md. It ranks the user's request, then quotes, names, numbers and technical terms as given, then the user's samples or guide, then blocks, then warnings, then the default voice, with the rule against inventing a fact, quote or number above all of it. In 1.3.1 nothing settled those conflicts, and a block on a quote could only be cleared by changing the quote.
- Changed: Step 3 and Step 6 of SKILL.md to match. A user's samples or guide win over a block, the check skips quotes and names, rate warnings come once per draft, and `--skip` turns off a rule the user's own guide allows.
- Changed: the full check in tells.md, rule for rule with the script, with the new reading rules and a section for rate warnings. Its examples now sit in quotation marks, so the check skips them when it runs on the skill's own files.
- Changed: nine lines of the skill's own text that the 1.4 check flagged: "a full read" and "can still be carried" in tells.md, "resets a room" in voice.md, "the audience in the room" in samples.md, four uses of "the room" in workshop.md, and "drive something downstream" in brand-narrative.md.
- Changed: the checker's version from 3.0 to 1.4, to match the skill. The README now counts more than 90 rules and explains `--skip`.

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
