# Contributing to PBHP

Thank you for your interest in improving the Pause Before Harm Protocol.

## How to Contribute

This repository is in evidence-preserving maintenance. Project Shadow 1.0 / R1 is locked, so this repository is not accepting feature expansion as a route into canonical R1. Reproducible defects, security reports, rights concerns, documentation corrections, and evidence gaps are in scope. See [CURRENT_STATUS.md](CURRENT_STATUS.md).

### Reporting Issues
- Use GitHub Issues for bug reports, maintenance proposals, and questions
- Include specific examples when possible
- For security vulnerabilities, email pausebeforeharmprotocol_pbhp@protonmail.com directly

### Submitting Changes
1. Fork the repository
2. Create a focused branch (`git checkout -b fix/short-description`)
3. Make your changes
4. Test with the self-test rubric (`implementation/PBHP_IMPLEMENTATION_SELF_TEST.md`)
5. Submit a pull request with a clear description

### What We're Looking For
- **Reproducible defects** in the preserved implementation or documentation
- **Security and rights reports** with concrete evidence
- **Test gaps** demonstrated by a failing or missing case
- **Documentation corrections** that improve accuracy without rewriting preserved history
- **Custody and provenance improvements** that keep exact identities auditable

### What We're Not Accepting Through This Repository
- Changes that make the core protocol longer than ~100 lines (brevity is a feature)
- Vendor-specific integrations in the core (keep it model-agnostic)
- Theoretical frameworks without practical application
- New Project Shadow R1 features, payloads, release bundles, Primitive Commons packages, custody archives, or Myth sidecar bytes
- Claims of production readiness, efficacy, safety, certification, or legal compliance

## Code of Conduct

Be constructive. The goal is preventing harm — that starts with how we treat each other.

## License

Contributions are licensed according to their destination paths, as specified in [LICENSE](LICENSE): MIT for material in `src/` and `eval/`; CC BY-SA 4.0 for the listed protocol and documentation paths. A pull request should identify which license applies to each added or changed file. New material in an unlisted path requires an explicit maintainer license designation before acceptance.

## Contact

- GitHub Issues (preferred for public discussion)
- Email: pausebeforeharmprotocol_pbhp@protonmail.com
- Social Media: facebook.com/plinst
