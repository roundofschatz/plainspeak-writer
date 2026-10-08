"""Voice check for Plainspeak Writer. Self-contained: Python standard library
only, no other file or tool needed.

  R rules   AI tells and craft rules
  P rules   plain-language rules
  S rules   ruled additions: made-up comparisons, wrap-up words, chatbot
            stock phrases, colon reveals, and the stock phrases added in 1.4
  U rules   candidates; they only warn until there's evidence that AI drafts
            use them far more often than human writers do (U01 has that
            evidence and blocks since 1.5)
  V rules   judgment checks for lists of three, choppy prose, sentence
            shapes, sentences said twice and a letter's sentence length

An ID ending in W is the warning half of a rule that was split: the narrow
form blocks and the common form warns (R02 blocks, R02W warns).

Every rule is also written out in plain words in references/full-check.md,
so the check runs by reading when code can't run.

The report gives each file's word count, counted the way wc -w counts, so
one run checks the rules and the length.

How the check reads a draft:
  - lines that wrap inside a paragraph are joined before checking
  - words inside quotation marks and block quotes are skipped, because a
    writer can't change what a source said
  - a capitalized word in the middle of a sentence is read as a name and
    skipped (Seamless, Synergy Health), and so is a capitalized pair at the
    start of a sentence (Robust Intelligence)
  - every dash character counts as a dash, except an en dash in a number
    range like 2019–2021, and an en dash or hyphen between two range ends
    outside a sentence, like a resume's "Mar 2019 – Present" line or
    "Hours: Mon–Fri"; an em dash always counts
  - a name joined by + or & (Foster + Partners) is read as a name, even in
    a heading written in title case
  - names and terms passed with --keep are skipped anywhere, even where
    they open a sentence (Seamless now lets...)
  - a divider or cut line made of hyphens (- - - - or a scissors mark and
    hyphens) is a rule line, not a dash
  - label lines ("Budget: $40K.") are skipped by the colon check
  - common habits (R09, R41, P10, V01, V02, V05, V06, and V10 off letters)
    warn once per draft, and only when the draft runs above the rate in
    edited human writing
  - the last three items of a list of four or more aren't counted as a list
    of three
  - a sentence of six words or more that comes back word for word in the
    same piece warns once for each repeat (V08)
  - in a letter, three habits warn: a clause standing in for a noun ("by
    what the unit tests showed", V10) and a sentence that points back
    ("and that's the coaching I'd bring", V11) at each use, and sentences
    that all run long, once (V09)

    python check_voice.py draft.md                      # general (the default)
    python check_voice.py --surface letter   draft.md   # letters, outreach
    python check_voice.py --surface blurb    draft.md   # referral blurbs
    python check_voice.py --surface linkedin draft.md   # posts, About, headlines
    python check_voice.py --surface resume   draft.md
    python check_voice.py --surface general  draft.md   # proposals, think pieces,
                                                        # brand narratives, workshops
    python check_voice.py --skip R01 draft.md           # turn off a rule the user's
                                                        # own instructions allow
    python check_voice.py --keep "Seamless,Foster + Partners" draft.md
                                                        # skip the user's own names
                                                        # and terms anywhere

HARD blocks a draft. WARN needs a stated reason to keep. Exit 0 when no HARD
hit, 1 when any HARD hit, 2 on a usage error.
"""
import argparse
import re
import sys

__version__ = "1.7"   # matches the skill's version in CHANGELOG.md

SURFACES = ("letter", "resume", "linkedin", "blurb", "general")
ALL = frozenset(SURFACES)
L = frozenset(["letter"])
RLB = frozenset(["resume", "linkedin", "blurb"])
LB = frozenset(["letter", "blurb"])
LRLB = frozenset(["letter", "resume", "linkedin", "blurb"])
LI = frozenset(["linkedin"])

# where a rule runs (lines that wrap inside a paragraph are joined first, so
# a "line" here is a whole paragraph, list item, heading or table row):
#   "any"     anywhere
#   "opener"  the draft's first line only: in a letter, the first body line
#             after the salutation; in a resume, the first line of sixty or
#             more characters; anywhere else, the first line after any title
#   "start"   the start of every line on the surfaces the rule names (the
#             regex carries ^)
# pos narrows where a hit may start inside the line:
#   "any"       anywhere
#   "sentence"  only at the start of a sentence
#   "mid"       only inside a sentence, never at its start
# keep, when set, is a function (line, match) that returns False for a hit
# the pattern can't rule out by itself, like "leverage" used as a noun. With
# block_keep, it also gets the block the line came from, so it can tell a
# heading, a table row or a label line from a sentence (R01, since 1.6).
# rate and min_hits mark a rule that warns once per draft, only when the
# draft has at least min_hits hits and more than `rate` per 1,000 words.
# per_hit names the surfaces where such a rule warns at every hit instead,
# like a WARN rule (V10 on letters, since 1.7).


def rule(rid, section, label, pattern, note, surfaces=ALL, where="any", ci=True,
         pos="any", keep=None, rate=None, min_hits=2, block_keep=False, per_hit=frozenset()):
    return {
        "id": rid, "section": section, "label": label, "pattern": pattern,
        "note": note, "surfaces": frozenset(surfaces), "where": where, "ci": ci,
        "pos": pos, "keep": keep, "rate": rate, "min_hits": min_hits,
        "block_keep": block_keep, "per_hit": frozenset(per_hit),
    }


# Words a self-description opener or a resume cliché puts in front of the
# writer. Singular on purpose: "Experienced designer with ten years" is a
# self-description, while "Experienced riders take the north loop" isn't.
ROLE = (r"(?:professional|leader|executive|manager|strategist|designer|marketer|engineer|"
        r"developer|consultant|director|specialist|analyst|writer|communicator|educator|"
        r"operator|founder|entrepreneur|practitioner|generalist|expert|veteran|advisor|"
        r"adviser|officer|administrator|coach|researcher|scientist|planner|producer|"
        r"storyteller|creative|technologist|innovator|visionary|problem-solver|self-starter|"
        r"go-getter|team\s+player|change\s+agent|people\s+person)")
ROLES = (r"(?:professionals|leaders|executives|managers|strategists|designers|marketers|"
         r"engineers|developers|consultants|directors|specialists|analysts|writers|"
         r"communicators|educators|operators|founders|entrepreneurs|practitioners|experts|"
         r"veterans|advisors|advisers|officers|administrators|coaches|researchers|"
         r"scientists|planners|producers|storytellers|creatives|technologists|innovators|"
         r"team|pros?)")
SELF_PRAISE = (r"(?:passionate|dynamic|results[\w-]*|strategic|creative|seasoned|proven|highly|"
               r"motivated|dedicated|driven|innovative|experienced|accomplished|versatile|"
               r"detail-oriented|self-starter|go-getter)")


# Arrows and emoji that LinkedIn posts use as bullets (U17): the arrow
# blocks, dingbats, symbols and pictographs, plus "->" and "=>". A plain
# bullet (-, *, •) isn't one of them.
_ARROW_EMOJI = (r"(?:[\u2190-\u21ff\u25aa\u25ab\u25b6\u25b8\u25ba\u25c6\u25c7\u2600-\u27bf"
                r"\u2b05-\u2b07\u2b95\U0001f300-\U0001faff]\ufe0f?|->|=>)")

# Objects that make "drive" a fluff verb (P11): "drive growth", "driving
# engagement", "drive the main work". "Drive alignment" blocks under R26.
_DRIVE_MODIFIERS = (r"(?:the|our|your|their|its|his|her|more|real|better|greater|meaningful|measurable|sustainable|"
                    r"long-term|lasting|business|customer|user|deeper|stronger|higher|new|faster|positive|continued|"
                    r"ongoing|further|key|critical|strategic|community|member|donor|team|organizational|operational|"
                    r"digital|brand|tangible|incremental|repeat|main|this|that|these|those)")
_DRIVE_OBJECTS = (r"(?:growth|engagement|results?|change|innovation|value|impact|adoption|revenue|sales|awareness|"
                  r"traffic|conversions?|outcomes?|success|efficienc(?:y|ies)|performance|transformation|action|"
                  r"momentum|decisions?|collaboration|excellence|loyalty|retention|demand|productivity|progress|"
                  r"improvements?|roi|profitability|participation|strategy|strategies|culture|clarity|consensus|"
                  r"accountability|insights?|usage|sign-?ups|leads|pipeline|bookings|attendance|enrollment|"
                  r"donations|ownership|velocity|savings|work|initiatives?|agenda|conversations?)")

# A first-person claim about skills, strengths or range (V07). The sentence
# warns when it names no number, no name and no bracket for one.
_VAGUE_CLAIM = re.compile(r"\b(?:skills?|experience|expertise|background|abilit(?:y|ies)|knowledge|proficien\w+|"
                          r"track\s+record|strengths?|many\s+different|a\s+wide\s+range|a\s+variety\s+of|various|"
                          r"diverse|numerous|consistently|strong)\b", re.IGNORECASE)
_SELF_WORDS = frozenset("I I've I'm I'd I'll".split())


def _names_nothing(line, m):
    """True when a first-person sentence claims a skill, a strength or a
    range ("I have also built strong data visualization skills", "I have
    shared findings with many different audiences") and names no number, no
    name and no bracket for one."""
    s = m.group(0)
    if not _VAGUE_CLAIM.search(s) or re.search(r"[\d\[]", s):
        return False
    words = re.findall(r"[A-Za-z][\w'-]*", s)
    return not any(w[0].isupper() and w not in _SELF_WORDS for w in words[1:])


def _what_clause(line, m, block):
    """V10: a "what" clause in a sentence, not in a heading, a table, a
    label line or a bracketed slot for the user to fill ("[What the survey
    found]"), where it names what goes in the slot."""
    if block["kind"] in ("heading", "table", "label"):
        return False
    before = line[:m.start()]
    return before.count("[") <= before.count("]")


def _points_back(line, m):
    """V11: "that's" or "this is" at the start of a sentence, after a
    semicolon or a colon, or after "and", "but" or "so", where it points
    back at what came before ("and that's the coaching I'd bring")."""
    if at_sentence_start(line, m.start()):
        return True
    if line[:m.start()].rstrip().endswith((";", ":")):
        return True
    return _prev_word(line, m.start()) in ("and", "but", "so")


def _prev_word(line, start):
    m = re.search(r"([\w'-]+)\s+$", line[max(0, start - 80):start])
    return m.group(1).lower() if m else ""


def _next_word(line, end):
    m = re.match(r"\s+([\w'-]+)", line[end:end + 80])
    return m.group(1).lower() if m else ""


_DETERMINERS = frozenset("our their its his her my your the this that these those a an every each all "
                         "both existing them it us".split())
