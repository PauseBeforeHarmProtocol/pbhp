# Merge into `PauseBeforeHarmProtocol/pbhp`

1. Create branch `agent/pbhp-current-distribution-2026-07-18` from `main`.
2. Copy this overlay into the repository root. It is additive and does not delete canonical protocol or source files.
3. Add the reviewed snippet from `README_PATCH.md` to the existing README.
4. Run `python scripts/validate_distribution.py` and the repository's existing 730-test suite.
5. Open a draft pull request.
6. After merge, create a reviewed `v0.9.5` GitHub release from the matching source state.
7. Keep Project Shadow in its separate private repository.
