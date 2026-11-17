# Privacy Policy

> **DRAFT -- REQUIRES LEGAL REVIEW**
> This document is a template prepared for `{{ORGANIZATION_NAME}}` (`{{LEGAL_ENTITY_NAME}}`) and does not constitute legal advice. Replace all `{{PLACEHOLDER}}` tokens and obtain qualified legal review prior to publication.

**Effective Date:** `{{EFFECTIVE_DATE}}`  
**Controller / Operator:** `{{LEGAL_ENTITY_NAME}}`  
**Registered Address:** `{{POSTAL_ADDRESS}}`  
**Privacy Contact:** `{{CONTACT_EMAIL}}`  
**Data Protection Officer (if applicable):** `{{DATA_PROTECTION_OFFICER_EMAIL}}`

---

## 1. Scope

This Privacy Policy describes how `{{ORGANIZATION_NAME}}` processes personal data when users process meeting or presentation transcripts using the `meeting-transcript-summary` skill package, CLI preprocessor (`scripts/clean_transcript.py`), and generated standalone HTML dashboards (`dashboard.html`).

## 2. Categories of Data Processed

1. **Transcript Inputs:** Spoken dialogue, participant names, presenter names, role titles, dates, timestamps, and task assignments contained in user-supplied `.txt`, `.vtt`, or `.srt` files.
2. **Generated Outputs:** Structured Markdown summaries and local HTML dashboard files derived exclusively from user-supplied transcript inputs.
3. **Client-Side Preference State:** A single local browser preference key (`dashboard_theme` set to `light` or `dark`) stored in `window.localStorage` when viewing a generated HTML dashboard locally.

## 3. Architecture and Data Minimization

- **Offline Static Dashboards:** Generated HTML dashboards execute locally in the user's browser with a restrictive `Content-Security-Policy` (`connect-src 'none'`, `font-src 'none'`). Dashboards do not load external fonts, third-party scripts, analytics trackers, or remote images, and do not transmit IP addresses or telemetry to third parties.
- **Local CLI Preprocessing:** `scripts/clean_transcript.py` runs locally on the user's machine and writes output only to standard output or the user-specified `--output` file path.
- **LLM Processing (Host Environment Dependent):** When `SKILL.md` is invoked through an external AI assistant or model provider configured by `{{ORGANIZATION_NAME}}`, transcript text is transmitted to `{{LLM_HOST_PROVIDER}}` hosted in `{{HOSTING_REGION}}` under the operator's configured account and data processing agreement.

## 4. Legal Basis and Regional Data Governance

Where GDPR or UK GDPR applies:
- Processing is performed under `{{LEGAL_BASIS_GDPR}}` (for example, Art. 6(1)(b) contract performance or Art. 6(1)(f) legitimate interests, or Art. 6(1)(a) consent where required for recorded transcripts).
- IP addresses and speaker identifiers are treated as personal data.
- For European Economic Area (EEA), UK, and Swiss deployments, `{{ORGANIZATION_NAME}}` pins model inference and storage endpoints to `{{EEA_HOSTING_REGION}}` and maintains Standard Contractual Clauses (SCCs) or verified adequacy mechanisms (`{{TRANSFER_MECHANISM}}`) for any cross-border sub-processors.
- Regulated health information (PHI under HIPAA) must not be submitted unless a signed Business Associate Agreement (`{{BAA_REFERENCE}}`) is active for `{{LLM_HOST_PROVIDER}}`.

## 5. Sub-Processors

| Sub-Processor | Purpose | Physical Region | Safeguard / Mechanism |
|---|---|---|---|
| `{{LLM_HOST_PROVIDER}}` | Transcript synthesis when skill instructions are invoked | `{{HOSTING_REGION}}` | `{{TRANSFER_MECHANISM}}` |
| None (Static HTML Dashboards & CLI) | Local rendering and caption normalization | Local User Device | Offline execution (`connect-src 'none'`) |

## 6. Data Retention

- **Local Files:** Generated Markdown summaries and `dashboard.html` files remain on the user's local filesystem until deleted by the user.
- **Hosted Logs (If Applicable):** `{{ORGANIZATION_NAME}}` retains hosted request logs and processed artifacts for `{{RETENTION_PERIOD_DAYS}}` days, after which records are permanently purged.

## 7. Data Subject Rights (Access, Portability, and Erasure)

Subject to applicable law, individuals may request:
1. **Access and Portability:** A copy of personal data processed by `{{ORGANIZATION_NAME}}` in a structured, machine-readable format (JSON, CSV, or Markdown).
2. **Rectification:** Correction of inaccurate participant or transcript records controlled by `{{ORGANIZATION_NAME}}`.
3. **Erasure (Right to be Forgotten):** Permanent deletion of personal data across active stores, backups, and sub-processors.

Submit requests to `{{CONTACT_EMAIL}}`. Verified requests are fulfilled within `{{ERASURE_SLA_DAYS}}` days (not exceeding 30 days where GDPR applies).
