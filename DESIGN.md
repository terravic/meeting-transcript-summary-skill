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

- **Self-Contained Execution:** Each dashboard must be a single standalone HTML5 document using standard CSS and vanilla JavaScript with zero external network dependencies and a restrictive `<meta http-equiv="Content-Security-Policy">` (`default-src 'none'; connect-src 'none'; font-src 'none'`).
- **Output Escaping and Export Sanitization:** Dynamic strings rendered into HTML or SVG containers must pass through `escapeHtml()`, dynamic hex colors must pass through `sanitizeHexColor()`, and CSV/Markdown exports must neutralize leading spreadsheet formula triggers (`=`, `+`, `-`, `@`, `\t`, `\r`).
- **Interactive Client State:** Tabs (`role="tablist"` / `role="tab"` / `role="tabpanel"`), filters, search, sorting, keyboard-focusable SVG nodes, inspector drawers (`Escape` dismissal and focus return), and theme switching must operate in client-side JavaScript without page reloads.
- **Output File Standard (`dashboard.html`):** When dashboard output is requested, generate a standalone HTML document written to `dashboard.html`.
- **Grounded Data Only:** Populate dashboards exclusively with facts, metrics, topics, and tasks extracted from the user's transcript. Placeholder or synthetic sample data is permitted only inside repository template and example files.

---

## 3. Light and Dark Theme Specifications

Every dashboard must support both light and dark color schemes with a persistent preference key (`dashboard_theme`) stored in `localStorage`.

- **Theme Switcher:** Provide a single plain-text toggle button (`#theme-toggle-btn`) in the header controls that displays `Light` while dark mode is active and `Dark` while light mode is active.
- **Color Tokens (WCAG 2.2 AA `>= 4.5:1` Text Contrast):**
  - **Light Mode (`[data-theme="light"]`):**
    - Base Background (`--bg-base`): `#FAFAF9`
    - Cards and Surfaces (`--bg-surface`): `#FFFFFF`
    - Borders and Chart Gridlines (`--border-color`, `--chart-grid`): `#E7E5E4` (`1px solid`, `6px` to `8px` border-radius)
    - Text Primary (`--text-primary`): `#1C1917`
    - Text Secondary (`--text-secondary`): `#57534E`
    - Accessible Accent Text (`--viz-teal-text`, `--viz-amber-text`, `--viz-indigo-text`, `--viz-emerald-text`, `--viz-rose-text`): `#0F766E`, `#B45309`, `#4338CA`, `#047857`, `#BE123C`
  - **Dark Mode (`:root, [data-theme="dark"]`):**
    - Base Background (`--bg-base`): `#0D0E11`
    - Cards and Surfaces (`--bg-surface`): `#16171D`
    - Borders and Chart Gridlines (`--border-color`, `--chart-grid`): `#292A30` (`1px solid`, `6px` to `8px` border-radius)
    - Text Primary (`--text-primary`): `#ECE8E2`
    - Text Secondary (`--text-secondary`): `#9A9895`
    - Accessible Accent Text (`--viz-teal-text`, `--viz-amber-text`, `--viz-indigo-text`, `--viz-emerald-text`, `--viz-rose-text`): `#2DD4BF`, `#F59E0B`, `#818CF8`, `#34D399`, `#FB7185`

---

## 4. Dashboard Layout and Component Rules

Dashboards must balance high information density with direct, scannable component structure.

- **Semantic Structure and Accessibility:** Maintain semantic HTML landmarks (`header`, `nav`, `main`, `footer`), a single `<h1>` document title with `<h2>` section headings, visible `:focus-visible` outlines, and explicit bracketed text tags (`[BLOCKER: UNASSIGNED]`, `[HARD GATE]`, `[HIGH]`/`[MED]`/`[LOW]`/`[GAP]`) so state never relies on color alone.
- **Text Displays:** Keep labels, headers, and summary entries concise and factual. Avoid conversational commentary in UI containers.
- **Tables:** Format tabular columns using `ui-monospace, monospace` with thin horizontal dividers (`1px solid`) and zero vertical borders.
- **Relationship Graphs:**
  - Use direct component titles such as "Interactive Relationship Node Map" or "Structural Data Diagram". Avoid physics-related terminology in visible UI labels.
  - Keep layout calculations deterministic and lightweight to avoid iframe rendering lag.

---

## 5. Data Visualization Color Palette

Container surfaces remain neutral and minimalist, while data visualizations (bar charts, coverage heatmaps, and relationship node maps) use high-contrast semantic colors legible against both light and dark surfaces. Avoid monochrome grayscale charts.

| Color Role | Graphical Fill Hex | Light Text Hex | Dark Text Hex | Visual Application |
| :--- | :--- | :--- | :--- | :--- |
| **Teal** | `#0D9488` | `#0F766E` | `#2DD4BF` | Primary data series, core central nodes, structural links, baseline metrics |
| **Amber** | `#D97706` | `#B45309` | `#F59E0B` | Secondary data series, warning gates, dynamic relationships, medium intensity |
| **Indigo** | `#4F46E5` | `#4338CA` | `#818CF8` | Comparison series, domain clusters, secondary network nodes |
| **Emerald** | `#059669` | `#047857` | `#34D399` | Verified outcomes, positive benchmark shifts, completed states |
| **Rose** | `#E11D48` | `#BE123C` | `#FB7185` | Critical risks, negative trends, unassigned blockers, high-priority anomalies |

### Visualization Guidelines
- **Matrices and Heatmaps:** Map density using clear contrast steps from low-alpha surface tints up to high-contrast solid fills (`#0F766E`, `#4338CA`, `#047857`, `#B45309`, `#BE123C` with `#FFFFFF` text `>= 5.0:1`), paired with explicit text prefixes (`[HIGH]`, `[MED]`, `[LOW]`, `[GAP]`).
- **Node Maps:** Assign distinct palette colors per topic or segment category, using semi-transparent versions of the source node color for directed edges and `system-ui, sans-serif` / `ui-monospace, monospace` for labels.
- **Plot Surface Contrast:** Keep plot backgrounds transparent so they inherit `--bg-surface` or `--bg-base`, with faint chart gridlines (`#E7E5E4` light, `#292A30` dark).

---

## 6. Verification Checklist

Before finalizing a generated dashboard, verify all criteria:
1. Standalone `dashboard.html` includes a restrictive `Content-Security-Policy` meta tag and runs cleanly without external stylesheets, fonts, or scripts.
2. Dynamic transcript strings are escaped via `escapeHtml()` and CSV/Markdown exports neutralize formula injection characters.
3. Theme switcher toggles cleanly between light and dark token sets via plain-text `Light` / `Dark` control, maintaining `>= 4.5:1` text contrast in both themes.
4. No multi-stop gradients, nested cards, routine non-critical badges, or decorative wireframe grids appear; critical states use explicit bracketed text tags.
5. Tabs, filters, accordions, heatmap cells, and SVG graph nodes are fully operable via keyboard with visible `:focus-visible` indicators.
6. All rendered strings match actual processed transcript data without ungrounded placeholders.