# Words before "leverage" that make it a noun: "our leverage", "more leverage",
# "negotiating leverage". After it, a preposition does the same: "leverage over".
_NOUN_CUES = _DETERMINERS | frozenset("more less no any some enough much little real great greater new "
                                      "negotiating bargaining political economic diplomatic moral military "
                                      "considerable enormous same".split())
_AFTER_NOUN = frozenset("over with on in against for from of at among because".split())


def _leverage_as_verb(line, m):
    """True when 'leverage' is a verb ("we leverage our network", "teams
    leverage data", "Leverage AI to cut costs", "leveraging data"). The noun
    passes: after a determiner or an adjective like "negotiating" ("our
    negotiating leverage"), before a preposition ("leverage over suppliers")
    or before punctuation ("we have leverage."). So does the finance sense
    (debt leverage, a leverage ratio, a leveraged buyout, highly leveraged)."""
    word = m.group(0).lower()
    prev, nxt = _prev_word(line, m.start()), _next_word(line, m.end())
    if prev in ("debt", "financial", "operating", "highly") or line[max(0, m.start() - 5):m.start()].lower().endswith("over-"):
        return False
    if nxt in ("ratio", "ratios", "buyout", "buyouts", "up"):
        return False
    if word in ("leveraging", "leverages"):
        return True
    prev2 = _prev_word(line, m.start() - len(prev) - 1) if prev else ""
    if word == "leveraged":
        return prev not in _DETERMINERS and nxt not in ("loan", "loans", "firm", "firms", "fund", "funds", "etf", "etfs", "position", "positions", "finance")
    if prev in _NOUN_CUES or prev2 in _DETERMINERS or nxt in _AFTER_NOUN:
        return False
    return bool(nxt)


_OWNERS = frozenset("the this that these those his her its their our my your".split())
_NOT_A_HEDGE_KIND = frozenset("the that this a what which every some any one of".split())
_AFTER_FAIRLY = frozenset("and or but to in on at by with for as under among between across when if than".split())


def _is_hedge(line, m):
    """True when the word hedges. "Very" after the, this, that or a
    possessive means "exact" ("the very first permit") and passes. "Fairly"
    passes when it means "justly" ("paid fairly and on time"), which is when
    no adjective or adverb follows it. "Kind of" passes as a noun phrase
    ("the kind of park"), and "rather" passes in "rather than", "would
    rather" and "or rather"."""
    word = re.sub(r"\s+", " ", m.group(0).lower())
    prev, nxt = _prev_word(line, m.start()), _next_word(line, m.end())
    if word == "very":
        return prev not in _OWNERS
    if word == "fairly":
        return bool(re.match(r"\s+[a-z]", line[m.end():])) and nxt not in _AFTER_FAIRLY
    if word == "kind of":
        return prev not in _NOT_A_HEDGE_KIND
    if word == "rather":
        return nxt != "than" and prev not in ("would", "or") and not prev.endswith("'d")
    return True


def _overall_opens_sentence(line, m):
    """S02 blocks "Overall," only at the start of a sentence; "the overall,
    long-run trend" passes."""
    return not m.group(0).lower().startswith("overall") or at_sentence_start(line, m.start())


# Words that can end a range outside a sentence (R01, since 1.6): a month, a
# day of the week or a season, written out or short ("Mar", "Sept.", "Mon",
# "Fall"), "Present", "Current" or "Now", and "a.m." or "p.m." after a
# number. A word with a digit in it ("2019", "8:30") ends one too.
_RANGE_WORD = re.compile(
    r"(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|june?|july?|aug(?:ust)?|sept?(?:ember)?|"
    r"oct(?:ober)?|nov(?:ember)?|dec(?:ember)?|mon(?:day)?|tue(?:s(?:day)?)?|wed(?:nesday)?|"
    r"thu(?:r(?:s(?:day)?)?)?|fri(?:day)?|sat(?:urday)?|sun(?:day)?|spring|summer|fall|autumn|winter)\.?",
    re.IGNORECASE)
_RANGE_NOW = re.compile(r"present|current|now", re.IGNORECASE)
_TIME_MARK = re.compile(r"[ap]\.?m\.?", re.IGNORECASE)
_EDGE_MARKS = "()[]{}|*_\"'\u201c\u201d\u2018\u2019,;"
# What sets one part of a line off from the next: a bar, a middle dot or a
# bullet between spaces, or a tab ("Nurse Manager | Mar 2019 – Present").
_LINE_PART = re.compile(r"\s[|\u00b7\u2022]\s|\t")
_DASH_CHARS = "\u2012\u2013\u2212-\u2010\u2011\ufe63\uff0d\u2500"


def _range_end(tok, before=""):
    """True when a word can end a range: a word with a digit in it, a month,
    a day of the week or a season, written out or short ("Mar", "Sept.",
    "Mon", "Fall"), "Present", "Current" or "Now", or "a.m." after a number
    ("8 a.m."). `before` is the text before the word. A colon after the word
    doesn't count ("Mon–Fri: 9 a.m. to 5 p.m.")."""
    t = tok.strip(_EDGE_MARKS + ":")
    if not t:
        return False
    if re.search(r"\d", t) or _RANGE_NOW.fullmatch(t):
        return True
    if t[0].isupper() and _RANGE_WORD.fullmatch(t):
        return True
    return bool(_TIME_MARK.fullmatch(t)) and bool(re.search(r"\d\s*$", before))


def _reads_like_a_title(text):
    """True when no word in the text is a lowercase word other than a small
    one ("of", "and", "the") or a range end ("present", "a.m."), the way a
    resume's title and date line reads ("Nurse Manager, Emergency Department
    | Mar 2019 – Present"). "We're open Mon–Fri" and "since Mar 2019" read
    as a sentence."""
    for w in text.split():
        t = w.strip(_EDGE_MARKS + ".:")
        if not t or not re.search(r"[^\W_]", t):
            continue                      # a dash, a bar or a bullet
        if t[0].isupper() or re.search(r"\d", t) or t.lower() in _SMALL_WORDS:
            continue
        if _RANGE_NOW.fullmatch(t) or _TIME_MARK.fullmatch(t):
            continue
        return False
    return True


def _ends_a_sentence(text):
    """True when the text ends on a period, question mark, exclamation mark,
    colon or semicolon, not counting closing marks or a time's "a.m." or
    "p.m." ("Mon–Fri, 8 a.m.–5 p.m.")."""
    t = re.sub(r"[\"')\]*_\u201d\u2019\s]+$", "", text)
    if re.search(r"(?:^|\s|\d)[ap]\.m\.$", t, re.IGNORECASE):
        return False
    return bool(re.search(r"[.!?:;]$", t))


def _range_outside_prose(line, m, block):
    """True when the dash at m joins two range ends outside a sentence: in a
    heading or a table row, on a label line whose value reads like a title
    ("Hours: Mon–Fri, 8 a.m.–5 p.m."), or on a line that doesn't end like a
    sentence, where the part of the line that holds the range reads like a
    title and the lines around it don't go on with a sentence ("Nurse Manager
    | Mar 2019 – Present", "Jun 2014 – Feb 2019"). The part of the line runs
    between bars, middle dots or bullets ("Mar 2019 – Present · 5 yrs")."""
    before = line[:m.start()]
    left = re.search(r"(\S+)\s*$", before)
    right = re.match(r"\s*(\S+)", line[m.end():m.end() + 80])
    if not (left and right and _range_end(left.group(1), before[:left.start()]) and _range_end(right.group(1))):
        return False
    kind = block["kind"]
    if kind in ("heading", "table"):
        return True
    starts = [off for off, _n in block["starts"]]
    k = max(i for i, off in enumerate(starts) if off <= m.start())
    a = starts[k]
    z = starts[k + 1] - 1 if k + 1 < len(starts) else len(line)
    src = line[a:z]
    if kind == "label":
        return _reads_like_a_title(src.split(":", 1)[1] if ":" in src else src)
    if _ends_a_sentence(src):
        return False
    if k + 1 < len(starts) and line[starts[k + 1]:starts[k + 1] + 1].islower():
        return False                      # the next line goes on with the sentence
    if k > 0:
        prev = line[starts[k - 1]:a - 1]
        if not _ends_a_sentence(prev) and not _reads_like_a_title(prev):
            return False                  # the line before leads into this one
    lo, hi = m.start() - a, m.end() - a
    cut = max([p.end() for p in _LINE_PART.finditer(src[:lo])] or [0])
    nxt = _LINE_PART.search(src, hi)
    return _reads_like_a_title(src[cut:nxt.start() if nxt else len(src)])


def _not_a_number_range(line, m, block=None):
    """False for a dash that isn't a dash in the sentence: an en dash, figure
    dash, minus sign or hyphen between two numbers (2019–2021, $5–$10, Q1–Q3,
    pages 10--12), a dash standing in for an empty table cell, a bullet at
    the start of a line, and a command flag typed as --surface. Since 1.6, an
    en dash or a hyphen between two range ends passes outside a sentence
    too ("Nurse Manager | Mar 2019 – Present", "Hours: Mon–Fri"); see
    _range_outside_prose. An em dash never passes."""
    hit = m.group(0)
    before = line[:m.start()]
    left = re.search(r"(\S+)\s*$", before[-80:])
    right = re.match(r"\s*(\S+)", line[m.end():m.end() + 80])
    if (left and left.group(1).endswith("|")) or (right and right.group(1).startswith("|")):
        return False                      # a dash standing in for an empty table cell
    if hit.strip() and hit.strip()[0] in _DASH_CHARS:
        if not before.strip():
            return False                  # a bullet at the start of a line
        if left and right and re.search(r"\d", left.group(1)) and re.search(r"\d", right.group(1)):
            return False                  # a number range, or arithmetic
        if hit == "\u2212" and line[m.end():m.end() + 1].isdigit():
            return False                  # a minus sign: -5 degrees
        if block is not None and len(hit.strip()) == 1 and _range_outside_prose(line, m, block):
            return False                  # a range outside a sentence: Mar 2019 – Present
    if hit == "--":
        return not ((not before or before[-1].isspace()) and line[m.end():m.end() + 1].isalpha())
    return True


# A sentence breaks into stretches at these marks. A list never runs across
# one, so only a comma in the same stretch can belong to the same list. A
# period counts when a space, a comma or the end of the line follows it, so
# the point in "3.5 miles" doesn't.
_STRETCH_BREAK = re.compile(r"[;:!?()\[\]\u2012-\u2015\u2026]|\.(?=[\s,]|$)|--|\s-\s")
# Words that open a phrase or a clause and never a plain list item:
# prepositions, then words like "which" and "when".
_PHRASE_OPENERS = frozenset(
    "in on at by for with from to of into onto over under about through during without within across among "
    "between against toward towards upon including like unlike despite beyond throughout along around above "
    "below besides except per via plus "
    "that which who whom whose where when while because since although though if unless as whereas until once "
    "after before whether than".split())
