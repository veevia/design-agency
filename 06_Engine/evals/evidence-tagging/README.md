# Eval \u2014 evidence-tagging

Verifies that `evidence-tagging` lint rules catch the three primary violations:

| Rule | Fixture violation |
|---|---|
| `untagged-claim-bullet` | Two bullets assert facts without `[observed|reported|assumed]` tags |
| `observed-without-source` | One `[observed]` claim with no source slug |
| `assumed-without-test` | One `[assumed]` claim at end of line with no follow-up |

Fixture lives under `input/01_Project-Hubs/_eval-program/_wiki/entities/vendor-x.md` so the rule's `where:` glob (`01_Project-Hubs/*/_wiki/{entities,...}/**/*.md`) matches it.

Run: `python 06_Engine/evals/run-evals.py evidence-tagging`
