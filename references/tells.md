# Tells and fixes

This file holds every rule the skill enforces. When a rule changes, update this file and `scripts/check_voice.py` together, and log it in `CHANGELOG.md`.

## Structural tells (the edit pass catches these)

Four root causes sit behind every row: the **likely word** (the model picks the common option), **pleasing raters** (tuning rewarded writing that looks clear, complete and polished), **caution** (training against overclaiming) and **drift** (in long pieces the model copies its own recent text).

| Tell | Main cause | How to steer it |
|---|---|---|
| Stock phrases and safe adjectives | Likely word | Replace with the fact: a name, number or what happened. Generic words fill gaps where facts are missing. |
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
| One sentence shape repeated down a document | Drift | Vary sentence shapes with intent. Only a full read of the document catches this. |
| Metaphors that point at nothing, and vague places ("the table", "the room") | Likely word: they sound vivid | Name the real place, or build the place in the sentence itself. A metaphor stays only if removing it collapses the meaning. |
| A metaphor tacked onto a sentence that already made its point, two metaphors in a row, or a fortune-cookie line that sounds deep and explains nothing | Pleasing raters: it looks crafted | One image per idea, found before the claim. If the reader would stop to admire it, cut it. |
| Abstractions that name no thing, and empty phrasing ("make people feel something", "drive alignment") | Pleasing raters: summarizing reads as insight | Write the specific version of what the phrase reaches for. |
| Terminal abstraction ("the work travels", "the method holds") | Pleasing raters: it sounds like a landing | Give the verb an object and a result, or cut the sentence. Swapping synonyms reproduces it. |
| Empty bridges ("at once", "the same" with nothing it's the same as, "bridge the gap") | Likely word | Cut the bridge or name the relationship. |
| Choppy prose: fragments, or runs of short separate statements | Likely word, plus "short sentences" rules applied to published writing | Join sentences that belong together with because, so, but, yet or which. Keep short runs for stacked proof points. |
| Empty assertions ("made a case I agree with", "this matters") | Pleasing raters: announcing a stance looks decisive | Put the content in the sentence and cut the announcement. |
| Rhetorical questions that restate the last sentence | Pleasing raters: reads as engaging | Cut the question and keep the concrete sentence. |
| Intensifier labels ("ironically", "entirely", "completely") | Pleasing raters: they tell the reader how to feel | Show the irony with the facts, or cut the label. |
| Faux shared wink ("We've all been there, right?") | Pleasing raters | Name the thing being winked at, or cut it. |
| Timing-brag flourish ("years before the role had a title") | Pleasing raters | Cut the timing clause and keep the claim. |
| Endings anchored in the person ("without any authority"), in the organization's flaws ("where nobody wanted change") or in nothing ("built four teams") | Pleasing raters: drama in place of an outcome | End every claim about the work on what it produced for the reader. |
| Drawn-out or inverted sentences ("X is the part I have to learn") | Likely word: imitates reflective prose | Put the subject and verb first. |
| Hanging references ("gave the hours back") | Likely word: compressed stock phrasing | Say who did what and what it got. |
| The indirect claim ("that is the work I have done") | Likely word | Say it directly: "I've done that work." Contract where speech would. |
| "Carry" as a verb for an abstraction ("a theme every section carries"), and "read" as a noun ("my read on this", "the client read") | Likely word | Say what the thing does ("one theme in every section"), and use the verb ("reading the client"). A literal object can still be carried. |
| "The more X, the more Y" | Pleasing raters: it sounds like an insight | Say the relationship directly, with the number or the cause. |
| Passive career verbs ("contributed to", "helped develop", "was involved in") and inflated ones ("authored", "architected") | Caution, and the likely word | Built, founded, led, wrote, designed, named, reversed. |
| Latinate defaults (utilize, demonstrate, commence) and "leverage" | Likely word: corporate text is everywhere | Use the plain word: use, show, start. "Leverage" always blocks except in its finance sense. The other words warn, because some audiences speak that way. |
| Borrowed frameworks used as your own ("organizational antibodies", "jobs to be done") | Likely word | Find the original version, or attribute it. |
| Internal method names and in-house jargon on anything a reader sees | The writer's shorthand leaking | Describe what the method does in plain words. Recognizable client and brand names stay. |
| Compression tells: first-person verbs turned into participles, periods turned into colons and fragments, place names cut first | Likely word, under a length limit | Cut from lists and proof points, never from voice. |

## The full check

This is every rule the skill enforces, written out so the check runs by reading, with no tools. When code can run, `scripts/check_voice.py` finds the same items faster, and each hit prints the ID below. Run it with the surface that matches the piece: `letter` for letters and outreach, `blurb` for referral blurbs, `linkedin` for posts, About sections and headlines, `resume`, or `general` for proposals, think pieces, brand narratives and workshop materials. Rules marked with a surface only apply there. Code blocks and inline code are skipped, and headings, list items, quotes and tables don't count toward the choppiness checks.

### Blocks: rewrite every hit

**Punctuation and construction**
- R01: Any em dash, or a double hyphen typed as one.
- R02: "Not just / only / simply / merely X, but Y", a trailing ", not just X", "is not just", "isn't just" and "doesn't just".
- P01: "It's not about X", "isn't about" and "It's not X, it's Y".
- R24: "I'm not a/an X. I'm the/a..."
- R29: A sentence that ends on the work, method, practice, thinking, framework, approach, system, discipline, model or process, followed by travels, holds, endures, carries, lasts, scales, transfers, persists, stands or remains.
- R40: "That is the / what / where / how / why / exactly / precisely" used as an indirect claim.
- R45: "...is the part/piece/thing I...", "has taught me where/that/what" and "what I've learned is".
- R30: "The more X, the more Y."
- S04: A second colon reveal in the same piece, meaning a colon followed by three words or fewer that end the sentence. The first one only warns.

**Openers and closers**
- R03 (letter): "I'm writing to express / apply / share / highlight / submit / convey".
- R04 (letter): A first body line that starts "Thank you for".
- R05 (letter): "My name is...". Open on the reader's world, never on your name.
- R08: A first line that starts "As a/an", "I am a/an", "Experienced", "Results-driven", "Proven", "A highly", "Seasoned", or "A dynamic / passionate / strategic / creative / results...". In a letter this checks the first body line. Elsewhere it checks the start of any line.
- R07 (resume, linkedin, blurb): A line that starts "Through extensive / years / fifteen / a decade...".
- R33 (letter, blurb): "Thank you for your (time and) consideration", "thank you for your/the time", "grateful and humbled", "humbled", "look forward to the opportunity / speaking / hearing / discussing / meeting / talking" and "would be honored".
- R25: "If we wait", "before someone else", "someone else figures / notices / will", "the window is closing", "now is the time", "the time is now" and "the opportunity is now".
- P06: "In today's", "In a world where" and "In an era of".
- P07: "Whether you're".
- P09: "Speaks for itself" and "results follow".
- S02: "In summary", "In conclusion", "To sum up", "Ultimately", "Moreover", "Furthermore", and "Overall," at the start of a sentence.

**Words**
- R09: very, really, quite, fairly, somewhat and a bit. "Kind of" when it hedges, but not "the kind of". "Rather", except in "rather than" and "would rather".
- R20: actually.
- P02: simply and literally.
- R10: "Significant" or "substantial" followed by improvement, growth, increase, impact, results, gains or value.
- P03: robust, comprehensive, powerful, seamless(ly), and "significant" on its own.
- P04: unlock, empower, elevate, streamline and foster.
- R26: "leverage synergies", synergy, "drive alignment", "unlock value", "deliver impact", "make people feel something" and "make resonance inevitable".
- R27: "bridge the gap". R28: "at once" as filler.
- R31: "magic ingredient(s)", "giant strides", "one moment at a time", "a fire within", "insatiable desire", "fundamental mission", "help others achieve greatness".
- R32: "strategy hacker", imagineer and "highly competitive".
- R34: "We've all been there".
- R35: impactful and high-impact.
- R37: truly, incredibly, absolutely, really, extremely, deeply, genuinely, hugely or remarkably in front of "one of", "the most / best / fastest / highest / first / largest / biggest", game-changing, innovative, excited, proud, unique, exceptional or transformative.
- R48: results-driven, "proven track record", "passionate about", seasoned, "dynamic professional", detail-oriented, "team player", go-getter, "thought leader" ("thought leadership" is fine), spearhead and wheelhouse.
- R06: "dynamic, results-oriented", results-oriented, "a passion for (human-centered) design" and "broad cross-industry experience".
- P05: world-class, best-in-class, holistic and cutting-edge.
- P08: "can help", "may be able to" and "could potentially".
- P12: leverage, leverages, leveraged and leveraging. The finance sense passes: debt leverage, financial leverage, operating leverage, highly leveraged, over-leveraged, leverage ratio and leveraged buyout.
- S03: delve, tapestry, "testament to", "it's worth noting", "it's important to note", "let's dive", "dive in(to)", game-changer and game-changing.
- R18: "from scratch".

**About the work and the writer**
- R11: "authored" and "architected" as verbs. Use wrote, built, designed or named. The nouns are fine.
- R12: "contributed to", "helped (to) develop", "was involved in", "played a role", and "supported" at the start of a line or after I, he, she, they or we.
- R16: "without (any) authority / institutional support", "swear word", "had to do it myself", "didn't want innovation" and "treated as overhead".
- R21: "years / a decade / decades / months before the / it / anyone / that / this", "before the role had a title/name", "before it/that/this had a name/title" and "before... existed / was a thing".
- R22: "lands with", "stood up", "stand(s/ing) up a/an/the", "running that loop" and "on the read".
- R23: "I state that plainly", "I'll / I will be candid / straight / honest / direct / frank / blunt", "to be honest / candid / frank", candidly, "rather than estimate", "I won't pretend", "in the interest of honesty / candor / transparency" and "full disclosure".

- R42: "gave/give the hours/time back", "the work that wins" and "what wins". Say who did what, and what it produced for whom.
- R39: carry, carries, carried and carrying, except carry-on and carryover. Say what the thing does. A literal object can be carried, so clear those by reading.
- R46: "Read" as a noun: a, an, the, my, his, her, our, your, this, that, one, honest, deeper, deep, closer, close, quick, cold, full, initial, first, second, good, hard, clear, client, market, community, business, behavioral, consumer, careful, fast or strong in front of "read", plus "reads" as a plural noun. It passes when "read" is a verb with an object ("the client read the brief"), while "a close read of the data" still fails. Use the verb: "reading the client."

**Names and internal vocabulary**
- Internal method names and in-house jargon on anything a reader sees. No pattern can know every name, so catch these by reading.

### Warnings: fix each one or clear it with a stated reason

- R13: utilize, demonstrate, commence, constructed and constructing. Use the plain word unless the audience speaks this way.
- R19: "organizational antibodies", "blue ocean" and "jobs to be done". Attribute them, or find the original version.
- R41: Uncontracted forms where speech would contract: that is, it is, I have, I am, I would, I will, I had, do not, does not, did not, cannot, is not, are not, was not, were not, there is, here is, what is, has not, have not, had not, will not, would not, could not, should not, he is, she is, we are, they are, you are, we have, they have, you have, we will, we would and let us. Keep the long form only for deliberate emphasis.
- R44: "Room" or "table" after the, a, that, this, any, our, your, every, one, whole or same (up to two words between), "in / into / around / across / to / at / on / from the room/table", "bring(s) to the table" and "standing in the room". It passes when the sentence itself builds the place.
- P10: just. Keep it only when it changes the meaning.
- P11: drive, drives and driving as fluff verbs.
- S01: "most people / companies / strategists / brands / founders / leaders / firms / agencies / designers / marketers / insight work", "unlike many" and "where others". It passes as a real comparison against a named competitor or a measured baseline.
- S04: The first colon reveal in a piece. Keep it only if it lands.
- V01: A list of three. It passes when each item is specific and does work.
- V02: Three or more sentences of 10 words or fewer in a row. It passes when the run stacks proof points.
- V03: An average under 14 words a sentence, or more than a third of sentences at 10 words or fewer.
- V04: More than half the paragraphs are one sentence long, in a piece of four or more paragraphs.
- The U rules below are candidates the skill's owner hasn't ruled on yet.
- U01: "Here's why / what / how / the thing / the kicker / the catch", "this matters", "let me explain", "the bottom line is" and "make no mistake".
- U02: "sort of".
- U03: navigate, realm, pivotal, crucial, and "landscape" except in "landscape architect" or "landscape architecture".
- U04: Exclamation marks.

## Cousins to watch

When a tell comes out, the model reaches for the nearest substitute. These count as the same tell:

- Em dash → a semicolon or colon standing in for a dramatic dash. A semicolon that joins two related clauses is fine.
- "Not X, but Y" → "Less X, more Y", "X? No. Y.", "Forget X. Y."
- A list of three → two mirrored clauses.
- A summary line → a rhetorical question at the end.
- A hedge word → "arguably", "in many ways", "to some extent".
- A made-up comparison → "unlike many", "where others".
- A terminal abstraction → the same construct with a synonym ("the method endures").

## Allowed

"Rather than" and "instead of". "Roughly". Contractions everywhere, and the uncontracted form when the emphasis is deliberate. "Didn't", "don't", "can't", "left" and "gone" about ideas and things. A semicolon joining related clauses, and a colon before a list. A specific three-item list inside a sentence. A short run of sentences that stacks proof points. A shared cultural reference used as a simile. An ellipsis for a spoken pause: "It's beautiful, sure… but what are we supposed to do with all that?"