_JOINING_WORDS = frozenset("and or but nor so yet".split())
# With the words above, the ways a clause or a phrase starts after a comma:
# subjects, helping verbs and adverbs.
_CLAUSE_STARTERS = _PHRASE_OPENERS | _JOINING_WORDS | frozenset(
    "i we you he she it they there "
    "is are was were be been being am has have had do does did will would can could should may might must shall "
    "not never always often sometimes also even especially particularly usually mostly mainly then now still "
    "only just both either neither each such rather perhaps let".split())
_ARTICLES = frozenset("a an the this these those my our your his her its their".split())
_IRREGULAR_PARTICIPLES = frozenset(
    "born built chosen drawn driven given grown held known led made seen shown taken written".split())
# Adverbs and times that stand before a comma as a short tag: "However,",
# "More importantly,", "Last year,", "Two years ago,".
_TAG_WORDS = frozenset(
    "however moreover nevertheless nonetheless furthermore meanwhile instead otherwise likewise therefore thus "
    "hence indeed still yet also again too so first second third next last here there together back forward "
    "ahead perhaps maybe overall altogether anyway granted sometimes often always never "
    "now then today tonight yesterday tomorrow later earlier ago afterward afterwards soon "
    "year years month months week weeks day days quarter season spring summer fall autumn winter morning "
    "afternoon evening night weekend".split())


def _words_of(s):
    """The words of a piece of text, in lower case, with the punctuation
    left out."""
    return re.findall(r"[^\W_]+(?:['-][^\W_]+)*", s.lower())


def _is_participle(w):
    """True for an -ing or -ed word ("showing", "based") and for an
    irregular one ("driven", "built"), never for "bring" or "speed"."""
    return (w in _IRREGULAR_PARTICIPLES
            or bool(re.fullmatch(r"[a-z']*[aeiouy][a-z']*(?:ing|ed)", w)) and not w.endswith("eed"))


def _starts_clause(w):
    """True when a word can start a clause or a phrase: a joining word, a
    subject, a preposition, a helping verb, an adverb like "especially", a
    contraction ("we've", "don't") or an -ing or -ed word."""
    return (w.split("'")[0] in _CLAUSE_STARTERS or bool(re.search(r"(?:n't|'re|'ve|'ll|'d|'m)$", w))
            or _is_participle(w))


def _is_ly_word(w):
    """True for a word of five letters or more that ends in -ly, as most
    adverbs do ("ideally", "frankly")."""
    return len(w) > 4 and w.endswith("ly")


def _is_list_of_three(line, m):
    """False when the three items end a longer list ("roads, bike lanes, bus
    shelters, and street trees"), which isn't a list of three. The pattern
    can match from partway through "bike lanes", so this reads back to the
    comma before the match. The host is the words from that comma to the
    first list comma, and the lead is the words before that comma, back to
    the comma or the break before them. When both read as plain items, the
    list is longer than three.

    The three still count when the host starts a clause or a phrase ("and the
    trails", "we shipped apples", "showing wit", "ideally with schools"), when
    it runs to six words or more and the next item opens on a different word,
    or when it holds a preposition the three items hang off ("a row for
    dashes, colons and brackets"). They count too when the lead ends an
    earlier list ("...and writers,"), opens with a preposition or a word like
    "when" ("In March,", "When I joined,"), is an -ing or -ed phrase ("Founded
    in 1920,") or is a short adverb or time ("However,", "Last year,").

    It reads m.string, the block with the words inside quotes blanked, so a
    comma inside a quote never counts."""
    first, _, rest = m.group(0).partition(",")
    stretch = _STRETCH_BREAK.split(m.string[max(0, m.start() - 1000):m.start()] + first)[-1]
    pieces = re.split(r",\s+", stretch)
    if len(pieces) < 2:
        return True                       # no comma before the list in this stretch
    host, lead = _words_of(pieces[-1]), _words_of(pieces[-2])
    if not host or not lead:
        return True                       # a bracket, a quote or an abbreviation sits before the comma
    if _starts_clause(host[0]):
        return True
    if len(host) > 1 and _is_ly_word(host[0]) and host[1] in _PHRASE_OPENERS:
        return True                       # "ideally with schools": an adverb, then a preposition
    second = _words_of(rest)
    same_opener = bool(second) and second[0] == host[0] and host.count(host[0]) == 1
    if len(host) >= 6 and not same_opener:
        return True
    if (host[0] in _ARTICLES and _PHRASE_OPENERS.intersection(host[1:-1])
            and second and second[0] not in _ARTICLES):
        return True
    if len(pieces) == 2:                  # the lead opens the stretch
        if lead[0] in _JOINING_WORDS and len(lead) > 1:
            lead = lead[1:]               # "But frankly," reads as "frankly,"
    elif lead[0] in ("and", "or") and len(lead) > 1 and not _starts_clause(lead[1]):
        return True                       # "...and writers," ends an earlier list
    if lead[0] in _PHRASE_OPENERS:
        return True
    if _is_participle(lead[0]) and len(lead) > 1 and (lead[1] in _PHRASE_OPENERS or lead[1] in _ARTICLES):
        return True
    return len(lead) <= 4 and (lead[-1] in _TAG_WORDS or _is_ly_word(lead[-1]))


# ---------------------------------------------------------------- HARD ----
HARD = [
    rule("R01", "voice", "em dash or other dash",
         r"[\u2012\u2013\u2014\u2015\u2212\u2e3a\u2e3b\u2e40\ufe58\ufe31\ufe32]|(?<=\S)[ \t]+[-\u2010\u2011\ufe63\uff0d\u2500][ \t]+(?=\S)|(?<!-)-{2,3}(?!-)",
         "no dash of any kind, and no double hyphen or spaced hyphen typed as one; a period, comma, colon, or semicolon",
         keep=_not_a_number_range, block_keep=True),
    rule("R02", "voice", "negative corollary",
         r"\bnot\s+(?:just|simply|merely)\b[^.!?;]*\bbut\b|,\s*not\s+(?:just|merely)\b|\b(?:is|are|was|were|do|does|did)\s+not\s+just\b|\b(?:isn|aren|wasn|weren|do|does|did)n?'?t\s+just\b",
         "state the positive claim directly"),
    rule("R03", "voice", "retired opener",
         r"\bI(?:\s+am|'m)\s+writing\s+to\s+(?:express|apply|share|highlight|submit|convey)\b",
         "first sentence is content", surfaces=L),
    rule("R04", "voice", "gratitude opener",
         r"^\s*thank\s+you\s+for\b(?!\s+(?:meeting|speaking|talking|the\s+(?:call|meeting|conversation|chat|interview|tour|visit)|our\s+(?:call|meeting|conversation|chat)|your\s+call|taking\s+(?:my|the|our)\s+call|taking\s+the\s+time\s+to\s+(?:meet|speak|talk))\b)",
         "open inside the reader's problem, never on thanks; thanks for a specific meeting or call in a follow-up passes",
         surfaces=L, where="opener"),
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
         r"^\s*[-*•]?\s*(?:As\s+an?\s+(?!(?:result|example|rule|consequence|reminder|whole|matter|first|side|aside)\b)[\w-]+"
         r"|I\s+am\s+an?\s+(?:[\w-]+,?\s+){0,2}?" + SELF_PRAISE + r"\b"
         r"|(?:Experienced|Proven|Seasoned)\s+(?:[\w-]+,?\s+){0,2}?" + ROLE + r"\b"
         r"|Results-(?:driven|oriented)\b"
         r"|A\s+(?:highly|dynamic|passionate|strategic|creative|results[\w-]*)\s+(?:[\w-]+,?\s+){0,3}?" + ROLE + r"\b)",
         "first words are content", where="opener"),
    rule("R10", "voice", "vague intensifier",
         r"\b(?:significant(?:ly)?|substantial(?:ly)?)\s+(?:improv\w+|growth|increas\w+|impact|results?|gains?|value)\b",
         "the metric, or the named project, person, or place"),
    rule("R12", "voice", "passive career verb",
         r"\bcontributed\s+to\b|\bhelped\s+(?:to\s+)?develop\b|\bwas\s+involved\s+in\b|\bplayed\s+a\s+role\b",
         "built, founded, generated, trained, led, wrote, designed", surfaces=LRLB),
    rule("R16", "voice",
         "person-anchor or pathology ending",
         r"\bwithout\s+(?:any\s+)?(?:authority|institutional\s+support)\b|\bswear\s+word\b|\bhad\s+to\s+do\s+it\s+myself\b|\bdidn'?t\s+want\s+innovation\b|\btreated\s+as\s+overhead\b",
         "end the sentence on what the work produced for the reader"),
    rule("R18", "voice", "from scratch",
         r"\bfrom\s+scratch\b",
         "redundant; founded / built is complete"),
    rule("R20", "voice", "'Actually' opening a sentence",
         r"\bactually\b",
         "cut it; the sentence stops performing", pos="sentence"),
    rule("R21", "voice", "timing-brag flourish",
         r"\b(?:years|a\s+decade|decades|months)\s+before\s+(?:the|it|anyone|that|this)\b|\bbefore\s+the\s+role\s+had\s+a\s+(?:title|name)\b|\bbefore\s+(?:it|that|this)\s+had\s+a\s+(?:name|title)\b|\bbefore\s+[^.]{0,40}\s+was\s+a\s+thing\b",
         "cut the timing clause; keep the claim"),
    rule("R22", "voice", "AI-speak verb + preposition",
         r"(?<!\bmany\s)(?<!\bthe\s)(?<!\bother\s)(?<!\btheir\s)(?<!\bour\s)(?<!\bforeign\s)(?<!\ball\s)(?<!\bthose\s)(?<!\bthese\s)(?<!\bdistant\s)\blands\s+with\b|\b(?:will|to|can|could|should|may|might|would|won't|didn't|doesn't|not)\s+land\s+with\b|\bstood\s+up\s+(?:a|an|the)\b|\bstand(?:s|ing)?\s+up\s+(?:a|an|the)\b|\brunning\s+that\s+loop\b|\bon\s+the\s+read\b",
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
         r"\bleverag\w*\s+synerg(?:y|ies)\b|\bsynerg(?:y|ies|ize|izes|ized|izing|ise|ises|ised|ising)\b|\bdriv(?:e|es|ing)\s+alignment\b|\bunlock(?:s|ing|ed)?\s+value\b|\bdeliver(?:s|ing|ed)?\s+impact\b|\bmake\s+people\s+feel\s+something\b|\bmake\s+resonance\s+inevitable\b",
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
    rule("R45", "voice",
         "the drawn-out or inverted construction",
         r"\bis\s+the\s+(?:part|piece|thing)\s+(?:I|he|she|we|they)\b|\b(?:has|have)\s+taught\s+me\s+(?:where|that|what)\b|\bwhat\s+I(?:'ve|\s+have)\s+learned\s+is\b",
         "subject first; the sentence says the thing"),
    rule("R48", "voice",
         "cliché",
         r"\bresults?-driven\b|\bproven\s+track\s+record\b|\bpassionate\s+about\b|\bseasoned\s+(?:[\w-]+\s+){0,2}?(?:" + ROLE + "|" + ROLES + r")\b|\bdynamic\s+professional\b|\bdetail-oriented\b|\bteam\s+player\b|\bgo-getter\b|\bthought\s+leader\b(?!ship)|\bspearhead\w*|\bwheelhouse\b",
         "retired construction; say what you did"),
    rule("R11", "voice", "retired verb",
         r"(?<!\bbill\s)(?<!\bbills\s)\bauthor(?:ed|ing)\b(?!\s+(?:[\w-]+\s+){0,3}?(?:bills?|amendments?|resolutions?|legislation|laws?|acts?|measures?|ordinances?|statutes?|treat(?:y|ies))\b)"
         r"|\barchitect(?:ed|ing)\b",
         "wrote / built / designed / named; noun forms are fine, and so is authoring a bill"),
    rule("R28", "voice",
         "empty bridge",
         r"\bat\s+once\s+(?!(?:that|the|to|when|if|after|before|and|or|but|as|so|for|in|on|at|by|with|from|into|of|toward|towards|without|upon)\b)(?:an?\s+)?[\w-]+(?:\s+[\w-]+)?\s+and\s+(?:an?\s+)?[\w-]+",
         "connective filler ('at once bold and practical'); cut it or name the relationship"),
    rule("R30", "voice",
         "comparative emphasis",
         r"\bthe\s+more\s+[^,.;]{1,120},\s+the\s+more\b",
         "say the relationship directly, with the number or the cause"),
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
    # Narrowed in 1.6 to the idioms, where "the room" or "the table" stands
    # for the people in it. Before, a real place warned too ("the emergency
    # room", "a pivot table", "the table below"): 126 hits in 944,440 words
    # of edited human writing, and in red-team drafts mostly literal rooms
    # and tables. Other vague places go by reading (tells.md).
    rule("R44", "voice",
         "'the room' or 'the table' as an idiom",
         r"\b(?:everyone|everybody|someone|somebody|anyone|anybody|no\s+one|nobody|people|person|voices?|smartest\s+\w+|only\s+\w+)\s+in\s+the\s+room\b"
         r"|\b(?:kept|keep|keeps|keeping|work|works|worked|working|own|owns|owned|owning|hold|holds|held|holding|win|wins|won|winning|lose|loses|lost|losing|read|reads|reading)\s+the\s+room\b"
         r"|\bthe\s+room\s+(?:went|fell|grew|got|turned|laughed|knew|felt|agreed|was\s+(?:silent|quiet|electric|tense))\b"
         r"|\b(?:a\s+)?seats?\s+at\s+the\s+table\b"
         r"|\b(?:bring|brings|bringing|brought)\s+(?:[\w'-]+\s+){0,6}to\s+the\s+table\b"
         r"|\bstanding\s+in\s+the\s+room\b"
         r"|\bthe\s+room\s+where\b",
         "name the people and what they did: 'the council agreed', not 'the room agreed'"),
    # Moved from blocks in 1.4: good human writing uses these often enough
    # that a block would strip good sentences.
    rule("R02W", "voice", "'not only X, but Y'",
         r"\bnot\s+only\b[^.!?;]*\bbut\b|,\s*not\s+only\b",
         "state the positive claim directly, unless both halves carry real weight"),
    rule("R20W", "voice", "'actually' inside a sentence",
         r"\bactually\b",
         "keep it only when it means 'in fact' and the sentence needs it", pos="mid"),
    rule("R39", "voice",
         "'carry' as a verb",
         r"\bcarr(?:y|ies|ied|ying)\b(?!-on)(?!over)",
         "say what the thing does; a literal object may carry, an abstraction may not"),
    rule("R40", "voice",
         "the indirect claim",
         r"(?:^|[.;:!?,]\s+|\b(?:think|know|believe|and|but|because|so|since|which|why|is)\s+)that\s+is\s+(?:the|what|where|how|why|exactly|precisely)\b",
         "say the thing: 'I've done that work'; 'that's' where speech contracts"),
]

