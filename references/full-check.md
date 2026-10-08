# The full check

This is every rule `scripts/check_voice.py` checks, written out so the check runs by reading. Read it only when the script can't run; when it can, the script finds the same items, and each hit prints the ID below. Check with the surface that matches the piece: `letter` for letters and outreach, `blurb` for referral blurbs, `linkedin` for posts, About sections and headlines, `resume`, or `general` for proposals, think pieces, brand narratives and workshop materials. A run without `--surface` uses `general`. Rules marked with a surface only apply there.

Read the draft the way the script does:

- Join lines that wrap inside a paragraph or a list item, so a phrase split by a line break still counts.
- Skip the words inside quotation marks, double or single, straight or curly, and inside block quotes. A writer can't change what a source said.
- Skip names. A capitalized word in the middle of a sentence is usually a name ("Synergy Health", "Google Drive"), and so is a capitalized pair at the start of a sentence ("Robust Intelligence", "Foster + Partners"). Words joined by + or & are a name anywhere, even in a heading in title case ("Why Foster + Partners"). A word in capitals, a hyphenated word and a word ending in -ed or -ing are never names, so "Spearheaded Salesforce rollout" still counts. In a title written in title case, capitals don't mark names. A capital after a colon starts a sentence ("Goal: Empower teams").
- Count every dash character as a dash. Keep the en dash in a number range ("2019–2021"), and an en dash or a hyphen between two range ends outside a sentence, as R01 says. A divider of three or more hyphens, stars or underscores, with or without a mark at either end, is a rule line, not a dash: a cut line on a handout ("✂ - - - -") passes.
- Skip label lines ("Budget: $40K.") for the colon check, S04.
- Skip code blocks and inline code. Headings, list items, quotes, tables and label lines don't count toward the checks on sentence length.

A block that lands on something the order in SKILL.md protects stays: a quote, name, number or technical term exactly as given, or something the user asked for. Pass the user's names and technical terms to the script with `--keep`, separated by commas (`--keep "Seamless,statistically significant"`), and it skips them anywhere, including where one opens a sentence. When the user's own instructions, samples or guide allow what a rule blocks, like dashes, that rule is off for the piece. Run the script with `--skip` and the rule's ID (`--skip R01`, or several separated by commas), and tell the user which rules are off.

## Blocks: rewrite every hit

**Punctuation and construction**
- R01: A dash used as a dash: the em dash, the en dash, the figure dash, the minus sign, the two-em and three-em dashes, the small em dash, a spaced hyphen, or a double or triple hyphen typed as one. An en dash or hyphen between two numbers passes anywhere ("2019–2021", "pages 10 - 12"), and so do a command flag like `--surface`, a dash standing in for an empty table cell and a bullet. Outside a sentence, an en dash or a single hyphen between two range ends passes too. Range ends are numbers and years; months, days of the week and seasons, written out or short ("Mar", "Sept.", "Mon", "Fall"); a time like "8 a.m."; and "Present", "Current" or "Now", with or without a colon after them ("Mon–Fri: 9 a.m. to 5 p.m."). Outside a sentence means in a heading or a table, on a label line whose value reads like a title ("Hours: Mon–Fri, 8 a.m.–5 p.m."), or on a line that doesn't end like a sentence and has no lowercase word but small ones like "of" and "and", like a resume's date line ("Nurse Manager, Emergency Department | Mar 2019 – Present", "Jun 2014 – Feb 2019"). On a line split by bars or middle dots, only the part that holds the range has to read that way ("Mar 2019 – Present · 5 yrs"). A range inside a sentence still blocks ("I've run the unit since Mar 2019 – Present."; write "since March 2019"), and so does a line that runs on into a sentence on the next line. An em dash blocks everywhere, a date line included. R01 stays a block as the skill's house style; when the user's own samples or guide use dashes, turn it off with `--skip R01`.
- R02: "Not just / simply / merely X, but Y", a trailing ", not just X", "is not just", "isn't just" and "doesn't just". "Not only X, but Y" warns under R02W, and the contracted "It's not just" blocks under S17.
- P01: "It's not about X", "isn't about" and "It's not X, it's Y". The two-sentence form warns under U10.
- R24: "I'm not a/an X. I'm the/a..."
- R29: A sentence that ends on "the work", "method", "practice", "thinking", "framework", "approach", "system", "discipline", "model" or "process", followed by "travels", "holds", "endures", "carries", "lasts", "scales", "transfers", "persists", "stands" or "remains".
- R45: "...is the part/piece/thing I...", "has taught me where/that/what" and "what I've learned is".
- R30: "The more X, the more Y."
- S04: A second colon reveal in the same piece, meaning a colon followed by three words or fewer that end the sentence. The first one only warns. Label lines, a colon that opens a quote and a numbered list after a colon don't count.
- S16: A question reveal at the start of a sentence, answered at once: "The result? A 40% drop", "The secret? Consistency." The script checks these words: "result", "answer", "reason", "catch", "kicker", "twist", "secret", "outcome", "verdict", "takeaway", "upshot", "payoff", "lesson", "truth", "difference", "fix", "solution", "problem" and "bottom line".

