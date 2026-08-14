# Current status and Project Shadow boundary

Reviewed: 2026-08-14

This repository preserves the **April 19, 2026 PBHP research snapshot** and its historical documentation. The snapshot is built on the v0.9.5-named files, but its final commit implemented 17 post-audit fix categories across 103 source/protocol lines explicitly labeled v0.9.6. The repository therefore has a documented version skew:

- top-level `VERSION` and filenames: v0.9.5;
- internal audit-correction labels: v0.9.6;
- latest formal GitHub release/tag: v0.9.0.

This branch is an untagged preserved snapshot, not a clean v0.9.5 or v0.9.6 release. Its `protocol/PBHP-ULTRA_v0.9.5.md` is byte-identical to the supplied reference copy:

- SHA-256: `c6c84db9b08d9b24da9b3e23dce5c1b98c81d1a65319018c59b1e4da833e5098`
- Local verification on 2026-08-14: 730 tests passed across 13 files, plus 20 subtests.

Those results apply only to the checked April 19 snapshot. They do not establish efficacy, safety, complete coverage, production readiness, certification, legal compliance, or suitability for a particular use. Resolving the version skew would require a separately reviewed, exact successor; this documentation repair does not relabel or mutate the protocol bytes.

## Locked Project Shadow identity

The current governed scope is:

`PROJECT SHADOW 1.0 / R1 REFERENCE / BETA-ACTIVE-TESTING / PRELIVE`

- R1 Beta2 family: `075b41ea4186b2d2edb0ed246ab7662cf8bbdf3160294e3eca176b9d0857b108`, including its 10 corrected descendants.
- Primitive Commons beta.5: `1ffdba41025c0b81da92d0bbb22d0eaa69488cffbc80936365034669110448d7`, containing 42 primitives and 10 compositions.
- Exact audited outer custody container: `827c13e80f09e3e3065cee4aa0bcc6afbc3e27061b83b7597754b7ea167f68a2`. It is recognized as custody only and is **not admitted**.
- Myth v0.3.4 removal-only successor: `3c8c8c0d3d9582c76b685c1b685260cc8179478ab310037c858b46257aa314c7`. It is prepared as a separate, default-off, mixed-rights, nonauthorizing external-research sidecar outside canonical R1. It is not part of an R1 package, and this repository does not publish its bytes.

The exact admission record has a verified detached Sigstore signature, Rekor inclusion evidence, and RFC 3161 external timestamp. That closes the signature and time-anchor gates for the admission record only.

The deterministic public-release candidate has now been fixed at SHA-256 `401c16592408455498526793e3ae524d9739d3c62de4e60de92f631f3cc0a3d8` (7,675,559 bytes). Its status is `PENDING_EXACT_CANDIDATE_HASH_AUTHORIZATION`. It has not been published, and this PBHP repository does not contain or authorize its download.

## Authority boundary

Nothing in this repository or status note authorizes production use, operational deployment, efficacy or safety claims, certification, legal-compliance claims, or reliance in place of qualified human judgment. Historical files retain their manufacture-time wording; this status note controls the current interpretation of this repository.

Current public teaching surface: [Pause Before Harm](https://pausebeforeharm.frylock117.chatgpt.site)

Canonical Project Shadow status surface: [Project Shadow](https://projectshadow.frylock117.chatgpt.site/status)
