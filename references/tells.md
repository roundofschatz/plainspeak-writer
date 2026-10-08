# Tells and fixes

This file holds the tells the edit pass looks for, the cousins that stand in for them, and what's allowed. The rule-by-rule check is in `full-check.md`, and `scripts/check_voice.py` runs the same rules. When a rule changes, update this file, `full-check.md` and the script together, and log it in `CHANGELOG.md`.

## Structural tells (the edit pass catches these)

Four root causes sit behind every row: the **likely word** (the model picks the common option), **pleasing raters** (tuning rewarded writing that looks clear, complete and polished), **caution** (training against overclaiming) and **drift** (in long pieces the model copies its own recent text).

| Tell | Main cause | How to steer it |
|---|---|---|
| Stock phrases and safe adjectives | Likely word | Replace with the fact: a name, number or what happened. Generic words fill gaps where facts are missing. |
| Facts the user didn't give: a scene, a true fact from memory, a plan the user didn't make, a reason or process that makes the argument work, an explanation of a term, a result or a view made bigger than the user said | Pleasing raters: specific detail reads as quality, so the model supplies it | Draft from the list of the user's facts in SKILL.md, Step 1. What isn't on it stays out of the piece and the notes; a bracket marks only a fact the piece can't stand without. |
| "Not just X, but Y" in every form, and "It's not about X, it's about Y" | Pleasing raters: it sounds sharp for little effort | Say Y. If X is a real view, name who holds it. "Rather than" and "instead of" state a contrast and stay. |
| Em dashes, colon reveals, one-line paragraphs | Likely word: punchy web style is everywhere | Use a period, comma, colon or semicolon, whichever the structure needs. A colon belongs before a list or an explanation. A short reveal after a colon is allowed once per piece at most, and only where it lands. Join one-line paragraphs into paragraphs that finish a thought. |
| The sentence shapes that invite an em dash: apposition, a statement followed by a list, a claim followed by its synthesis | Likely word | Apposition becomes two sentences. A statement and its list take a colon or two sentences. A claim and its synthesis take a period. |
| Lists of three, mirror-image sentences | Pleasing raters: they read as polished | A three-item list inside a sentence is fine when each item is specific and does work. Three-part parallels standing in for the logic between paragraphs aren't. Break a mirrored pair by changing the second sentence's shape. |
| A summary line closing each paragraph | Pleasing raters: completeness gets rewarded | Cut the last line of the paragraph and see if anything's lost. |
| A moral, a summary or a big line at the end | Pleasing raters: completeness gets rewarded | End somewhere only this piece could end: the last fact, the ask, the next step or the one sentence the argument earned. |
| Urgency or scarcity coda ("now is the time", "the window is closing", "if we wait") | Pleasing raters: a manufactured ending | End on the substantive conviction. |
| Saying it twice, signposting ("Here's why this matters") | Pleasing raters, plus not knowing the reader | Name the reader and what they already know, then say it once. |
| Hedges, both-sides balance, no stance | Caution | State the position and commit to one recommendation. If something is uncertain, say so once. |
| Defensive meta-statement ("to be candid", "I state that plainly", "in the interest of transparency") | Caution | Honesty shows in the specificity of the claim. If the number exists, give it; if not, drop the topic. |
| Symmetrical negation ("I'm not an X. I'm the person who...") | Caution dressed as polish | Break the mirror and state the capability in its own terms. |
| Intensifier before a superlative ("truly one of the best") | Caution: the writer doesn't trust the claim | Lay the evidence, then state the superlative flat. |
| Made-up comparisons ("most strategists stop at the deck") | Likely word: common in marketing copy | Compare only against a named competitor, a real number or a stated baseline. |
| Tells multiplying in long pieces | Drift | Draft in sections, write the final version in a fresh chat, and run the edit pass separately from drafting. |
| One sentence shape repeated down a document | Drift | Vary sentence shapes with intent. Only reading the whole document catches this. |
| Metaphors that point at nothing, and vague places ("the table", "the room") | Likely word: they sound vivid | Name the real place, or build the place in the sentence itself. A metaphor stays only if removing it collapses the meaning. |
| A metaphor tacked onto a sentence that already made its point, two metaphors in a row, or a fortune-cookie line that sounds deep and explains nothing | Pleasing raters: it looks crafted | One image per idea, found before the claim. If the reader would stop to admire it, cut it. |
| Abstractions that name no thing, and empty phrasing ("make people feel something", "drive alignment") | Pleasing raters: summarizing reads as insight | Write the specific version of what the phrase reaches for. |
| Terminal abstraction ("the work travels", "the method holds") | Pleasing raters: it sounds like a landing | Give the verb an object and a result, or cut the sentence. Swapping synonyms reproduces it. |
| Empty bridges ("at once", "the same" with nothing it's the same as, "bridge the gap") | Likely word | Cut the bridge or name the relationship. |
| Choppy prose: fragments, or runs of short separate statements | Likely word, plus "short sentences" rules applied to published writing | Join sentences that belong together with because, so, but, yet or which. Keep short runs for stacked proof points. |
| Long, flat prose: in a letter, sentences that average more than 24 words, or fewer than one in ten of 10 words or fewer | Drift: the model copies its own sentence length, and the rules against choppy prose push it long | Split a long sentence where it holds two facts, so one stands short. Use short sentences for proof points and longer ones for narrative, as voice.md says. |
| An opener that points back: a sentence that starts on "That", "This" or "It" and a verb, and refers to the sentence before instead of naming the thing ("That deliverable is a document...", "This is what I meant") | Likely word | Name the thing as the subject, or join the sentence to the one before. |
| A short flat line right after a long one ("An app isn't one product.", "Don't overthink it."), in the same paragraph or opening the next | Pleasing raters: it sounds like a landing | Fold the point into the long sentence, or cut the short line if it only restates it. |
| A claim about skills or results that names nothing ("I have also built strong data visualization skills", "I've shared findings with many different audiences") | Caution, and the likely word | Name the tool, the number, the audience or the example the user gave, or cut the claim. |
| Empty assertions ("made a case I agree with", "this matters") | Pleasing raters: announcing a stance looks decisive | Put the content in the sentence and cut the announcement. |
| Rhetorical questions that restate the last sentence | Pleasing raters: reads as engaging | Cut the question and keep the concrete sentence. |
| Intensifier labels ("ironically", "entirely", "completely") | Pleasing raters: they tell the reader how to feel | Show the irony with the facts, or cut the label. |
| Faux shared wink ("We've all been there, right?") | Pleasing raters | Name the thing being winked at, or cut it. |
| Timing-brag flourish ("years before the role had a title") | Pleasing raters | Cut the timing clause and keep the claim. |
| Endings anchored in the person ("without any authority"), in the organization's flaws ("where nobody wanted change") or in nothing ("built four teams") | Pleasing raters: drama in place of an outcome | End every claim about the work on a result the user gave, or on the claim itself. Keep it as big as the user said it was. |
| Drawn-out or inverted sentences ("X is the part I have to learn") | Likely word: imitates reflective prose | Put the subject and verb first. |
| Hanging references ("gave the hours back", "help their math teachers do what ours did") | Likely word: compressed stock phrasing | Say who did what and what it got, or say the same point in fewer words: "do the same". |
| A "what" clause standing in for a noun ("by what the unit tests showed", "what your second shift would need") | Likely word | Name the thing ("the unit test results"), or put the actor first ("the unit tests showed which students to regroup"). |
| The indirect claim, a sentence that points back instead of saying the thing ("that is the work I have done", "and that's the coaching I'd bring", "which is the work I've done since 2021") | Likely word | Make the thing the subject: "I've done that work", "I'd bring that coaching". Contract where speech would. |
| "Carry" as a verb for an abstraction ("a theme every section carries"), and "read" as a noun ("my read on this", "the client read") | Likely word | Say what the thing does ("one theme in every section"), and use the verb ("reading the client"). Literal uses pass ("each beam must carry 40 tons"). |
| "The more X, the more Y" | Pleasing raters: it sounds like an insight | Say the relationship directly, with the number or the cause. |
| Passive career verbs ("contributed to", "helped develop", "was involved in") and inflated ones ("authored", "architected") | Caution, and the likely word | Built, founded, led, wrote, designed, named, reversed. |
| Latinate defaults ("utilize", "demonstrate", "commence") and "leverage" | Likely word: corporate text is everywhere | Use the plain word: use, show, start. "Leverage" as a verb blocks; the noun and the finance sense pass. The other words warn, because some audiences speak that way. |
| Borrowed frameworks used as your own ("organizational antibodies", "jobs to be done") | Likely word | Find the original version, or attribute it. |
| Internal method names and in-house jargon on anything a reader sees | The writer's shorthand leaking | Describe what the method does in plain words. Recognizable client and brand names stay. |
| Compression tells: first-person verbs turned into participles, periods turned into colons and fragments, place names cut first | Likely word, under a length limit | Cut from lists and proof points, never from voice. |

## Cousins to watch

When a tell comes out, the model reaches for the nearest substitute. These count as the same tell:

- Em dash → a semicolon or colon standing in for a dramatic dash. A semicolon that joins two related clauses is fine.
- "Not X, but Y" → "Less X, more Y" (U12), "This isn't X. It's Y." (U10), "X? No. Y.", "Forget X. Y."
- A list of three → two mirrored clauses.
- A summary line → a rhetorical question at the end.
- A hedge word → "arguably" (S13), "in many ways" and "to some extent" (U11).
- A made-up comparison → "unlike many", "where others" (S01).
- A terminal abstraction → the same construct with a synonym ("the method endures").

## Allowed

Quotes, names, numbers and technical terms exactly as given, even when they hold a word a rule blocks: a quote that says "really", a company called Seamless, a "statistically significant" result. "Rather than" and "instead of". "Roughly". Contractions everywhere, and the uncontracted form when the emphasis is deliberate. "Didn't", "don't", "can't", "left" and "gone" about ideas and things. A semicolon joining related clauses, and a colon before a list. A specific three-item list inside a sentence. A short run of sentences that stacks proof points. A shared cultural reference used as a simile. An en dash in a number range, like "2019–2021", and an en dash or hyphen in a date or time range outside a sentence, like a resume's "Mar 2019 – Present" line or "Hours: Mon–Fri". Thanks for a specific meeting or call at the start of a follow-up letter. An ellipsis for a spoken pause: "It's beautiful, sure… but what are we supposed to do with all that?"
