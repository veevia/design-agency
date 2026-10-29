# Script style — transcript → optimized presentation script

Turn a raw transcript into a spoken script that's tight enough to present but keeps the real
substance. Default register here: **English studio keynote** (the source transcript is English,
audience is an internal design studio / XFN). Adapted from garden-skills `SCRIPT-STYLE.md`,
de-localized from a Chinese video-site style to an English keynote.

> **Three hard floors** (fail any → rewrite the whole script):
> 1. **Information retention ≥ 60%** — a re-say, not a summary. Cut filler/repetition/cross-talk;
>    keep facts, numbers, examples, names, and the argument chain.
> 2. **Strip AI-slop** — even short, second-person sentences can reek of machine if they use
>    fake-empathy / fake-profundity / self-aggrandizing / template phrases / 3-clause parallelism.
> 3. **Keep the source language** — English transcript → English script. Preserve real terms,
>    product names, quotes.

## Form rules (English keynote)

1. **Spoken, not written.** "Therefore one observes" → "So here's the thing." Contractions OK.
2. **Short sentences.** Aim ≤ 18 words. Break compound sentences. A presenter needs to breathe.
3. **Second person.** "you / we", not "the user / the reader / one".
4. **Hook first (cold open).** Beat 1 lands in ~3 seconds — a tension, a contrast, or a stake.
   - ✓ "Customers kept asking for AI magic. Our engineers kept saying: too much."
   - ❌ "Hi everyone, today I'll walk you through our engagement method."
5. **One idea per beat, split by `---`.** Each `---` is a scene-step boundary downstream.
6. **Numbers → stakes**, but keep the punchy ones literal. "We compressed six months of research
   into about three weeks" keeps the contrast; bury the rest.
7. **No structure-words / no template phrases.** Kill "first / second / finally", "in essence",
   "fundamentally", "at its core", "in conclusion", "to summarize". Let rhythm carry structure.
8. **Concrete over abstract.** "they wanted a dashboard — but couldn't say why" beats "stakeholders
   had unclear requirements."

## Strip AI-slop — five tics to delete

1. **Fake empathy** — "I know you've all struggled with…", "you're not alone". Just state the fact.
2. **Fake profundity** — "this is precisely why…", "what's remarkable is…". Drop the wrapper; if the
   point goes flat without it, the point was flat — fix the content, not the rhetoric.
3. **Self-aggrandizing** — "I want to be very clear here", "this part is crucial". Good points don't
   need a warm-up. Just say it.
4. **Template phrases** — "in essence / fundamentally / at the end of the day / simply put". Cut.
5. **Three-clause parallelism** — "it detects, it predicts, it prevents." Keep the one with the most
   information; replace the rest with a concrete example.

## Read-aloud test (the real gate)

Read 3 beats OUT LOUD. Any line you'd never actually say → AI-slop, rewrite. Any line you want to
skip → it's filler or parallelism. Fix and re-read until all three sound like a person talking.

## What to do after

1. Save as `script.md` (beats separated by `---`). Keep the raw transcript as the detail source.
2. Self-check against the form rules + the five tics + the read-aloud test BEFORE moving to outline.
3. Continue into the scene outline in the same pass (group beats into scenes, pull an info pool).
