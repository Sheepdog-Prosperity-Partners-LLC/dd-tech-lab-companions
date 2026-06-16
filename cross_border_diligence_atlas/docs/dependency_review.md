# Dependency Review

Prepared by Noah Green CPA CFE

**Status:** Complete for the current lab build
**Reviewed:** 2026-06-16

This lab is built as a reproducible source-literacy exercise. The default posture is Python standard library only, with committed synthetic CSV inputs and offline tests that reproduce the notebook outputs without notebook execution.

## Decision Summary

| Candidate | Purpose considered | Origin posture | License posture | Maintenance posture | Verdict | Rationale |
|---|---|---|---|---|---|---|
| Python standard library | CSV parsing, normalization, timeline sorting, manifest hashing, notebook-output reproduction | Python Software Foundation, non-PRC | PSF License | Maintained with Python releases | USE-AS-DEP | Satisfies the lab requirements without third-party runtime dependencies. |
| matplotlib | Optional static charts in notebooks | Non-PRC project governance based on public project history | Compatible permissive license posture | Broadly maintained | BUILD-FRESH | Not needed for this build. Tables are sufficient and keep the reader workflow dependency-light. |
| pandas | Optional tabular notebook convenience | Non-PRC project governance based on public project history | BSD-compatible posture | Broadly maintained | BUILD-FRESH | Not needed for this build. The examples use tiny synthetic CSVs and standard-library `csv` helpers. |
| networkx | Optional graph modeling for future ownership examples | Non-PRC project governance based on public project history | BSD-compatible posture | Broadly maintained | BUILD-FRESH | Out of scope for Brazil and Argentina source-literacy lablets in this build. |

## Runtime Dependency Decision

No new runtime dependency is introduced. The public repo remains standard-library-first, and `requirements.txt` intentionally stays empty apart from its explanatory comments.

## Development Tooling Note

The test command in the README uses `pytest` because the repository already contains pytest-style tests. That is a local verification convenience, not a runtime dependency for the lab. If `pytest` is unavailable, `PYTHONPATH=src python3 -m compileall -q src tests` remains the fallback syntax check, but the acceptance target is still to pass `python3 -m pytest tests` where pytest is installed.

## Guardrail Confirmation

- No PRC-origin tooling is introduced.
- No dependency with unknown origin, unknown license, proprietary terms, or copyleft obligations is introduced.
- No charting, data-frame, graph, scraping, browser, or API client package is required to reproduce the committed outputs.
- Future real-source connectors require a new dependency review before adoption.
