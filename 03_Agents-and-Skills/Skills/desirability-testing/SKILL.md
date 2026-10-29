---
name: desirability-testing
title: Test whether users actually want the concept
description: Measure participants' emotional responses to the prototype using reaction cards or word-association — to surface desirability and brand-fit signals that task-based testing misses. Use when the sprint question includes appeal, trust, or "would you use this?" components, or when the concept represents a significant change from the current product and the team needs to understand whether the change is welcomed or threatening.
status: stable
contract-exempt: "design-method knowledge skill — a reusable thinking tool, not an executable contract"
when_to_load:
  - When the sprint question includes appeal, trust, or "would you use this?" components
  - When the concept represents a significant change from the current product and the team needs to understand whether the change is welcomed or threatening
  - When the Decider needs to distinguish between "technically works" and "people want it"
  - When multiple concepts are being compared — desirability testing provides a numeric signal for comparison alongside task performance data
  - At the end of Act 4 or during Act 5 debrief — after the participant has fully experienced the prototype
applies-to: emotional response measurement, brand perception, desirability signal, concept appeal, feature prioritisation by affect
done_when:
  - Participants react to the concept against desirability signals
  - Want/no-want evidence is captured, not just usability notes
  - Findings feed the synthesis and forward decision
metadata:
  duration: 5–10 min within Five-Act Interview (Act 4 or Act 5 debrief)
  team-size: Interviewer; observer logs reactions
  sprint-phase: 6 Validate
---

# Desirability Testing

**TL;DR:** Desirability testing measures how people *feel* about a product, not just whether they can use it. The most common technique is the Product Reaction Cards: 118 cards with single adjectives (both positive and negative). After the prototype interaction, participants select the words that best describe their experience. The spread of words — and the reasons participants give for their choices — reveals emotional fit, brand alignment, and the gap between "usable" and "desirable." A product that tests well on task completion but scores low on desirability will fail in adoption.

## When to use

- When the sprint question includes appeal, trust, or "would you use this?" components
- When the concept represents a significant change from the current product and the team needs to understand whether the change is welcomed or threatening
- When the Decider needs to distinguish between "technically works" and "people want it"
- When multiple concepts are being compared — desirability testing provides a numeric signal for comparison alongside task performance data
- At the end of Act 4 or during Act 5 debrief — after the participant has fully experienced the prototype

## Product Reaction Cards — condensed sprint set

The full set has 118 cards. For sprint use, a curated set of 40 is sufficient — covering the key emotional dimensions:

**Positive (20):**
Approachable · Attractive · Clearly Structured · Comprehensive · Confident · Convenient · Creative · Dependable · Efficient · Empowering · Engaging · Easy to Use · Fast · Familiar · Innovative · Intuitive · Professional · Reliable · Satisfying · Time-Saving

**Negative (20):**
Boring · Busy · Complex · Confusing · Disconnected · Distracting · Dull · Hard to Use · Inconsistent · Irrelevant · Intimidating · Overwhelming · Rigid · Slow · Time-Consuming · Unclear · Unattractive · Uncontrollable · Uninviting · Unpredictable

## Administration

**Instructions to participant:**
> "Here are 40 words. Some describe how people feel when they use products. Please select the 5 words that best describe your experience with what you just saw — there's no right answer, both positive and negative words are valid choices."

**After selection:**
> "You chose [word 1]. Can you tell me what made you choose that word?"

Follow up on every word selected — the story behind the word is more valuable than the count.

## Scoring and analysis

For a sprint (5 participants):

| Analysis | Method |
|---|---|
| **Word frequency** | Count how many participants chose each word; any word chosen by ≥3/5 participants is a signal |
| **Valence ratio** | Positive words chosen / total words chosen; a ratio ≥ 0.75 indicates broadly positive desirability |
| **Outlier watch** | A negative word chosen by all 5 participants is a critical signal even if overall valence is positive |
| **Comparison** | If testing multiple concepts, compare frequency tables side-by-side — the concept with more high-frequency positive words and fewer high-frequency negative words is the stronger desirability signal |

```markdown
## Desirability Test Results — [Sprint Name] · [Concept Name] · [Date]

### Word selection summary (n=5)

| Word | P1 | P2 | P3 | P4 | P5 | Total | Valence |
|---|---|---|---|---|---|---|---|
| Efficient | ✓ | ✓ | ✓ | ✓ | | 4 | + |
| Reliable | ✓ | ✓ | | ✓ | ✓ | 4 | + |
| Overwhelming | | ✓ | ✓ | ✓ | ✓ | 4 | – |
| Professional | ✓ | ✓ | ✓ | | | 3 | + |
| Confusing | | ✓ | ✓ | | ✓ | 3 | – |

### Valence ratio: 11 positive / 19 total = 0.58 ← below target

### Key story: "Overwhelming"
"I chose Overwhelming because there's too much on the detail screen — the urgency score, the records, the suggested priority. I'm sure it's all important but when I first see it I don't know where to look."
— P2, P3, P4 (all gave similar explanations)

### Signal: The prototype reads as powerful but over-dense at first exposure. Consider progressive disclosure for the inline records.
```

## Desirability testing variants

| Variant | Description | Best for |
|---|---|---|
| **Product Reaction Cards** | 40–118 adjective cards, select 5 | Comprehensive emotional profile; quantitative comparison |
| **Word Cloud / Open response** | "Write 3 words that describe this experience" | Fast; no card set required; less structured data |
| **Emoji reaction** | Participant selects 1–3 emojis at key moments | Remote testing; mobile-first |
| **Semantic differential scale** | Rate concept on bipolar adjective scales (Complex ← → Simple, Boring ← → Exciting) | Quantitative; easy to average across participants |
| **Would you use / recommend** | Single question: "Would you use this in your daily workflow? Why?" | Fast signal; complements CSAT data |

For sprint use: **Product Reaction Cards (40-card set)** or **semantic differential** are fastest to administer and produce comparable data across 5 participants.

## Watch-outs

- **Administering too early:** Desirability testing after 5 minutes of prototype exposure produces surface reactions. Administer after the participant has completed at least 2 tasks and experienced the core flow.
- **Reading into single words without follow-up:** "Complex" chosen by all 5 participants could mean "complex in a good way (powerful)" or "complex in a bad way (overwhelming)." Always ask "what made you choose that word?"
- **Desirability replacing usability data:** A product that is highly desirable but unusable will fail. Use desirability testing alongside task completion and error rate data, not instead of it.
- **Forcing participants to choose only positive words:** If the prototype is weak, participants will choose negative words. That is useful data. Do not signal to the participant which words you "want" them to choose.

## Agent facilitation guide

When conducting desirability testing analysis:
1. Tally word selections across all participants (one count per participant per word)
2. Calculate valence ratio: positive words / total words chosen
3. Identify any word chosen by ≥3/5 participants — these are primary signals
4. For each high-frequency word: synthesise the verbal explanations participants gave
5. Flag: any negative word chosen by ≥3/5 participants (regardless of overall valence ratio) as a critical concern
6. Output: frequency table + valence ratio + 2–3 key stories from participant explanations

## Connects to

- [Five-Act Interview](../five-act-interview/SKILL.md) — desirability test runs during Act 5 (debrief); can also follow Act 4 tasks
- [Usability Metrics](../usability-metrics/SKILL.md) — desirability complements task completion rate; together they give usable + desirable picture
- [Synthesis](../research-synthesis/SKILL.md) — desirability word frequency is one of the synthesis inputs alongside task observations
- [Post-Test Survey](../post-test-survey/SKILL.md) — SUS measures ease-of-use; desirability testing measures emotional appeal — use both
