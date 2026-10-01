"""Voice check for Plainspeak Writer. Self-contained: Python standard library
only, no other file or tool needed.

  R rules   AI tells and craft rules
  P rules   plain-language rules
  S rules   ruled additions: made-up comparisons, wrap-up words, chatbot
            stock phrases, colon reveals
  U rules   candidates not yet ruled on; they only warn
  V rules   judgment checks for lists of three and choppy prose

Every rule is also written out in plain words in references/tells.md
("The full check"), so the check runs by reading when code can't run.

    python check_voice.py --surface letter   draft.md   # letters, outreach
    python check_voice.py --surface blurb    draft.md   # referral blurbs
    python check_voice.py --surface linkedin draft.md   # posts, About, headlines
    python check_voice.py --surface resume   draft.md
    python check_voice.py --surface general  draft.md   # proposals, think pieces,
                                                        # brand narratives, workshops

HARD blocks a draft. WARN needs a stated reason to keep. Exit 0 when no HARD
hit, 1 when any HARD hit, 2 on a usage error.
"""
import argparse
import re
import sys

__version__ = "3.0"

SURFACES = ("letter", "resume", "linkedin", "blurb", "general")
ALL = frozenset(SURFACES)
L = frozenset(["letter"])
RLB = frozenset(["resume", "linkedin", "blurb"])
LB = frozenset(["letter", "blurb"])

# where a rule runs on a line:
#   "any"     anywhere on any line
#   "opener"  letters: the first body line after the salutation only;
#             other surfaces: any line start (the regex carries ^)
#   "start"   line start on every surface the rule names (the regex carries ^)


def rule(rid, section, label, pattern, note, surfaces=ALL, where="any", ci=True):
    return {
        "id": rid, "section": section, "label": label, "pattern": pattern,
        "note": note, "surfaces": frozenset(surfaces), "where": where, "ci": ci,
    }