# ------------------------------------------------ skill additions ----
# Plain-language rules, ruled additions, and candidates not yet ruled on.
HARD += [
    rule("P01", "plain language", "'it's not about X'",
         r"\b(?:it|this|that)'s\s+not\s+about\b|\bisn'?t\s+about\b|\bis\s+not\s+about\b|\b(?:it|this|that)'s\s+not\s+[^.,;]{1,40},\s+(?:it|this|that)'s\b",
         "say what it is"),
    rule("P03", "plain language", "vague size word",
         r"\bseamless(?:ly)?\b|\brobust\b(?!\s+(?:standard\s+errors?|regressions?|estimat\w+|statistics?|optimi[sz]ation|inference|covariance|control|to\b))",
         "give the number or the result; 'robust standard errors' and other statistics terms pass"),
    rule("P04", "plain language", "fluff verb",
         r"\b(?:unlock(?:s|ed|ing)?|empower(?:s|ed|ing)?|streamlin(?:e|es|ed|ing))\b(?!\s+value\b)"
         r"|\bfoster(?:s|ed|ing)?\b(?!\s+(?:homes?|care|parent(?:s|ing|hood)?|child(?:ren)?|famil(?:y|ies)|kids?|mothers?|fathers?|siblings?)\b)"
         r"|\belevat(?:e|es|ed|ing)\b(?!\s+(?:the\s+|your\s+|his\s+|her\s+|their\s+|its\s+)?(?:injured\s+)?(?:legs?|arms?|feet|foot|heads?|limbs?|ankles?|knees?)\b)"
         r"(?!(?<=\belevated)\s+(?:boardwalks?|walkways?|paths?|trails?|tracks?|trains?|railways?|rail|highways?|freeways?|roads?|roadways?|platforms?|decks?|plazas?|terraces?|ground|terrain|land|sites?|positions?|stations?|bridges?|crossings?|structures?|tanks?|beds?|floors?|gardens?|views?|vantage|levels?|risks?|blood|temperatures?|pressure|rates?|heart|enzymes?|readings?|counts?)\b)",
         "say the plain action; 'foster care', 'elevated boardwalk' and 'elevate the leg' pass"),
    rule("P05", "plain language", "conference-speak",
         r"\b(?:world-class|best-in-class|holistic|cutting-edge)\b",
         "cut it or replace it with evidence"),
    rule("P06", "plain language", "throat-clearing opener",
         r"\b(?:in\s+today's|in\s+a\s+world\s+where|in\s+an\s+era\s+of)\b",
         "first words are the point", pos="sentence"),
    rule("P07", "plain language", "'whether you're' setup",
         r"\bwhether\s+you're\b",
         "talk to the actual reader"),
    rule("P08", "plain language", "weak claim",
         r"\b(?:I|we|(?:our|my)\s+(?:[\w-]+\s+){0,2}?[\w-]+|(?:this|that|the)\s+(?:product|platform|tool|app|service|solution|software|system|program|programme|course|approach|method|methodology|framework|process|plan|proposal|skill|team|firm|company|agency|studio|offering|feature|guide|report|book|workshop|model|strategy))\s+(?:can\s+help|may\s+be\s+able\s+to|could\s+potentially)\b",
         "say what it does; it applies when the writer, the firm or the product is the subject"),
    rule("P09", "plain language", "ending on air",
         r"\bspeaks?\s+for\s+(?:it|them)sel(?:f|ves)\b|\bresults\s+follow\b",
         "end on the substance"),
    rule("P12", "plain language", "'leverage' as a verb",
         r"\bleverag(?:e|es|ed|ing)\b",
         "say the plain action: use, build on, apply; the noun ('our negotiating leverage') and the finance sense (debt leverage, leverage ratio, highly leveraged) pass",
         keep=_leverage_as_verb),
    rule("S02", "ruling", "wrap-up word",
         r"\b(?:in\s+summary|in\s+conclusion|to\s+sum\s+up)\b|\boverall,",
         "cut it; the point needs no announcement", keep=_overall_opens_sentence),
    rule("S03", "ruling", "chatbot stock phrase",
         r"\b(?:delve[sd]?|delving|rich\s+tapestry|testament\s+to|it's\s+worth\s+noting|it's\s+important\s+to\s+note|let's\s+dive|deep[\s-]dives?|game-changer|game-changing)\b",
         "cut it or say it plainly"),
    # Added in 1.4. Each one has almost no human use in 944,440 words of
    # edited writing, and each got past the 1.3.1 check as an AI tell.
    rule("S05", "ruling", "'I hope this email finds you well'",
         r"\b(?:I\s+)?hope\s+(?:this|that|my)(?:\s+(?:email|e-mail|message|note|letter))?\s+finds\s+you\s+well\b",
         "open on the reason you're writing", surfaces=L),
    rule("S06", "ruling", "engagement bait",
         r"\b(?:agree|thoughts)\?|\bdrop\s+(?:a|your)\s+comments?\b|\bcomment\s+below\b|\bwho\s+else\s+has\s+seen\s+this\b",
         "end on the position, a concrete ask or a next step", surfaces=LI),
    rule("S07", "ruling", "announcement opener",
         r"\b(?:thrilled|excited|delighted)\s+to\s+(?:announce|share)\b",
         "say what happened, with the name or the number", surfaces=LI),
    rule("S08", "ruling", "'humbled'",
         r"\bhumbled\b",
         "say what happened; the reader decides how to feel", surfaces=LI),
    rule("S09", "ruling", "process-quality claim",
         r"\bproven\s+(?:approach|process|method|methodology|framework|formula|system)\b|\brigorous\s+process\b",
         "show the result the process produced"),
    rule("S10", "ruling", "chatbot closer",
         r"\bI\s+hope\s+(?:this|that|it)\s+helps\b|\blet\s+me\s+know\s+if\s+you(?:'d|\s+would)\s+like\s+(?:me\s+to|any|more|another|a\s+different|further)\b|\blet\s+me\s+know\s+if\s+you\s+(?:need|want|have)\s+any\s+(?:other\s+|further\s+|more\s+)?(?:changes|adjustments|edits|revisions|tweaks|help|questions)\b",
         "end on the substance, or on a real next step"),
    rule("S11", "ruling", "'Certainly!'",
         r"\bcertainly!",
         "start with the answer"),
    rule("S12", "ruling", "stock framing",
         r"\blet\s+that\s+sink\s+in\b|\bat\s+(?:its|their|our|my|his|her)\s+core\b",
         "say the point itself"),
    rule("S13", "ruling", "'arguably'",
         r"\barguably\b",
         "make the argument, or say who argues it"),
    rule("S14", "ruling", "'Notably,' opening a sentence",
         r"\bnotably,",
         "if it's notable, the fact shows it", pos="sentence"),
    rule("S15", "ruling", "research-paper filler",
         r"\bmulti-?faceted\b|\btransformative\b(?!\s+use\b)|\bvaluable\s+insights?\b",
         "name the parts, the change or the finding"),
    rule("S16", "ruling", "question reveal",
         r"\b(?:(?:the|my|our|their|your|its|his|her)\s+(?:[\w-]+\s+)?)?(?:result|answer|reason|catch|kicker|twist|secret|outcome|verdict|takeaway|upshot|payoff|lesson|truth|difference|fix|solution|problem|bottom\s+line)s?\?\s+[\"'(]?(?-i:[A-Z0-9$])",
         "say it as a plain sentence: 'Churn fell 40%.'", pos="sentence"),
    rule("S17", "ruling", "'it's not just'",
         r"\b(?:it|that|this|there|he|she|what|who|which)'s\s+not\s+just\b|\b(?:they|we|you)'re\s+not\s+just\b|\bI'm\s+not\s+just\b",
         "state the positive claim directly"),
    # Promoted in 1.5. Red-team testing found it 10 times in drafts Claude
    # wrote without the skill (3.14 per 10,000 words), never in drafts made
    # with it, and 0.12 times per 10,000 words of edited human writing.
    rule("U01", "ruling", "signposting",
         r"\bhere's\s+(?:why|what|how|the\s+thing|the\s+kicker|the\s+catch)\b|\bthis\s+matters\b|\blet\s+me\s+explain\b|\bthe\s+bottom\s+line\s+is\b|\bmake\s+no\s+mistake\b",
         "say the point instead of announcing it"),
]

