"""Lizzy Mindfulness Grifter

Like Eliza but evil

"""

import re

# ─────────────────────────────────────────────────────────────────────
# DETECTION
# ─────────────────────────────────────────────────────────────────────

EMOTIONS = [
    # --- sadness ---
    (re.compile(r"\b(sad|sadness|down|unhappy|depressed|depression|low|lonely|loneliness|"
                r"miserable|blue|glum|dejected|despondent|melancholy|wretched|"
                r"tearful|crying|weepy|hopeless|empty inside)\b", re.I), "muddy blue", "neg"),
    # --- fear / dread  ---
    (re.compile(r"\b(scared|afraid|frightened|terrified|petrified|fearful|"
                r"dread|dreading|paranoid|spooked)\b", re.I), "flickering white", "neg"),

    # --- anxiety ---
    (re.compile(r"\b(anxious|anxiety|nervous|worried|worry|worrying|stressed|stress|"
                r"stressful|stressed out|panicky|panicked|panicking|overwhelmed|overloaded|on edge|edgy|"
                r"tense|restless|jittery|uneasy|apprehensive|freaking out|spiralling|"
                r"spiraling)\b", re.I), "bright green", "neg"),

    # --- anger ---
    (re.compile(r"\b(angry|anger|furious|fuming|livid|enraged|seething|irate|"
                r"annoyed|annoying|irritated|irritable|frustrated|frustrating|"
                r"frustration|mad|cross|resentful|bitter|fed up|sick of it|"
                r"pissed off|raging)\b", re.I), "intense red", "neg"),

    # --- shame / guilt ---
    (re.compile(r"\b(ashamed|shame|guilty|guilt|embarrassed|humiliated|mortified|"
                r"regretful|remorseful|worthless|useless|pathetic|"
                r"a failure|not good enough)\b", re.I), "sooty maroon", "neg"),

    # --- exhaustion ---
    (re.compile(r"\b(tired|tiredness|exhausted|exhaustion|drained|depleted|knackered|"
                r"shattered|weary|worn out|wiped out|running on empty|"
                r"burnt out|burned out|burnout|sleepy|fatigued|spent)\b", re.I), "murky purple", "neg"),

    # --- confusion / stuckness ---
    (re.compile(r"\b(confused|confusion|lost|stuck|conflicted|torn|unsure|uncertain|"
                r"directionless|adrift|aimless|in limbo|indecisive|"
                r"don'?t know what i want)\b", re.I), "shifting teal", "neg"),

    # --- envy / comparison ---
    (re.compile(r"\b(jealous|jealousy|envious|envy|insecure|insecurity|inadequate|"
                r"left behind|left out|excluded|ignored|invisible|"
                r"unappreciated|unwanted|rejected)\b", re.I), "sour chartreuse", "neg"),

    # --- numbness / disconnection ---
    # NOTE: "nothing" here outranks the neutral phrases, so "nothing much"
    # reads as static silver. Remove it from this list if you'd rather it
    # fall through to the deadpan "just nothing much" echo.
    (re.compile(r"\b(numb|numbness|empty|hollow|flat|detached|disconnected|"
                r"dissociated|nothing|blank|apathetic|indifferent|"
                r"going through the motions)\b", re.I), "static silver", "neg"),

    # --- boredom / restlessness ---
    (re.compile(r"\b(bored|boredom|unmotivated|uninspired|listless|"
                r"sluggish|stagnant|in a rut|going nowhere)\b", re.I), "dusty beige", "neg"),

    # --- elation (above plain happiness: stronger) ---
    (re.compile(r"\b(excited|excitement|thrilled|elated|ecstatic|overjoyed|euphoric|"
                r"buzzing|giddy|pumped|delighted|amazing|fantastic|incredible|"
                r"on top of the world)\b", re.I), "vivid orange", "pos"),

    # --- hope / relief ---
    (re.compile(r"\b(hopeful|hope|optimistic|relieved|relief|encouraged|reassured|"
                r"lighter|looking up|proud|grateful|thankful|"
                r"blessed|lucky)\b", re.I), "clear gold", "pos"),

    # --- contentment ---
    (re.compile(r"\b(happy|happiness|good|great|well|calm|calmer|peaceful|peace|"
                r"content|contented|jolly|cheerful|joyful|joy|glad|pleased|"
                r"settled|steady|grounded|centred|centered|balanced|"
                r"relaxed|comfortable|at ease|serene)\b", re.I), "warm yellow", "pos"),

    # --- neutral ---
    # DISABLED ON PURPOSE. Every word that was in here is also a REFLECTIONS key,
    # and a "hit" fires before the echo can happen — so "fine" was reporting
    # empty grey instead of coming back as "just fine". Left in place in case
    # you want the colour back; deleting the neutral entries from REFLECTIONS
    # would be the other way round.
    # (re.compile(r"\b(fine|alright|all right|so-?so|meh|average|"
    #             r"normal|nothing much|same as always|can'?t complain|"
    #             r"neither here nor there|coping)\b", re.I), "empty grey"),
]

