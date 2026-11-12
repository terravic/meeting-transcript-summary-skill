# Interactive Web Dashboard Guide

This document defines the architecture, layout specifications, and mode-tailored data contracts for rendering self-contained interactive HTML/CSS/JavaScript dashboards in sandboxed web runtimes, in accordance with [DESIGN.md](../DESIGN.md).

---

## 1. Dashboard Architecture

Dashboards are self-contained HTML5 documents using standard CSS and vanilla JavaScript that run offline or inside a sandboxed `<iframe>` with zero external network dependencies.

### Key Runtime Characteristics
- **Output File Standard:** By default, no dashboard is built (`dashboard = no dashboard`). Only when the user explicitly requests a dashboard in the prompt (for example, `"yes dashboard"`, `"build dashboard"`, `"create dashboard"`, or `"with dashboard"`), write the standalone HTML document to `dashboard.html`.
- **Mode-Tailored Templates:**
  - **Meeting Mode Dashboard:** Uses [templates/meeting_dashboard_template.html](../templates/meeting_dashboard_template.html) to present collaborative meeting records (`Executive Brief`, `Interactive Relationship Node Map`, `Action Items` Monospace Table / Flat Owner Lanes, and `Discussion Record`).
  - **Presentation Mode Dashboard:** Uses [templates/presentation_dashboard_template.html](../templates/presentation_dashboard_template.html) to focus directly on the **Interactive Relationship Node Map** (active on load) and the sequential **Chronological Walkthrough**, omitting meeting-specific Executive Brief metrics and Action Items.
- **Visual Design Alignment ([DESIGN.md](../DESIGN.md)):**
  - **Typography:** Uses `system-ui, sans-serif` for UI text and headers paired with `ui-monospace, monospace` for tabular data, dates, and numeric readouts.
  - **Flat Surfaces:** Uses solid light/dark surface tokens with `1px solid` hairline borders (`6px` to `8px` border-radius) and zero multi-stop gradients.
  - **Flat Bento Grids:** Uses single-layer bento grids separated by `1px solid` hairline dividers without nested cards.
  - **Critical-Only Status Indicators:** Displays status badges strictly for critical blockers or gates (for example, `UNASSIGNED BLOCKER` in `#E11D48` or `HARD GATE` in `#D97706`).
- **Concise, Fact-First Data Copy:** All string fields populated into `MEETING_DATA` and `PRESENTATION_DATA` (`objective`, `decisions`, `impacts`, `risks`, `context`, `explanation`, `rationale`, `conclusion`, `summary`, `visualsAndMetrics`, `takeaway`) must use the same direct, zero-"he said / she said" style required for Markdown output -- never verbose prose or speaker-turn narration.

---

## 2A. Meeting Mode Dashboard Components

When running in **Meeting Mode**, the dashboard ([templates/meeting_dashboard_template.html](../templates/meeting_dashboard_template.html)) comprises four primary interface modules:

### 2A.1 Executive Brief (Flat Bento Grid and Data Visualizations)
- **KPI Strip:** Flat 4-column bento grid displaying monospaced counts for approved decisions, architecture domains, tracked deliverables, and target cutover date.
- **Data Visualizations:**
  - **Telemetry, Cost, and Payload Benchmarks:** SVG comparison chart using the semantic 5-color visualization palette (`#0D9488`, `#D97706`, `#4F46E5`, `#059669`, `#E11D48`) over faint chart gridlines (`#E7E5E4` light / `#292A30` dark).
  - **Topic and Owner Coverage Matrix (Heatmap):** High-contrast gradient heatmap matrix mapping participants to topic domains, highlighting unassigned critical gaps in Rose (`#E11D48`).
- **Executive Summary Bento:** Flat 2x2 bento grid displaying `Objective`, `Approved Decisions`, `Strategic Outcomes & Impact`, and `Critical Risks & Blockers`.

### 2A.2 Interactive Relationship Node Map
- **Visual Topology:** An interactive SVG node-link map representing the central meeting objective (`#0D9488` Teal), radiating outward to topic nodes colored from the 5-color palette (`#4F46E5`, `#059669`, `#D97706`, `#E11D48`).
- **Semi-Transparent Color-Matched Edges:** Directed edges use semi-transparent versions of the source node color over faint chart gridlines (`#E7E5E4` in light mode, `#292A30` in dark mode).
- **Node Selection and Inspector:** Clicking any node opens a slide-out Detail Inspector drawer presenting Context, Technical Mechanism, Spoken Rationale, and Key Conclusion.

### 2A.3 Action Items (Monospace Table and Flat Owner Lanes)
- **Filtering Toolbar:** View switcher (`Monospace Table` | `Owner Lanes`), Live Search Input, Owner Dropdown Filter, CSV and Markdown export buttons, and Monospace Row Count.
- **Views:**
  1. **Monospace Table (Default):** Tabular view using `ui-monospace, monospace` with thin `1px solid` horizontal dividers and zero vertical borders.
  2. **Owner Lanes:** Flat bento columns organized per owner with thin horizontal dividers and zero nested cards.

### 2A.4 Discussion Record
- Flat collapsible topic rows separated by `1px solid` horizontal dividers.

---

## 2B. Presentation Mode Dashboard Components

When running in **Presentation Mode**, the dashboard ([templates/presentation_dashboard_template.html](../templates/presentation_dashboard_template.html)) comprises two focused tabs:

### 2B.1 Interactive Relationship Node Map (Default Active View on Load)
- **Immediate Graph Focus:** Opens directly to the interactive SVG Node Map (`#tab-graph` active on load) accompanied by a flat bento header displaying the presentation's `Core Theme`.
- **Chronological and Conceptual Topology:**
  - **Central Node:** Represents the `CORE THEME` (`#0D9488` Teal).
  - **Chronological Segment Nodes (`#1..#N`):** Each node displays its monospaced chronological sequence number (`#1`, `#2`, ...) above its concise `shortTitle`, colored from the 5-color palette.
  - **Slide / Segment Detail Inspector Drawer:** Clicking any node slides out the Inspector displaying `What Was Presented & Said`, `Slide Visuals, Demos & Metrics Cited`, and `Stated Key Takeaway`.

### 2B.2 Chronological Walkthrough (Tab 2)
- Sequential, numbered flat accordion rows (`#01` through `#0N`) presenting the chronological description and summary of what was presented from start to finish.

---

## 3. Light and Dark Theme Specifications ([DESIGN.md](../DESIGN.md))

- **Theme Switcher (`#theme-toggle-btn`):** A single plain-text toggle button switching between `Light` and `Dark` modes (`localStorage` key `dashboard_theme`).
- **Light Mode (`[data-theme="light"]`):**
  - Base Background: `#FAFAF9`
  - Cards and Surfaces: `#FFFFFF`
  - Borders and Chart Gridlines: `#E7E5E4` (`1px solid`, `6px` to `8px` border-radius)
  - Text Primary: `#1C1917`
  - Text Secondary: `#787774`
- **Dark Mode (`:root, [data-theme="dark"]`):**
  - Base Background: `#0D0E11`
  - Cards and Surfaces: `#16171D`
  - Borders and Chart Gridlines: `#292A30` (`1px solid`, `6px` to `8px` border-radius)
  - Text Primary: `#ECE8E2`
  - Text Secondary: `#9A9895`
- **Data Visualization Palette:**
  - **Teal:** `#0D9488`
  - **Amber:** `#D97706`
  - **Indigo:** `#4F46E5`
  - **Emerald:** `#059669`
  - **Rose:** `#E11D48`
