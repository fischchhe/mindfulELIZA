# Lizzy

A rule-based conversational agent in the ELIZA tradition, playing a mindfulness
coach who is trying to sell you a course.

Built as the ELIZA exercise from Chapter 2 of Jurafsky and Martin, *Speech and
Language Processing*, then extended with a stage-based dialogue manager. Started out as regex practice but then became a fun thing to show my friends. 

## Background

Weizenbaum's ELIZA (1966) ran a script called DOCTOR that imitated a Rogerian
therapist. The choice of therapeutic style was deliberate: a Rogerian therapist
can reflect the patient's own words back at them indefinitely and still sound
competent, so the program needed no world knowledge at all. Pattern matching and
pronoun substitution were enough for users to attribute understanding to it.

Lizzy uses the same mechanics with a different script. Instead of reflecting
neutrally, she:

- assigns every stated emotion an aura colour and keeps referring to it
- treats denial as confirmation
- refuses to accept that a chat user could be in a positive mood
- pushes towards a $249 course over roughly six turns

## Running

```bash
python3 Eliza.py
```

Standard library only, no dependencies. Exit with `bye`, `quit`, `exit`, or an
empty line.

```
Hello, I'm Lizzy, web-certified mindfullness coach. How are you feeling today?
> im in a good mood today
Mm. Good, you say. Your aura is indeed warm yellow. And yet the edges of it are
fraying, just slightly. That is usually something underneath. So tell me, how
are you really?
```

## Architecture

Three layers. All content is data; the engine contains no dialogue and no
emotion vocabulary.

**1. Detection**

- `EMOTIONS`: list of `(pattern, colour, valence)`. 13 categories, priority
  ordered, since `detect()` returns on first match.
- `NEGATION`: three-word window before the match, so "not sad" is distinguished
  from "sad".
- `REFUSAL` / `CONSENT`: line-initial `no` and `yes`, matched with `.match()`
  rather than `.search()` so "there's no point" is not read as a refusal.
- `ALIASES`: normalises nouns and participles to the adjective form, so
  templates never produce "feeling stressful".
- `REFLECTIONS`: pronoun substitution, compiled into a single alternation sorted
  longest-key-first so multi-word entries match before their constituents.

Functionally this is a crude dialogue act classifier: rejection, acceptance,
inform.

**2. Script**

`STAGES` is a nested dict. Outer key is the dialogue stage, inner key is the
classified user move:

| key | fires when |
| --- | --- |
| `hit` | an emotion was named |
| `miss` | nothing matched |
| `denial` | an emotion was named under negation |
| `positive` | the emotion has positive valence |
| `refusal` | the turn opened with `no` |

Each entry holds a template (`say`) and a transition (`goto`):

- omitted: advance to the next stage in `ORDER`
- `"stay"`: repeat the current stage
- a stage name: jump anywhere in the graph

**3. Engine**

`reply()` runs the same sequence each turn: detect, update memory, select an
outcome key, resolve the transition, check the stall counter, format the
template.

- `choose_key()` returns only keys the current stage defines, falling back
  through a priority list to `miss`, so stages need not be exhaustive.
- `STALL_LIMIT` forces a transition after three self-loops, preventing dead
  ends. `STALL_LIMITS` overrides this per stage.

## The undermine loop

Positive valence routes to a dedicated `undermine` stage which can only be left
by producing a negative emotion (`hit` is checked after `positive`, so within
that stage a `hit` necessarily means negative). Its stall limit is set to 99.

This was added to fix a real bug rather than as a joke: positive input was being
processed by templates written for problems, producing output like "and how long
has this been an issue in your life" after the user said they felt good.
Encoding valence in the emotion table fixed it without special cases in the
engine.

## Extending

| Task | Edit |
| --- | --- |
| add a feeling | one tuple in `EMOTIONS` |
| change a line | one `say` in `STAGES` |
| reroute the dialogue | one `goto` |
| add a stage | one key in `STAGES`; `ORDER` derives from insertion order |

Validating the transition graph:

```python
for name, stage in STAGES.items():
    for key, entry in stage.items():
        goto = entry.get("goto")
        if goto not in (None, "stay") and goto not in STAGES:
            print(f"broken link: {name}.{key} -> {goto}")
```

## Known limitations

- **`nothing`** is in the numbness category, so "nothing is wrong" is read as
dissociation. Left in place deliberately.
- **The neutral category is disabled.** Its words are all `REFLECTIONS` keys,
  and a `hit` pre-empts the echo, so "fine" returned an aura colour instead of
  the intended "just fine". Kept in the source, commented, with the reason.
- **First-match-wins ordering** means category priority is positional. Adding a
  category in the wrong place changes classification.
- **No parsing of any kind.** Word-level pattern matching only, as in the
  original.

## Note

The persona is a parody of wellness marketing: confident diagnosis, manufactured
problem, paid solution. It is not a therapeutic tool and is not intended to
resemble one.

## References

Weizenbaum, J. (1966). ELIZA: A Computer Program For the Study of Natural
Language Communication Between Man And Machine. *Communications of the ACM* 9(1).

Jurafsky, D. and Martin, J. H. *Speech and Language Processing*, Chapter 2.