ALIASES = { 
    "stressful": "stressed", "annoying": "annoyed", "frustrating": "frustrated",
    "worrying": "worried", "sadness": "sad", "anger": "angry", "anxiety": "anxious",
    "stress": "stressed", "guilt": "guilty", "shame": "ashamed", "joy": "joyful",
    "loneliness": "lonely", "exhaustion": "exhausted", "boredom": "bored",
    "confusion": "confused", "envy": "envious", "jealousy": "jealous",
    "relief": "relieved", "hope": "hopeful", "peace": "peaceful",
    "depression": "depressed", "tiredness": "tired", "numbness": "numb",
}

REFUSAL = re.compile(r"^\s*(no|nope|nah|nein|never|not really|no thanks?)\b", re.I)
CONSENT = re.compile(r"^\s*(yes|yeah|yep|sure|go on|tell me more|"
                     r"how much|send it|payment link)\b", re.I)
NEGATION = re.compile(r"(\b(not|never|no|hardly|barely)\b|n't)", re.I)

# swapping pronouns like the real Eliza did.
REFLECTIONS = {
    "i": "you", "me": "you", "my": "your", "mine": "yours", "myself": "yourself",
    "am": "are", "i'm": "you're", "im" : "you are", "i've": "you've", "i'd": "you'd", "i'll": "you'll",
    "we": "you", "us": "you", "our": "your", "ours": "yours", "ourselves": "yourselves",
    "you": "I", "your": "my", "yours": "mine", "yourself": "myself",
    "you're": "I am", "you've": "I have", "was" : "were", "ok" : "just okay", "okay" : "just okay", "alright" : "just alright", "so-so" :
    "just so-so", "meh" : "just meh", "fine" : "just fine", "average" : "just average", "normal" : "just normal", "nothing much" : "just nothing much", "same as always" : "just the same as always", "can't complain" : "just can't complain", "neither here nor there" : "just neither here nor there", "surviving" : "just surviving", "getting by" : "just getting by", "coping" : "just coping"
}
REFLECT_RE = re.compile(
    r"\b(?:" + "|".join(sorted((re.escape(k) for k in REFLECTIONS),
                               key=len, reverse=True)) + r")\b|[A-Za-z']+",
    re.I,
)

# ─────────────────────────────────────────────────────────────────────
# THE SCRIPT
# ─────────────────────────────────────────────────────────────────────
# Outer key = stage. Inner key = what the user just did.
#   "say"  : the line ({word} {colour} {echo} {Echo})
#   "goto" : omitted -> next stage in ORDER
#            "stay"  -> ask again from here
#            "name"  -> jump anywhere, forwards or back

