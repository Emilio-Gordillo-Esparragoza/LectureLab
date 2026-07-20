# Security Policy for LectureLab

## Supported versions

Security fixes are applied on the `main` branch of this repository.

## Reporting a vulnerability

Please **do not** open a public issue for security-sensitive reports.

Email the maintainer listed on the GitHub profile for
[Emilio-Gordillo-Esparragoza/LectureLab](https://github.com/Emilio-Gordillo-Esparragoza/LectureLab),
or use GitHub **Private vulnerability reporting** (Security → Advisories) if enabled.

Include:

- A short description of the issue
- Steps to reproduce / proof of concept (if safe)
- Affected files or dependency versions when relevant

We aim to acknowledge reports within a reasonable time and will coordinate a fix
before any public disclosure when appropriate.

## Automated protections

This repository runs:

- Dependency audits (`pip-audit`) and Dependabot updates
- CodeQL and OpenSSF Scorecard
- Secret scanning (Gitleaks)
- SLSA build provenance attestations for source archives on `main` / tags
