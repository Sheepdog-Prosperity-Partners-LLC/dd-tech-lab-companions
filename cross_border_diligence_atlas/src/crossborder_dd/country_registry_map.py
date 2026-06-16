"""Starter source map records for Brazil and Argentina."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SourceRecord:
    country: str
    source_name: str
    source_url: str
    access_method: str
    identifiers: tuple[str, ...]
    lab_use: str
    limitation: str


STARTER_SOURCES: tuple[SourceRecord, ...] = (
    SourceRecord(
        country="Brazil",
        source_name="Receita Federal Dados Abertos",
        source_url="https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/dados-abertos",
        access_method="portal and bulk files",
        identifiers=("CNPJ",),
        lab_use="CNPJ parsing on synthetic sample",
        limitation="Bulk file metadata must be captured before any real-data use.",
    ),
    SourceRecord(
        country="Brazil",
        source_name="Portal da Transparencia Sancoes",
        source_url="https://portaldatransparencia.gov.br/sancoes",
        access_method="portal, download, API",
        identifiers=("CNPJ", "CPF where public"),
        lab_use="sanctions screen on synthetic sample",
        limitation="A hit is a lead, not a finding.",
    ),
    SourceRecord(
        country="Argentina",
        source_name="Registro Nacional de Sociedades",
        source_url="https://www.argentina.gob.ar/justicia/registro-nacional-sociedades",
        access_method="search portal",
        identifiers=("CUIT", "CDI"),
        lab_use="source literacy only until terms are checked",
        limitation="No-hit is inconclusive.",
    ),
    SourceRecord(
        country="Argentina",
        source_name="Datos Justicia RNS",
        source_url="https://datos.jus.gob.ar/dataset/registro-nacional-de-sociedades",
        access_method="bulk ZIP datasets",
        identifiers=("CUIT", "CDI"),
        lab_use="RNS parser on synthetic sample",
        limitation="Schema review required before real-data use.",
    ),
)


def sources_by_country(country: str) -> list[SourceRecord]:
    wanted = country.strip().casefold()
    return [source for source in STARTER_SOURCES if source.country.casefold() == wanted]


def lab_enabled_sources() -> list[SourceRecord]:
    return [source for source in STARTER_SOURCES if "synthetic" in source.lab_use]