# ---------------------------------------------------------------- HARD ----
HARD = [
    rule("R01", "voice", "em dash",
         r"[—―]|(?<!-)--(?!-)",
         "no em dash, and no double hyphen typed as one; a period, comma, colon, or semicolon"),
    rule("R02", "voice", "negative corollary",
         r"\bnot\s+(?:just|only|simply|merely)\b[^.!?;]*\bbut\b|,\s*not\s+(?:just|only|merely)\b|\b(?:is|are|was|were|do|does|did)\s+not\s+just\b|\b(?:isn|aren|wasn|weren|do|does|did)n?'?t\s+just\b",
         "state the positive claim directly"),
    rule("R03", "voice", "retired opener",
         r"\bI(?:\s+am|'m)\s+writing\s+to\s+(?:express|apply|share|highlight|submit|convey)\b",
         "first sentence is content", surfaces=L),
    rule("R04", "voice", "gratitude opener",
         r"^\s*thank\s+you\s+for\b",
         "open inside the reader's problem, never on thanks", surfaces=L, where="opener"),
    rule("R05", "voice", "writer-first opener",
         r"\bmy\s+name\s+is\b",
         "open on the reader's world, never on your name", surfaces=L),
    rule("R06", "voice", "generic-summary DNA",
         r"\bdynamic,?\s+results-oriented\b|\bresults-oriented\b|\ba\s+passion\s+for\s+(?:human-centered\s+)?design\b|\bbroad\s+cross-industry\s+experience\b",
         "retired generic summary language; name the capability and what it produced"),
    rule("R07", "voice",
         "prohibited Summary lead-in",
         r"^\s*[-*•]?\s*Through\s+(?:extensive|\d+|fifteen|twenty|ten|a\s+decade|years)\b",
         "open on what the work produced, not on how long it took", surfaces=RLB, where="start"),
    rule("R08", "voice", "throat-clearing line start",
         r"^\s*[-*•]?\s*(?:As\s+an?\b|I\s+am\s+an?\b|Experienced\b|Results-driven\b|Proven\b|A\s+highly\b|Seasoned\b|A\s+(?:dynamic|passionate|strategic|creative|results)\b)",
         "first words are content", where="opener"),
    rule("R09", "voice", "hedge qualifier",
         r"\b(?:very|really|quite|fairly|somewhat|a\s+bit)\b|(?<!\bthe\s)(?<!\bthat\s)(?<!\bthis\s)(?<!\ba\s)(?<!\bwhat\s)(?<!\bwhich\s)(?<!\bevery\s)(?<!\bsome\s)(?<!\bany\s)(?<!\bone\s)(?<!\bof\s)\bkind\s+of\b|(?<!would\s)(?<!'d\s)\brather\b(?!\s+than\b)",
         "cut the hedge; the number or the plain claim"),
    rule("R10", "voice", "vague intensifier",
         r"\b(?:significant(?:ly)?|substantial(?:ly)?)\s+(?:improv\w+|growth|increas\w+|impact|results?|gains?|value)\b",
         "the metric, or the named project, person, or place"),
    rule("R12", "voice", "passive career verb",
         r"\bcontributed\s+to\b|\bhelped\s+(?:to\s+)?develop\b|\bwas\s+involved\s+in\b|\bplayed\s+a\s+role\b|(?:^\s*[-*•]?\s*|\b(?:I|he|she|they|we)\s+)supported\b",
         "built, founded, generated, trained, led, wrote, designed"),
    rule("R16", "voice",
         "person-anchor or pathology ending",
         r"\bwithout\s+(?:any\s+)?(?:authority|institutional\s+support)\b|\bswear\s+word\b|\bhad\s+to\s+do\s+it\s+myself\b|\bdidn'?t\s+want\s+innovation\b|\btreated\s+as\s+overhead\b",
         "end the sentence on what the work produced for the reader"),
    rule("R18", "voice", "from scratch",
         r"\bfrom\s+scratch\b",
         "redundant; founded / built is complete"),
    rule("R20", "voice", "'actually' as a clarifier",
         r"\bactually\b",
         "cut it; the sentence stops performing"),
    rule("R21", "voice", "timing-brag flourish",
         r"\b(?:years|a\s+decade|decades|months)\s+before\s+(?:the|it|anyone|that|this)\b|\bbefore\s+the\s+role\s+had\s+a\s+(?:title|name)\b|\bbefore\s+(?:it|that|this)\s+had\s+a\s+(?:name|title)\b|\bbefore\s+[^.]{0,40}\s+(?:existed|was\s+a\s+thing)\b",
         "cut the timing clause; keep the claim"),
    rule("R22", "voice", "AI-speak verb + preposition",
         r"\blands?\s+with\b|\bstood\s+up\b|\bstand(?:s|ing)?\s+up\s+(?:a|an|the)\b|\brunning\s+that\s+loop\b|\bon\s+the\s+read\b",
         "plain speech: works, built, doing that work"),
    rule("R23", "voice", "defensive meta-statement",
         r"\bI\s+state\s+that\s+plainly\b|\bI(?:'ll|\s+will)\s+be\s+(?:candid|straight|honest|direct|frank|blunt)\b|\bto\s+be\s+(?:honest|candid|frank)\b|\bcandidly\b|\brather\s+than\s+estimate\b|\bI\s+(?:won'?t|will\s+not)\s+pretend\b|\bin\s+the\s+interest\s+of\s+(?:honesty|candor|transparency)\b|\bfull\s+disclosure\b",
         "if the number exists, give it; if not, omit the topic"),
    rule("R24", "voice", "symmetrical negation",
         r"\bI(?:'m|\s+am)\s+not\s+(?:a|an)\s+[^.!?]{1,60}[.!?]\s+I(?:'m|\s+am)\s+(?:the|a|an)\b",
         "break the mirror; state the capability in its own terms"),
    rule("R25", "voice", "urgency or scarcity coda",
         r"\bif\s+we\s+wait\b|\bbefore\s+someone\s+else\b|\bsomeone\s+else\s+(?:figures|notices|will)\b|\bthe\s+window\s+is\s+closing\b|\bnow\s+is\s+the\s+time\b|\bthe\s+time\s+is\s+now\b|\bthe\s+opportunity\s+is\s+now\b",
         "end on the substantive conviction"),
    rule("R26", "voice", "consulting speak / empty phrasing",
         r"\bleverag\w*\s+synerg\w*|\bsynerg\w+|\bdriv(?:e|es|ing)\s+alignment\b|\bunlock(?:s|ing|ed)?\s+value\b|\bdeliver(?:s|ing|ed)?\s+impact\b|\bmake\s+people\s+feel\s+something\b|\bmake\s+resonance\s+inevitable\b",
         "name the specific thing the phrase gestures at"),
    rule("R27", "voice",
         "bridge the gap",
         r"\bbridg(?:e|es|ed|ing)\s+the\s+gap\b",
         "cliché; the specific version of the connection"),
    rule("R29", "voice",
         "terminal-abstraction construct",
         r"\b(?:the|this|that|my|our|its|his)\s+(?:work|methodology|method|practice|thinking|frameworks?|approach|system|discipline|model|process)\s+(?:travels|holds|endures|carries|lasts|scales|transfers|persists|stands|remains)\s*(?:[.;:!?]|$)",
         "name what it does, to what, producing what result"),
    rule("R31", "voice",
         "fortune-cookie stock / florid stacking",
         r"\bmagic\s+ingredients?\b|\bgiant\s+strides\b|\bone\s+moment\s+at\s+a\s+time\b|\ba\s+fire\s+within\b|\binsatiable\s+desire\b|\bfundamental\s+mission\b|\bhelp\s+others\s+achieve\s+greatness\b",
         "sounds profound and names nothing"),
    rule("R32", "voice",
         "performance vocabulary",
         r"\bstrategy\s+hacker\b|\bimagineers?\b|\bhighly\s+competitive\b",
         "performance vocabulary; say what you do"),
    rule("R33", "voice",
         "performed-warmth closer",
         r"\bthank\s+you\s+for\s+your\s+(?:time\s+and\s+)?consideration\b|\bthank\s+you\s+for\s+(?:your|the)\s+time\b|\bgrateful\s+and\s+humbled\b|\bhumbled\b|\blook\s+forward\s+to\s+(?:the\s+opportunity|speaking|hearing|discussing|meeting|talking)\b|\bwould\s+be\s+honou?red\b",
         "the invitation is the last sentence", surfaces=LB),
    rule("R34", "voice",
         "faux shared-awareness wink",
         r"\bwe'?ve\s+all\s+been\s+there\b",
         "name the thing being winked at, or cut it"),
    rule("R35", "voice",
         "'impactful' and kin",
         r"\bimpactful\b|\bhigh-impact\b",
         "bare empty word; name the result"),
    rule("R37", "voice",
         "intensifier before a superlative",
         r"\b(?:truly|incredibly|absolutely|really|extremely|deeply|genuinely|hugely|remarkably)\s+(?:one\s+of|the\s+(?:most|best|fastest|highest|first|largest|biggest)|game-changing|innovative|excited|proud|unique|exceptional|transformative)\b",
         "the flat superlative; no amplifier"),
    rule("R40", "voice",
         "the indirect claim",
         r"(?:^|[.;:!?,]\s+|\b(?:think|know|believe|and|but|because|so|since|which|why|is)\s+)that\s+is\s+(?:the|what|where|how|why|exactly|precisely)\b",
         "say the thing: 'I've done that work'; 'that's' where speech contracts"),
    rule("R45", "voice",
         "the drawn-out or inverted construction",
         r"\bis\s+the\s+(?:part|piece|thing)\s+(?:I|he|she|we|they)\b|\b(?:has|have)\s+taught\s+me\s+(?:where|that|what)\b|\bwhat\s+I(?:'ve|\s+have)\s+learned\s+is\b",
         "subject first; the sentence says the thing"),
    rule("R48", "voice",
         "cliché",
         r"\bresults?-driven\b|\bproven\s+track\s+record\b|\bpassionate\s+about\b|\bseasoned\b|\bdynamic\s+professional\b|\bdetail-oriented\b|\bteam\s+player\b|\bgo-getter\b|\bthought\s+leader\b(?!ship)|\bspearhead\w*|\bwheelhouse\b",
         "retired construction"),
    rule("R11", "voice", "retired verb",
         r"\b(?:author(?:ed|ing)|architect(?:ed|ing))\b",
         "wrote / built / designed / named; noun forms are fine"),
    rule("R28", "voice",
         "empty bridge",
         r"\bat\s+once\b",
         "connective filler; cut it or name the relationship"),
    rule("R30", "voice",
         "comparative emphasis",
         r"\bthe\s+more\s+[^,.;]{1,120},\s+the\s+more\b",
         "say the relationship directly, with the number or the cause"),
    rule("R39", "voice",
         "'carry' as a verb",
         r"\bcarr(?:y|ies|ied|ying)\b(?!-on)(?!over)",
         "say what the thing does; a literal object may carry, an abstraction may not"),
    rule("R46", "voice",
         "'read' as a noun",
         r"(?<![\w-])(?:a|an|the|my|his|her|our|your|this|that|one|honest|deeper|deep|closer|close|quick|cold|full|initial|first|second|good|hard|clear|client|market|community|business|behavioral|consumer|careful|fast|strong)\s+read\b(?!-)(?!\s+(?:the|a|an|it|them|this|that|these|those|what|how|where|who|whether|about|through|every|each|his|her|their|our|my|your|and|as|like|more|closely|well|carefully|widely|for|in|at|by|out|up|over|off|aloud|again|before|after|all|both|either|neither|no|some|any|much|most|less|fewer|many|only|just|first|next|last|from|everything|nothing|something|anything|me|us|him|you|people|residents?|data)\b)|\b(?:the|his|my|our|these|those|their|your|two|three)\s+reads\b",
         "the verb instead: 'reading the client'"),
    rule("R42", "voice",
         "the hanging phrase (named literals)",
         r"\b(?:gave|give|gives|giving)\s+(?:the\s+)?(?:hours|time)\s+back\b|\bthe\s+work\s+that\s+wins\b|\bwhat\s+wins\b",
         "say who did what, and what it produced for whom"),
]