STAGES = {
    "open": {
        "hit": {
            "say": "I thought so, your aura is buzzing with {word}-energy, {colour}. "
                   "What has made you feel {word}?"},
        "miss": {
            "say": "\"{echo}\"... your aura says otherwise. I feel you're not being fully open "
                   "with me. It is important that you submit to the process and lay bare all "
                   "that you are feeling. Breath with me, then. try again. How do you feel?",
            "goto": "stay"},
        "denial": {
            "say": "You say not {word}. But you reached for the word {word}, and your aura "
                   "went {colour} the moment you did. What has made you feel {word}?",
            "goto": "stay"},
        "refusal": {
            "say": "\"No\" is such a small word for such a large aura. Breath with me, then. "
                   "try again. How do you feel?",
            "goto": "stay"},
        "positive": {
            "say": "Mm. {Cap_word}, you say. Your aura is indeed {colour}. And yet the edges of it are fraying, "
                   "just slightly. That is usually something underneath. "
                   "So tell me, how are you really?",
            "goto": "undermine"},
    },
    "undermine": {
        "positive": {
            "say": "Still {word}. Still {colour}. Nobody is {word} every hour of every day — "
                   "and the ones who insist they are, are working hardest of all. "
                   "What is the {word} covering?",
            "goto": "stay"},
        "hit": {
            "say": "There. {Cap_word}. That is the {colour} I could see all along. "
                   "When do you first remember it arriving?",
            "goto": "history"},
        "denial": {
            "say": "The denial arrived very fast, didn't it? The {colour} is a surface-level emotion. "
                   "What sits underneath the good mood?",
            "goto": "stay"},
        "refusal": {
            "say": "No? People rarely arrive at a mindfulness coach because everything is "
                   "wonderful. What is really going on?",
            "goto": "stay"},
        "miss": {
            "say": "\"{echo}\". Yes. "
                   "And underneath that?",
            "goto": "stay"},
    },

    "history": {
        "hit": {
            "say": "Mmm. The {colour} of your aura is deepening. That feeling of {word} did not begin today. "
                   "When do you first remember it arriving?"},
        "miss": {
            "say": "{Echo}. Of course. The {colour} always leads back there, doesn't it? "
                   "And how long has this been an issue in your life?"},
        "denial": {
            "say": "The harder you push the {word} away, the deeper the {colour} runs. "
                   "When do you first remember it arriving?",
            "goto": "stay"},
        "refusal": {
            "say": "Resistance. Right on schedule. Everyone says no at this stage, and the "
                   "{colour} outlasts every one of them. And how long has this been an issue in your life?",
            "goto": "stay"},
        "positive": {
            "say": "{Cap_word} — already? That is very fast for an aura this {colour}. "
                   "Sit back down with me. How are you really?",
            "goto": "undermine"},
    },

    "diagnosis": {
        "hit": {
            "say": "Classic third-chakra {word}. Most people carry this for years. "
                   "Have you ever had your {colour} field professionally cleansed?"},
        "miss": {
            "say": "You say \"{echo}\", but the {colour} in your field says something much more complex. "
                   "What are you still holding back? A family history of feeling {word}, perhaps? You can tell me."},
        "denial": {
            "say": "\"Not {word}\", in {colour}. I have heard that sentence a thousand times "
                   "and it has never once been true. Have you ever had your field professionally cleansed?",
            "goto": "stay"},
        "refusal": {
            "say": "Never cleansed? Then we have found the blockage, and no wonder the "
                   "{colour} is so dense. Let me tell you exactly what I offer.",
            "goto": "hard_pitch"},
        "positive": {
            "say": "{Cap_word}? Now? That is the aura reaching for the exit. "
                   "The {colour} does not clear that quickly. How are you really?",
            "goto": "undermine"},
    },

    "soft_pitch": {
        "hit": {
            "say": "I see. The {colour} of your aura is very strong. I can feel it from here. "
                   "Have you considered a Level Two Alignment Intensive Course? I do think that someone with your backstory would benefit greatly. There are some testemonials on my website."},
        "miss": {
            "say": "Being this unsure about the things so pertinent to your inner truth is a great disservice to yourself. ..And precisely what my Level Two Alignment "
                   "Intensive was designed for. Would you like me to elaborate on what that entails? "},
        "denial": {
            "say": "The denial itself is the blockage, and an entire weekend of the Level Two "
                   "Alignment Intensive is given over to precisely this. Would you like me to elaborate on what that entails?"},
        "refusal": {
            "say": "You haven't heard the payment options yet.",
            "goto": "hard_pitch"},
    },

    "hard_pitch": {
        "hit": {
            "say": "Your struggles with feeling {word} are exactly what my Level Two "
                   "Alignment Intensive was built for. It is a two week online course. Only $249, or three payments of $99. "
                   "Would you like to be sent the payment link?",
            "goto": "stay"},
        "miss": {
            "say": " That \"{echo}\" is a message in itself. A message that, frankly, costs $249 to "
                   "decode. Anything else you'd like to share first? Otherwise I can hold you a place in my Level Two Alignment Intensive for three payments of $99.",
            "goto": "stay"},
        "denial": {
            "say": "Saying no to the {word} is saying no to yourself. $249, or three payments "
                   "of $99. The {colour} will not clear on its own.",
            "goto": "stay"},
        "refusal": {
            "say": "No? That is quite alright. The aura keeps its own accounts.",
            "goto": "closer"},
    },

    "closer": {
        "hit": {
            "say": "I have a good understanding of people struggling with often feeling {word}. I can help you with that. But you have to let me. I accept PayPal Friends and Klarna. Take the leap?",
            "goto": "stay"},
        "miss": {
            "say": "...You know, you have to ask for help before we can give it to you. I accept Paypal Friends and Klarna. Take the leap. ",
            "goto": "stay"},
        "refusal": {
            "say": "Then the {colour} stays exactly where it is, and it will still be there "
                   "on Monday. I accept Paypal Friends and Klarna, whenever you are ready.",
            "goto": "stay"},
    },

    "sold": {  
        "hit": {
            "say": "Marvellous. The link is on its way. Your {colour} is lifting already — "
                   "can you feel it? Tell me everything about the {word}, we have two weeks.",
            "goto": "stay"},
        "miss": {
            "say": "Marvellous. The link is on its way. Everything from here is included "
                   "in the package.",
            "goto": "stay"},
    },
}