**Openers and closers**
- R03 (letter): "I'm writing to express / apply / share / highlight / submit / convey".
- R04 (letter): A first body line that starts "Thank you for". Thanks for a specific meeting or call in a follow-up passes: "Thank you for meeting with me on Tuesday", "Thank you for the call".
- R05 (letter): "My name is...". Open on the reader's world, never on your name.
- S05 (letter): "I hope this email finds you well", "I hope this finds you well" and their kin.
- R08: A self-description on the draft's first line. In a letter that's the first body line, in a resume the first line of 60 or more characters, and anywhere else the first line after any title. It blocks "As a/an" and the next word ("As a founder"), "I am a/an" followed within three words by a self-praising word ("passionate", "results-driven", "highly", "experienced"), "Experienced", "Proven" or "Seasoned" followed by a role ("Experienced product manager"), "Results-driven" and "Results-oriented", and "A highly / dynamic / passionate / strategic / creative / results-[anything]" followed by a role. "As a result", "As an example", "As a rule", "As a consequence", "As a reminder", "As a whole", "As a matter of fact", "As a first step" and "As a side note" pass, and so do "Experienced riders take the north loop" and "Proven reserves fell".
- R07 (resume, linkedin, blurb): A line that starts "Through extensive / years / fifteen / a decade...".
- R33 (letter, blurb): "Thank you for your (time and) consideration", "thank you for your/the time", "grateful and humbled", "humbled", "look forward to the opportunity / speaking / hearing / discussing / meeting / talking" and "would be honored". On LinkedIn, "humbled" blocks under S08.
- S06 (linkedin): Engagement bait: "Agree?", "Thoughts?", "Drop a comment", "comment below" and "Who else has seen this".
- S07 (linkedin): "Thrilled / excited / delighted to announce / share".
- S08 (linkedin): "humbled".
- S10: Chatbot closers: "I hope this helps", "Let me know if you'd like (me to / any / more / another / a different / further)..." and "Let me know if you need / want / have any (other / further / more) changes / adjustments / edits / revisions / tweaks / help / questions". A plain ask passes: "Let me know if you're free Tuesday."
- S11: "Certainly!"
- R25: "If we wait", "before someone else", "someone else figures / notices / will", "the window is closing", "now is the time", "the time is now" and "the opportunity is now".
- P06: "In today's", "In a world where" and "In an era of" at the start of a sentence.
- P07: "Whether you're".
- P09: "Speaks for itself" and "results follow".
- S02: "In summary", "In conclusion", "To sum up", and "Overall," at the start of a sentence or a list item. "Moreover", "furthermore" and "ultimately" warn under S02W.
- S12: "Let that sink in" and "At its / their / our / my / his / her core".
- S14: "Notably," at the start of a sentence.
- U01: Signposting: "Here's why / what / how / the thing / the kicker / the catch", "this matters", "let me explain", "the bottom line is" and "make no mistake". It moved from the candidates in 1.5, when AI drafts were found using it about 26 times as often as human writers.