# ---------------------------------------------------------------- WARN ----
# WARN where context decides: the rule names a real exception.
WARN = [
    rule("R13", "voice", "Latinate default",
         r"\butili[sz](?:e|es|ed|ing)\b|\bdemonstrat(?:e|es|ed|ing)\b|\bcommenc(?:e|es|ed|ing)\b|\bconstruct(?:ed|ing)\b",
         "use the plain word unless the audience speaks this way"),
    rule("R19", "voice", "borrowed framework",
         r"\borganizational\s+antibodies\b|\bblue\s+ocean\b|\bjobs[- ]to[- ]be[- ]done\b",
         "use original language, or attribute it"),
    rule("R41", "voice",
         "uncontracted form where speech contracts",
         r"\b(?:that\s+is|it\s+is|I\s+have|I\s+am|I\s+would|I\s+will|I\s+had|do\s+not|does\s+not|did\s+not|cannot|is\s+not|are\s+not|was\s+not|were\s+not|there\s+is|here\s+is|what\s+is|has\s+not|have\s+not|had\s+not|will\s+not|would\s+not|could\s+not|should\s+not|he\s+is|she\s+is|we\s+are|they\s+are|you\s+are|we\s+have|they\s+have|you\s+have|we\s+will|we\s+would|let\s+us)\b",
         "contract unless the emphasis is deliberate"),
    rule("R44", "voice",
         "the vague place",
         r"\b(?:the|a|that|this|any|our|your|every|one|whole|same)\s+(?:(?!(?:the|a|an|that|this)\b)\w+\s+){0,2}(?:room|table)\b(?!\s+of\s+contents)|\b(?:in|into|around|across|to|at|on|from)\s+the\s+(?:room|table)\b|\bbrings?\s+to\s+the\s+table\b|\bstanding\s+in\s+the\s+room\b",
         "a real, named place, or one the sentence itself just built"),
]

