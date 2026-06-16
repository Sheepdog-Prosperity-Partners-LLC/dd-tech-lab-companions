#!/usr/bin/env python3
"""
Medicare provider billing-outlier screen, peer-relative anomaly scoring on public CMS data.

The data-miner relator method, reduced to its core: pick a service (HCPCS code), define a
peer group (provider specialty), and find the providers whose *intensity* of that service
(procedures per patient) sits far above their peers. That ranked list is a set of LEADS,
not findings. An outlier is a question, not an answer.

Data source: CMS "Medicare Physician and Other Practitioners by Provider and Service"
(public, keyless): https://data.cms.gov/provider-summary-by-type-of-service/medicare-physician-other-practitioners
Method lineage (prior art): Khoshgoftaar/Herland (Florida Atlantic Univ.) LEIE-labeled approach;
NBER unsupervised explainable Medicare-fraud detection. We build the screen fresh on commodity
OSS (pandas; DuckDB shown for scale) rather than vendoring any restricted demo repository.

Prepared by Noah Green CPA CFE for the Sheepdog Prosperity Partners DD Tech Lab.
Illustrative, provided as-is. Makes no allegation against any provider; the output is a triage
list of leads that require records-level review before anything is called a finding.

Usage:
  python3 medicare_outlier_screen.py --hcpcs 36902 --min-peers 30 --z 3.5
  python3 medicare_outlier_screen.py --hcpcs 36902 --state TX --out outliers_36902_TX.csv
"""
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request

import pandas as pd

# CMS Medicare Physician and Other Practitioners by Provider and Service (latest year distribution)
CMS_DATASET = "92396110-2aed-4d63-a6a2-5d6207d46a29"
CMS_URL = f"https://data.cms.gov/data-api/v1/dataset/{CMS_DATASET}/data"
NUM_COLS = ["Tot_Benes", "Tot_Srvcs", "Tot_Bene_Day_Srvcs",
            "Avg_Sbmtd_Chrg", "Avg_Mdcr_Alowd_Amt", "Avg_Mdcr_Pymt_Amt"]


def fetch_hcpcs(hcpcs: str, state: str | None, cache: str, page: int = 5000) -> pd.DataFrame:
    """Pull every provider that billed `hcpcs` (optionally one state) from the CMS API, paginated.
    Caches to CSV so the screen is reproducible and re-runnable without re-hitting the API."""
    if os.path.exists(cache):
        print(f"[cache] {cache}", file=sys.stderr)
        return pd.read_csv(cache, dtype={"Rndrng_NPI": str})
    rows, offset = [], 0
    while True:
        params = {"filter[HCPCS_Cd]": hcpcs, "size": page, "offset": offset}
        if state:
            params["filter[Rndrng_Prvdr_State_Abrvtn]"] = state
        req = urllib.request.Request(CMS_URL + "?" + urllib.parse.urlencode(params),
                                     headers={"User-Agent": "ngo-ddlab/1.0"})
        with urllib.request.urlopen(req, timeout=60) as r:
            batch = json.loads(r.read().decode())
        rows.extend(batch)
        print(f"[fetch] hcpcs={hcpcs} offset={offset} got={len(batch)} total={len(rows)}", file=sys.stderr)
        if len(batch) < page:
            break
        offset += page
    df = pd.DataFrame(rows)
    df.to_csv(cache, index=False)
    return df


def screen(df: pd.DataFrame, min_peers: int, z_threshold: float,
           min_srvcs: int = 20, min_benes: int = 11) -> pd.DataFrame:
    """Peer-relative outlier score. Peer group = provider specialty. Signal = intensity
    (services per beneficiary). Robust z-score (median/MAD) so a few extreme billers do not
    drag the benchmark. Flags = high intensity AND material volume."""
    for c in NUM_COLS:
        df[c] = pd.to_numeric(df.get(c), errors="coerce")
    df = df[(df["Tot_Benes"] >= min_benes) & (df["Tot_Srvcs"] >= min_srvcs)].copy()
    # Intensity: how many of this procedure per patient, the overuse signal.
    df["srvcs_per_bene"] = df["Tot_Srvcs"] / df["Tot_Benes"]
    df["allowed_total"] = df["Avg_Mdcr_Alowd_Amt"] * df["Tot_Srvcs"]

    peer = df.groupby("Rndrng_Prvdr_Type")["srvcs_per_bene"]
    med = peer.transform("median")
    mad = peer.transform(lambda s: (s - s.median()).abs().median())
    n_peers = peer.transform("size")
    # Robust (modified) z-score; 0.6745 makes MAD comparable to a standard deviation.
    df["peer_median"] = med.round(2)
    df["peers_in_specialty"] = n_peers
    df["robust_z"] = (0.6745 * (df["srvcs_per_bene"] - med) / mad).where(mad > 0)

    leads = df[(df["peers_in_specialty"] >= min_peers) & (df["robust_z"] >= z_threshold)].copy()
    cols = ["Rndrng_NPI", "Rndrng_Prvdr_Last_Org_Name", "Rndrng_Prvdr_Type",
            "Rndrng_Prvdr_State_Abrvtn", "Tot_Benes", "Tot_Srvcs", "srvcs_per_bene",
            "peer_median", "peers_in_specialty", "robust_z", "allowed_total"]
    return leads.sort_values("robust_z", ascending=False)[cols].round(2)


def main():
    ap = argparse.ArgumentParser(description="Medicare peer-relative billing-outlier screen (leads, not findings).")
    ap.add_argument("--hcpcs", required=True, help="HCPCS/CPT code to screen, e.g. 36902")
    ap.add_argument("--state", default=None, help="Optional 2-letter state filter")
    ap.add_argument("--min-peers", type=int, default=30, help="Min providers in a specialty to benchmark (stable stats)")
    ap.add_argument("--z", type=float, default=3.5, help="Robust z-score threshold to flag a lead")
    ap.add_argument("--out", default=None, help="Output CSV path")
    ap.add_argument("--cache", default=None, help="Raw-pull cache CSV path")
    a = ap.parse_args()

    cache = a.cache or f"cms_{a.hcpcs}{('_'+a.state) if a.state else ''}.csv"
    out = a.out or f"outliers_{a.hcpcs}{('_'+a.state) if a.state else ''}.csv"

    df = fetch_hcpcs(a.hcpcs, a.state, cache)
    leads = screen(df, a.min_peers, a.z)
    leads.to_csv(out, index=False)
    print(f"\nScreened {len(df):,} provider rows for HCPCS {a.hcpcs}. "
          f"{len(leads)} lead(s) at robust_z >= {a.z}.  ->  {out}\n", file=sys.stderr)
    with pd.option_context("display.width", 160, "display.max_columns", 20):
        print(leads.head(12).to_string(index=False))
    print("\nThese are LEADS, not findings. An outlier has innocent explanations "
          "(subspecialty referral magnet, sicker panel, coding of a legitimately complex mix). "
          "Confirm with records before anything is called fraud.", file=sys.stderr)


if __name__ == "__main__":
    main()
