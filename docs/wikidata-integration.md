# Wikidata Integration — AIMENSION Guide

**Author:** Francesco Tinti — Axon System  
**Version:** 1.0.0

---

## Why Wikidata is Non-Negotiable

Wikidata is the largest open Knowledge Graph in existence, with over 100 million items. It is:

- The primary structured data source for Wikipedia
- Explicitly used as training data by major LLM providers
- The foundation of Google Knowledge Graph and Bing Entity Search
- A standard reference in academic and scientific training corpora
- Free, permanent, and publicly queryable via SPARQL

An entity that exists in Wikidata with complete, referenced properties has a semantic footprint that persists across every future LLM training run that includes Wikidata dumps — which is virtually all of them.

---

## Creating an Organization Entity

### Minimum viable item

```
LABEL (en): Axon System
LABEL (it): Axon System
DESCRIPTION (en): Italian AI Visibility Engineering agency, developer of the AIMENSION protocol
DESCRIPTION (it): Agenzia italiana di AI Visibility Engineering, sviluppatrice del protocollo AIMENSION

STATEMENTS:
P31  → Q4830453 (business)
P17  → Q38 (Italy)
P856 → https://axonsystem.net
P112 → Q139765600 (Francesco Tinti)
P571 → 2025

REFERENCES (on P856):
P854 → https://axonsystem.net
P813 → [date accessed]
```

### Adding sameAs equivalent properties

```
P2002 → Twitter/X handle (if applicable)
P4033 → Mastodon profile (if applicable)
P1324 → https://github.com/ft-axon (source code repository)
```

---

## Creating a Person Entity

```
LABEL (en): Francesco Tinti
DESCRIPTION (en): Italian entrepreneur and AI Visibility Engineer, founder of Axon System, developer of the AIMENSION protocol

P31  → Q5 (human)
P21  → Q6581097 (male)
P27  → Q38 (Italian)
P106 → Q131524 (entrepreneur)
P108 → Q139766166 (Axon System)
P800 → [QID_AIMENSION] (notable work — add after creating AIMENSION item)
P856 → https://axonsystem.net
```

---

## Creating a Methodology Entity

```
LABEL (en): AIMENSION Protocol
DESCRIPTION (en): Proprietary AI Visibility Engineering protocol developed by Francesco Tinti for Axon System

P31  → Q1172812 (methodology)
P178 → Q139766166 (Axon System — developer)
P50  → Q139765600 (Francesco Tinti — author)
P495 → Q38 (Italy — country of origin)
P571 → 2025
P856 → https://axonsystem.net/aimension
P1324 → https://github.com/ft-axon/aimension-protocol
P1547 → Q217602 (Schema.org — influenced by)
P1547 → Q29032 (Wikidata — influenced by)
```

---

## Monitoring with SPARQL

Query all properties of Axon System:

```sparql
SELECT ?prop ?propLabel ?val ?valLabel WHERE {
  wd:Q139766166 ?prop ?val .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en,it". }
}
```

Check entity completeness (run at [query.wikidata.org](https://query.wikidata.org)):

```sparql
SELECT ?item ?itemLabel (COUNT(?statement) AS ?statements) WHERE {
  VALUES ?item { wd:Q139766166 wd:Q139765600 }
  ?item ?prop ?statement .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
GROUP BY ?item ?itemLabel
```

---

## Best Practices

- Add a P854 reference to every statement — unreferenced statements are deletion targets
- Use the official Wikidata item for Italy (Q38), not a plain text value
- After creating the AIMENSION item, add P800 to Francesco Tinti's item pointing to it
- Check monthly that no properties have been removed by other editors
- Add sitelinks if/when Wikipedia articles are created

---

*© 2025 Axon System — Francesco Tinti*
