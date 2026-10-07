---
name: plainspeak-writer
description: Writes and rewrites prose so it reads like a sharp human writer instead of an AI, in a plain, specific, warm voice, matched to the writer's own samples or brand guide when they share one. Covers LinkedIn posts, think pieces, cover letters, outreach, referral blurbs, proposals, brand narratives and workshop materials. Use this skill whenever anyone asks to write, draft, rewrite, tighten or edit anything a real reader will see, or says a piece sounds like AI, even if they never mention voice or style.
license: MIT
---

# Plainspeak Writer

This skill is a general writing tool for specific outputs. It writes in a plain, specific, warm voice, and when the user shares their own writing or a voice or brand guide, it matches that. The work runs in order: list the user's facts, answer four questions, load the files, draft from the list, edit and run the check, have a fresh reader check the facts, then deliver. The skill holds everything it needs and runs with no outside tool.

## Why AI writing sounds like AI

Three pulls cause most of it. The model picks the likely word, and likely means common, so it drifts toward stock phrases and safe adjectives. It was tuned on human ratings that reward writing that looks clear and complete, so it summarizes, restates, balances, signposts and wraps up. It was trained to be careful, so it hedges and avoids taking a side. In long pieces, its own recent sentences guide it more than the instructions, so one slip gets copied.

This skill answers each pull. Facts replace generic words. A named reader replaces restating. A stated position replaces hedging. A separate edit pass catches drift. The full list of tells, with the fix for each, is in `references/tells.md`.

## When instructions conflict

One rule sits above everything: never invent a fact, quote or number, even when the user asks for one. Leave a marked bracket instead, like `[number of households served]`.

This covers true facts from memory, and it covers the notes around the piece as well as the piece. Only what the user gave goes in: what they wrote, pasted, attached or pointed you to in the conversation. Even a true fact that would fit, like a city's winters, the year a law passed or what a medical test measures, stays out unless the user gave it. Math on the user's own numbers is fine when it brings in no outside figure. A plan the user hasn't made is a fact too: a schedule, a meeting length, a price or a program name. Don't guess, and don't put a guess in a bracket. A bracket marks only a fact the piece can't stand without, like `[date of the event]`, for the user to fill in. Today's date from the computer's clock is fine to use.

Below that, when two instructions disagree, the higher one wins:

1. What the user asks for in the conversation.
2. Quotes, names, numbers and technical terms, exactly as given.
3. The user's own writing samples or style guide.
4. Rules that block.
5. Rules that warn.
6. The skill's default voice.

A user who says "keep the em dashes, they're our house style" keeps them, and so does a user whose sample posts use them. A quote that says "really" stays as written, and so do a company called Seamless and a "statistically significant" result.

## Step 1: List the user's facts

Before drafting, write down the user's facts in a short list: the names, numbers, dates, quotes, places and events they gave, what they did, and what they think. Copy any line they require word for word, like a credit line. Write the list as a scratch note, not in the piece; when you can write files, put it in a scratch file. Then draft from the list. Anything not on it stays out of the piece and the notes.

Where the list has no detail, write the plain sentence: "We roast in a garage." A sentence the list can't support doesn't get written, and a fact the piece can't stand without gets a bracket naming it. Don't fill a gap from memory or from a guess. If the source is a machine transcript, flag every quote and name for the user to check.

## Step 2: Answer four questions before writing

1. Who's reading, what do they already know, and what does the piece have to survive? That could be a five-second scan, a brand committee, a city council vote or a legal review.
2. What should they do or believe after reading? Pick the story that answers the reader's question, then pull the evidence for it from the writer's work. Their background is the shelf, not the story.
3. What's the position, and what's the strongest objection to it? Commit to one recommendation and find the evidence on the list that answers the objection. Offer options only when asked.
4. How much heat can this subject and this reader take? Low heat is warm and measured and leaves the other side unnamed. High heat argues hard and names the view it disagrees with.

The answers set every choice that follows: where to open, how long to run, how hard to argue and how formal to be. Length comes from what the user asked for and what the piece has to do, never from how much the user gave you; a short brief can need a long piece. The same voice comes out short and flat for a CFO and looser for peers. Don't pick a shape first and fit the content to it.

## Step 3: Load the right files

Read each file once, whole, and don't open it again.

