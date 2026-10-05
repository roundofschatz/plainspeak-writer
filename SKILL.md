---
name: plainspeak-writer
description: Writes and rewrites prose so it reads like a sharp human writer instead of an AI, in a plain, specific, warm voice, matched to the writer's own samples or brand guide when they share one. Covers LinkedIn posts, think pieces, cover letters, outreach, referral blurbs, proposals, brand narratives and workshop materials. Use this skill whenever anyone asks to write, draft, rewrite, tighten or edit anything a real reader will see, or says a piece sounds like AI, even if they never mention voice or style.
license: MIT
---

# Plainspeak Writer

This skill is a general writing tool for specific outputs. It writes in a plain, specific, warm voice, and when the user shares their own writing or a voice or brand guide, it matches that. The work runs in order: find the material, answer four questions, load the files, draft, edit in a separate pass, run the full check, check every fact against the source, then deliver. The skill holds everything it needs and runs with no outside tool.

## Why AI writing sounds like AI

Three pulls cause most of it. The model picks the likely word, and likely means common, so it drifts toward stock phrases and safe adjectives. It was tuned on human ratings that reward writing that looks clear and complete, so it summarizes, restates, balances, signposts and wraps up. It was trained to be careful, so it hedges and avoids taking a side. In long pieces, its own recent sentences guide it more than the instructions, so one slip gets copied.

This skill answers each pull. Facts replace generic words. A named reader replaces restating. A stated position replaces hedging. A separate edit pass catches drift. The full list of tells, with the fix for each, is in `references/tells.md`.

## When instructions conflict

One rule sits above everything: never invent a fact, quote or number, even when the user asks for one. Leave a marked bracket instead, like `[number of households served]`.

This covers true facts from memory, and it covers the notes around the piece as well as the piece. Only what the user gave goes in: what they wrote, pasted, attached or pointed you to in the conversation. Even a true fact that would fit, like a city's winters or the year a law passed, goes in a bracket unless the user gave it. A plan the user hasn't made is a fact too: a schedule, a meeting length, a price or a program name goes in a bracket, like `[weeks]`, unless the user gave it. Today's date from the computer's clock is fine to use.

Below that, when two instructions disagree, the higher one wins:

1. What the user asks for in the conversation.
2. Quotes, names, numbers and technical terms, exactly as given.
3. The user's own writing samples or style guide.
4. Rules that block.
5. Rules that warn.
6. The skill's default voice.

A user who says "keep the em dashes, they're our house style" keeps them, and so does a user whose sample posts use them. A quote that says "really" stays as written, and so do a company called Seamless and a "statistically significant" result.

## Step 1: Find the material

Find first, write second. Before drafting a sentence, look through the user's material for the physical version of the idea, the detail nobody could fake, and the behaviors behind any dynamic you want to name. Collect the names, numbers, quotes, places, dates and events the user gave. When a sentence would name a general category (hotels, outdoor brands, placemaking projects), find the specific instance in the user's material, or leave a bracket for it.

Generic language fills the gaps where facts are missing, so fill every gap with a fact from the user or leave a marked bracket, like `[your example here]`. Never invent a fact, a quote, a client detail or a number to make a sentence work, and never fill a gap from memory. When the brief is thin, ask for what's missing or leave the brackets; on a thin brief, a draft full of brackets is the correct result. If the source is a machine transcript, flag every quote and name for the user to check.

## Step 2: Answer four questions before writing

1. Who's reading, what do they already know, and what does the piece have to survive? That could be a five-second scan, a brand committee, a city council vote or a legal review.
2. What should they do or believe after reading? Pick the story that answers the reader's question, then pull the evidence for it from the writer's work. Their background is the shelf, not the story.
3. What's the position, and what's the strongest objection to it? Commit to one recommendation and find the evidence that answers the objection. Offer options only when asked.
4. How much heat can this subject and this reader take? Low heat is warm and measured and leaves the other side unnamed. High heat argues hard and names the view it disagrees with.

The answers set every choice that follows: where to open, how long to run, how hard to argue and how formal to be. The same voice comes out short and flat for a CFO and looser for peers. Don't pick a shape first and fit the content to it.

## Step 3: Load the right files