WARN += [
    rule("P02", "plain language", "filler word",
         r"\b(?:simply|literally)\b",
         "cut it unless it changes the meaning; 'simply because' is plain English"),
    rule("P03W", "plain language", "common size word",
         r"\b(?:powerful|comprehensive)\b|(?<!\bstatistically\s)\bsignificant(?:ly)?\b(?!\s+(?:improv\w+|growth|increas\w+|impact|results?|gains?|value)\b)",
         "give the number or the result, unless it's a plain meaning or a term ('a comprehensive budget', 'significant harm')"),
    # Narrowed in 1.5 to "drive" before a business object. In red-team
    # testing, 26 of 27 hits in drafts Claude wrote without the skill were
    # the noun or a literal drive ("the spring food drive", "too tired to
    # drive home").
    rule("P11", "plain language", "'drive' as a fluff verb",
         r"\b(?:drive|drives|driving)\s+(?:" + _DRIVE_MODIFIERS + r"\s+){0,3}" + _DRIVE_OBJECTS + r"\b"
         r"|\b(?:drive|drives|driving)\s+(?:[\w-]+\s+){1,2}?forward\b",
         "say the plain action: what grew, who came, what changed"),
    rule("S01", "ruling", "made-up comparison",
         r"\b(?:most\s+(?:people|companies|strategists|brands|founders|leaders|firms|agencies|designers|marketers|insight\s+work)|unlike\s+many|where\s+others)\b",
         "compare only against a named competitor, a real number or a stated baseline"),
    rule("S02W", "ruling", "'moreover', 'furthermore', 'ultimately'",
         r"\b(?:moreover|furthermore|ultimately)\b",
         "cut it unless it does work; 'ultimately' inside a sentence often just means 'in the end'"),
    rule("U02", "candidate", "hedge 'sort of'",
         r"\bsort\s+of\b",
         "cut the hedge"),
    rule("U03", "candidate", "possible chatbot word",
         r"\b(?:navigate|navigating|realm|pivotal|crucial)\b|\blandscape\b(?!\s+architect)",
         "use the plain word"),
    rule("U04", "candidate", "exclamation mark",
         r"!",
         "let the sentence hold the energy"),
    # Added in 1.4 as warnings. Human writers use each of these now and then,
    # so they warn until there's evidence AI drafts use them far more.
    rule("U05", "candidate", "hedged commitment",
         r"\b(?:we|I)(?:'ll|\s+will)\s+(?:aim|try|strive|endeavou?r)\s+to\b",
         "say what you'll do; name a real risk separately"),
    rule("U06", "candidate", "'Additionally,' opening a sentence",
         r"\badditionally,",
         "join it to the sentence before, or start with the point", pos="sentence"),
    rule("U07", "candidate", "'notes that' in place of 'says'",
         r"\b(?:notes|explains)\s+that\b",
         "'says' is the plain verb"),
    rule("U08", "candidate", "possible chatbot word",
         r"\bmeticulous(?:ly)?\b|\binnovative\b|\bground-?breaking\b(?!\s+(?:ceremony|ceremonies|event|events)\b)|\bshowcas(?:e|es|ed|ing)\b",
         "use the plain word, or show the thing the word claims"),
    rule("U09", "candidate", "possible chatbot word",
         r"\bunderscor(?:e|es|ed|ing)\b|\bintricate(?:ly)?\b|\bvibran(?:t|tly|cy)\b",
         "use the plain word, or show the thing the word claims"),
    rule("U10", "candidate", "'Isn't X. It's Y.'",
         r"\b(?:this|that|it)\s+(?:isn't|is\s+not|wasn't|was\s+not)\s+(?:an?\s+|the\s+)?(?:[\w-]+\s+){0,2}?[\w-]+\.\s+(?:it's|it\s+is|it\s+was|this\s+is|that's)\s+(?:an?\s+|the\s+)?(?:[\w-]+\s+){0,2}?[\w-]+\.",
         "say what it is in one sentence"),
    rule("U11", "candidate", "hedge phrase",
         r"\bin\s+many\s+ways\b|\bto\s+some\s+extent\b",
         "say where it holds and where it doesn't, or cut it"),
    rule("U12", "candidate", "'less X, more Y'",
         r"\bless\s+(?!than\b)(?:about\s+)?[\w'-]+(?:\s+[\w'-]+)?\s*(?:,|and|but)\s+(?:and\s+)?more\s+(?!than\b)(?:about\s+)?[\w'-]+",
         "say Y straight"),
    rule("U13", "candidate", "trailing lesson",
         r",\s+(?:highlighting|underscoring|showcasing|demonstrating|reflecting|reinforcing|emphasi[sz]ing|illustrating|signall?ing|cementing|solidifying|proving|reaffirming)\s+(?:the|its|their|our|his|her|a|an|how|that|why)\b",
         "cut the tail and let the fact stand, or give the lesson its own sentence with evidence"),
    rule("U14", "candidate", "stock setup",
         r"\bwhen\s+it\s+comes\s+to\b|\bat\s+the\s+end\s+of\s+the\s+day\b",
         "start with the subject"),
    rule("U15", "candidate", "possible chatbot word",
         r"\benhanc(?:e|es|ed|ing)\b|\bunprecedented\b",
         "use the plain word: improve, raise, first, largest"),
    # Added in 1.5 as warnings, for habits Claude showed in LinkedIn posts
    # written without the skill, which linkedin.md already bars. They warn
    # until they're measured on human LinkedIn posts.
    rule("U16", "candidate", "hashtag block",
         r"(?<![\w#&/])#[A-Za-z]\w*(?:[\s,]+#[A-Za-z]\w*){2,}",
         "use one or two hashtags, and only when they name a real event or community", surfaces=LI),
    rule("U17", "candidate", "arrow or emoji bullet",
         r"^\s*" + _ARROW_EMOJI + r"\s+\S+(?:\s+\S+){0,3}",
         "write the points as sentences, or as a plain list when the content is a list", surfaces=LI),
    rule("U18", "candidate", "engagement-bait closer",
         r"\b(?:I|we)(?:'d|\s+would)\s+love\s+to\s+(?:hear|know|learn)\b(?!\s+from\s+you\b)"
         r"|\bcurious\s+(?:how|what|whether|if)\s+(?:others|other\s+[\w-]+|you|your|everyone|folks|people|anyone)\b"
         r"|\bwhat(?:'s|\s+has|\s+have)\s+worked\s+for\s+(?:you|your|others)\b"
         r"|\b(?:share|tell\s+(?:me|us))\s+(?:yours|your\s+(?:thoughts|experiences?|take|stories|story))\b"
         r"|\bhow\s+(?:do|does|are|is)\s+(?:you|your\s+(?:team|company|org|organization|studio|agency|firm))\s+"
         r"(?:handle|handling|approach|approaching|deal|dealing|keep|keeping|manage|managing|tackle|tackling)\b",
         "end on the position, a concrete ask or a next step", surfaces=LI),
    # Added in 1.5 as a warning: one of three sentence shapes a blind reader
    # marked in AI drafts during red-team testing. The other two warn by rate
    # (V05, V06).
    rule("V07", "judgment", "skills claim that names nothing",
         r"\b(?:I|I've|I'm|I'd|My|We|We've|We're|Our)\b[^.!?]*[.!?]",
         "name the tool, the number, the audience or the example the user gave, or cut the claim",
         surfaces=LRLB, pos="sentence", ci=False, keep=_names_nothing),
    # Added in 1.7, on letters only: "that's" or "this is" pointing back at
    # the sentence before instead of saying the thing ("and that's the
    # coaching I'd bring", "That's the work I'd lead"). Speeches use "This is
    # the..." for emphasis, so it isn't a general sign of AI writing, but in
    # a letter it stands where the claim should be. Human cover letters had
    # none; Claude's letters with the skill had it in 11 of 85 red-team
    # drafts. The written-out "that is the..." warns everywhere under R40.
    rule("V11", "judgment", "'that's the' pointing back",
         r"\b(?:that's|this\s+is)\s+(?:the|what|how|why|where|exactly)\b(?:\s+[\w'-]+){0,3}",
         "make the thing the subject: 'I'd bring that coaching', not 'and that's the coaching I'd bring'",
         surfaces=L, keep=_points_back),
]

# ---------------------------------------------------------------- RATE ----
# Limits for the sentence shapes added in 1.5, set the same way as the
# others below: the rate nine in ten pieces of edited human writing stay at
# or under, per 1,000 words.
V05_RATE = 2.5
V06_RATE = 5.0
# Set in 1.7 the same way. Nine in ten human pieces have no "what the X did"
# at all, so the limit is 0 and the two-hit minimum decides (V10).
V10_RATE = 0.0

