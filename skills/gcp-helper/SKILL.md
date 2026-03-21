---
name: gcp-helper
description: Use when managing GCP resources like GCE, GCS, or GKE via gcloud CLI.
---

# GCP Helper

## Overview
Assists in the management of Google Cloud Platform (GCP) resources by providing standardized commands and best practices.

## When to Use
- Managing GCE instances, GCS buckets, or GKE clusters.
- Checking IAM permissions or configuring service accounts.
- Deploying Cloud Functions or Cloud Run services.

## Core Pattern
Always verify the current active project before making any changes.

```bash
# Verify project
gcloud config get-value project
```

## Quick Reference
| Service | Common Command |
|---------|----------------|
| GCE | `gcloud compute instances list` |
| GCS | `gsutil ls` |
| GKE | `gcloud container clusters list` |

## Implementation
1. Check project: `gcloud config get-value project`.
2. List resources: `gcloud [service] list`.
3. Perform action.

## Common Mistakes
- Working in the wrong project.
- Forgetting to authenticate (`gcloud auth login`).
