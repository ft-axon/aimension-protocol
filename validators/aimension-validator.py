#!/usr/bin/env python3
"""
AIMENSION Protocol — Consistency Validator v1.0
Axon System | Francesco Tinti | axonsystem.net

Usage:
  python aimension-validator.py --all
  python aimension-validator.py --wikidata Q139766166
  python aimension-validator.py --jsonld schemas/organization.jsonld
  python aimension-validator.py --site https://axonsystem.net
"""

import json, sys, argparse, requests
from datetime import datetime

WIKIDATA_SPARQL = "https://query.wikidata.org/sparql"
HEADERS = {"User-Agent": "AIMENSION-Validator/1.0 (axonsystem.net)"}

G = "\033[92m"; R = "\033[91m"; Y = "\033[93m"; B = "\033[94m"; E = "\033[0m"; BD = "\033[1m"
def ok(m): print(f"  {G}✓{E} {m}")
def fail(m): print(f"  {R}✗{E} {m}")
def warn(m): print(f"  {Y}⚠{E} {m}")
def info(m): print(f"  {B}→{E} {m}")

REQUIRED = {
    "organization": ["P31","P856","P17","P112","P571"],
    "person":       ["P31","P106","P27","P108"],
    "methodology":  ["P31","P178","P50","P495","P571","P856"]
}

def check_wikidata(qid, etype="organization"):
    print(f"\n{BD}[Wikidata] {qid} ({etype}){E}")
    q = f"SELECT ?p ?v WHERE {{ wd:{qid} ?p ?v . FILTER(STRSTARTS(STR(?p),'http://www.wikidata.org/prop/direct/')) }} LIMIT 100"
    try:
        r = requests.get(WIKIDATA_SPARQL, params={"query":q,"format":"json"}, headers=HEADERS, timeout=10)
        r.raise_for_status()
        bindings = r.json()["results"]["bindings"]
        if not bindings: fail(f"{qid} not found"); return {"found":False}
        ok(f"{qid} found — {len(bindings)} statements")
        found = set(b["p"]["value"].split("/P")[-1] and "P"+b["p"]["value"].split("/P")[-1] for b in bindings if "/P" in b["p"]["value"])
        missing = [p for p in REQUIRED.get(etype,[]) if p not in found]
        if missing: warn(f"Missing: {', '.join(missing)}")
        else: ok("All required properties present")
        pct = (len(REQUIRED.get(etype,[])) - len(missing)) / max(len(REQUIRED.get(etype,[])),1) * 100
        info(f"Completeness: {pct:.0f}%")
        return {"found":True,"completeness_pct":pct,"missing":missing}
    except Exception as e:
        fail(f"Error: {e}"); return {"found":False}

def validate_jsonld(path):
    print(f"\n{BD}[JSON-LD] {path}{E}")
    try:
        with open(path) as f: data = json.load(f)
        ok("JSON syntax valid")
    except Exception as e:
        fail(f"Parse error: {e}"); return {"valid":False}
    issues = []
    if "@context" not in data: warn("No @context"); issues.append("no_context")
    entities = data.get("@graph", [data])
    wikidata_refs = sum(1 for e in entities for sa in ([e.get("sameAs",[])] if isinstance(e.get("sameAs"),[]) else [e.get("sameAs",[])]) if "wikidata.org" in str(sa))
    if wikidata_refs: ok(f"{wikidata_refs} Wikidata sameAs reference(s)")
    else: warn("No Wikidata sameAs — triangulation incomplete")
    placeholders = sum(1 for e in entities for sa in ([e.get("sameAs",[])] if isinstance(e.get("sameAs"),[]) else [e.get("sameAs",[])]) if "Q[QID_" in str(sa))
    if placeholders: warn(f"{placeholders} placeholder QID(s) — replace with real values")
    score = max(0, 100 - len(issues)*20 - placeholders*15)
    info(f"Score: {score}/100")
    return {"valid": len(issues)==0, "score":score}

def check_site(url):
    print(f"\n{BD}[Site] {url}{E}")
    results = {}
    for path, label in [("/llms.txt","llms.txt"), ("/aimension.jsonld","JSON-LD endpoint")]:
        try:
            r = requests.get(url+path, timeout=8)
            if r.status_code == 200: ok(f"{label} reachable")
            else: warn(f"{label} → HTTP {r.status_code}")
            results[label] = r.status_code == 200
        except: warn(f"Could not reach {label}")
    try:
        r = requests.get(url, timeout=8)
        if "application/ld+json" in r.text: ok("JSON-LD found in homepage")
        else: warn("No JSON-LD in homepage <head>")
        if "wikidata.org" in r.text: ok("Wikidata references in HTML")
    except: warn("Could not fetch homepage")
    return results

def main():
    parser = argparse.ArgumentParser(description="AIMENSION Validator v1.0")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--wikidata", metavar="QID")
    parser.add_argument("--jsonld", metavar="FILE")
    parser.add_argument("--site", metavar="URL")
    args = parser.parse_args()

    print(f"\n{BD}AIMENSION™ Validator v1.0 — Axon System{E}")
    print(f"{'─'*50}")

    results = {}
    if args.wikidata or args.all:
        results["wikidata"] = check_wikidata(args.wikidata or "Q139766166")
    if args.jsonld or args.all:
        results["jsonld"] = validate_jsonld(args.jsonld or "examples/axon-system-full.jsonld")
    if args.site or args.all:
        results["site"] = check_site(args.site or "https://axonsystem.net")

    if not any([args.wikidata, args.jsonld, args.site, args.all]):
        parser.print_help()

    print(f"\n{'═'*50}")
    print(f"{BD}Report — {datetime.now().strftime('%Y-%m-%d %H:%M')}{E}")
    scores = [v.get("completeness_pct", v.get("score",0)) for v in results.values() if isinstance(v,dict)]
    if scores:
        avg = sum(scores)/len(scores)
        color = G if avg>=80 else Y if avg>=50 else R
        print(f"  Overall: {color}{avg:.0f}/100{E}")
        if avg >= 80: print(f"  {G}Entity well-positioned for LLM citation{E}")
        elif avg >= 50: print(f"  {Y}Partial — complete remaining pillars{E}")
        else: print(f"  {R}Critical gaps — entity unlikely to be cited{E}")

if __name__ == "__main__": main()
