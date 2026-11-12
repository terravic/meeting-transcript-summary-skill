# Dashboard Design Specification

This specification defines visual, structural, and technical constraints for generating and updating self-contained HTML dashboards in this repository. All dashboard templates and generated dashboard files must follow these standards.

---

## 1. Layout and Structural Constraints

| Element Category | Prohibited Pattern | Required Standard |
| :--- | :--- | :--- |
| **Typography** | External third-party font stylesheets or inconsistent display fonts | Use `system-ui, sans-serif` for interface text and headers, paired with `ui-monospace, monospace` for tabular data, dates, and numeric readouts. |
| **Backgrounds** | Multi-stop decorative gradients or purple/lavender color washes | Use flat solid surfaces with `1px solid` hairline borders (`6px` to `8px` border-radius) for visual separation. |
| **Container Nesting** | Card-in-card nesting that adds excessive padding and clutter | Use flat bento-style grids separated by thin borderless or `1px solid` dividers. |
| **Status Badges** | Routine "Ready" or "Active" labels on every item | Display status indicators strictly for errors, warnings, blockers, or critical gates. |
| **Gridlines** | Background wireframe grids behind cards or page layouts | Restrict faint gridlines exclusively to chart and graph plot areas. |
| **Header Hierarchy** | Decorative graphics next to metric headings | Use direct plain-text hierarchy and monospaced labels. |

---

## 2. Sandbox Environment and Technical Constraints

Dashboards must execute reliably inside sandboxed browser iframes and standalone local browser tabs.

- **Self-Contained Execution:** Each dashboard must be a single standalone HTML5 document using standard CSS and vanilla JavaScript with zero external network dependencies.
- **Interactive Client State:** Tabs, filters, search, sorting, node inspection drawers, and theme switching must operate smoothly in client-side JavaScript without page reloads.
- **Output File Standard (`dashboard.html`):** When dashboard output is requested, generate a standalone HTML document written to `dashboard.html`.
- **Grounded Data Only:** Populate dashboards exclusively with facts, metrics, topics, and tasks extracted from the user's transcript. Placeholder or synthetic sample data is permitted only inside repository template and example files.

---

## 3. Light and Dark Theme Specifications

Every dashboard must support both light and dark color schemes with a persistent preference key (`dashboard_theme`) stored in `localStorage`.

- **Theme Switcher:** Provide a single plain-text toggle button (`#theme-toggle-btn`) in the header controls that displays `Light` while dark mode is active and `Dark` while light mode is active.
- **Color Tokens:**
  - **Light Mode (`[data-theme="light"]`):**
    - Base Background (`--bg-base`): `#FAFAF9`
    - Cards and Surfaces (`--bg-surface`): `#FFFFFF`
    - Borders and Chart Gridlines (`--border-color`, `--chart-grid`): `#E7E5E4` (`1px solid`, `6px` to `8px` border-radius)
    - Text Primary (`--text-primary`): `#1C1917`
    - Text Secondary (`--text-secondary`): `#787774`
  - **Dark Mode (`:root, [data-theme="dark"]`):**
    - Base Background (`--bg-base`): `#0D0E11`
    - Cards and Surfaces (`--bg-surface`): `#16171D`
    - Borders and Chart Gridlines (`--border-color`, `--chart-grid`): `#292A30` (`1px solid`, `6px` to `8px` border-radius)
    - Text Primary (`--text-primary`): `#ECE8E2`
    - Text Secondary (`--text-secondary`): `#9A9895`

---

## 4. Dashboard Layout and Component Rules

Dashboards must balance high information density with direct, scannable component structure.

- **Text Displays:** Keep labels, headers, and summary entries concise and factual. Avoid conversational commentary in UI containers.
- **Tables:** Format tabular columns using `ui-monospace, monospace` with thin horizontal dividers (`1px solid`) and zero vertical borders.
- **Relationship Graphs:**
  - Use direct component titles such as "Interactive Relationship Node Map" or "Structural Data Diagram". Avoid physics-related terminology in visible UI labels.
  - Keep layout calculations deterministic and lightweight to avoid iframe rendering lag.

---

## 5. Data Visualization Color Palette

Container surfaces remain neutral and minimalist, while data visualizations (bar charts, coverage heatmaps, and relationship node maps) use high-contrast semantic colors legible against both light and dark surfaces. Avoid monochrome grayscale charts.

| Color Role | Hex Code | Visual Application |
| :--- | :--- | :--- |
| **Teal** | `#0D9488` | Primary data series, core central nodes, structural links, baseline metrics |
| **Amber** | `#D97706` | Secondary data series, warning gates, dynamic relationships, medium intensity |
| **Indigo** | `#4F46E5` | Comparison series, domain clusters, secondary network nodes |
| **Emerald** | `#059669` | Verified outcomes, positive benchmark shifts, completed states |
| **Rose** | `#E11D48` | Critical risks, negative trends, unassigned blockers, high-priority anomalies |

### Visualization Guidelines
- **Matrices and Heatmaps:** Map density using clear contrast steps from desaturated surface tones up to saturated Indigo (`#4F46E5`) or Teal (`#0D9488`), reserving Rose (`#E11D48`) for critical unassigned gaps.
- **Node Maps:** Assign distinct palette colors per topic or segment category, using semi-transparent versions of the source node color for directed edges.
- **Plot Surface Contrast:** Keep plot backgrounds transparent so they inherit `--bg-surface` or `--bg-base`, with faint chart gridlines (`#E7E5E4` light, `#292A30` dark).

---

## 6. Verification Checklist

Before finalizing a generated dashboard, verify all criteria:
1. Standalone `dashboard.html` runs cleanly without external stylesheets or scripts.
2. Theme switcher toggles cleanly between light and dark token sets via plain-text `Light` / `Dark` control.
3. No multi-stop gradients, nested cards, routine non-critical badges, or decorative wireframe grids appear.
4. Charts, heatmaps, and node maps use the semantic 5-color palette with legible contrast in both themes.
5. All rendered strings match actual processed transcript data without ungrounded placeholders.
