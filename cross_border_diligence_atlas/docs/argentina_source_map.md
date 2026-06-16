# Argentina Source Map

Prepared by Noah Green CPA CFE

**Status:** Working source map for the lab
**Last reviewed:** 2026-06-16
**Purpose:** Show a U.S. diligence team which Argentine public-source surfaces can support source literacy before relying on seller-provided records. This is not a legal opinion, a jurisdiction-level score, or a substitute for Argentine counsel.

## Source Table

| Source | Official URL | Access method | Main identifiers | Update cadence | Terms posture | Lab use | Limit |
|---|---|---|---|---|---|---|---|
| Datos Argentina | https://datos.gob.ar/ | National open-data catalog and APIs | Dataset-specific | Dataset-specific | Public open-data catalog; read each dataset license and metadata | Source discovery | Catalog quality and dataset maintenance vary. |
| Registro Nacional de Sociedades | https://www.argentina.gob.ar/justicia/registro-nacional-sociedades | Search portal | CUIT, CDI, razon social | Search page states source-data dates and update notes | Official government search page; record query date and displayed source note | Entity-source literacy | No-hit is inconclusive. Local registry coverage and source dates matter. |
| RNS Datos Justicia | https://datos.jus.gob.ar/dataset/registro-nacional-de-sociedades | Bulk CSV and ZIP resources | CUIT, CDI, legal-person fields | Dataset page shows monthly update posture and resource dates | Creative Commons Attribution 4.0 on the dataset page as reviewed 2026-06-16 | RNS parser on synthetic sample | Schema review required before real-data use. |
| IGJ Datos Justicia | https://datos.jus.gob.ar/dataset/entidades-constituidas-en-la-inspeccion-general-de-justicia-igj | Bulk dataset | IGJ entity and authority fields | Dataset-specific | Check dataset metadata before use | Future local-registry parser | IGJ scope is not national completeness. |
| Boletin Oficial | https://www.boletinoficial.gob.ar/ | Official gazette search and notice pages | Publication date, entity name, notice class | Daily official publication pattern, verify per query | Official gazette site; preserve notice URL, date, and search terms | Timeline builder on synthetic sample | Search can miss notices and automated timeline summaries can omit context. |
| Boletin Oficial Timeline | https://timeline.boletinoficial.gob.ar/ | Timeline search tool | Entity name and notice timeline | Tool-specific | Read tool warnings and verify against official notice text | Future timeline lablet with warnings | Treat as source discovery only. Verify notice text in the official gazette. |
| CNV | https://www.cnv.gov.ar/ | Securities regulator portal | Issuer, filing, fund, and market-participant fields | Source-specific | Official portal; capture filing URL and access date | Future filing metadata example | Securities filings are disclosures, not adverse events by themselves. |
| BCRA API | https://www.bcra.gob.ar/apis-banco-central/ | Central bank API documentation | Endpoint-specific identifiers | API-specific | BCRA API page links manuals and legal notice per API | Future financial-system context examples | Avoid publishing personal or sensitive financial details. |

## Lab Positioning

The current Argentina notebooks use only synthetic rows shaped like Argentine public-source records. They teach CUIT normalization, RNS row parsing, official-gazette timeline construction, and conservative memo labeling. They do not query live systems, make Argentine-law conclusions, or clear a party for a transaction.

## Escalation

Escalate to Argentine counsel, securities counsel, anti-corruption counsel, privacy counsel, or other specialist counsel when a record appears adverse, when a notice's legal effect matters, or when the result will affect price, closing, indemnity, escrow, termination rights, or a regulatory disclosure.