**Words**
- R20: "Actually" at the start of a sentence. Inside a sentence it warns under R20W.
- R10: "Significant" or "substantial" followed by "improvement", "growth", "increase", "impact", "results", "gains" or "value".
- P03: "robust" and "seamless(ly)". Statistics terms pass: "robust standard errors", "robust regression", "robust estimates", "robust inference", and "robust to" ("robust to outliers"). "Significant", "powerful" and "comprehensive" warn under P03W.
- P04: "unlock", "empower", "elevate", "streamline" and "foster", with their -s, -ed and -ing forms. "Foster" passes before home, care, parent, child, family, kids, mother, father or sibling ("foster care"). "Elevated" passes for height and for measurements ("an elevated boardwalk", "elevated blood pressure"), and "elevate" passes for a body part ("elevate the injured leg").
- R26: "leverage synergies", "synergy" ("synergism" and "synergistic" pass), "drive alignment", "unlock value", "deliver impact", "make people feel something" and "make resonance inevitable".
- R27: "bridge the gap".
- R28: "At once" as filler between two qualities: "at once bold and practical", "at once a promise and a warning". "Left at once" and "all three went off at once" pass.
- R31: "magic ingredient(s)", "giant strides", "one moment at a time", "a fire within", "insatiable desire", "fundamental mission", "help others achieve greatness".
- R32: "strategy hacker", "imagineer" and "highly competitive".
- R34: "We've all been there".
- R35: "impactful" and "high-impact".
- R37: "truly", "incredibly", "absolutely", "really", "extremely", "deeply", "genuinely", "hugely" or "remarkably" in front of "one of", "the most / best / fastest / highest / first / largest / biggest", "game-changing", "innovative", "excited", "proud", "unique", "exceptional" or "transformative".
- R48: "results-driven", "proven track record", "passionate about", "seasoned" before a person ("a seasoned marketer"; "seasoned to taste" passes), "dynamic professional", "detail-oriented", "team player", "go-getter", "thought leader" ("thought leadership" is fine), "spearhead" and "wheelhouse".
- R06: "dynamic, results-oriented", "results-oriented", "a passion for (human-centered) design" and "broad cross-industry experience".
- P05: "world-class", "best-in-class", "holistic" and "cutting-edge".
- P08: "can help", "may be able to" and "could potentially" when the writer, the firm or the product is the subject: "we can help", "our platform can help", "this tool could potentially". "A mother can help a child adapt" passes.
- P12: "Leverage" as a verb: "we leverage", "to leverage", "leveraging", "leveraged our". The noun passes ("our negotiating leverage"), and so does the finance sense: debt leverage, financial leverage, operating leverage, highly leveraged, over-leveraged, leverage ratio and leveraged buyout.
- S03: "delve", "rich tapestry", "testament to", "it's worth noting", "it's important to note", "let's dive", "deep dive", "game-changer" and "game-changing". A real tapestry and a real dive pass.
- S09: "proven approach / process / method / methodology / framework / formula / system" and "rigorous process".
- S13: "arguably".
- S15: "multifaceted", "transformative" and "valuable insights". "Transformative use", the legal term, passes.
- S17: "It's not just" and the other contracted forms: "that's not just", "we're not just", "I'm not just".
- R18: "from scratch".

