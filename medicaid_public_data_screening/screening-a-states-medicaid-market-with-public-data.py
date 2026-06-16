#!/usr/bin/env python3
"""Runnable script companion for the Medicaid public-data screening notebook.

This script is extracted from the paired notebook and preserves the same public
data workflow: NPPES provider cache, optional CMS Parquet grouping, address
clustering, controller rollup, growth-off-zero billing join, and optional
HHS-OIG LEIE timing checks. It uses public data only and prints public-safe
display identifiers.
"""


# Notebook cell 1
# Beginner setup
# Run this cell once in a fresh notebook environment.

# Notebook cell 2
# Step 1: Pull a de-duplicated NPPES provider cache. [beginner]
#
# This is a faithful distillation of case_03_lv_homecare/nppes_cluster.py,
# rewritten with requests for notebook readability. The defaults match the
# article's Nevada home-care example. NPPES is public and keyless.

import json
import re
import time
from pathlib import Path

import requests

NPPES_API = "https://npiregistry.cms.hhs.gov/api/"
TAXONOMY_DESCS = [
    "Home Health",
    "In Home Supportive Care",
    "Personal Care Attendant",
    "Behavior Analyst",
    "Behavior Technician",
]
CITIES = ["Las Vegas", "North Las Vegas", "Henderson"]
CACHE_PATH = Path("nppes_nv_records.json")