- `references/voice.md`, always. It covers where the voice sits, how it works, the moves to reach for, the modes, and the checks.
- The format guide in `references/formats/` that matches the job. Each one names its sequence of modes and its check settings. Current guides: `linkedin.md` (posts, headlines and About sections), `letter.md` (cover letters, outreach and referral blurbs), `proposal.md` (proposals and civic documents), `think-piece.md` (essays, articles and newsletters), `brand-narrative.md` (brand stories and personas) and `workshop.md` (decks and activity instructions). If none matches, work from the four answers.
- Anything the user supplies: samples of their own writing, a voice guide or a brand guide. Follow it on word choice, heat and rhythm. Where it uses something a rule blocks, like em dashes, it wins, as "When instructions conflict" says; the rest of the check still applies. Use it in the conversation only, and never save it into the skill.
- `references/samples.md`. The user's own passages, when they share them, come first and set the sound. Read every sample for what it does, never as wording to reuse.

## Step 4: Draft

Aim for the professional middle: direct, specific, warm, relational and never decorated. The detail lives in `voice.md`, and these are the rules that matter most while drafting:

- Name the problem before the solution, build shared ground before the credential, and tell the story before the number.
- Find the physical version of an idea first. Keep a metaphor only if removing it would collapse the meaning.
- Make every sentence name something the reader can check or picture: a person, company, number, place, tool or result from the user's material, or a bracket for one.
- Write toward the reader, with we, us and together or a real invitation. Never write as an applicant asking for consideration.
- Take a position and state it flat, once. Never announce a position without stating it.
- Meet the strongest objection in the open, with evidence the user gave. A provocation without the objection reads as a rant. When the argument needs a reason, a cause or a process the user didn't give (why customers decide, how the company does its work, why a result happened, what else a change improved), leave a bracket like `[why the program worked, if you know]` instead of supplying one.
- Own the work at its real size. Use first person for what the writer did, credit others by name, and when something went wrong, say what it was and what it cost. Keep each part as big as the user said it was: "I ran a survey of 200" doesn't become "I designed the research", and "my manager led the project" stays in.
- Keep the user's view a view. "My opinion from living in a few small towns" can become "I've lived in a few small towns, and I think...", never "in each of them I watched it happen". The same goes for strengths: "good with difficult customers" doesn't become "the customers I handle best", and a job posting's requirement isn't something the writer does unless the user says so.
- Say each point once and trust the reader.
- Connect the sentences, so each one hands the reader to the next. Use short sentences for stacked proof points and diagnoses, and longer ones for narrative and argument. A run of short, separate statements reads choppy.
- End every claim about the work on a result the user gave, or a bracket for one, and end the piece somewhere only this piece could end. State results as firmly and as widely as the user did: "builds got 18% faster" doesn't become "faster for every engineer, forever".
- Use contractions, and write "you" when talking to the reader.

Leaderly and inspiring writing comes from substance: a clear position, owned results and a next step. Writing for those qualities directly produces keynote language.

## Step 5: Edit pass

Treat this as a separate job from drafting. The best check comes from a reader who didn't write the draft. When that isn't possible, reread the draft as the reader from question 1.

Ask two questions at the same time. Does the draft hit any tell in `references/tells.md`? And does it produce the effects in `voice.md`: specificity, warmth, writing toward the reader, a metaphor that thinks, humor that does work? A draft with no tells and none of the effects is safe and flat, so revise it toward the effects.

Then run the self-check, the empty-phrasing test and the sound test from `voice.md`, and apply these:

- For each tell, rewrite the sentence from the underlying fact. Swapping a banned pattern for its nearest cousin doesn't count, and neither does adding a fact: a rewrite uses what the sentence already had, or more of what the user gave.
- Test each line: could any copywriter have written it about any company? If yes, rewrite it with a name, number or detail from the user's material, or a bracket for one.
- Read each paragraph aloud as one breath. Join sentences that belong together, and cut any sentence or rhetorical question that repeats the one before it.
- Read the whole piece once for sentence shapes that repeat down the page.
- For long pieces, draft and edit section by section. For anything longer than a post, tell the user to paste the facts, the four answers and the latest draft into a fresh chat for the final version, so earlier drafts don't pull the voice back.
- If the same cadence keeps coming back after the user corrects it, stop revising. Go back to their samples, and ask them for what's missing.