**About the work and the writer**
- R11: "authored" and "architected" as verbs. Use wrote, built, designed or named. The nouns are fine, and so is authoring a bill, an amendment or other legislation.
- R12 (letter, resume, linkedin, blurb): "contributed to", "helped (to) develop", "was involved in" and "played a role".
- R16: "without (any) authority / institutional support", "swear word", "had to do it myself", "didn't want innovation" and "treated as overhead".
- R21: "years / a decade / decades / months before the / it / anyone / that / this", "before the role had a title/name", "before it/that/this had a name/title" and "before... was a thing".
- R22: "lands with" and "will / can / to land with", "stood up a/an/the", "stand(s/ing) up a/an/the", "running that loop" and "on the read". Standing up passes, and so does land as a noun ("the same land with", "many lands with").
- R23: "I state that plainly", "I'll / I will be candid / straight / honest / direct / frank / blunt", "to be honest / candid / frank", "candidly", "rather than estimate", "I won't pretend", "in the interest of honesty / candor / transparency" and "full disclosure".
- R42: "gave/give the hours/time back", "the work that wins" and "what wins". Say who did what, and what it produced for whom.
- R46: "Read" as a noun: a, an, the, my, his, her, our, your, this, that, one, honest, deeper, deep, closer, close, quick, cold, full, initial, first, second, good, hard, clear, client, market, community, business, behavioral, consumer, careful, fast or strong in front of "read", plus "reads" as a plural noun. It passes when "read" is a verb with an object ("the client read the brief"), while "a close read of the data" still fails. Use the verb: "reading the client."

**Names and internal vocabulary**
- Internal method names and in-house jargon on anything a reader sees. No pattern can know every name, so catch these by reading.

## Warnings: fix each one or clear it with a stated reason

