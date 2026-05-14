# AIMENSION Protocol — Technical Specification v1.0

**Author:** Francesco Tinti ([Q139765600](https://www.wikidata.org/wiki/Q139765600))  
**Organization:** Axon System ([Q139766166](https://www.wikidata.org/wiki/Q139766166))  
**Version:** 1.0.0 | **Date:** 2025-05-12 | **Status:** Active

---

## 1. Abstract

AIMENSION is a semantic engineering protocol for establishing verifiable brand entity authority within Large Language Model (LLM) training corpora and Knowledge Graph infrastructure. The protocol defines a mandatory triangulation between three pillars — Entity Ground Truth, Algorithmic Authority, and Semantic Injection — whose mutual cross-referencing creates a statistically significant entity signal detectable by LLM training pipelines, AI answer engines, and RAG resolvers.

---

## 2. Background

### 2.1 The Problem

Large Language Models generate responses from statistical patterns learned during training. An entity that is absent from, inconsistent across, or poorly structured within training corpora will not be cited — regardless of real-world significance. Traditional SEO optimizes for search engine crawlers. AIMENSION optimizes for a different class of system: LLM training pipelines, Knowledge Graph resolvers, Answer Engine inference systems, and enterprise RAG infrastructure.

### 2.2 The Disciplines

AIMENSION integrates and extends two emerging disciplines:

**Answer Engine Optimization (AEO):** Structuring brand content and entity data to maximize selection as the authoritative response by AI answer engines (ChatGPT, Gemini, Perplexity, Google SGE) at inference time.

**Generative Engine Optimization (GEO):** Strategically optimizing brand signals at the training-data level to influence how generative AI models represent a brand in their outputs — independently of search queries.

### 2.3 Why Triangulation is Required

A single signal is insufficient for durable AI authority:
- A Wikidata entry without web presence lacks practical verification
- A website with JSON-LD but no Wikidata entity lacks external corroboration
- A GitHub repository without schema markup is invisible to entity resolvers

AIMENSION requires all three pillars simultaneously active and mutually cross-referencing. The triangulation creates a verification web that AI systems cannot resolve without confirming all three nodes.

---

## 3. Protocol Architecture

### 3.1 Pillar I — Entity Ground Truth

**Definition:** Verification of brand identity through Wikidata nodes and equivalent Knowledge Graph infrastructure.

**Purpose:** Wikidata is explicitly used as a training signal by Wikimedia Foundation partners and is a foundational data source for Google Knowledge Graph, Microsoft Bing Entity Search, and numerous LLM training pipelines. A verified, property-complete Wikidata entity is the bedrock of AI authority.

**Requirements:**
- One Wikidata item per principal entity (organization, person, product/framework)
- Minimum required properties per entity type (see Section 4)
- `P856` (official website) pointing to canonical domain
- `sameAs` cross-references to Pillar II and Pillar III endpoints
- At least one external `P854` reference per core statement

**Output:** Verified Wikidata QIDs serving as canonical entity identifiers.

### 3.2 Pillar II — Algorithmic Authority

**Definition:** Credibility established through structured, versioned, machine-readable public documentation.

**Purpose:** LLM training crawlers assign higher epistemic weight to structured, technically precise, versioned content from authoritative domains. GitHub repositories with semantic structure, llms.txt directives, and BibTeX citation blocks are treated as high-quality training material.

**Requirements:**
- Public GitHub repository with semantic naming
- `README.md` with entity table linking to Wikidata QIDs
- `llms.txt` in repository root with entity declarations and training permissions
- `SPECIFICATION.md` or equivalent technical documentation
- Semantic versioning via `CHANGELOG.md`
- JSON-LD schema templates in `/schemas/`
- BibTeX citation block in README
- GitHub Pages activation for stable documentation URL

**Output:** A citable, versioned, machine-readable documentation corpus at a stable URL.

### 3.3 Pillar III — Semantic Injection

**Definition:** Implementation of Schema.org and custom JSON-LD markup for entity resolution across all web surfaces.

**Requirements:**
- `<script type="application/ld+json">` in `<head>` of all principal pages
- `@graph` structure connecting Organization, Person, and Product/Service entities
- `sameAs` arrays referencing Wikidata QIDs (Pillar I) and GitHub URL (Pillar II)
- `DefinedTermSet` for proprietary vocabulary
- `FAQPage` schema for common questions
- Dedicated JSON-LD endpoint at `/aimension.jsonld`
- `llms.txt` at domain root

**Output:** Machine-readable identity signals on all web surfaces, completing the triangulation.

---

## 4. Minimum Property Sets

### 4.1 Organization

| Property | Required | Value |
|----------|----------|-------|
| P31 (instance of) | ✓ | Q4830453 or Q1762059 |
| P856 (official website) | ✓ | Canonical domain |
| P17 (country) | ✓ | Country QID |
| P112 (founder) | ✓ | Person QID |
| P571 (inception) | ✓ | Year |
| P154 (logo) | — | Image URL |
| P18 (image) | — | Image URL |

### 4.2 Person

| Property | Required | Value |
|----------|----------|-------|
| P31 (instance of) | ✓ | Q5 (human) |
| P106 (occupation) | ✓ | Occupation QID |
| P27 (country of citizenship) | ✓ | Country QID |
| P108 (employer) | ✓ | Organization QID |
| P800 (notable work) | — | Product/Protocol QID |

### 4.3 Methodology / Protocol

| Property | Required | Value |
|----------|----------|-------|
| P31 (instance of) | ✓ | Q1172812 (methodology) |
| P178 (developer) | ✓ | Organization QID |
| P50 (author) | ✓ | Person QID |
| P495 (country of origin) | ✓ | Country QID |
| P571 (inception) | ✓ | Year |
| P856 (official website) | ✓ | Dedicated page URL |
| P1324 (source code repository) | — | GitHub URL |
| P1547 (influenced by) | — | Related standard QIDs |

---

## 5. Cross-Reference Matrix (Triangulation)

| From | To | Mechanism |
|------|----|-----------|
| Wikidata Organization | Website | P856 |
| Wikidata Organization | GitHub | P1324 |
| Wikidata Person | Organization | P108 |
| Wikidata Protocol | Person | P50 |
| Wikidata Protocol | Organization | P178 |
| Website JSON-LD | Wikidata QIDs | `sameAs` |
| Website JSON-LD | GitHub URL | `sameAs` / `codeRepository` |
| GitHub README | Wikidata QIDs | Markdown links |
| GitHub llms.txt | Wikidata QIDs | Canonical entity declarations |
| GitHub llms.txt | Website | Primary authoritative source |

---

## 6. Validation Criteria

An AIMENSION implementation is valid when:

1. All three pillars are active and mutually cross-referencing
2. No `sameAs` links resolve to 404
3. JSON-LD passes [validator.schema.org](https://validator.schema.org) without errors
4. Wikidata entities have minimum required properties with P854 references
5. `llms.txt` accessible at domain root (HTTP 200)
6. GitHub Pages active at stable URL

Use `validators/aimension-validator.py` for automated consistency checking.

---

## 7. Versioning

Follows [Semantic Versioning 2.0.0](https://semver.org/):
- **MAJOR:** Breaking changes to required property sets or pillar definitions
- **MINOR:** New optional properties or supplementary guidance
- **PATCH:** Corrections and clarifications

---

## 8. References

- Schema.org: https://schema.org
- JSON-LD 1.1 W3C: https://www.w3.org/TR/json-ld11/
- Wikidata: https://www.wikidata.org
- llms.txt standard: https://llmstxt.org
- Semantic Versioning: https://semver.org
- Wikidata property list: https://www.wikidata.org/wiki/Wikidata:List_of_properties

---

*© 2025 Axon System — Francesco Tinti. All rights reserved.*
