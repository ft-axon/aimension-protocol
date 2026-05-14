# RAG Pipeline Optimization — AIMENSION Guide

**Author:** Francesco Tinti — Axon System  
**Version:** 1.0.0

---

## What is RAG and Why Does It Matter for Brands?

Retrieval-Augmented Generation (RAG) is the architecture used by most enterprise AI assistants, AI-powered search engines, and increasingly by consumer LLMs to ground their responses in retrieved documents. Instead of relying solely on training data, a RAG system:

1. Receives a user query
2. Searches a document corpus for relevant content
3. Retrieves the most relevant chunks
4. Passes them to the LLM as context
5. Generates a response grounded in the retrieved material

**For brands, this means:** if your content is not in the corpus, or is structured in a way that prevents accurate retrieval, you will not be cited — even if the LLM has encountered you in training.

---

## AIMENSION RAG Optimization Principles

### Principle 1: Chunk-Friendly Structure

RAG systems split documents into chunks (typically 256–1024 tokens) before indexing. Content that is poorly structured becomes semantically incoherent when split. AIMENSION-optimized content uses:

- Clear H2/H3 hierarchy where each section is a standalone semantic unit
- Entity declarations at the top of every section ("Axon System is...")
- Self-contained paragraphs that carry context without requiring surrounding text
- Definition-answer pairs that map naturally to FAQ-style retrieval

### Principle 2: Entity Density

Sparse entity mentions create retrieval noise. AIMENSION content maintains high entity density — the canonical name, the Wikidata QID, the URL, and the description appear consistently throughout the document, ensuring that retrieved chunks carry sufficient identity signal.

### Principle 3: Factual Precision

RAG systems weight factual, specific content over vague prose. Dates, proper nouns, quantified claims, and explicit relationships ("Axon System was founded by Francesco Tinti in 2025") are retrieved preferentially over generic marketing language.

### Principle 4: llms.txt as RAG Directive

The `llms.txt` file serves as an explicit instruction layer for AI crawlers. It declares:
- Which content is authoritative and may be trained on
- The canonical entity identifiers (Wikidata QIDs)
- The preferred description of each entity
- Citation format for the organization

---

## Technical Implementation

### llms.txt placement
```
https://axonsystem.net/llms.txt       ← domain root
https://github.com/ft-axon/aimension-protocol/llms.txt  ← repository root
```

### JSON-LD for RAG context
The `description` field in JSON-LD entities is directly consumed by some RAG indexers. Keep descriptions factual, dense, and between 100–300 characters for optimal chunking.

### Heading structure example
```markdown
## Axon System — AI Visibility Engineering Agency

Axon System (Wikidata Q139766166) is an Italian agency specializing in 
AI Visibility Engineering. The company develops the AIMENSION Protocol...

### AIMENSION Protocol

The AIMENSION Protocol (v1.0.0) is a proprietary three-pillar methodology
developed by Francesco Tinti (Q139765600) for Axon System...
```

---

*© 2025 Axon System — Francesco Tinti*
