# Plainspeak Writer

Plainspeak Writer is a Claude skill for writing that reads like a sharp person wrote it. It drafts and edits specific outputs, catches the habits that make text sound machine-made, and checks every draft against more than 90 rules before you see it.

It handles these outputs:

- LinkedIn posts, headlines and About sections
- Cover letters, outreach and referral blurbs
- Proposals and civic documents
- Think pieces, articles and newsletters
- Brand narratives and personas
- Workshop decks and activity instructions

## Why AI writing sounds like AI

Three pulls cause most of it. A model picks the likely word, and the likely word is the common one, so drafts drift toward stock phrases and safe adjectives. Models are tuned on human ratings that reward text that looks clear and complete, so they summarize, restate, balance every claim and close on a tidy moral. They're trained to be careful, so they hedge and avoid taking a side. In long drafts, a model's own recent sentences guide it more than its instructions, so one slip gets copied down the page.

Plainspeak Writer answers each pull: facts replace generic words, a named reader replaces restating, a stated position replaces hedging, and a separate edit pass catches drift.

## How it works

Every piece runs through seven steps:

1. **List your facts.** Names, numbers, places, quotes and what happened, from what you give it, written down once before drafting. The piece uses only that list. The skill never invents a fact or a quote, fills one in from memory or guesses, and a fact the piece can't do without gets a bracket for you to fill.
2. **Answer four questions.** Who's reading and what the piece has to survive, what they should do or believe after, the position and its strongest objection, and how much heat the subject can take.
3. **Load the right files.** The voice guide, the format guide for the job, and any samples or brand guide you share. The skill's own sample passages load only when you share no writing of your own.
4. **Draft** from the list, in a plain, warm voice that writes toward the reader.
5. **Edit, then run the check.** The edit looks for the tells and for what the voice should produce, reads each paragraph aloud and cuts what repeats. The check finds rules that block and warnings that need a stated reason, and counts the words.
6. **Have a fresh reader check the facts.** Where Claude can start a separate agent, a reader that sees only your message, the fact list and the draft quotes anything you didn't give, and the writer cuts it.
7. **Deliver** the piece exactly as checked, with an edit log when you ask for one, and a short list of the brackets to fill.

The fact check in step 6 needs a tool that lets Claude start a second agent, like Claude Code or Cowork. Without one, Claude checks its own draft, and in testing that let a problem through in about 1 draft in 8, like a fact you didn't give or a changed quote. In plain Claude chat, check the names, numbers and quotes yourself before you use a piece.

## What's in the folder

```
plainspeak-writer/
├── SKILL.md                     the steps Claude follows
├── README.md                    this file
├── LICENSE                      MIT
├── CHANGELOG.md                 every change, newest first
├── references/
│   ├── voice.md                 where the voice sits, how it works, moves, modes, checks
│   ├── tells.md                 every tell with its cause and fix
│   ├── full-check.md            every rule the script checks, for when it can't run
│   ├── samples.md               public-domain passages and writers to study
│   └── formats/
│       ├── linkedin.md
│       ├── letter.md
│       ├── proposal.md
│       ├── think-piece.md
│       ├── brand-narrative.md
│       └── workshop.md
└── scripts/
    └── check_voice.py           optional checker with the same rules as full-check.md
```

The repository is the skill folder, so the folder name has to stay `plainspeak-writer`. Skills only load from a folder whose name matches the `name` field in SKILL.md.

## Install

Custom skills don't sync between Claude products, so install Plainspeak Writer in each one you use.

**Claude Code.** Clone the repository into your skills folder. Use `~/.claude/skills/` for every project, or `.claude/skills/` inside one project:

```bash
git clone https://github.com/roundofschatz/plainspeak-writer ~/.claude/skills/plainspeak-writer
```

**Claude.ai.** Download `plainspeak-writer.zip` from the Releases page and upload it under Skills in Settings. Custom skills need a paid plan with code execution turned on. Don't upload the file from GitHub's green "Download ZIP" button, because it names the folder `plainspeak-writer-main`, which no longer matches the skill's name. To build the zip yourself, zip the `plainspeak-writer` folder.

**Claude API.** Upload the `plainspeak-writer` folder through the Skills API.

The current steps for each product are in Anthropic's [Agent Skills documentation](https://platform.claude.com/docs/en/agents-and-tools/agent-skills).

## Use

Ask for the output you need, and give Claude the facts. For example:

> Write a LinkedIn post responding to the panel I attended. Here are my notes and the slides.

> Turn these bullet points into a proposal for a city parks department. The budget is $40,000 and the deadline is March.

> This cover letter sounds like AI. Fix it.

**To match your own voice,** share three to five passages you've written that got the result you wanted, or a voice or brand guide. Plainspeak Writer follows them on word choice, heat and rhythm in that conversation. It never saves them into the skill.

## The check

Every rule is written out in plain words in `references/full-check.md`, so Claude can run the check by reading, with no tools. When code can run, `scripts/check_voice.py` finds the same items faster, counts the words, and Claude never opens that file. It needs Python 3 and nothing else. From inside the folder:

```bash
python scripts/check_voice.py --surface linkedin draft.txt
```

Set the surface to match the piece: `letter` for letters and outreach, `blurb` for referral blurbs, `linkedin` for posts, About sections and headlines, `resume`, or `general` for proposals, think pieces, brand narrative and workshop material. A run without `--surface` uses `general`. HARD hits block the draft, and WARN hits stay only with a stated reason. Run `--list-rules` to see every rule.

The check skips words inside quotation marks and block quotes, and capitalized names in the middle of a sentence, so a source's words and a company's name inside a sentence don't count against your draft. Habits good writers share, like lists of three and the word "just", warn only when a draft uses them more than nine in ten pieces of edited human writing do. When your own samples or style guide use something a rule blocks, like em dashes, turn that rule off with `--skip R01`. Pass your own names and technical terms with `--keep "Seamless,statistically significant"`, and the check skips them anywhere, even where a name opens a sentence.

A clean check means the draft has none of the surface patterns. Whether it's good writing is still the edit pass's call.

## Contributing

Pull requests are welcome when they keep to these rules:

- **Keep it general.** No personal details, clients or private work in any file. Plainspeak Writer is a tool for anyone.
- **Build on what's here.** Change or extend a rule instead of replacing the file around it.
- **Log every change** in `CHANGELOG.md`: what was added, changed or removed, and why. Nothing comes out without a line saying so.
- **Keep the two checks in step.** A rule added to `check_voice.py` gets a plain-words entry in `full-check.md`, with the same ID.
- **Show the evidence for a new rule.** Include a real example of the tell and the plain version that replaces it.
- **Promote candidates with care.** The candidate U rules only warn. To make one block, show where it fires on human writing and where it doesn't, the way U01's move to a block in 1.5 did.
- **Run the check on your own docs** before you open the pull request.

To add a format, create `references/formats/<name>.md` with what the reader needs, the sequence of modes, length and limits, and the check settings. Then list it in Step 3 of `SKILL.md`.

## License

Plainspeak Writer is released under the MIT License. See `LICENSE` for the terms.
