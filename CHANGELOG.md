# Changelog

Every change to this skill is logged here: what was added, changed or removed, and why. Nothing comes out without a line saying so. Newest first.

## 1.5 · Only what the user gave
Why: a red-team test of 1.4 ran 30 writing jobs, twice each with the skill and twice without, plus 12 briefs once each way. 38 of the 72 drafts made with the skill had at least one fact the user never gave, against 51 of 72 drafts Claude wrote without it. Most were details made up to fill a thin brief, true facts from memory and plans the user never made, like a schedule or a call length. The skill's own instructions to be specific caused most of them. The lines that asked for a specific instance, a scene or a named result didn't repeat the rule against inventing facts, so on a thin brief they won.

Instructions:
- Added: to "When instructions conflict" in SKILL.md, that the rule against inventing covers true facts from memory and the notes around the piece, and that a plan the user hasn't made (a schedule, a meeting length, a price, a program name) goes in a bracket. Today's date from the computer's clock is fine.
- Added: Step 7 of SKILL.md, a source check. Every name, number, date, quote and claim of what happened, in the piece and the notes, has to be in the user's material or in a bracket. The check script can't see an invented fact, so this step is what catches one. Deliver moves to Step 8.
- Changed: Steps 1, 4 and 5 of SKILL.md. Each line that asks for a specific instance, something the reader can check or picture, or a detail only this piece has now says it comes from the user's material or goes in a bracket. A claim about the work ends on a result the user gave, as firmly and widely as the user gave it, and the writer owns the work at its real size. A rewrite made to clear a tell can't add a fact; in the test, one fix for choppy sentences added a passenger count the user never gave.
- Changed: Step 8 (Deliver). The notes after the piece list what to fill in or verify, and add no fact, source or figure of their own. In the test, the notes were a second route for outside facts, like a survey's name or the year a law passed.
- Changed: voice.md. Under move 3 ("Specificity is the trust signal"), an instance the user didn't give goes in a bracket, never in from memory. The specific-world opener, the personal stake and the density of specifics take their facts from the user, and the self-check asks whether every name, number and event is one the user gave.
- Changed: letter.md. The opening fact comes from the user or the job posting, or a bracket. The closing ask leaves its length and date in brackets unless the user gave them. The writer's part is written at its real size, with the lead named when someone else led.
- Changed: proposal.md. Specifics come from the user's notes, never from local history or market facts the model knows. Scope, dates, sizes, prices and past work use the user's figures and bracket the rest. A program name the user didn't give is described, or offered in a bracket for the user to decide.
- Changed: think-piece.md, brand-narrative.md and linkedin.md. The opening scene, the case, the sensory detail and the physical thing come from the user's material. When there isn't one, the draft asks or leaves a bracket.
- Changed: workshop.md. A rule of thumb or a timing the user didn't give goes in a bracket for the facilitator.
- Added: to tells.md, a row for facts the user didn't give, and rows for three sentence shapes a blind reader marked in AI drafts: an opener that points back ("That deliverable is..."), a short flat line after a long one, and a skills claim that names nothing. The endings row now ends a claim on a result the user gave.