# ------------------------------------------------ skill additions ----
# Plain-language rules, ruled additions, and candidates not yet ruled on.
HARD += [
    rule("P01", "plain language", "'it's not about X'",
         r"\b(?:it|this|that)'s\s+not\s+about\b|\bisn'?t\s+about\b|\bis\s+not\s+about\b|\b(?:it|this|that)'s\s+not\s+[^.,;]{1,40},\s+(?:it|this|that)'s\b",
         "say what it is"),
    rule("P02", "plain language", "filler word",
         r"\b(?:simply|literally)\b",
         "cut it unless it changes the meaning"),
    rule("P03", "plain language", "vague size word",
         r"\b(?:robust|comprehensive|powerful|seamless(?:ly)?)\b|\bsignificant(?:ly)?\b(?!\s+(?:improv\w+|growth|increas\w+|impact|results?|gains?|value)\b)",
         "give the number or the result"),
    rule("P04", "plain language", "fluff verb",
         r"\b(?:unlock(?:s|ed|ing)?|empower(?:s|ed|ing)?|elevat(?:e|es|ed|ing)|streamlin(?:e|es|ed|ing)|foster(?:s|ed|ing)?)\b(?!\s+value\b)",
         "say the plain action"),
    rule("P05", "plain language", "conference-speak",
         r"\b(?:world-class|best-in-class|holistic|cutting-edge)\b",
         "cut it or replace it with evidence"),
    rule("P06", "plain language", "throat-clearing opener",
         r"\b(?:in\s+today's|in\s+a\s+world\s+where|in\s+an\s+era\s+of)\b",
         "first words are the point"),
    rule("P07", "plain language", "'whether you're' setup",
         r"\bwhether\s+you're\b",
         "talk to the actual reader"),
    rule("P08", "plain language", "weak claim",
         r"\b(?:can\s+help|may\s+be\s+able\s+to|could\s+potentially)\b",
         "say what it does"),
    rule("P09", "plain language", "ending on air",
         r"\bspeaks?\s+for\s+(?:it|them)sel(?:f|ves)\b|\bresults\s+follow\b",
         "end on the substance"),
    rule("P12", "plain language", "'leverage'",
         r"(?<!debt\s)(?<!financial\s)(?<!operating\s)(?<!highly\s)(?<!over-)\bleverag(?:e|es|ed|ing)\b(?!\s+(?:ratios?|buyouts?)\b)",
         "say the plain action: use, build on, apply; the finance sense (debt leverage, leverage ratio, highly leveraged) passes"),
    rule("S02", "ruling", "wrap-up word",
         r"\b(?:in\s+summary|in\s+conclusion|to\s+sum\s+up|ultimately|moreover|furthermore)\b|(?:^|[.!?]\s+)overall,",
         "cut it; the point needs no announcement"),
    rule("S03", "ruling", "chatbot stock phrase",
         r"\b(?:delve[sd]?|delving|tapestry|testament\s+to|it's\s+worth\s+noting|it's\s+important\s+to\s+note|let's\s+dive|dive\s+in(?:to)?|game-changer|game-changing)\b",
         "cut it or say it plainly"),
]