- R13: "utilize", "demonstrate", "commence", "constructed" and "constructing". Use the plain word unless the audience speaks this way.
- R19: "organizational antibodies", "blue ocean" and "jobs to be done". Attribute them, or find the original version.
- R44: "The room" or "the table" standing for the people in it, in these idioms: someone, everyone, anyone, no one, nobody, people, a person, a voice, the smartest person or the only one "in the room" ("I hope someone in the room asks"); "the room" after keep, work, own, hold, win, lose or read, in any tense ("kept the room calm", "read the room"); "the room went / fell / grew / got / turned / laughed / knew / felt / agreed" and "the room was silent / quiet / electric / tense"; "a seat at the table"; "bring" something "to the table", in any tense and with up to six words between ("brings ten years of payroll experience to the table"); "standing in the room"; and "the room where". A real room or table passes: "the emergency room", "a pivot table", "the table below", "set the room in tables of four". Other vague places ("a demo with the buyer in the room") go by reading, under the row for vague places in tells.md.
- R02W: "Not only X, but Y" and a trailing ", not only X". It passes when both halves do real work.
- R20W: "Actually" inside a sentence. Keep it only when it means "in fact" and the sentence needs it.
- R39: "carry", "carries", "carried" and "carrying" as a verb, except "carry-on" and "carryover". Say what an abstraction does instead. Literal uses pass by reading: "each beam must carry 40 tons", "the store will carry the line".
- R40: "That is the / what / where / how / why / exactly / precisely" used as an indirect claim. On letters, the contracted "that's" and "this is" warn under V11.
- P02: "simply" and "literally". Keep them only when they change the meaning; "simply because" is plain English.
- P03W: "significant(ly)" on its own, "powerful" and "comprehensive". Plain meanings and terms pass by reading: "a comprehensive budget", "significant harm", "a comprehensive metabolic panel". "Statistically significant" never warns.
- P11: "drive", "drives" and "driving" as fluff verbs, before a business object ("drive growth", "driving engagement", "drive the main work", "drive it forward"). The noun and a literal drive pass ("the spring food drive", "drive home").
- S01: "most people / companies / strategists / brands / founders / leaders / firms / agencies / designers / marketers / insight work", "unlike many" and "where others". It passes as a real comparison against a named competitor or a measured baseline.
- S02W: "moreover", "furthermore" and "ultimately". Inside a sentence, "ultimately" usually means "in the end" and passes by reading.
- S04: The first colon reveal in a piece. Keep it only if it lands.
- V03: An average under 14 words a sentence, or more than 35% of sentences at 10 words or fewer.
- V04: More than half the paragraphs are one sentence long, in a piece of four or more paragraphs.
- V07 (letter, resume, linkedin, blurb): A first-person sentence that claims a skill, a strength or a range ("skills", "experience", "expertise", "a wide range", "many different", "consistently", "strong") and names no number, no name and no bracket for one: "I have also built strong data visualization skills."
- V08: A sentence of six words or more that comes back word for word in the same piece, compared in lower case with the punctuation dropped. It warns once for each repeat, so a sentence said three times warns twice. Paragraphs, list items and label lines count, and so do words inside quotation marks, since the writer chooses to quote a line twice. Headings, tables, block quotes and code don't. A title or an initial doesn't end a sentence ("Mr. Speaker", "John A. Notte"). A sentence may move from one piece to another when it states the same fact and is still true; inside one piece it appears once. Keep a repeat only for a stated reason, like a refrain or a line the user asked for in two places.
- V09 (letter): Sentences that all run long. Read the body only: the paragraphs from the greeting to the sign-off, or from the first line of 60 characters or more when there's no greeting, with bracketed slots taken out. In a body of 200 words or more, it warns once when fewer than 10% of the sentences run 10 words or fewer, or when they average more than 24 words. Fix it by splitting a long sentence where it holds two facts, so one stands short. A short line that only restates the long one before it trips V06 instead, and V03 warns at the other end, past 35% short or under an average of 14.
- V10 (letter): "What" followed by "the", "your", "our", "their", "my", "his", "her", "its", "this", "that", "these" or "those", one to three more words and a verb, standing in for the noun it describes: "by what the unit tests showed", "what your second shift would need", "what their students have learned". The verbs are show, do, need, mean, find, want, get, have and make in their usual forms, with "would", "will", "could", "might", "must", "can" or "should" allowed before them. "Said", "says", "told" and "tell" don't count, so "write down what the sign told you" passes, and neither do bracketed slots ("[What the survey found]"), headings, tables and label lines. On letters each one warns; elsewhere V10 warns by rate, below. Name the thing ("the unit test results"), or put the actor first ("the unit tests showed which students to regroup").
- V11 (letter): "That's" or "this is" followed by "the", "what", "how", "why", "where" or "exactly", at the start of a sentence, after a semicolon or a colon, or after "and", "but" or "so", pointing back at the sentence before instead of saying the thing: "and that's the coaching I'd bring", "That's the work I'd lead with your 30 math teachers", "This is the role I want". Make the thing the subject: "I'd bring that coaching". The written-out "that is the..." warns under R40 on every surface, and ", which is the work I've done" goes by reading, under the indirect claim in tells.md.
- The U rules below are candidates. They warn until there's evidence that AI drafts use them far more often than human writers do; then they can become blocks.
- U02: "sort of".
- U03: "navigate", "realm", "pivotal", "crucial", and "landscape" except in "landscape architect" or "landscape architecture".
- U04: Exclamation marks.
- U05: "We'll / I'll / we will aim / try / strive / endeavor to". Say what you'll do, and name a real risk separately.
- U06: "Additionally," at the start of a sentence.
- U07: "notes that" and "explains that" where a person would write "says".
- U08: "meticulous(ly)", "innovative", "groundbreaking" and "showcase", with its -s, -d and -ing forms. "A groundbreaking ceremony" passes.
- U09: "underscore", with its -s, -d and -ing forms, "intricate(ly)", "vibrant" and "vibrancy".
- U10: "This isn't X. It's Y." across two short sentences, and its past tense, "It wasn't X. It was Y."
- U11: "in many ways" and "to some extent".
- U12: "Less X, more Y", including "less about X and more about Y".
- U13: A trailing phrase that states the lesson: a comma, then "highlighting", "underscoring", "showcasing", "demonstrating", "reflecting", "reinforcing", "emphasizing", "illustrating", "signaling", "cementing", "solidifying", "proving" or "reaffirming", then "the", "its", "their", "our", "his", "her", "a", "an", "how", "that" or "why" ("The program cut costs, highlighting the value of early planning").
- U14: "When it comes to" and "at the end of the day".
- U15: "enhance", with its -s, -d and -ing forms, and "unprecedented".
- U16 (linkedin): Three or more hashtags in a row. One or two that name a real event or community are fine.
- U17 (linkedin): A line that starts with an arrow or an emoji as a bullet ("→ The buyer isn't the user."). An arrow inside a sentence passes.
- U18 (linkedin): Engagement-bait closers: "I'd / we'd / I would love to hear / know / learn" (but "we'd love to hear from you" in a hiring post passes), "curious how others...", "what's worked for you", "share your thoughts / experience" and "how does your team handle / approach / keep...".

