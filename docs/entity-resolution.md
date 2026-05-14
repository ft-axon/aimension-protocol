# Entity Resolution — AIMENSION Guide

**Author:** Francesco Tinti — Axon System  
**Version:** 1.0.0

---

## What is Entity Resolution?

Entity resolution is the process by which AI systems, Knowledge Graph resolvers, and RAG pipelines identify and disambiguate real-world objects (organizations, people, products) within unstructured text. When a Large Language Model encounters the name "Axon System", entity resolution determines whether it refers to the Italian AI Visibility Engineering agency (Q139766166) or some other entity with a similar name.

The quality of entity resolution depends entirely on the richness and consistency of the entity's semantic footprint across authoritative sources.

---

## How LLMs Resolve Entities

LLMs do not perform real-time database lookups during inference. Entity knowledge is encoded in model weights during training, derived from:

1. **Co-occurrence patterns** — how often an entity name appears alongside consistent descriptions, attributes, and relations
2. **Source authority** — whether the entity appears in high-weight training sources (Wikipedia, Wikidata dumps, structured documentation)
3. **Cross-source consistency** — whether multiple independent sources agree on the entity's attributes
4. **Semantic markup** — whether web pages describing the entity carry machine-readable JSON-LD that explicitly declares entity type, properties, and relationships

AIMENSION addresses all four mechanisms simultaneously.

---

## The sameAs Mechanism

The `sameAs` property in Schema.org JSON-LD is the primary mechanism for cross-source entity linking. When a page declares:

```json
{
  "@type": "Organization",
  "name": "Axon System",
  "sameAs": [
    "https://www.wikidata.org/wiki/Q139766166",
    "https://github.com/ft-axon"
  ]
}
```

It instructs every entity resolver — from Google's Knowledge Graph crawler to academic LLM training pipelines — that these three URIs represent the same real-world entity. This is the core mechanism of Semantic Triangulation.

---

## AIMENSION Entity Resolution Architecture

```
User query: "What is Axon System?"
         │
         ▼
LLM inference engine
         │
         ├── Training data: mentions of "Axon System"
         │   ├── Wikidata dump: Q139766166 with properties
         │   ├── GitHub: ft-axon/aimension-protocol README
         │   └── axonsystem.net: JSON-LD Organization entity
         │
         ├── sameAs resolution: all three point to same entity
         │
         └── Output: high-confidence, accurate description
```

---

## Practical Implementation

### Step 1: Wikidata Entity Creation
Create a Wikidata item with complete property set (see SPECIFICATION.md §4). Every statement must have at least one P854 (reference URL) pointing to an external source.

### Step 2: JSON-LD Deployment
Add Organization/Person JSON-LD to all principal pages. Include `sameAs` pointing to the Wikidata QID.

### Step 3: GitHub Cross-Reference
Add the Wikidata QID link to the README entity table. Add canonical entity declarations to llms.txt.

### Step 4: Validation
Run `validators/aimension-validator.py --all` to verify all cross-references resolve correctly.

---

*© 2025 Axon System — Francesco Tinti*