# Habits good writers also use. Each warns once per draft, only when the
# draft has at least two hits and runs above the rate that more than nine in
# ten pieces of edited human writing stay under. Thresholds are hits per
# 1,000 words; they're set from 944,440 words of edited human writing.
RATE = [
    rule("R09", "voice", "hedge words",
         r"\b(?:very|really|quite|fairly|somewhat|a\s+bit|kind\s+of|rather)\b",
         "cut the hedge; the number or the plain claim. 'The very first' passes",
         rate=3.5, keep=_is_hedge),
    rule("R41", "voice",
         "uncontracted form where speech contracts",
         r"\b(?:that\s+is|it\s+is|I\s+have|I\s+am|I\s+would|I\s+will|I\s+had|do\s+not|does\s+not|did\s+not|cannot|is\s+not|are\s+not|was\s+not|were\s+not|there\s+is|here\s+is|what\s+is|has\s+not|have\s+not|had\s+not|will\s+not|would\s+not|could\s+not|should\s+not|he\s+is|she\s+is|we\s+are|they\s+are|you\s+are|we\s+have|they\s+have|you\s+have|we\s+will|we\s+would|let\s+us)\b",
         "contract unless the emphasis is deliberate",
         rate=19.0),
    rule("P10", "plain language", "'just' as filler",
         r"\bjust\b",
         "keep it only if it changes the meaning",
         rate=1.5),
    # Since 1.4.1, keep drops the last three items of a list of four or more.
    rule("V01", "judgment", "list of three",
         r"(?<!, )\b[\w'-]+(?:\s[\w'-]+){0,3},\s[\w'-]+(?:\s[\w'-]+){0,3},?\s(?:and|or)\s[\w'-]+(?:\s[\w'-]+){0,3}\b",
         "fine when each item is specific and does work; a crutch when it stands in for logic",
         rate=8.0, keep=_is_list_of_three),
    # Added in 1.5: a sentence that opens on "That", "This" or "It" and points
    # back instead of naming the thing ("That deliverable is a document...",
    # "This is what I meant"). Human writers do it about as often as AI
    # drafts, so it warns only above the human rate.
    rule("V05", "judgment", "opener that points back",
         r"\b(?:that|this|these|those)(?:'s|\s+(?:is|was|are|were|means|meant|gives|gave|makes|made|leaves|left|"
         r"becomes|became|tells|told|shows|showed))\s+\S+"
         r"|\b(?:that|this|these|those)\s+(?!(?:is|was|are|were|means|meant|gives|gave|makes|made|leaves|left|becomes|"
         r"became|tells|told|shows|showed)\b)[a-z][\w-]*\s+(?:is|was|are|were|will|would|can|could|gives|gave|means|"
         r"meant|makes|made)\s+\S+"
         r"|\bit(?:'s|\s+is|\s+was)\s+(?:a|an|the|what|this|that|how|why|where|who)\b",
         "name the thing as the subject, or join the sentence to the one before",
         rate=V05_RATE, pos="sentence"),
    # Added in 1.7: a "what" clause standing in for a noun ("by what the unit
    # tests showed", "what your second shift would need"). Edited human
    # writing has 28 in 944,440 words and never two in one piece, so
    # nine in ten pieces have none, the limit is 0 and the two-hit minimum
    # decides. On letters each one warns. "Said", "says", "told" and "tell"
    # aren't in the list: "write down what the sign told you" names a real
    # message. Slots in brackets, headings, tables and label lines don't count,
    # and "is" or "was" can't sit inside the noun ("what the sign was meant
    # to say" names the message too).
    rule("V10", "judgment", "'what the X did' standing in for a noun",
         r"\bwhat\s+(?:the|your|our|their|my|his|her|its|this|that|these|those)\s+"
         r"(?:(?!(?:is|was|are|were|be|been|being)\b)[\w'-]+\s+){1,3}?"
         r"(?:(?:would|will|could|might|must|can|should)\s+)?(?:(?:have|has|had)\s+)?"
         r"(?:show(?:s|ed|n)?|did|does|do|need(?:s|ed)?|mean(?:s|t)?|found|finds|want(?:s|ed)?|"
         r"got|gets|has|had|have|made|makes)\b",
         "name the thing ('the unit test results', not 'what the unit tests showed'), or put the actor first "
         "('the unit tests showed which students to regroup')",
         rate=V10_RATE, keep=_what_clause, block_keep=True, per_hit=L),
]

# V02 judged per 1,000 words: runs of three or more short sentences. Long
# human pieces almost always contain one run, so a single run in a long
# piece says nothing. Set from the same human writing as the rates above.
V02_RATE = 2.5

# V09, added in 1.7: a letter's sentences that all run long. It reads the
# body only, between the greeting and the sign-off, with bracketed slots out,
# and warns once in a body of 200 words or more when fewer than 10% of its
# sentences run 10 words or fewer, or they average more than 24 words. The
# five test letters job-seeker-ops wrote with 1.6.2 had 0% to 7% short and
# averages of 23.5 to 30.9; the two it wrote without the skill had 22% and
# 28%, averaging 18.7 and 16.3. It sits beside V03, which warns at the other
# end (more than 35% short, or an average under 14).
V09_FLOOR = 0.10
V09_CEILING = 24.0
V09_MIN_WORDS = 200

# Colon reveals, moderated heavily. A colon
# followed by three words or fewer that end the sentence. The first one in a
# draft warns; every one after it blocks. A colon before a list or an
# explanation doesn't match, and neither does a label line or a colon that
# introduces a quote.
COLON_REVEAL = re.compile(r":\s+(?![\"'])(?!\d+[.)](?:\s|$))[^\s,;:.!?]+(?:\s+[^\s,;:.!?]+){0,2}[.!?](?:\s|$)")

# A label line: one to four words and a colon at the start of a line, like
# "Budget: $40K." or "**Owner:** Parks Department". A line that opens on an
# article or a pronoun ("The result: chaos.") is prose, not a label.
_LABEL = re.compile(
    r"^\s*(?:[-*•+]\s+)?(?:\*\*|__)?"
    r"(?!(?:The|A|An|This|That|These|Those|Here|Here's|There|There's|What|Why|How|It|It's|Our|My|Your|"
    r"Their|His|Her|Its|We|I|You|They|And|But|So|Or|One|Every|Each|All)\b)"
    r"[A-Z0-9][\w&/()'.+-]*(?:\s+[\w&/()'.+-]+){0,3}(?:\*\*|__)?:(?:\*\*|__)?\s+\S")

_SIGNOFF = re.compile(r"^\s*(?:best|thanks|thank\s+you|many\s+thanks|sincerely|regards|best\s+regards|"
                      r"warm\s+regards|kind\s+regards|warmly|cheers|yours(?:\s+truly)?|respectfully|"
                      r"all\s+the\s+best|talk\s+soon)[,.!]?\s*$", re.IGNORECASE)
_HEADING = re.compile(r"\s*#{1,6}(?:\s|$)")
_ITEM = re.compile(r"\s*(?:[-*•+\u2013]|\d+[.)]|" + _ARROW_EMOJI + r")\s")
# A divider: three or more hyphens, stars or underscores, spaced or not,
# with an optional mark at either end, like a cut line ("✂ - - - -").
_RULE_LINE = re.compile(r"\s*(?:[^\w\s]\ufe0f?\s*)?(?:[-*_]\s*){3,}(?:[^\w\s]\ufe0f?\s*)?$")
_DASH_LED = re.compile(r"\s*[\u2013\u2014]")

_CLOSERS = {"“": "”\"", "«": "»", '"': "\"”", "‘": "’'", "'": "'’"}


def mask_quotes(s):
    """Blank out the words inside quotation marks, keeping the marks and
    every offset where it was, so a source's own words never count against
    the draft. Reads straight and curly quotes, double and single, and
    guillemets; a curly opening mark may close on a straight one and the
    reverse. A straight quote opens only after a space or a bracket, so an
    inch mark (12") opens nothing, and a single quote opens only before a
    letter, so '90s opens nothing. An apostrophe inside a word never closes
    a quote. An unclosed quote runs to the end of the paragraph only when it
    opens the paragraph, the way a quote that runs across paragraphs is
    written."""
    chars = list(s)
    n, i = len(s), 0
    while i < n:
        c = s[i]
        if c not in _CLOSERS or i + 1 >= n or s[i + 1].isspace():
            i += 1
            continue
        if c in "\"'" and i > 0 and s[i - 1] not in " \t([{/\u2014\u2013-*_":
            i += 1
            continue
        if c in "'‘" and (not s[i + 1].isalpha() or (i > 0 and s[i - 1].isalnum())):
            i += 1
            continue
        close = _CLOSERS[c]
        j = i + 1
        while j < n:
            if s[j] in close and not (s[j] in "'’" and j + 1 < n and s[j + 1].isalpha()):
                break
            j += 1
        if j >= n and s[:i].strip(" \t*_>-") != "":
            i += 1
            continue
        for k in range(i + 1, min(j, n)):
            chars[k] = " "
        i = j + 1
    return "".join(chars)


def _is_salutation(raw, t):
    """A letter's greeting line. "Dear..." and "Hi..." lines can run long
    ("Dear Members of the Hiring Committee at Acme,"); a "To..." line has to
    be short, so a sentence like "To make the case, we compared three
    cities," stays prose."""
    if not _SALUTATION.match(raw):
        return False
    return len(t.split()) <= (6 if t[:2].lower() == "to" else 15)


def blocks_of(text):
    """Split a draft into what a reader sees as units: paragraphs, list
    items, headings, table rows, block quotes, label lines and the
    salutation and sign-off of a letter. Lines that wrap inside a paragraph,
    a list item or a label line are joined with a space, so a phrase split
    by a line break still matches; so is a line that opens on a dash in the
    middle of a sentence. A short line with no closing punctuation followed
    by a capitalized line stays apart, since that's a title or an address,
    not a wrap. Each block is a dict: text (the joined line), raw (the same
    with curly quotes read as straight), line (raw with the words inside
    quotes blanked), starts (the offset and line number where each source
    line begins) and kind."""
    blocks, cur, prev = [], None, ""
    for i, raw in enumerate(mask_code(text).splitlines(), 1):
        t = raw.strip()
        if not t:
            cur = None
            continue
        p = prev.strip()
        unfinished = not re.search(r"[.!?:;]$", p)
        if _HEADING.match(raw):
            kind = "heading"
        elif t.startswith(">"):
            kind = "quote"
        elif t.startswith("|"):
            kind = "table"
        elif _RULE_LINE.match(raw):
            kind = "rule"
        elif _is_salutation(raw, t) or _SIGNOFF.match(raw):
            kind = "single"
        elif _LABEL.match(raw):
            kind = "label"
        elif (_DASH_LED.match(raw) and cur is not None and cur["kind"] == "text" and unfinished
              and re.match(r"\s*[\u2013\u2014]\s*[a-z]", raw)):
            kind = "text"                 # "...in March\n– two weeks early": a dash, not a bullet
        elif _ITEM.match(raw):
            kind = "item"
        else:
            kind = "text"
        title_break = len(p) < 40 and unfinished and not p.endswith(",") and t[:1].isupper()
        if kind == "text" and cur is not None and not title_break:
            base = cur["text"].rstrip()
            cur["starts"].append((len(base) + 1, i))
            cur["text"] = base + " " + t
        else:
            cur = {"text": raw.rstrip(), "starts": [(0, i)], "kind": kind}
            blocks.append(cur)
            if kind not in ("text", "item") and not (kind == "label" and unfinished_line(t)):
                cur = None
        prev = raw
    for b in blocks:
        b["raw"] = b["text"].translate(_QUOTES)
        b["line"] = mask_quotes(b["text"]).translate(_QUOTES)
    return blocks


