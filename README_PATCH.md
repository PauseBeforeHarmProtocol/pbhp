# Suggested README addition

Add this block near the Quick Start section after reviewing the overlay:

```markdown
## Website and component downloads

The canonical protocol remains version 0.9.5. A separate additive distribution layer is available under [`website/`](website/) and [`distribution/`](distribution/). Each component page provides a concise explanation, evidence state, test plan, and direct download without replacing the full protocol specification.

- [Browse the generated website](website/index.html)
- [Browse individual component packs](distribution/components/)
- [Download category bundles](distribution/bundles/)
- [Read the current release boundary](CURRENT_RELEASE.md)
```

Also publish a GitHub release/tag matching source version **0.9.5** so the release page no longer trails the repository source.