WARN += [
    rule("P10", "plain language", "'just' as filler",
         r"\bjust\b",
         "keep it only if it changes the meaning"),
    rule("P11", "plain language", "'drive' as a fluff verb",
         r"\b(?:drive|drives|driving)\b(?!\s+alignment\b)",
         "say the plain action unless it's a literal drive"),
    rule("S01", "ruling", "made-up comparison",
         r"\b(?:most\s+(?:people|companies|strategists|brands|founders|leaders|firms|agencies|designers|marketers|insight\s+work)|unlike\s+many|where\s+others)\b",
         "compare only against a named competitor, a real number or a stated baseline"),
    rule("V01", "judgment", "list of three",
         r"(?<!, )\b[\w'-]+(?:\s[\w'-]+){0,3},\s[\w'-]+(?:\s[\w'-]+){0,3},?\s(?:and|or)\s[\w'-]+(?:\s[\w'-]+){0,3}\b",
         "fine when each item is specific and does work; a crutch when it stands in for logic"),
    rule("U01", "candidate", "signposting",
         r"\bhere's\s+(?:why|what|how|the\s+thing|the\s+kicker|the\s+catch)\b|\bthis\s+matters\b|\blet\s+me\s+explain\b|\bthe\s+bottom\s+line\s+is\b|\bmake\s+no\s+mistake\b",
         "say the point instead of announcing it"),
    rule("U02", "candidate", "hedge 'sort of'",
         r"\bsort\s+of\b",
         "cut the hedge"),
    rule("U03", "candidate", "possible chatbot word",
         r"\b(?:navigate|navigating|realm|pivotal|crucial)\b|\blandscape\b(?!\s+architect)",
         "use the plain word"),
    rule("U04", "candidate", "exclamation mark",
         r"!",
         "let the sentence hold the energy"),
]

# Colon reveals, moderated heavily. A colon
# followed by three words or fewer that end the sentence. The first one in a
# draft warns; every one after it blocks. A colon before a list or an
# explanation doesn't match.
COLON_REVEAL = re.compile(r":\s+[^\s,;:.!?]+(?:\s+[^\s,;:.!?]+){0,2}[.!?](?:\s|$)")


def mask_code(text):
    """Blank out fenced code blocks and inline code spans, keeping every
    line and column where it was, so command-line flags and code never
    trip a prose rule."""
    out, fenced = [], False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            fenced = not fenced
            out.append(" " * len(line))
            continue
        if fenced:
            out.append(" " * len(line))
            continue
        out.append(re.sub(r"`[^`]*`", lambda m: " " * len(m.group(0)), line))
    return "\n".join(out)


