# Brazil Source Map

Prepared by Noah Green CPA CFE

**Status:** Working source map for the lab
**Last reviewed:** 2026-06-16
**Purpose:** Show a U.S. diligence team which Brazilian public-source surfaces can support source literacy before relying on seller-provided records. This is not a legal opinion, a jurisdiction-level score, or a substitute for Brazilian counsel.

## Source Table

| Source | Official URL | Access method | Main identifiers | Update cadence | Terms posture | Lab use | Limit |
|---|---|---|---|---|---|---|---|
| Receita Federal Dados Abertos | https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/dados-abertos | Government portal and bulk files | CNPJ | Source-specific, verify on download | Official public portal; record access date and file metadata before production use | CNPJ parsing on synthetic sample | Identifier format quality does not prove current registration status. |
| Receita Federal data repository | https://www.gov.br/receitafederal/dados | Download repository for Receita Federal public datasets | CNPJ and tax-administration dataset fields | Source-specific, verify each file | Official public repository; terms and file layout must be captured per pull | Future bulk-file loader | Layout and filenames can change. |
| Portal da Transparencia Sancoes | https://portaldatransparencia.gov.br/sancoes | Portal search, downloads, and API-linked records | CNPJ, CPF where lawfully public, sanctioning body fields | Source-specific, verify endpoint and extraction date | Official public portal; log endpoint, filters, access date, and terms page | Sanctions and debarment crosscheck on synthetic sample | A hit is a lead, not a finding. Read the official record and escalate. |
| Portal da Transparencia API | https://portaldatransparencia.gov.br/api-de-dados | API documentation and data endpoints | Endpoint-specific identifiers | Endpoint-specific | Official API; capture endpoint, parameters, rate limits, and terms before use | Future connector | API availability and schemas can change. |
| CVM Dados Abertos | https://dados.cvm.gov.br/ | Open-data portal and downloadable securities datasets | Registrant, fund, issuer, and filing fields | Dataset-specific | Official public data portal; terms and dataset metadata must be logged | Future securities registrant context | Not a general company registry. |
| Banco Central do Brasil IFData | https://dadosabertos.bcb.gov.br/ | Open-data portal downloads | Financial-institution and reporting fields | Dataset-specific | Official open-data portal; locate the current IFData dataset page and log metadata before use | Future regulated-institution example | Financial-institution context only. |
| Compras.gov.br Dados Abertos | https://dadosabertos.compras.gov.br/ | Swagger API documentation and federal procurement endpoints | Supplier and procurement-system fields | Endpoint-specific | Official public API; log endpoint, parameters, and terms before use | Future procurement crosscheck | Procurement participation is not adverse by itself. |

## Lab Positioning

The current Brazil notebooks use only synthetic rows shaped like Brazilian public-source records. They teach identifier normalization, source routing, and lead labeling. They do not query live government systems, make Brazilian-law conclusions, or clear a party for a transaction.

## Escalation

Escalate to Brazilian counsel, sanctions counsel, export counsel, anti-corruption counsel, or procurement counsel when a public record appears adverse, when a legal status must be interpreted, or when the result will affect price, closing, indemnity, escrow, termination rights, or a regulatory disclosure.