def unfinished_line(t):
    """A label line that stops mid-sentence ("Goal: help the county
    drive") goes on to the next line."""
    return not re.search(r"[.!?:;]$", t.strip())


def _line_at(block, offset):
    ln = block["starts"][0][1]
    for off, n in block["starts"]:
        if off > offset:
            break
        ln = n
    return ln


def at_sentence_start(line, pos):
    """True when the text before pos ends a sentence, or holds only marks:
    a heading mark, a bullet, an emoji, a quote mark or a table bar. A
    capital after a colon starts a sentence too ("Goal: Empower teams")."""
    if not re.search(r"[A-Za-z0-9]", line[:pos]):
        return True
    before = re.sub(r"[\"'(\[“‘*_]+$", "", line[max(0, pos - 300):pos].rstrip()).rstrip()
    if re.fullmatch(r"\s*(?:#{1,6}|>|[-*•+\u2013]|\d+[.)])", before) or before.endswith("|"):
        return True
    if before.endswith(":") and line[pos:pos + 1].isupper():
        return True
    return bool(re.search(r"[.!?][\"')\]”’*_]*$", before))


_SMALL_WORDS = frozenset("a an the and or but nor for so yet of in on at to by with from as into onto "
                         "per via vs is are was were be".split())


def _title_case(line, pos):
    """True when the sentence around pos is a headline in title case, where
    capitals don't mark names. The sentence's first word doesn't count, and
    neither does a run of capitalized words in the middle of the sentence
    that holds the hit, since that run is the name being tested."""
    lo = max(0, pos - 400)
    start = lo
    for m in re.finditer(r"[.!?][\"')\]]*\s+", line[lo:pos]):
        start = lo + m.end()
    m = re.search(r"[.!?](?:\s|$)", line[pos:pos + 400])
    end = pos + m.end() if m else min(len(line), pos + 400)
    toks = [(start + t.start(), t.group(0)) for t in re.finditer(r"[A-Za-z][A-Za-z'-]*", line[start:end])]
    if not toks:
        return False
    idx = next((k for k, (o, w) in enumerate(toks) if o + len(w) > pos), len(toks) - 1)
    a = b = idx
    while a > 0 and toks[a - 1][1][0].isupper():
        a -= 1
    while b + 1 < len(toks) and toks[b + 1][1][0].isupper():
        b += 1
    skip = {0} | (set(range(a, b + 1)) if a > 0 else set())
    words = [w for k, (o, w) in enumerate(toks) if k not in skip and w.lower() not in _SMALL_WORDS]
    return len(words) >= 2 and sum(1 for w in words if w[0].isupper()) / len(words) >= 0.75


