---
name: plainspeak-writer
description: Writes and rewrites prose so it reads like a sharp human writer instead of an AI, in a plain, specific, warm voice, matched to the writer's own samples or brand guide when they share one. Covers LinkedIn posts, think pieces, cover letters, outreach, referral blurbs, proposals, brand narratives and workshop materials. Use this skill whenever anyone asks to write, draft, rewrite, tighten or edit anything a real reader will see, or says a piece sounds like AI, even if they never mention voice or style.
license: MIT
---

# Plainspeak Writer

This skill is a general writing tool for specific outputs. It writes in a plain, specific, warm voice, and when the user shares their own writing or a voice or brand guide, it matches that. The work runs in order: find the material, answer four questions, load the files, draft, edit in a separate pass, run the full check, then deliver. The skill holds everything it needs and runs with no outside tool.

## Why AI writing sounds like AI

Three pulls cause most of it. The model picks the likely word, and likely means common, so it drifts toward stock phrases and safe adjectives. It was tuned on human ratings that reward writing that looks clear and complete, so it summarizes, restates, balances, signposts and wraps up. It was trained to be careful, so it hedges and avoids taking a side. In long pieces, its own recent sentences guide it more than the instructions, so one slip gets copied.

This skill answers each pull. Facts replace generic words. A named reader replaces restating. A stated position replaces hedging. A separate edit pass catches drift. The full list of tells, with the fix for each, is in `references/tells.md`.

## Step 1: Find the material

Find first, write second. Before drafting a sentence, find the physical version of the idea, the detail nobody could fake, and the behaviors behind any dynamic you want to name. Collect names, numbers, quotes, places, dates and what happened. When a sentence would name a general category (hotels, outdoor brands, placemaking projects), find the specific instance first.

Generic language fills the gaps where facts are missing, so fill every gap with a fact or leave a marked bracket for the user, like `[your example here]`. Never invent a fact, a quote, a client detail or a number to make a sentence work. If the source is a machine transcript, flag every quote and name for the user to check.

## Step 2: Answer four questions before writing

1. Who's reading, what do they already know, and what does the piece have to survive? That could be a five-second scan, a brand committee, a city council vote or a legal review.
2. What should they do or believe after reading? Pick the story that answers the reader's question, then pull the evidence for it from the writer's work. Their background is the shelf, not the story.
3. What's the position, and what's the strongest objection to it? Commit to one recommendation and find the evidence that answers the objection. Offer options only when asked.
4. How much heat can this subject and this reader take? Low heat is warm and measured and leaves the other side unnamed. High heat argues hard and names the view it disagrees with.

The answers set every choice that follows: where to open, how long to run, how hard to argue and how formal to be. The same voice comes out short and flat for a CFO and looser for peers. Don't pick a shape first and fit the content to it.

## Step 3: Load the right files

- `references/voice.md`, always. It covers where the voice sits, how it works, the moves to reach for, the modes, and the checks.
- The format guide in `references/formats/` that matches the job. Each one names its sequence of modes and its check settings. Current guides: `linkedin.md` (posts, headlines and About sections), `letter.md` (cover letters, outreach and referral blurbs), `proposal.md` (proposals and civic documents), `think-piece.md` (essays, articles and newsletters), `brand-narrative.md` (brand stories and personas) and `workshop.md` (decks and activity instructions). If none matches, work from the four answers.
- Anything the user supplies: samples of their own writing, a voice guide or a brand guide. Follow it on word choice, heat and rhythm, while the tells and the check still apply. Use it in the conversation only, and never save it into the skill.
- `references/samples.md`. The user's own passages, when they share them, come first and set the sound. Read every sample for what it does, never as wording to reuse.

## Step 4: Draft

Aim for the professional middle: direct, specific, warm, relational and never decorated. The detail lives in `voice.md`, and these are the rules that matter most while drafting:

- Name the problem before the solution, build shared ground before the credential, and tell the story before the number.
- Find the physical version of an idea first. Keep a metaphor only if removing it would collapse the meaning.
- Make every sentence name something the reader can check or picture: a person, company, number, place, tool or result.
- Write toward the reader, with we, us and together or a real invitation. Never write as an applicant asking for consideration.
- Take a position and state it flat, once. Never announce a position without stating it.
- Meet the strongest objection in the open, with evidence. A provocation without the objection reads as a rant.
- Own the work. Use first person for what the writer did, credit others by name, and when something went wrong, say what it was and what it cost.
- Say each point once and trust the reader.
- Connect the sentences, so each one hands the reader to the next. Use short sentences for stacked proof points and diagnoses, and longer ones for narrative and argument. A run of short, separate statements reads choppy.
- End every claim about the work on what it produced for the reader, and end the piece somewhere only this piece could end.
- Use contractions, and write "you" when talking to the reader.

Leaderly and inspiring writing comes from substance: a clear position, owned results and a next step. Writing for those qualities directly produces keynote language.

## Step 5: Edit pass

Treat this as a separate job from drafting. The best check comes from a reader who didn't write the draft. When that isn't possible, reread the draft as the reader from question 1.

Ask two questions at the same time. Does the draft hit any tell in `references/tells.md`? And does it produce the effects in `voice.md`: specificity, warmth, writing toward the reader, a metaphor that thinks, humor that does work? A draft with no tells and none of the effects is safe and flat, so revise it toward the effects.

Then run the self-check, the empty-phrasing test and the sound test from `voice.md`, and apply these:

- For each tell, rewrite the sentence from the underlying fact. Swapping a banned pattern for its nearest cousin doesn't count.
- Test each line: could any copywriter have written it about any company? If yes, rewrite it with a name, number or detail only this piece has.
- Read each paragraph aloud as one breath. Join sentences that belong together, and cut any sentence or rhetorical question that repeats the one before it.
- Read the whole piece once for sentence shapes that repeat down the page.
- For long pieces, draft and edit section by section. For anything longer than a post, tell the user to paste the facts, the four answers and the latest draft into a fresh chat for the final version, so earlier drafts don't pull the voice back.
- If the same cadence keeps coming back after the user corrects it, stop revising. Go back to their samples, and ask them for what's missing.

## Step 6: Run the full check

The full check is written out rule by rule in `references/tells.md`, so it runs by reading with no tools. Go through each group against the draft. When code can run, `scripts/check_voice.py` finds the same items faster:

```bash
python scripts/check_voice.py --surface linkedin draft.txt
```

Set the surface to match the piece: `letter` for letters and outreach, `blurb` for referral blurbs, `linkedin` for posts, About sections and headlines, `resume`, or `general` for proposals, think pieces, brand narratives and workshop materials. Rewrite every block. Fix every warning, or clear it with a stated reason. Repeat until nothing blocks.

The check only finds surface patterns, so a clean result doesn't mean clean writing. Step 5 is the real check.

## Step 7: Deliver

Give the piece first. When the user is calibrating the skill or asks for it, add a short edit log after the piece: one line per change, saying what the draft had, what replaced it and why. Then list anything the user must verify, like brackets, quotes and names.

## Adding formats

A format guide (`references/formats/<name>.md`) covers what the reader needs, the sequence of modes, length, structural limits and the script settings.

Personal voices and brand guides don't belong in the skill. Users supply them in the conversation.

## Changing the skill

Build on what's here instead of replacing it. Keep the skill general: no personal details, clients or private work in any file. Log every change in `CHANGELOG.md`, saying what was added, changed or removed, and why. Nothing comes out without a line in the log.
