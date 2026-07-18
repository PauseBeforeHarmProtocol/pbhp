# GitHub Repository Setup

This publication repository is GitHub-ready. It includes deterministic site generation, one component test plan per public component, release manifests, a validation workflow, issue templates, and a public/private boundary scan.

## Recommended repository layout

- Keep the existing public PBHP source repository as the canonical PBHP protocol/code line.
- Publish this combined website and Project Shadow release repository as a separate repository so its runtime, TEVV, website, and component-library version histories remain explicit.
- Link the two repositories in both READMEs without merging their version numbers or claims.

## First push

```bash
git clone PBHP_SHADOW_PUBLIC_SITES_REPO_2026-07-18.bundle pbhp-shadow-public-sites
cd pbhp-shadow-public-sites
git remote add origin <new-github-repository-url>
git push -u origin main --tags
```

## Branch protection

Require the `validate-public-sites` workflow before merge. Require at least one reviewer for changes to runtime claims, evidence states, publication allowlists, component metadata, test plans, or deployment instructions. Do not permit force pushes to `main`.

## Component change rule

A component change must update its source entry, generated `README.md`, `component.json`, and `TEST_PLAN.md`; regenerate all affected packs and manifests; retain adverse results; run the full validation suite; and receive a dated release receipt.

## GitHub Releases

Attach the complete repository ZIP, Git bundle, PBHP and Shadow deployment ZIPs, component-library bundles, checksums, validation summary, and release receipt. Describe what is specified, observed, adverse, and still open. Never label a release independently validated unless a materially independent party has actually completed that work.