def api_query(taxonomy_desc, city, skip=0, limit=200):
    params = {
        "version": "2.1",
        "state": "NV",
        "city": city,
        "taxonomy_description": taxonomy_desc,
        "address_purpose": "LOCATION",
        "limit": limit,
        "skip": skip,
    }
    response = requests.get(
        NPPES_API,
        params=params,
        headers={"User-Agent": "dd-tech-lab-public-data-screen/1.0"},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def pull_window(taxonomy_desc, city):
    records = []
    skip = 0
    while skip <= 1000:  # NPPES caps skip at 1000, limit at 200.
        page = api_query(taxonomy_desc, city, skip=skip)
        results = page.get("results") or []
        records.extend(results)
        if len(results) < 200:
            break
        skip += 200
        time.sleep(0.2)
    return records


if CACHE_PATH.exists():
    nppes_cache = json.loads(CACHE_PATH.read_text())
    print(f"Loaded {len(nppes_cache):,} de-duplicated NPPES records from {CACHE_PATH}.")
else:
    seen = set()
    nppes_cache = []
    for taxonomy in TAXONOMY_DESCS:
        for city in CITIES:
            for record in pull_window(taxonomy, city):
                npi = record.get("number")
                if npi and npi not in seen:
                    seen.add(npi)
                    nppes_cache.append(record)

    CACHE_PATH.write_text(json.dumps(nppes_cache))
    print(f"Cached {len(nppes_cache):,} de-duplicated NPPES records to {CACHE_PATH}.")

# Notebook cell 4
# Step 2: Connect DuckDB to the CMS provider-level Medicaid Parquet. [beginner -> intermediate]
#
# Download the CMS provider-level Medicaid Parquet separately and place it next
# to this notebook as cms.parquet. Do not commit it.
#
# Source landing page:
# https://opendata.hhs.gov/datasets/medicaid-provider-spending/
# Direct bulk files are periodically versioned by CMS/HHS; use the current
# Parquet file from that landing page.

from pathlib import Path

import duckdb

CMS_PARQUET = Path("cms.parquet")
con = duckdb.connect()

if not CMS_PARQUET.exists():
    print("Place the CMS Medicaid provider-level Parquet at ./cms.parquet, then rerun this cell.")
else:
    yearly = con.execute(
        '''
        SELECT LEFT(CAST(CLAIM_FROM_MONTH AS VARCHAR), 4) AS year,
               ROUND(SUM(TOTAL_PAID), 0) AS paid,
               SUM(TOTAL_PATIENTS) AS patient_months,
               COUNT(DISTINCT BILLING_PROVIDER_NPI_NUM) AS billing_npis
        FROM read_parquet(?)
        GROUP BY 1
        ORDER BY 1
        ''',
        [str(CMS_PARQUET)],
    ).fetchall()
    for year, paid, patient_months, billing_npis in yearly:
        print(year, f"${paid:,.0f}", f"{patient_months:,.0f} patient-months", f"{billing_npis:,} billers")

# Notebook cell 5
# Step 3: Cluster organization providers by practice address. [intermediate]
#
# Faithful distillation of nppes_cluster.py + refine_clusters.py:
# - normalize LOCATION addresses
# - split NPI-1 from NPI-2
# - rank org-density clusters
# - classify likely shared-office/agent false positives by officials-to-org ratio

from collections import defaultdict

VIRTUAL_TOKENS = re.compile(
    r"\b(REGUS|IPOSTAL|EARTH CLASS|LEGALZOOM|MAILBOX|UPS STORE|PMB|"
    r"REGISTERED AGENT|INCORP|NORTHWEST REGISTERED|COGENCY|HARVARD BUSINESS|"
    r"CSC|VIRTUAL|DAVINCI|ANYTIME MAILBOX)\b"
)


def location_address(record):
    for address in record.get("addresses", []):
        if address.get("address_purpose") == "LOCATION":
            return address
    return {}


def normalize_address(address):
    line = (address.get("address_1") or "").upper()
    line = re.sub(r"[.,]", " ", line)
    line = re.sub(r"\b(SUITE|STE|UNIT|#)\b", "STE", line)
    line = re.sub(r"\s+", " ", line).strip()
    city = (address.get("city") or "").upper().strip()
    zip5 = (address.get("postal_code") or "")[:5]
    return f"{line} | {city} {zip5}"


def provider_name(record):
    basic = record.get("basic", {})
    return basic.get("organization_name") or " ".join(
        part for part in [basic.get("first_name"), basic.get("last_name")] if part
    )


def authorized_official(record):
    basic = record.get("basic", {})
    return " ".join(
        part
        for part in [
            basic.get("authorized_official_first_name"),
            basic.get("authorized_official_last_name"),
        ]
        if part
    ).upper().strip()


clusters = defaultdict(lambda: {"npi1": set(), "npi2": set(), "org_names": set(), "officials": set()})
for record in nppes_cache:
    address = location_address(record)
    key = normalize_address(address)
    cluster = clusters[key]
    if record.get("enumeration_type") == "NPI-2":
        cluster["npi2"].add(str(record.get("number")))
        cluster["org_names"].add(provider_name(record))
        official = authorized_official(record)
        if official:
            cluster["officials"].add(official)
    else:
        cluster["npi1"].add(str(record.get("number")))


def classify_cluster(key, cluster):
    org_count = len(cluster["npi2"])
    official_count = len(cluster["officials"])
    ratio = official_count / max(1, org_count)
    text = f"{key} {' '.join(cluster['org_names'])}".upper()
    if VIRTUAL_TOKENS.search(text):
        return "VIRTUAL_BRAND"
    if ratio >= 0.75:
        return "SHARED_OFFICE_OR_AGENT"
    if ratio <= 0.40:
        return "SINGLE_CONTROLLER"
    return "MIXED"


address_cluster_rows = []
for key, cluster in clusters.items():
    org_count = len(cluster["npi2"])
    if org_count < 2:
        continue
    address_cluster_rows.append(
        {
            "address_cluster_id": f"addr_{len(address_cluster_rows) + 1:04d}",
            "org_npis": org_count,
            "individual_npis": len(cluster["npi1"]),
            "distinct_officials": len(cluster["officials"]),
            "officials_to_org_ratio": round(len(cluster["officials"]) / max(1, org_count), 2),
            "classification": classify_cluster(key, cluster),
            # The real address is intentionally not displayed in this public notebook.
            "address": key,
        }
    )

address_cluster_rows = sorted(address_cluster_rows, key=lambda r: r["org_npis"], reverse=True)
for row in address_cluster_rows[:10]:
    safe = {k: v for k, v in row.items() if k != "address"}
    print(safe)

# Notebook cell 6
# Step 4: Roll up organization providers by authorized official. [intermediate]
#
# Faithful distillation of controller_rollup.py. Display uses synthetic row IDs
# rather than printing real official names in the notebook output.

controller_map = defaultdict(lambda: {"npis": set(), "org_names": set(), "addresses": set()})
for record in nppes_cache:
    if record.get("enumeration_type") != "NPI-2":
        continue
    official = authorized_official(record)
    if not official:
        continue
    controller_map[official]["npis"].add(str(record.get("number")))
    controller_map[official]["org_names"].add(provider_name(record))
    controller_map[official]["addresses"].add(normalize_address(location_address(record)))

controller_rows = []
for official, values in controller_map.items():
    controller_rows.append(
        {
            "controller_id": f"controller_{len(controller_rows) + 1:04d}",
            "distinct_org_npis": len(values["npis"]),
            "distinct_org_names": len(values["org_names"]),
            "distinct_addresses": len(values["addresses"]),
            "reenumeration_delta": len(values["npis"]) - len(values["org_names"]),
            # The real official name is retained for local analysis, but not displayed below.
            "authorized_official": official,
        }
    )

controller_rows = sorted(
    controller_rows,
    key=lambda row: (row["distinct_org_npis"], row["distinct_addresses"]),
    reverse=True,
)
for row in controller_rows[:10]:
    safe = {k: v for k, v in row.items() if k != "authorized_official"}
    print(safe)

# Notebook cell 7
# Step 5: Growth-off-zero billing join. [intermediate]
#
# Faithful distillation of billing_screen.py:
# - load organization NPIs from the NPPES cache
# - join billing provider NPI to the CMS Parquet
# - find providers whose first billing month is 2023+ and total paid exceeds $300k
#
# Important: TOTAL_PATIENTS in this file is a patient-month denominator after
# aggregation, not unique patients.

org_npis = sorted(
    str(record.get("number"))
    for record in nppes_cache
    if record.get("enumeration_type") == "NPI-2" and record.get("number")
)

if not CMS_PARQUET.exists():
    print("Skipping billing join until ./cms.parquet is present.")
else:
    con.execute("CREATE OR REPLACE TEMP TABLE nv_orgs(npi VARCHAR)")
    con.executemany("INSERT INTO nv_orgs VALUES (?)", [(npi,) for npi in org_npis])
    lead_rows = con.execute(
        '''
        SELECT BILLING_PROVIDER_NPI_NUM AS npi,
               SUM(TOTAL_PAID) AS paid,
               SUM(TOTAL_PATIENTS) AS patient_months,
               SUM(TOTAL_CLAIM_LINES) AS claim_lines,
               ROUND(SUM(TOTAL_PAID) / NULLIF(SUM(TOTAL_PATIENTS), 0), 2) AS paid_per_patient_month,
               MIN(CLAIM_FROM_MONTH) AS first_month,
               MAX(CLAIM_FROM_MONTH) AS last_month,
               COUNT(DISTINCT CLAIM_FROM_MONTH) AS active_months
        FROM read_parquet(?)
        WHERE BILLING_PROVIDER_NPI_NUM IN (SELECT npi FROM nv_orgs)
        GROUP BY 1
        HAVING MIN(CLAIM_FROM_MONTH) >= '2023-01'
           AND SUM(TOTAL_PAID) > 300000
        ORDER BY paid DESC
        ''',
        [str(CMS_PARQUET)],
    ).fetchall()

    for idx, (npi, paid, patient_months, claim_lines, paid_per_pm, first_month, last_month, active_months) in enumerate(lead_rows, 1):
        print(
            {
                "lead_id": f"growth_lead_{idx:03d}",
                "paid": round(paid, 2),
                "patient_months": int(patient_months or 0),
                "claim_lines": int(claim_lines or 0),
                "paid_per_patient_month": paid_per_pm,
                "first_month": first_month,
                "last_month": last_month,
                "active_months": active_months,
            }
        )

# Notebook cell 8
# Step 6: OIG-LEIE exclusion join on billing and servicing NPI. [intermediate]
#
# Download the HHS-OIG LEIE CSV separately and place it next to this notebook
# as leie.csv. Do not commit it.
#
# Source landing page:
# https://oig.hhs.gov/exclusions/exclusions_list.asp

LEIE_CSV = Path("leie.csv")

if not CMS_PARQUET.exists() or not LEIE_CSV.exists():
    print("Skipping LEIE join until both ./cms.parquet and ./leie.csv are present.")
else:
    con.execute(
        '''
        CREATE OR REPLACE TEMP TABLE leie AS
        SELECT *
        FROM read_csv_auto(?, header=true, all_varchar=true)
        WHERE NPI IS NOT NULL
          AND NPI != ''
          AND NPI != '0'
        ''',
        [str(LEIE_CSV)],
    )
    leie_hits = con.execute(
        '''
        SELECT role,
               COUNT(*) AS matched_rows,
               SUM(total_paid) AS total_paid,
               SUM(post_exclusion_paid) AS post_exclusion_paid
        FROM (
          SELECT 'billing' AS role,
                 SUM(c.TOTAL_PAID) AS total_paid,
                 SUM(
                   CASE
                     WHEN CAST(c.CLAIM_FROM_MONTH || '-01' AS DATE) >= STRPTIME(l.EXCLDATE, '%Y%m%d')
                     THEN c.TOTAL_PAID ELSE 0
                   END
                 ) AS post_exclusion_paid
          FROM read_parquet(?) c
          JOIN leie l ON c.BILLING_PROVIDER_NPI_NUM = l.NPI
          WHERE c.BILLING_PROVIDER_NPI_NUM IN (SELECT npi FROM nv_orgs)
          GROUP BY c.BILLING_PROVIDER_NPI_NUM, l.NPI, l.EXCLDATE

          UNION ALL

          SELECT 'servicing' AS role,
                 SUM(c.TOTAL_PAID) AS total_paid,
                 SUM(
                   CASE
                     WHEN CAST(c.CLAIM_FROM_MONTH || '-01' AS DATE) >= STRPTIME(l.EXCLDATE, '%Y%m%d')
                     THEN c.TOTAL_PAID ELSE 0
                   END
                 ) AS post_exclusion_paid
          FROM read_parquet(?) c
          JOIN leie l ON c.SERVICING_PROVIDER_NPI_NUM = l.NPI
          WHERE c.BILLING_PROVIDER_NPI_NUM IN (SELECT npi FROM nv_orgs)
          GROUP BY c.SERVICING_PROVIDER_NPI_NUM, l.NPI, l.EXCLDATE
        )
        GROUP BY role
        ORDER BY role
        ''',
        [str(CMS_PARQUET), str(CMS_PARQUET)],
    ).fetchall()
    for role, matched_rows, total_paid, post_exclusion_paid in leie_hits:
        print(
            {
                "role": role,
                "matched_rows": matched_rows,
                "total_paid": round(total_paid or 0, 2),
                "post_exclusion_paid": round(post_exclusion_paid or 0, 2),
            }
        )
