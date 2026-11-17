# Cookie and Local Storage Policy

> **DRAFT -- REQUIRES LEGAL REVIEW**
> This document is a template prepared for `{{ORGANIZATION_NAME}}` (`{{LEGAL_ENTITY_NAME}}`) and does not constitute legal advice. Replace all `{{PLACEHOLDER}}` tokens and obtain qualified legal review prior to publication.

**Effective Date:** `{{EFFECTIVE_DATE}}`  
**Operator:** `{{LEGAL_ENTITY_NAME}}`  
**Contact:** `{{CONTACT_EMAIL}}`

---

## 1. Overview

The standalone HTML dashboards generated from `templates/meeting_dashboard_template.html` and `templates/presentation_dashboard_template.html` (`dashboard.html`) do **not** set HTTP cookies, advertising identifiers, cross-site tracking pixels, or analytics beacons.

## 2. Client-Side Storage Inventory

| Key Name | Storage Mechanism | Category | Purpose | Expiration | Third-Party Sharing |
|---|---|---|---|---|---|
| `dashboard_theme` | `window.localStorage` | Strictly Functional (User Interface Preference) | Remembers whether the user toggled `light` or `dark` color mode when viewing the local dashboard. | Persistent in local browser profile until cleared by user | None (never transmitted over any network) |

## 3. Managing or Clearing Local Storage

Users may clear the `dashboard_theme` key at any time through standard browser developer tools (`Application -> Local Storage`) or by clearing site/file data in browser privacy settings. If `localStorage` is blocked or disabled in sandboxed environments, the dashboard degrades cleanly to the default in-memory theme without losing functionality.

## 4. Hosted Web Portal Deployments (If Applicable)

If `{{ORGANIZATION_NAME}}` embeds these dashboards inside a hosted web application that introduces session cookies (`HttpOnly; Secure; SameSite=Lax`) or optional telemetry, `{{ORGANIZATION_NAME}}` must list each cookie in the table above and obtain prior opt-in consent before setting any non-essential storage items under ePrivacy Directive Art. 5(3) and GDPR.