def prose_only(text):
    """The prose paragraphs of a draft: no code, headings, list items,
    quotes, tables or bracketed notes. Used by the choppiness checks."""
    keep = []
    for line in mask_code(text).splitlines():
        t = line.strip()
        if re.match(r"(?:#|[-*•]\s|\d+[.)]\s|>|\|)", t) or (t.startswith("[") and t.endswith("]")):
            keep.append("")
        else:
            keep.append(line)
    return "\n".join(keep)


def document_checks(text):
    """Checks that need the whole draft. Returns (hard, warn) lists of
    (line, label, hit, note) tuples; line 0 means the whole draft."""
    hard, warn = [], []
    lines = mask_code(text).splitlines()
    reveals = []
    for i, raw in enumerate(lines, 1):
        for m in COLON_REVEAL.finditer(raw.translate(_QUOTES)):
            reveals.append((i, m.group(0).strip()))
    for n, (ln, hit) in enumerate(reveals):
        label = "S04 colon reveal"
        if n == 0:
            warn.append((ln, label, hit, "one per piece at most, and only where it lands"))
        else:
            hard.append((ln, label, hit, "a second reveal in one piece; rewrite it as a plain sentence"))

    body = re.sub(r"\[[^\]]*\]", "", prose_only(text))
    sentences = [x.strip() for x in re.split(r'(?<=[.!?])["\']?\s+', body) if x.strip()]
    lengths = [len(x.split()) for x in sentences]
    run = worst = 0
    for n in lengths:
        run = run + 1 if n <= 10 else 0
        worst = max(worst, run)
    if worst >= 3:
        warn.append((0, "V02 choppy run", f"{worst} short sentences in a row",
                     "fine only when it stacks proof points; otherwise join the sentences"))
    if lengths:
        short_share = sum(1 for n in lengths if n <= 10) / len(lengths)
        avg = sum(lengths) / len(lengths)
        if short_share > 0.35 or avg < 14:
            warn.append((0, "V03 choppy overall",
                         f"average {avg:.1f} words per sentence, {short_share:.0%} of 10 words or fewer",
                         "staccato is a tactic, never the default"))
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", prose_only(text)) if p.strip()]
    if len(paragraphs) >= 4:
        one = [p for p in paragraphs if len(re.findall(r"[.!?](\s|$)", p)) <= 1 and not p.startswith("[")]
        if len(one) / len(paragraphs) > 0.5:
            warn.append((0, "V04 staccato layout", f"{len(one)} of {len(paragraphs)} paragraphs are one sentence",
                         "join one-line paragraphs into paragraphs that finish a thought"))
    return hard, warn


_SALUTATION = re.compile(r"^\s*(?:To|Dear|Greetings|Hi|Hello|Hey)\b.*[:,]\s*$", re.IGNORECASE)

# Curly quotes are read as straight quotes for matching (Word exports curl
# them); the mapping is one character to one, so hit offsets do not move.
_QUOTES = str.maketrans({"\u2019": "'", "\u2018": "'", "\u201c": '"', "\u201d": '"'})


def _compiled(r):
    if "_re" not in r:
        r["_re"] = re.compile(r["pattern"], re.IGNORECASE if r["ci"] else 0)
    return r["_re"]


def label_of(r):
    return f"{r['id']} {r['label']}"


def opener_line(lines):
    """The line number of a letter's first body line: the first non-empty
    line after the salutation, or, when no salutation is found in the first
    fifteen non-empty lines, the first line of sixty or more characters
    (a name, date, phone, or address line is shorter than a sentence)."""
    seen = 0
    for i, line in enumerate(lines, 1):
        if not line.strip():
            continue
        seen += 1
        if _SALUTATION.match(line):
            for j in range(i, len(lines)):
                if lines[j].strip():
                    return j + 1
            return None
        if seen >= 15:
            break
    for i, line in enumerate(lines, 1):
        if len(line.strip()) >= 60:
            return i
    return None


def scan(text, rules, surface="letter"):
    """Return [(line, label, hit, note)] for every rule hit on this surface,
    in line order, then rule order. `text` is split on universal newlines."""
    if surface not in SURFACES:
        raise ValueError(f"unknown surface {surface!r}; one of {', '.join(SURFACES)}")
    lines = mask_code(text).splitlines()
    opener = opener_line(lines) if surface == "letter" else None
    hits = []
    for i, raw in enumerate(lines, 1):
        line = raw.translate(_QUOTES)
        for r in rules:
            if surface not in r["surfaces"]:
                continue
            if r["where"] == "opener" and surface == "letter" and i != opener:
                continue
            for m in _compiled(r).finditer(line):
                hits.append((i, label_of(r), m.group(0).strip(), r["note"]))
    return hits