## Rate warnings: once per draft

Good writers use these habits too, so a single use means nothing. Each one warns once per draft, when the draft has at least two hits and runs above the rate that more than nine in ten pieces of edited human writing stay at or under. Rates are per 1,000 words of the draft, outside code, and quotes and names are skipped as everywhere else.

- R09: Above 3.5 per 1,000 words, the hedge words "very", "really", "quite", "fairly", "somewhat", "a bit", "kind of" and "rather". "Very" after the, this, that or a possessive passes ("the very first permit"), and so do "fairly" meaning "justly" ("paid fairly and on time"), "the kind of park", "rather than", "would rather" and "or rather". A booster before a superlative ("truly one of the best") still blocks under R37.
- R41: Above 19 per 1,000 words, long forms where speech would contract: "that is", "it is", "I have", "I am", "I would", "I will", "I had", "do not", "does not", "did not", "cannot", "is not", "are not", "was not", "were not", "there is", "here is", "what is", "has not", "have not", "had not", "will not", "would not", "could not", "should not", "he is", "she is", "we are", "they are", "you are", "we have", "they have", "you have", "we will", "we would" and "let us". Keep the long form for deliberate emphasis.
- P10: Above 1.5 per 1,000 words, "just". Keep it only when it changes the meaning.
- V01: Above 8 per 1,000 words, lists of three ("roads, parks, and trails"). A list of four or more items isn't a list of three, so nothing counts in "roads, bike lanes, bus shelters, and street trees". The script tells the two apart from the comma before the three items. When a plain item sits on each side of that comma, the list is longer than three. The three still count when that comma closes an opening phrase ("In March,", "However,", "Last year,", "Founded in 1920,") or an earlier list ("...and writers,"). They count too when the words after it start a clause or a phrase ("and the trails", "we shipped apples", "showing wit", "ideally with schools"), hold a preposition the three items hang off ("a row for dashes, colons and brackets") or run to six words or more while the next item opens on a different word. The script can't read every case. A longer list still counts when an item opens with an -ing or -ed word ("hiring plans") or a preposition ("in Ohio, in Maine, in Iowa, or in Texas"), and it passes by reading. A list of three after a name between commas ("My manager, Dana, likes...") is missed, and it counts by reading. A list passes when each item is specific and does work.
- V02: At least two runs and above 2.5 runs per 1,000 words, where a run is three or more sentences of 10 words or fewer in a row. A run passes when it stacks proof points.
- V05: Above 2.5 per 1,000 words, openers that point back: a sentence that starts on "That", "This", "These" or "Those" with "is", "was", "means", "gives", "makes" or a like verb ("That's", "This is", "That gives us"), on one of them with a noun and a verb ("That deliverable is", "That facilitation will"), or on "It's", "It is" or "It was" before "a", "an", "the", "what", "this", "that", "how", "why", "where" or "who" ("It's an understandable instinct"). Human writers use this shape about as often as AI drafts do, so it warns only above their rate. "It's hard to say" passes. Fix it by naming the thing.
- V06: Above 5 per 1,000 words, short flat lines after long ones: a sentence of three to eight words that ends on a period, right after a sentence of 15 words or more, in the same paragraph or at the start of the next one. A short line passes when it adds a fact the user gave instead of restating the line before.
- V10: On every surface but letters, at two hits or more in a draft, "what the X did" standing in for a noun, as V10 above describes it. Edited human writing has about three of these in every 100,000 words and never two in one piece, so the rate nine in ten pieces stay at or under is 0, and the two-hit minimum decides.
