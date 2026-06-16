# Data Sources

Prepared by Noah Green CPA CFE

**Status:** Current for the Brazil and Argentina lab notebooks
**Last reviewed:** 2026-06-16

No live government dataset is bundled in this repository. The committed input CSVs and publishable outputs are synthetic or redacted lab artifacts. Real-source links are documented in the country source maps and must be rechecked before production use.

## Committed Inputs

| Dataset | File | Source URL | Access date | Terms or license note | Update method | Status |
|---|---|---|---|---|---|---|
| Synthetic Brazil entities | `data/synthetic/brazil_entities.csv` | Synthetic lab data, no live URL | 2026-06-16 | Synthetic, safe for publication | Manual sample maintained in repo | Active lab input |
| Synthetic Brazil sanctions rows | `data/synthetic/brazil_sanctions.csv` | Synthetic lab data, no live URL | 2026-06-16 | Synthetic, safe for publication | Manual sample maintained in repo | Active lab input |
| Synthetic Argentina RNS rows | `data/synthetic/argentina_rns.csv` | Synthetic lab data, no live URL | 2026-06-16 | Synthetic, safe for publication | Manual sample maintained in repo | Active lab input |
| Synthetic Argentina gazette events | `data/synthetic/gazette_events.csv` | Synthetic lab data, no live URL | 2026-06-16 | Synthetic, safe for publication | Manual sample maintained in repo | Active lab input |

## Committed Outputs

| Dataset | File | Source URL | Access date | Terms or license note | Update method | Status |
|---|---|---|---|---|---|---|
| Brazil entity-registry screen output | `data/redacted_outputs/BR_01_entity_registry_screen.csv` | Generated from synthetic input | 2026-06-16 | Synthetic/redacted, safe for publication | Regenerate by running notebook or reproduction tests | Expected output |
| Brazil sanctions/procurement crosscheck output | `data/redacted_outputs/BR_02_sanctions_procurement_crosscheck.csv` | Generated from synthetic input | 2026-06-16 | Synthetic/redacted, safe for publication | Regenerate by running notebook or reproduction tests | Expected output |
| Argentina RNS entity-screen output | `data/redacted_outputs/AR_01_rns_entity_screen.csv` | Generated from synthetic input | 2026-06-16 | Synthetic/redacted, safe for publication | Regenerate by running notebook or reproduction tests | Expected output |
| Argentina gazette timeline output | `data/redacted_outputs/AR_02_boletin_timeline_builder.csv` | Generated from synthetic input | 2026-06-16 | Synthetic/redacted, safe for publication | Regenerate by running notebook or reproduction tests | Expected output |
| U.S. memo source-flag output | `data/redacted_outputs/US_memo_country_risk_flags.csv` | Generated from synthetic lab logic | 2026-06-16 | Synthetic/redacted, safe for publication | Regenerate by running notebook or reproduction tests | Expected output |

## Real-Source Registry

The lab docs point readers to official public-source surfaces, but no live download is included. Before any real-source use, record source URL, exact endpoint or file, access date, terms or license, update cadence, query parameters, and any source-specific warning in this file and the relevant country source map.