def read_text(path):
    with open(path, encoding="utf-8-sig", newline=None) as fh:
        return fh.read()


def report_files(paths, surface, by_rule=False):
    """Build the report lines for the given files. Returns (lines, any_hard)."""
    out = []
    any_hard = False
    per_file = []
    for path in paths:
        try:
            text = read_text(path)
        except OSError as e:
            out.append(f"FAIL: cannot read {path}: {e}")
            any_hard = True
            continue
        hard = scan(text, HARD, surface)
        warn = scan(text, WARN, surface)
        dhard, dwarn = document_checks(text)
        hard += dhard
        warn += dwarn
        per_file.append((path, hard, warn))
        if hard:
            any_hard = True

    out.append(f"check_voice {__version__}   surface: {surface}")
    if by_rule:
        groups = {}
        for path, hard, warn in per_file:
            for cls, hits in (("HARD", hard), ("WARN", warn)):
                for ln, label, hit, note in hits:
                    groups.setdefault((cls, label, note), []).append((path, ln, hit))
        order = {label_of(r): n for n, r in enumerate(HARD + WARN)}
        for (cls, label, note), items in sorted(groups.items(), key=lambda kv: (kv[0][0] != "HARD", order.get(kv[0][1], 999))):
            out.append("")
            out.append(f"[{cls}] {label}   ({len(items)} hits): {note}")
            for path, ln, hit in items:
                out.append(f"  {path} L{ln}: \"{hit}\"")
        nh = sum(len(h) for _p, h, _w in per_file)
        nw = sum(len(w) for _p, _h, w in per_file)
        out.append("")
        out.append(f"{len(per_file)} files: {nh} HARD, {nw} WARN")
    else:
        for path, hard, warn in per_file:
            out.append("")
            out.append(f"=== {path} ===")
            if not hard and not warn:
                out.append("PASS: no pattern violations.")
                continue
            if hard:
                out.append(f"HARD FAIL ({len(hard)}):")
                for ln, label, hit, note in hard:
                    out.append(f"  L{ln}: [{label}] \"{hit}\": {note}")
            if warn:
                out.append(f"WARN ({len(warn)}), each cleared by a named decision or fixed:")
                for ln, label, hit, note in warn:
                    out.append(f"  L{ln}: [{label}] \"{hit}\": {note}")
            if not hard:
                out.append("No HARD fails; WARN items need a human decision.")
    out.append("")
    out.append("RESULT: " + ("FAIL: hard violations present." if any_hard else "PASS: no hard violations."))
    return out, any_hard


def main(argv=None):
    ap = argparse.ArgumentParser(prog="check_voice.py", add_help=True,
                                 description="Plainspeak Writer's voice check for any draft.")
    ap.add_argument("files", nargs="*", help="draft file(s) to check")
    ap.add_argument("--surface", choices=SURFACES, default="letter",
                    help="letter, blurb, linkedin, resume or general (default: letter)")
    ap.add_argument("--by-rule", action="store_true", help="group hits by rule across files")
    ap.add_argument("--out", help="write the report to this file (UTF-8, LF)")
    ap.add_argument("--list-rules", action="store_true", help="print the rule table and exit")
    args = ap.parse_args(argv)

    if args.list_rules:
        for cls, rules in (("HARD", HARD), ("WARN", WARN)):
            for r in rules:
                surf = "all" if r["surfaces"] == ALL else ",".join(s for s in SURFACES if s in r["surfaces"])
                print(f"{cls}\t{r['id']}\t{r['section']}\t{r['label']}\t{surf}\t{r['where']}")
        return 0
    if not args.files:
        ap.print_usage()
        print("check_voice.py: a draft file is required (see --help)")
        return 2

    lines, any_hard = report_files(args.files, args.surface, args.by_rule)
    report = "\n".join(lines) + "\n"
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    sys.stdout.write(report)
    if args.out:
        with open(args.out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(report)
        sys.stdout.write(f"[report written to {args.out}]\n")
    return 1 if any_hard else 0


if __name__ == "__main__":
    sys.exit(main())
