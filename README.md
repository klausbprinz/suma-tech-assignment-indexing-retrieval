---
projectName: "suma-tech-assignment-indexing-retrieval"
author: "Klaus Prinz"
domain: "learning"
status: "active"
createdDate: "2026-11-07"
tags: [solr, solr schema, pysolr, project gutenberg, information retrieval, edismax, morelikethis, mlt, faceting, podman, podman-compose]
requester: ""
ticketId: ""
---

# suma-tech-assignment-indexing-retrieval

> **Quick Summary:** Suma-tech assignment two. See `docs/assignment/README.md`.

---

## Quick Start & How to Run

1. **Environment:** Ensure you are using the `suma-tech` Conda environment (to create run `conda env create -f environment.yaml`).
2. **Setup:** Not needed.
3. **Inputs:** Not needed.
4. **Execution:** First run scripts in `scripts/preparation`, then run scripts in `scripts/assignment` sequentially.

---

## Container Setup
```bash
mkdir -p solrdata
podman unshare chown -R 8983:8983 solrdata
podman-compose up -d
```

*(Verify Solr is running by opening http://localhost:8983 in your browser).*

---

 ## Core Creation (Optional) 
Create a default core to test with:
```bash
podman-compose exec solr solr create -c my1stcore
```

---

## Troubleshooting: VS Code File Visibility (Rootless Podman)

Because this project uses rootless Podman, files created inside containers (such as Solr cores) are mapped to high-numbered host UIDs. This can cause VS Code to show `Permission denied` errors or empty directories under `solrdata/`.

To grant your host user read and execute permissions without breaking container write access, run:

```bash
podman unshare chmod -R o+rX solrdata
```

Or use this
```bash
podman unshare chmod -R 777 solrdata
```

## Context & Objectives
This repository contains the implementation deliverables for **Suma-Tech Assignment 2** (Project Gutenberg Search Pipeline).
All runnable **assignment deliverables and implementation scripts** are located in the `scripts/assignment/` directory. For deep-dive assignment requirements, refer to `docs/assignment/README.md`.

---

## Project Layout

```text
.
├── data/                       # Local data folder, assignment-data and pg-metadata
├── docs/assignment/            # Assignment README
├── notebooks/                  # Testing notebook
├── scripts/                    # Core python scripts
├── compose.yaml                # Podman Compose setup
├── environment.yaml            # Information on used environment
└── README.md
```

---

## Documentation & Visuals
Not now.

---

## Dependencies & Requirements
Not now.

---

## Notes & Future TODOs
Not now.

---