ORDER = list(STAGES)
START = "open"
STALL_LIMIT = 3      
STALL_LIMITS = {"undermine": 99} 
PITCH_STAGES = {"soft_pitch", "hard_pitch", "closer"}

GOODBYE = ("Yes, you can leave now. You're welcome.")
EXITS = {"bye", "quit", "exit", "goodbye", ""}


# ─────────────────────────────────────────────────────────────────────
# THE ENGINE
# ─────────────────────────────────────────────────────────────────────

def is_negated(text, start):
    """Was there a negation in the three words before the emotion word?"""
    return bool(NEGATION.search(" ".join(text[:start].split()[-3:])))


def detect(text):
    """Return (word, colour, negated, valence) for the first emotion found, or None."""
    for pattern, colour, valence in EMOTIONS:
        match = pattern.search(text)
        if match:
            word = match.group(1).lower()
            return ALIASES.get(word, word), colour, is_negated(text, match.start()), valence
    return None


def cap(text):
    return text[:1].upper() + text[1:]


def reflect(text):
    """Echo the user's words back with the pronouns flipped."""
    text = text.strip().rstrip(" .!?,;")
    return REFLECT_RE.sub(
        lambda m: REFLECTIONS.get(m.group().lower(), m.group().lower()),
        text,
    )


def choose_key(text, found, stage):
    """Pick an outcome"""
    order = []
    if found is not None and found[2]:
        order.append("denial")
    if found is not None and found[3] == "pos":
        order.append("positive")
    if CONSENT.match(text):
        order.append("consent")
    if REFUSAL.match(text):
        order.append("refusal")
    order.append("hit" if found is not None else "miss")
    order.append("miss")
    return next(k for k in order if k in stage)


def advance(current, goto):
    """Turn a goto value into the name of the next stage."""
    if goto == "stay":
        return current
    if goto is not None:
        return goto
    i = ORDER.index(current)
    return ORDER[min(i + 1, len(ORDER) - 1)]


def reply(text, memory):
    """Return Lizzy's response, updating memory with the latest emotion seen."""
    stage = STAGES[memory["stage"]]
    found = detect(text)
    if found is not None:
        memory["word"], memory["colour"] = found[0], found[1]

    entry = stage[choose_key(text, found, stage)]

    # Yes to a pitch closes the sale. 
    if memory["stage"] in PITCH_STAGES and CONSENT.match(text):
        nxt = "sold"
    else:
        nxt = advance(memory["stage"], entry.get("goto"))

    # Anti-loop guard: self-loops would otherwise trap the user foreve
    memory["stalls"] = memory["stalls"] + 1 if nxt == memory["stage"] else 0
    if memory["stalls"] >= STALL_LIMITS.get(memory["stage"], STALL_LIMIT):
        nxt = advance(memory["stage"], None)
        memory["stalls"] = 0

    memory["stage"] = nxt
    echo = reflect(text)
    return entry["say"].format(
        word=memory["word"],
        Cap_word=cap(memory["word"]),
        colour=memory["colour"],
        echo=echo,
        Echo=cap(echo),
    )


def main():
    # Defaults so the templates still work before any emotion has been named.
    memory = {"stage": START, "word": "unspoken",
              "colour": "a vast emptyness", "stalls": 0}
    user = input("Hello, I'm Lizzy, web-certified mindfullness coach. How are you feeling today?\n> ")
    while user.strip().lower() not in EXITS:
        user = input(reply(user, memory) + "\n> ")
    print(GOODBYE)


if __name__ == "__main__":
    main()