The check:
- Changed: U01 (signposting: "Here's what", "Here's how", "this matters") moves from a warning to a block. Claude without the skill used it 10 times in 72 drafts (3.14 per 10,000 words), the skill never, and edited human writing 0.12 times per 10,000 words.
- Added: `--keep`, which takes the user's names and technical terms, separated by commas, and skips them anywhere. In the test, P03 blocked the company name "Seamless" where it opened a sentence.
- Changed: a name joined by + or & ("Foster + Partners") is read as a name even in a heading in title case or a memo's Re: line, where P04 blocked "Foster".
- Changed: R01 passes a divider or cut line made of hyphens ("✂ - - - -"), which it blocked on a printable handout.
- Changed: P11 warns on "drive" only before a business object ("drive growth", "driving engagement", "drive the main work"). In the test, 26 of its 27 hits in drafts made without the skill were the noun or a literal drive ("the spring food drive").
- Added, as warnings on LinkedIn: U16, three or more hashtags in a row; U17, an arrow or emoji used as a bullet; U18, engagement-bait closers like "I'd love to hear what's worked". Claude without the skill used them in 13, 10 and 5 of 20 posts, and the skill in none; linkedin.md already bars all three. A line that opens on an arrow or emoji now counts as a list item when wrapped lines are joined.
- Added, as warnings that fire once per draft above the rate nine in ten pieces of edited human writing stay at or under: V05, an opener that points back, above 2.5 per 1,000 words, and V06, a short flat line after a long one, above 5. Human writers open on "That" or "This" about as often as AI drafts do (13 per 10,000 words in the human writing, 13 in drafts Claude wrote without the skill), so the reading pass in tells.md does most of the work on V05. V06 separates them better: its warning fires on 10% of the human pieces and on a third of the drafts, with the skill or without it. V07, a skills claim that names nothing, warns per sentence in letters, resumes, LinkedIn and blurbs.
- Changed: the checker's version to 1.5, and the full check in tells.md to match.