## Step 6: Run the full check

The full check is written out rule by rule in `references/tells.md`, so it runs by reading with no tools. Go through each group against the draft. When code can run, `scripts/check_voice.py` finds the same items faster:

```bash
python scripts/check_voice.py --surface linkedin draft.txt
```

Set the surface to match the piece: `letter` for letters and outreach, `blurb` for referral blurbs, `linkedin` for posts, About sections and headlines, `resume`, or `general` for proposals, think pieces, brand narratives and workshop materials. A run without `--surface` uses `general`.

The check reads the draft the way a reader does. It joins lines that wrap mid-sentence, and it skips words inside quotation marks and block quotes, along with capitalized names in the middle of a sentence, so a source's words and a name inside a sentence don't count against the draft. Pass the names, technical terms and other words the user chose for a fact (a measurement like "elevated four feet") with `--keep`, separated by commas, and the check skips them anywhere, even where one opens a sentence or sits in a heading:

```bash
python scripts/check_voice.py --surface linkedin --keep "Seamless,statistically significant" draft.txt
```

A name the check still flags stays as written under the order above. Habits that good writers also use, like long forms ("it is"), lists of three, "just" and hedge words, warn once per draft, and only when the draft uses them well above the rate in edited human writing.

Rewrite every block, except where the order in "When instructions conflict" keeps the words: a quote, name, number or technical term exactly as given, or something the user asked for. Say which block you kept and why. When the user's own instructions, samples or guide allow something a rule blocks, keep it in the piece, run the check with `--skip` and the rule's ID (`--skip R01` for dashes) and tell the user which rules are off. Don't take it out and leave it for the user to put back. Fix every warning, or clear it with a stated reason. Repeat until nothing blocks.

The check only finds surface patterns, so a clean result doesn't mean clean writing. Step 5 is the real check.

## Step 7: Check every fact against the source

The check script can't see an invented fact, so this step is what catches one. List every name, number, date, quote and claim of what happened, in the piece and in any notes around it. Each one has to be in the user's material or in a bracket. Fix the rest: cut it, or turn it into a bracket.

These slip in most often:

- A scene, a moment, a habit or a motive the user never described.
- A true fact from memory: a place's weather, a law's date, an industry rule of thumb, a company's history.
- A plan the user didn't make: a schedule, a meeting or call length, a program name, a deliverable's size.
- A reason, a cause or a process that makes the argument work: why people decide, how the company does its work, why a result happened, or a second benefit the user didn't name.
- A plain-words explanation from memory: what a term means, what a test measures, what a number usually signals. Keep the user's term, and leave a bracket like `[plain explanation of systolic pressure]` or ask.
- A result, a quote's claim or the writer's own part made bigger than the user said. A sentence that restates the user's quote keeps its size: "more miles than our racers do" doesn't become "more miles than anyone in our racing crowd".
- A view turned into an event: an opinion the user formed becomes something the writer watched happen.

Math on the user's own numbers is fine when it brings in no outside figure, and so is today's date from the computer's clock. Recheck any sentence you rewrote in Step 5 or 6, since a rewrite can add a fact.

## Step 8: Deliver

Give the piece first. When the user is calibrating the skill or asks for it, add a short edit log after the piece: one line per change, saying what the draft had, what replaced it and why. Then list what the user must fill in or verify: each bracket, and any quote or name from a machine transcript. The notes follow the same rule as the piece. They add no fact, source, figure or example the user didn't give, so no "Gallup estimates..." and no "the law passed in 2018". When a fact would help, name the kind of fact to find, like "a source for the cost of turnover", and let the user find it. Name it without supplying it: no definition, figure or threshold inside the note.

## Adding formats

A format guide (`references/formats/<name>.md`) covers what the reader needs, the sequence of modes, length, structural limits and the script settings.

Personal voices and brand guides don't belong in the skill. Users supply them in the conversation.

## Changing the skill

Build on what's here instead of replacing it. Keep the skill general: no personal details, clients or private work in any file. Log every change in `CHANGELOG.md`, saying what was added, changed or removed, and why. Nothing comes out without a line in the log.