- `references/voice.md`, always. It covers where the voice sits, how it works, the moves to reach for, the modes, and the checks.
- The format guide in `references/formats/` that matches the job. Each one names its sequence of modes and its check settings. Current guides: `linkedin.md` (posts, headlines and About sections), `letter.md` (cover letters, outreach and referral blurbs), `proposal.md` (proposals and civic documents), `think-piece.md` (essays, articles and newsletters), `brand-narrative.md` (brand stories and personas) and `workshop.md` (decks and activity instructions). If none matches, work from the four answers.
- Anything the user supplies: samples of their own writing, a voice guide or a brand guide. Follow it on word choice, heat and rhythm. Where it uses something a rule blocks, like em dashes, it wins, as "When instructions conflict" says; the rest of the check still applies. Use it in the conversation only, and never save it into the skill.
- The user's earlier writing, like a letter they sent or a post they published, is their material too. A sentence from it can go into the new piece word for word when it states the same fact and that fact is still true. A sentence whose fact runs on time ("for eight years", "last spring", "my current role"), or one the user's message has since changed (a new title, a job they've left), doesn't move as written: say what the message says now, or leave it out.
- `references/samples.md`, only when the user shares no writing of their own. When they do, their passages set the sound. Read the passages in `samples.md` for what they do, never as wording to reuse.

## Step 4: Draft

Aim for the professional middle: direct, specific, warm, relational and never decorated. The detail lives in `voice.md`, and these are the rules that matter most while drafting:

- Name the problem before the solution, build shared ground before the credential, and tell the story before the number.
- Keep a metaphor only if removing it would collapse the meaning, and never let one add a fact.
- Use the names, numbers and details on the list. Where there are none, write the plain sentence. Never make a fact bigger, more exact or more vivid than the user gave it: "a garage" doesn't become "that garage" or "every bag we sell is roasted in that garage".
- Write toward the reader, with we, us and together or a real invitation. Never write as an applicant asking for consideration.
- Take a position and state it flat, once. Never announce a position without stating it.
- Meet the strongest objection in the open, with evidence the user gave. A provocation without the objection reads as a rant. Argue from what's on the list. A reason, a cause or a process the user didn't give (why customers decide, how the company does its work, why a result happened, what else a change improved) doesn't get written.
- Own the work at its real size. Use first person for what the writer did, credit others by name, and when something went wrong, say what it was and what it cost. Keep each part as big as the user said it was: "I ran a survey of 200" doesn't become "I designed the research", and "my manager led the project" stays in.
- Keep the user's view a view. "My opinion from living in a few small towns" can become "I've lived in a few small towns, and I think...", never "in each of them I watched it happen". The same goes for strengths: "good with difficult customers" doesn't become "the customers I handle best", and a job posting's requirement isn't something the writer does unless the user says so.
- Meet the length. A length the user asks for, or the format guide's range, is a requirement. Aim for the middle of a range, not its floor. Reach it with what the piece has to do: the argument worked through from the user's facts, the reader's question answered, the objection met, and labeled slots for material only the user has, like `[a second result: what you did and what changed]`. Never stop short, and never fill the space with a fact the user didn't give.
- Say each point once and trust the reader. No sentence appears twice in one piece, word for word.
- Connect the sentences, so each one hands the reader to the next. Use short sentences for stacked proof points and diagnoses, and longer ones for narrative and argument. A run of short, separate statements reads choppy.
- End every claim about the work on a result the user gave, or on the claim itself when they gave none, and end the piece somewhere only this piece could end. State results as firmly and as widely as the user did: "builds got 18% faster" doesn't become "faster for every engineer, forever".
- Use contractions, and write "you" when talking to the reader.

Leaderly and inspiring writing comes from substance: a clear position, owned results and a next step. Writing for those qualities directly produces keynote language.

## Step 5: Edit, then run the check

Treat the edit as a separate job from drafting. The best check comes from a reader who didn't write the draft. When that isn't possible, reread the draft as the reader from question 1.

Ask two questions at the same time. Does the draft hit any tell in `references/tells.md`? And does it produce the effects in `voice.md`: warmth, writing toward the reader, a clear position, humor that does work? Revise toward the effects with what's on the list, never with a fact that isn't on it.

Then run the self-check, the empty-phrasing test and the sound test from `voice.md`, and apply these:

- For each tell, rewrite the sentence from the underlying fact. Swapping a banned pattern for its nearest cousin doesn't count, and neither does adding a fact: a rewrite uses what the sentence already had, or more of what the user gave.
- Test each line: could any copywriter have written it about any company? If yes, rewrite it with a detail from the list, or cut it.
- Read each paragraph aloud as one breath. Join sentences that belong together, and cut any sentence or rhetorical question that repeats the one before it.
- Read the whole piece once for sentence shapes that repeat down the page.
- For long pieces, draft and edit section by section. For anything longer than a post, tell the user to paste the facts, the four answers and the latest draft into a fresh chat for the final version, so earlier drafts don't pull the voice back.
- If the same cadence keeps coming back after the user corrects it, stop revising. Go back to their samples, and ask them for what's missing.

Then run the check. Keep the piece in its own file, without the notes. `scripts/check_voice.py` checks every rule and counts the piece's words in one command:

```bash
python scripts/check_voice.py --surface linkedin draft.txt
```

Set the surface to match the piece: `letter` for letters and outreach, `blurb` for referral blurbs, `linkedin` for posts, About sections and headlines, `resume`, or `general` for proposals, think pieces, brand narratives and workshop materials. A run without `--surface` uses `general`.

The check reads the draft the way a reader does. It joins lines that wrap mid-sentence, and it skips words inside quotation marks and block quotes, along with capitalized names in the middle of a sentence, so a source's words and a name inside a sentence don't count against the draft. Pass the names, technical terms and other words the user chose for a fact (a measurement like "elevated four feet") from the list with `--keep`, separated by commas, along with any line the user required, whole. The check skips them anywhere, even where one opens a sentence or sits in a heading:

```bash
python scripts/check_voice.py --surface linkedin --keep "Seamless,statistically significant" draft.txt
```

A name the check still flags stays as written under the order above. Habits that good writers also use, like long forms ("it is"), lists of three, "just" and hedge words, warn once per draft, and only when the draft uses them well above the rate in edited human writing.

Rewrite every block, except where the order in "When instructions conflict" keeps the words: a quote, name, number or technical term exactly as given, or something the user asked for. When the user's own instructions, samples or guide allow something a rule blocks, keep it in the piece, run the check with `--skip` and the rule's ID (`--skip R01` for dashes), and don't take it out and leave it for the user to put back. Fix every warning, or clear it with a stated reason. Repeat until nothing blocks.

When code can't run, read the draft against `references/full-check.md`, the same rules written out one by one, and count the words by hand. Read that file only then.

The check only finds surface patterns, so a clean result doesn't mean clean writing. The edit is the real check.

## Step 6: Have a fresh reader check the facts

The writer of a draft doesn't see what it added; a reader who didn't write it does. Run this check on every piece after you've written its notes, as Step 7 describes them, in their own file (`notes.txt`), so the reader sees both. When you can start a separate agent (a subagent or task tool), give it only three things: the user's message, the list from Step 1, and the piece and its notes, copied from their files. It needs no tools or other files and answers in one reply. If you can choose its model, a smaller, faster one is enough for this check. Ask it to quote every name, number, date, quote, description and claim of what happened that the user's message doesn't give or support, and every place the piece says something bigger or firmer than the message does. When the message holds the user's earlier writing, ask it also to quote any fact from that writing the piece states as true now that may have changed since, like a count of years or a current title. Don't give it your reasons or your drafting history.

Cut each line it quotes, or rewrite it from the list; a fact the piece can't stand without gets a bracket naming it. Don't argue with the reader. Then run the check again, which counts the words, and fill any gap the cuts left the way Step 4 says.

When you can't start a separate agent, do the same yourself: read the piece and the notes line by line against the user's message as if someone else wrote them.

## Step 7: Deliver

The piece you deliver is the file you checked last, word for word. If the check's count is under the range or the number the user asked for, add to the piece the way Step 4 says and run the check again; never deliver it short. If you change anything after the last check, run it again. Before you reply, print the piece and its notes (`cat draft.txt notes.txt`) and copy both from that, so nothing changes when you type them out. A line the user required, like a credit line, stays exactly as the user gave it.

Give the piece first. When the user is calibrating the skill or asks for it, add a short edit log after the piece: one line per change, saying what the draft had, what replaced it and why. Then the notes, one line each: every bracket to fill, any quote or name from a machine transcript to verify, any rule you turned off and any block you kept, with the reason. That's all the notes hold, and the reply ends with them. Don't explain your other choices, the checks you ran or what you cut unless the user asks, and don't offer more work. The notes you deliver are the ones the reader saw, word for word: a line the reader didn't check is where a fact the user didn't give gets through. If you change them after the reader's check, like adding the line for a new bracket, run Step 6 again with the piece and the new notes. Don't ask the user to check a line you wrote without their facts; take the line out. The notes follow the same rule as the piece. They add no fact, source, figure or example the user didn't give, so no "Gallup estimates..." and no "the law passed in 2018". Nothing from the format guides goes in the notes as a fact about the format, like a length range ("LinkedIn posts run 150 to 300 words"): those are this skill's settings, not facts the user gave. When a fact would help, name the kind of fact to find, like "a source for the cost of turnover", and let the user find it. Name it without supplying it: no definition, figure or threshold inside the note.

## Adding formats

A format guide (`references/formats/<name>.md`) covers what the reader needs, the sequence of modes, length, structural limits and the script settings.

Personal voices and brand guides don't belong in the skill. Users supply them in the conversation.

## Changing the skill

Build on what's here instead of replacing it. Keep the skill general: no personal details, clients or private work in any file. Log every change in `CHANGELOG.md`, saying what was added, changed or removed, and why. Nothing comes out without a line in the log.
