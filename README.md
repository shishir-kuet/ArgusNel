# ArgusNel

ArgusNel is a modular experimental search engine designed to explore the architecture of modern web search systems.
The project focuses on implementing the fundamental components of a search engine including web crawling, URL frontier management, content processing, indexing, and ranking.

The goal of ArgusNel is to demonstrate how large-scale search engines discover, process, and retrieve information from the web while maintaining a clean and extensible system architecture.

---

## Project Goals

ArgusNel is designed to:

* Explore real-world search engine architecture
* Implement core information retrieval techniques
* Build a scalable and modular crawling system
* Experiment with ranking and search algorithms
* Serve as a research and learning platform for search technologies

---

## Current Implementation

The current stage of ArgusNel focuses on building an advanced web crawler with several key subsystems.

### Implemented Components

* Web crawler core
* URL frontier with priority queue
* URL normalization and canonicalization
* Robots.txt compliance system
* Crawl scheduler with domain-based politeness
* Content deduplication using SHA256 hashing

These components form the foundation of a professional crawler architecture.

---

## Crawler Architecture

The crawler system is composed of multiple modules that each handle a specific responsibility.

```
URL Normalizer
       ↓
URL Frontier
       ↓
Scheduler
       ↓
Robots Handler
       ↓
Crawler Core
       ↓
Content Deduplicator
       ↓
Page Storage
```

Each module operates independently to keep the crawler scalable and maintainable.

---

## Repository Structure

```
ArgusNel
│
├── crawler
│   ├── crawler.py
│   ├── scheduler.py
│   ├── robots_handler.py
│   ├── url_frontier.py
│   ├── url_normalizer.py
│   └── content_deduplicator.py
│
├── parser
├── processing
├── indexer
├── ranking
├── search
├── storage
├── api
├── tests
├── ui
│
├── data
├── requirements.txt
└── README.md
```

This structure allows the project to evolve into a complete search engine system.

---

## Planned Features

The project roadmap includes several additional components.

### Indexing System

* Text tokenization
* Stopword removal
* Stemming
* Inverted index construction

### Ranking Engine

* TF-IDF ranking
* BM25 scoring
* Page importance analysis

### Search Engine

* Query processing
* Result ranking
* Search API

### Advanced Features

* Semantic search with embeddings
* Distributed crawling
* Query auto-completion
* Spelling correction
* Search analytics

---

## Technologies

The system is primarily implemented in Python.

Key libraries used:

* requests
* beautifulsoup4

Additional tools may be introduced as the project evolves.

---

## Development Philosophy

ArgusNel emphasizes modular system design where each subsystem is responsible for a single part of the search pipeline.
This approach makes the project easier to extend and experiment with new search technologies.

---

## Long-Term Vision

ArgusNel aims to become a full experimental search platform capable of:

* crawling web data
* building search indexes
* ranking documents
* providing search results through an API and user interface

The project serves as a practical exploration of how modern search engines operate internally.

---