After a rerun of the 30 test jobs on the changes above, 8 of 60 drafts made with the skill still had a fact the user never gave, down from 31. They came in five ways, and these close them:
- Added: to Step 4 of SKILL.md, that the user's view stays a view. "My opinion from living in a few small towns" had become "in each of them I watched the same announcement play out", and "good with difficult customers" had become "the customers I handle best". letter.md and the personal stake in voice.md say the same.
- Added: to Step 4, that a reason, a cause or a process the user didn't give goes in a bracket. Drafts had supplied why customers decide, how a company sizes its systems, why a health program worked and what else a cleanup improved, to make the argument work.
- Added: to Step 7's list, plain-words explanations from memory (a draft explained what systolic pressure and a metabolic panel are), reasons and processes, views turned into events, and a quote restated in stronger words ("more miles than our racers do" had become "more miles than anyone in our racing crowd").
- Changed: Step 8. A note naming a fact to find gives no definition, figure or threshold; one had given the 30% line for rent burden.
- Changed: Step 6. `--keep` takes the words the user chose for a fact as well as names (one draft wrote "raised four feet" for the user's "elevated four feet"), and a pattern the user's samples use stays in the piece with `--skip`, instead of coming out for the user to put back (one draft dropped the dashes the user's sample posts use).

After a second rerun, 4 of 60 drafts still had a fact the user never gave. Each new rule had cut the count, but the skill's own instructions to make every sentence concrete kept pulling the other way. This round takes those out instead of adding more:
- Changed: Step 1 of SKILL.md. The skill writes the user's facts down once, in a scratch note, and drafts only from that list. Anything not on it stays out of the piece and the notes, and a thin brief makes a short, plain piece.
- Removed: the fact check that ran at the end as Step 7. Nothing made it run and nothing showed that it had; the list at the start replaces it. Deliver is Step 7 again, and a line the user requires goes in exactly as it stands on the list.
- Removed: the lines that asked for detail the user hadn't given: "make every sentence name something the reader can check or picture", "find the physical version of an idea first", specificity as an effect to revise toward, and "let the metaphor generate specifics". Under voice.md move 3, the skill keeps the general word when the user gave no instance.
- Changed: no guesses, in a bracket or out of one. A bracket names only a fact the piece can't stand without, like a date. Brackets that held a suggested value ("a [20]-minute call", a suggested program name) are gone, and a reason or process the user didn't give isn't written at all.
- Changed: letter.md. A cover letter runs 250 to 450 words, and one under 250 fails; on a thin brief it reaches the length with labeled slots for the writer's own proof.
- Changed: the think-piece, brand-narrative, proposal and workshop guides to match, two rows in tells.md, and V07's fix, which now cuts a claim the user gave nothing for.

A 30-draft test of that round still had 4 drafts with a fact the user didn't give or a length the user asked for and didn't get, and the pieces ran short. The model that writes a draft doesn't see what it added; in every test, a fresh reader did. So:
- Removed: "A thin brief makes a short, plain piece." It was read as permission to stop early, and a 200-word brand story came in at 93 words. Length now comes from what the user asked for and what the piece has to do, never from how much the user gave; a short brief can need a long piece.
- Added: to Step 4, that a length the user asks for, or a format guide's range, is a requirement, met from the user's facts, the argument the piece has to make and labeled slots for the user's own material, never by stopping short or by adding facts.
- Added: Step 7, a fresh reader. Where the skill can start a separate agent, a reader that sees only the user's message, the fact list and the draft quotes every line the message doesn't support, and the writer cuts or rewrites each one. Where it can't, the skill rereads the draft against the message line by line. Deliver is Step 8.

A 30-draft test of that round had no made-up content in any piece. Two drafts still had a fact the user didn't give in the notes, one where the notes were written after the reader's check and one where the reader never ran, and some pieces still ran short. So:
- Changed: Step 7. The reader checks every piece, and the notes are written first so it sees them. It needs no tools, answers in one reply, and can run on a smaller, faster model, since a check against a short list doesn't need the strongest one.
- Added: to Step 8, a word count before delivery, with `wc -w` when code can run. A piece under its range or the user's number gets filled the way Step 4 says, never delivered short. Nothing is added to the notes after the check.
- Removed: "Stop sooner if the point is made" from linkedin.md, for the same reason "a thin brief makes a short, plain piece" came out of SKILL.md. Three posts had come in at 78 to 119 words against 150 to 300.

## 1.4.1 · A list of four isn't a list of three
Why: V01 counted the last three items of a longer list as a list of three. Its pattern only refused a match that started right after a comma, so a list of four or more still matched from partway through an item: "roads, bike lanes, bus shelters, and street trees" counted from "lanes". On October 1, 2026, a 498-word test letter got five V01 hits, 10.0 per 1,000 words, and a warning. A reader counts three lists of three in it, 6.0 per 1,000, which is under the limit of 8.

- Changed: V01 no longer counts the last three items of a list of four or more. The script reads back to the comma before the three items, and when a plain item sits on each side of that comma, the list is longer than three. The three still count when that comma closes an opening phrase ("In March,", "When I joined,", "However,", "Last year,", "Founded in 1920,"), when the words after it start a clause or a phrase ("and", "which", "we", "in", "showing", "ideally with") or when six or more words run from it to the list's first comma. The pattern is the same, so every hit 1.4.1 reports, 1.4 reported too. The test letter now gets three hits and no warning.
- Left out on purpose: the shorter fix, dropping every hit that has a comma before it. Of V01's 4,691 hits on the 944,440 words of human writing, 1,924 have one, and most of them follow an opening phrase or a new clause ("In March, we shipped apples, pears, and plums"). 1.4.1 drops 321.
- Unchanged: V01's limit of 8 per 1,000 words. On the human writing, V01's hits fell from 4,691 to 4,370, and the pieces above the limit fell from 34 of 358 to 22. The limit was set at the rate nine in ten human pieces stay under. That rate is now 7.6, so 8 is a little looser than it was.
- Unchanged: what the script still can't read. A longer list still counts when an item opens with an -ing or -ed word ("hiring plans") or a preposition ("in Ohio, in Maine, in Iowa, or in Texas"), since the same words open a phrase that leads into a real list of three ("showing wit, sparkle and aplomb"). A list of three after a name between commas ("My manager, Dana, likes...") is missed. The full check in tells.md says both go by reading.
- Changed: the V01 entry in the full check in tells.md, to match the script, and the checker's version to 1.4.1.
- Added: cases that check V01's hit count, in the red-team folder (`checker/count_cases/lists.jsonl`, run by `checker/run_count_cases.py`): seven longer lists that count nothing, nine lists of three that still count, and the three limits above.

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