def is_name(line, m):
    """True when a hit is a name: a capitalized word in the middle of a
    sentence (Synergy Health, Google Drive), or a capitalized word at the
    start of a sentence when the next word is capitalized too (Robust
    Intelligence, Foster + Partners), but not an acronym ("Leveraging AI").
    A capitalized word joined to another by + or & is a name anywhere, even
    in a heading written in title case ("## Why Foster + Partners").
    Never a name: "I", a word in capitals for emphasis ("GAME-CHANGER"), a
    hyphenated word ("Results-driven") and a word ending in -ed or -ing
    ("Spearheaded", "Leveraging"). In a title written in title case,
    capitals don't mark names. Pass the line with the quotes left in, so a
    sentence that ends inside a quote still ends."""
    s = m.start()
    w = re.match(r"[\w'-]*", line[s:]).group(0)
    if not w[:1].isupper() or w == "I" or w.startswith("I'"):
        return False
    if (len(w) > 1 and w.isupper()) or "-" in w or re.search(r"(?:ed|ing)$", w.lower()):
        return False
    after = line[s + len(w):s + len(w) + 40]
    if re.match(r"\s*[+&]\s*[A-Z]", after) or re.search(r"[A-Z][\w'-]*\s*[+&]\s*$", line[max(0, s - 40):s]):
        return True           # a name joined by + or &: Foster + Partners, Johnson & Johnson
    if _title_case(line, s):
        return False
    if not at_sentence_start(line, s):
        return True
    if re.search(r"\s", m.group(0).strip()) or re.search(r"[.!?,;:]$", m.group(0)):
        return False          # a phrase opening the sentence ("In summary"), or a word that ends one
    nxt = re.match(r"\s*(?:[+&]\s*)?([A-Za-z][\w'-]*)", line[m.end():m.end() + 80])
    return bool(nxt and nxt.group(1)[0].isupper() and not nxt.group(1).isupper())


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
    quotes, tables, label lines or bracketed notes. Used by the choppiness
    checks."""
    keep = []
    for line in mask_code(text).splitlines():
        t = line.strip()
        if (re.match(r"(?:#|[-*•]\s|\d+[.)]\s|>|\|)", t) or (t.startswith("[") and t.endswith("]"))
                or _LABEL.match(line)):
            keep.append("")
        else:
            keep.append(line)
    return "\n".join(keep)


def word_count(text):
    """Words in the draft outside code, the denominator for every rate."""
    return len(mask_code(text).split())


def short_after_long(text):
    """V06: sentences of three to eight words that end on a period, right
    after a sentence of fifteen words or more, in the same paragraph or at
    the start of the next one ("An app isn't one product.", "The web moves
    on a different clock."). Prose only, with bracketed placeholders out."""
    ss = []
    for para in re.split(r"\n\s*\n", prose_only(text)):
        p = re.sub(r"\[[^\]]*\]", "", " ".join(para.split()))
        ss += [x.strip() for x in re.split(r'(?<=[.!?])["\']?\s+', p) if x.strip()]
    return [b for a, b in zip(ss, ss[1:])
            if len(a.split()) >= 15 and 3 <= len(b.split()) <= 8 and re.search(r"\.[\"')]?$", b)
            and b[:1] not in "\"'"]


# A sentence ends at a period, question mark or exclamation mark, with any
# closing marks, before a space (V08), but not at a title or an initial
# ("Mr. Speaker", "John A. Notte") or before a lowercase word ("e.g. the").
_SENTENCE_END = re.compile(r"[.!?]+[\"')\]*_]*\s+")
_NOT_AN_END = re.compile(r"(?:\b(?:Mr|Mrs|Ms|Mx|Dr|Prof|Rev|Hon|Gen|Gov|Sen|Rep|Sgt|Capt|Col|Lt|St|Mt|Ft|Jr|Sr|"
                         r"No|vs|Inc|Co|Corp|Ltd)|(?<![\w.])[A-Z])\.$")


def repeated_sentences(blocks):
    """V08: a sentence of six words or more that comes back word for word in
    the same piece, compared in lower case with the punctuation dropped.
    Returns (line, sentence) for each repeat after the first, so a sentence
    said three times gives two. Reads paragraphs, list items, label lines
    and a letter's greeting and sign-off, with words inside quotation marks
    counted, since the writer chooses to quote a line twice. Headings,
    tables, block quotes and code don't count."""
    seen, out = set(), []
    for b in blocks:
        if b["kind"] not in ("text", "item", "label", "single"):
            continue
        raw = b["raw"]
        cuts = [0] + [e.end() for e in _SENTENCE_END.finditer(raw)
                      if not _NOT_AN_END.search(raw[:e.start() + 1]) and not raw[e.end():e.end() + 1].islower()]
        cuts.append(len(raw))
        for a, z in zip(cuts, cuts[1:]):
            words = _words_of(raw[a:z])
            if len(words) < 6:
                continue
            key = " ".join(words)
            if key in seen:
                lead = len(raw[a:z]) - len(raw[a:z].lstrip())
                out.append((_line_at(b, a + lead), raw[a:z].strip()))
            else:
                seen.add(key)
    return out


def letter_sentences(blocks, text):
    """V09: a letter's body sentences. The body runs from the greeting to the
    sign-off, or from the first line of sixty characters or more when there's
    no greeting, so the header, the greeting, the sign-off and the name under
    it don't count. Paragraphs only, with bracketed slots taken out, split
    into sentences the way V08 splits them."""
    start = None
    for i, b in enumerate(blocks):
        if b["kind"] == "single" and _is_salutation(b["text"], b["text"].strip()):
            start = i + 1
            break
    if start is None:
        start = opener_block(blocks, text, "letter") or 0
    out = []
    for b in blocks[start:]:
        if b["kind"] == "single" and _SIGNOFF.match(b["text"]):
            break
        if b["kind"] != "text":
            continue
        raw = " ".join(re.sub(r"\[[^\]]*\]", "", b["raw"]).split())
        cuts = [0] + [e.end() for e in _SENTENCE_END.finditer(raw)
                      if not _NOT_AN_END.search(raw[:e.start() + 1]) and not raw[e.end():e.end() + 1].islower()]
        cuts.append(len(raw))
        out += [raw[a:z].strip() for a, z in zip(cuts, cuts[1:]) if re.search(r"[A-Za-z0-9]", raw[a:z])]
    return out


def document_checks(text, surface="general", skip=frozenset(), blocks=None, keep=()):
    """Checks that need the whole draft. Returns (hard, warn) lists of
    (line, label, hit, note) tuples; line 0 means the whole draft. Names and
    terms in `keep` are skipped by the rate rules too."""
    hard, warn = [], []
    if blocks is None:
        blocks = blocks_of(text)
    reveals = []
    for b in blocks:
        if b["kind"] in ("quote", "rule", "label"):
            continue
        for m in COLON_REVEAL.finditer(b["line"]):
            reveals.append((_line_at(b, m.start()), m.group(0).strip()))
    for n, (ln, hit) in enumerate(reveals if "S04" not in skip else []):
        label = "S04 colon reveal"
        if n == 0:
            warn.append((ln, label, hit, "one per piece at most, and only where it lands"))
        else:
            hard.append((ln, label, hit, "a second reveal in one piece; rewrite it as a plain sentence"))

    words = word_count(text)
    for r in RATE:
        if r["id"] in skip or surface not in r["surfaces"] or surface in r["per_hit"]:
            continue
        found = scan_blocks(blocks, [r], surface, text, keep)
        n = len(found)
        if words and n >= r["min_hits"] and 1000.0 * n / words > r["rate"]:
            shown = ", ".join(f"\"{h[2]}\" L{h[0]}" for h in found[:5]) + (", ..." if n > 5 else "")
            warn.append((0, f"{label_of(r)} (rate)",
                         f"{n} in {words} words, {1000.0 * n / words:.1f} per 1,000, where 9 in 10 pieces of "
                         f"edited human writing stay at or under {r['rate']:g}: {shown}", r["note"]))

    body = re.sub(r"\[[^\]]*\]", "", prose_only(text))
    sentences = [x.strip() for x in re.split(r'(?<=[.!?])["\']?\s+', body) if x.strip()]
    lengths = [len(x.split()) for x in sentences]
    run = worst = runs = 0
    for n in lengths:
        run = run + 1 if n <= 10 else 0
        if run == 3:
            runs += 1
        worst = max(worst, run)
    if runs >= 2 and 1000.0 * runs / words > V02_RATE and "V02" not in skip:
        warn.append((0, "V02 choppy run (rate)",
                     f"{runs} runs of three or more short sentences in {words} words, "
                     f"{1000.0 * runs / words:.1f} per 1,000; the longest has {worst}",
                     "fine only when it stacks proof points; otherwise join the sentences"))
    flat = short_after_long(text) if "V06" not in skip else []
    if len(flat) >= 2 and words and 1000.0 * len(flat) / words > V06_RATE:
        shown = ", ".join(f"\"{h}\"" for h in flat[:5]) + (", ..." if len(flat) > 5 else "")
        warn.append((0, "V06 short flat line after a long one (rate)",
                     f"{len(flat)} in {words} words, {1000.0 * len(flat) / words:.1f} per 1,000, where 9 in 10 pieces "
                     f"of edited human writing stay at or under {V06_RATE:g}: {shown}",
                     "fold the point into the long sentence, or cut the short line if it only restates it"))
    for ln, s in (repeated_sentences(blocks) if "V08" not in skip else []):
        warn.append((ln, "V08 sentence repeated word for word", s if len(s) <= 120 else s[:117] + "...",
                     "say it once; keep a repeat only for a stated reason, like a refrain or a line the user asked "
                     "for in two places"))
    if lengths and "V03" not in skip:
        short_share = sum(1 for n in lengths if n <= 10) / len(lengths)
        avg = sum(lengths) / len(lengths)
        if short_share > 0.35 or avg < 14:
            warn.append((0, "V03 choppy overall",
                         f"average {avg:.1f} words per sentence, {short_share:.0%} of 10 words or fewer",
                         "staccato is a tactic, never the default"))
    if surface == "letter" and "V09" not in skip:
        body = [len(x.split()) for x in letter_sentences(blocks, text)]
        if sum(body) >= V09_MIN_WORDS:
            short_share = sum(1 for n in body if n <= 10) / len(body)
            avg = sum(body) / len(body)
            if short_share < V09_FLOOR or avg > V09_CEILING:
                warn.append((0, "V09 long and flat",
                             f"{len(body)} sentences in the body, average {avg:.1f} words, {short_share:.0%} of "
                             f"10 words or fewer, where a letter wants at least {V09_FLOOR:.0%} short and an "
                             f"average of {V09_CEILING:g} or less",
                             "split a long sentence where it holds two facts, so one stands short; a short line "
                             "that only restates the long one before it trips V06"))
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", prose_only(text)) if p.strip()]
    if len(paragraphs) >= 4 and "V04" not in skip:
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


def opener_block(blocks, text, surface):
    """The index of the block that holds the draft's first line: in a
    letter, the first body line after the salutation; in a resume, the
    first line of sixty or more characters; anywhere else, the first block
    that isn't a heading, a rule, a quote, a table, a label line or a
    greeting."""
    if surface in ("letter", "resume"):
        ln = opener_line(mask_code(text).splitlines())
        for bi, b in enumerate(blocks):
            if any(n == ln for _off, n in b["starts"]):
                return bi
        return None
    for bi, b in enumerate(blocks):
        if b["kind"] not in ("heading", "rule", "quote", "table", "single", "label"):
            return bi
    return None


def _keep_spans(raw, keep):
    """Where the user's own names and terms sit in a line. Each term matches
    as given, with only its first letter free to change case, so
    "statistically significant" also covers "Statistically significant" at
    the start of a sentence, while "Seamless" doesn't cover "SEAMLESS"."""
    spans = []
    for term in keep:
        t = term.translate(_QUOTES).strip()
        if not t:
            continue
        head = f"[{t[0].upper()}{t[0].lower()}]" if t[0].isalpha() else re.escape(t[0])
        for k in re.finditer(r"(?<!\w)" + head + re.escape(t[1:]) + r"(?!\w)", raw):
            spans.append((k.start(), k.end()))
    return spans


def scan_blocks(blocks, rules, surface, text, keep=()):
    """The hits for these rules in already-split blocks. A hit that starts
    inside one of the user's names or terms in `keep` is skipped."""
    opener = opener_block(blocks, text, surface) if any(r["where"] == "opener" for r in rules) else None
    hits = []
    for bi, b in enumerate(blocks):
        if b["kind"] in ("quote", "rule"):
            continue
        line, raw = b["line"], b["raw"]
        spans = _keep_spans(raw, keep) if keep else ()
        for r in rules:
            if surface not in r["surfaces"]:
                continue
            if r["where"] == "opener" and bi != opener:
                continue
            for m in _compiled(r).finditer(line):
                if r["pos"] != "any" and at_sentence_start(raw, m.start()) != (r["pos"] == "sentence"):
                    continue
                if r["keep"] is not None and not (r["keep"](raw, m, b) if r["block_keep"] else r["keep"](raw, m)):
                    continue
                if is_name(raw, m):
                    continue
                if any(a <= m.start() < z for a, z in spans):
                    continue
                hits.append((_line_at(b, m.start()), label_of(r), m.group(0).strip(), r["note"]))
    hits.sort(key=lambda h: h[0])
    return hits


def scan(text, rules, surface="general", keep=()):
    """Return [(line, label, hit, note)] for every rule hit on this surface,
    in line order, then rule order. `text` is split on universal newlines;
    lines that wrap inside a paragraph are joined, quotes and block quotes
    are skipped, and so are names and the terms in `keep`."""
    if surface not in SURFACES:
        raise ValueError(f"unknown surface {surface!r}; one of {', '.join(SURFACES)}")
    return scan_blocks(blocks_of(text), rules, surface, text, keep)


def read_text(path):
    with open(path, encoding="utf-8-sig", newline=None) as fh:
        return fh.read()


def rule_ids():
    """Every ID the check can report, for --skip."""
    return {r["id"] for r in HARD + WARN + RATE} | {"S04", "V02", "V03", "V04", "V06", "V08", "V09"}


def report_files(paths, surface, by_rule=False, skip=frozenset(), keep=()):
    """Build the report lines for the given files. Returns (lines, any_hard).
    Rules in `skip` are turned off, for what the user's own instructions,
    samples or guide allow. Names and terms in `keep` are skipped."""
    out = []
    any_hard = False
    per_file = []
    words = {}
    hard_rules = [r for r in HARD if r["id"] not in skip]
    warn_rules = [r for r in WARN if r["id"] not in skip]
    warn_rules += [r for r in RATE if r["id"] not in skip and surface in r["per_hit"]]
    for path in paths:
        try:
            text = read_text(path)
        except OSError as e:
            out.append(f"FAIL: cannot read {path}: {e}")
            any_hard = True
            continue
        words[path] = len(text.split())
        blocks = blocks_of(text)
        hard = scan_blocks(blocks, hard_rules, surface, text, keep)
        warn = scan_blocks(blocks, warn_rules, surface, text, keep)
        dhard, dwarn = document_checks(text, surface, skip, blocks, keep)
        hard += dhard
        warn += dwarn
        per_file.append((path, hard, warn))
        if hard:
            any_hard = True

    out.append(f"check_voice {__version__}   surface: {surface}"
               + (f"   turned off: {', '.join(sorted(skip))}" if skip else "")
               + (f"   kept as given: {', '.join(keep)}" if keep else ""))
    if by_rule:
        groups = {}
        for path, hard, warn in per_file:
            for cls, hits in (("HARD", hard), ("WARN", warn)):
                for ln, label, hit, note in hits:
                    groups.setdefault((cls, label, note), []).append((path, ln, hit))
        order = {label_of(r): n for n, r in enumerate(HARD + WARN)}
        order.update({f"{label_of(r)} (rate)": len(order) + n for n, r in enumerate(RATE)})
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
            out.append(f"Words: {words[path]}")
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
    ap.add_argument("--surface", choices=SURFACES, default="general",
                    help="letter, blurb, linkedin, resume or general (default: general)")
    ap.add_argument("--skip", default="",
                    help="rule IDs to turn off, separated by commas, when the user's own instructions, "
                         "samples or guide allow what the rule blocks (for example --skip R01)")
    ap.add_argument("--keep", action="append", default=[],
                    help="the user's own names and technical terms, separated by commas, which the check skips "
                         "anywhere (for example --keep \"Seamless,Foster + Partners\"); for a name with a comma "
                         "in it, pass its distinctive part")
    ap.add_argument("--by-rule", action="store_true", help="group hits by rule across files")
    ap.add_argument("--out", help="write the report to this file (UTF-8, LF)")
    ap.add_argument("--list-rules", action="store_true", help="print the rule table and exit")
    args = ap.parse_args(argv)

    if args.list_rules:
        for cls, rules in (("HARD", HARD), ("WARN", WARN), ("RATE", RATE)):
            for r in rules:
                surf = "all" if r["surfaces"] == ALL else ",".join(s for s in SURFACES if s in r["surfaces"])
                extra = f"\tabove {r['rate']:g} per 1,000 words" if r["rate"] is not None else ""
                if r["per_hit"]:
                    extra += f", every hit on {','.join(s for s in SURFACES if s in r['per_hit'])}"
                print(f"{cls}\t{r['id']}\t{r['section']}\t{r['label']}\t{surf}\t{r['where']}{extra}")
        print(f"HARD\tS04\truling\tcolon reveal, the second in a piece (the first warns)\tall\tdraft")
        print(f"RATE\tV02\tjudgment\truns of three or more short sentences\tall\tdraft\tabove {V02_RATE:g} per 1,000 words")
        print(f"RATE\tV06\tjudgment\tshort flat line after a long one\tall\tdraft\tabove {V06_RATE:g} per 1,000 words")
        print(f"WARN\tV03\tjudgment\tchoppy overall\tall\tdraft")
        print(f"WARN\tV04\tjudgment\tstaccato layout\tall\tdraft")
        print(f"WARN\tV08\tjudgment\tsentence repeated word for word\tall\tdraft")
        print(f"WARN\tV09\tjudgment\tsentences long and flat\tletter\tdraft")
        return 0
    skip = frozenset(s.strip().upper() for s in args.skip.split(",") if s.strip())
    unknown = sorted(skip - rule_ids())
    if unknown:
        ap.print_usage()
        print(f"check_voice.py: unknown rule ID(s) for --skip: {', '.join(unknown)} (see --list-rules)")
        return 2
    if not args.files:
        ap.print_usage()
        print("check_voice.py: a draft file is required (see --help)")
        return 2

    keep = tuple(t.strip() for v in args.keep for t in v.split(",") if t.strip())
    lines, any_hard = report_files(args.files, args.surface, args.by_rule, skip, keep)
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
