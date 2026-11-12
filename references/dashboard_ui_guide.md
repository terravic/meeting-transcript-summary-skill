# Interactive Web Dashboard Guide

This document outlines the architecture, layout specifications, and mode-tailored data contracts for rendering interactive HTML/JS/CSS dashboards in web-based Canvas runtimes, strictly adhering to [DESIGN.md](../DESIGN.md).

---

## 1. Dashboard Architecture

Agent harnesses render dynamic user interfaces by executing self-contained HTML5, modern CSS, and vanilla JavaScript inside a sandboxed `<iframe>`.

### Key Runtime Characteristics:
- **Artifact Emission Standard:** By default, no dashboard is built (`dashboard = no dashboard`). Only when the user explicitly requests a dashboard in the prompt (e.g., `"yes dashboard"`, `"build dashboard"`, `"create dashboard"`, `"with dashboard"`), you MUST emit the standalone HTML file as a user-facing artifact named `dashboard.html` (using `write_to_file` with `ArtifactMetadata: { UserFacing: true, Summary: "Interactive Evaluation Dashboard", RequestFeedback: false }`). This ensures the dashboard immediately opens and renders directly in the preview pane.
- **Mode-Tailored Templates:**
  - **Meeting Mode Dashboard:** Uses [templates/meeting_dashboard_template.html](../templates/meeting_dashboard_template.html) to present collaborative meeting records (`Executive Brief`, `Interactive Relationship Node Map`, `Action Items` Monospace Table / Flat Owner Lanes, and `Discussion Record`).
  - **Presentation Mode Dashboard:** Uses [templates/presentation_dashboard_template.html](../templates/presentation_dashboard_template.html) to focus directly on the **Interactive Relationship Node Map** (active on load) and the sequential **Chronological Walkthrough**, omitting meeting-specific Executive Brief metrics and Action Items.
- **Zero AI Slop Compliance ([DESIGN.md](../DESIGN.md)):**
  - **Typography:** Uses `'DM Sans'` for UI/headers paired with `'IBM Plex Mono'` for all tabular data, dates, and numeric readouts. Never use `Inter` or `Roboto`.
  - **No Purple/Lavender Gradients:** Uses flat solid surfaces and `1px solid` hairline borders (`6px` to `8px` radius).
  - **No Card-in-Card Nesting:** Uses flat bento-style grids separated by `1px solid` hairline dividers.
  - **Critical-Only Status Indicators:** Only displays status badges when an item is in an error, warning, or critical blocker state (e.g., `UNASSIGNED BLOCKER` in `#E11D48` or `HARD GATE` in `#D97706`).
- **Concise, Fact-First Data Copy:** All string fields populated into `MEETING_DATA` and `PRESENTATION_DATA` (`objective`, `decisions`, `impacts`, `risks`, `context`, `explanation`, `rationale`, `conclusion`, `summary`, `visualsAndMetrics`, `takeaway`) must use the same crisp, telegraphic, zero-"he said / she said" style required for Markdown output—never verbose prose or speaker-turn narration.

---

## 2A. Meeting Mode Dashboard Components

When running in **Meeting Mode**, the dashboard ([templates/meeting_dashboard_template.html](../templates/meeting_dashboard_template.html)) comprises four primary interface modules:

### 2A.1 Executive Brief (Flat Bento Grid & Data Visualizations)
- **KPI Strip:** Flat 4-column bento grid displaying monospaced counts for approved decisions, architecture domains, tracked deliverables, and target cutover dates.
- **Data Visualizations:**
  - **Telemetry, Cost & Payload Benchmarks:** Vibrant SVG comparison chart using the semantic visualization palette (`#0D9488`, `#D97706`, `#4F46E5`, `#059669`, `#E11D48`) over faint chart gridlines (`#E7E5E4` light / `#292A30` dark).
  - **Topic & Owner Coverage Matrix (Heatmap):** High-contrast gradient heatmap matrix mapping participants to architecture domains, highlighting unassigned critical gaps in Deep Rose (`#E11D48`).
- **Executive Summary Bento:** Flat 2×2 bento grid displaying `Objective`, `Approved Decisions`, `Strategic Outcomes & Impact`, and `Critical Risks & Blockers`.

### 2A.2 Interactive Relationship Node Map
- **Visual Topology:** An interactive SVG node-link map representing the central meeting objective (`#0D9488` Vibrant Teal), radiating outwards to distinct topic nodes colored from the approved 5-color visualization palette (`#4F46E5`, `#059669`, `#D97706`, `#E11D48`).
- **Semi-Transparent Color-Matched Edges:** Directed edges use semi-transparent versions of the source node color with faint background chart gridlines (`#E7E5E4` in light mode, `#292A30` in dark mode).
- **Node Selection and Inspector:** Clicking any node opens a slide-out Detail Inspector drawer presenting the full Context, Technical Mechanism, Spoken Rationale, and Key Conclusion.

### 2A.3 Action Items (Monospace Table & Flat Owner Lanes)
- **Filtering Toolbar:** View switcher (`Monospace Table` | `Owner Lanes`), Live Search Input, Owner Dropdown Filter, CSV and Markdown export buttons, and Monospace Row Count.
- **Views:**
  1. **Monospace Table (Default):** Tabular view using `'IBM Plex Mono'` with thin `1px solid` horizontal dividers and zero vertical borders.
  2. **Owner Lanes:** Flat bento columns organized per owner with thin horizontal dividers and zero card-in-card nesting.

### 2A.4 Discussion Record
- Flat collapsible topic rows separated by `1px solid` horizontal dividers.

---

## 2B. Presentation Mode Dashboard Components

When running in **Presentation Mode**, the dashboard ([templates/presentation_dashboard_template.html](../templates/presentation_dashboard_template.html)) comprises two focused tabs:

### 2B.1 Interactive Relationship Node Map (Default Active View on Load)
- **Immediate Graph Focus:** Opens directly to the interactive SVG Node Map (`#tab-graph` active on load) accompanied by a flat bento header displaying the presentation's `Core Theme`.
- **Chronological and Conceptual Topology:**
  - **Central Node:** Represents the `CORE THEME` (`#0D9488` Vibrant Teal).
  - **Chronological Segment Nodes (`#1..#N`):** Each node displays its monospaced chronological sequence number (`#1`, `#2`, ...) above its concise `shortTitle`, colored from the 5-color visualization palette.
  - **Slide / Segment Detail Inspector Drawer:** Clicking any node slides out the Inspector displaying `What Was Presented & Said`, `Slide Visuals, Demos & Metrics Cited`, and `Stated Key Takeaway`.

### 2B.2 Chronological Walkthrough (Tab 2)
- Sequential, numbered flat accordion rows (`#01` through `#0N`) presenting the chronological description and summarization of what was said from beginning to end.

---

## 3. Light and Dark Theme Specifications ([DESIGN.md](../DESIGN.md))

- **Theme Switcher (`#theme-toggle-btn`):** A single, minimalist, textless icon button toggling between an inline SVG sun icon and moon icon.
- **Light Mode (`[data-theme="light"]`):**
  - Background: `#FAFAF9`
  - Cards & Surfaces: `#FFFFFF`
  - Borders & Chart Gridlines: `#E7E5E4` (`1px solid`, `6px` to `8px` border-radius)
  - Text Primary: `#1C1917`
  - Text Secondary: `#787774`
- **Dark Mode (`:root, [data-theme="dark"]`):**
  - Background: `#0D0E11`
  - Cards & Surfaces: `#16171D`
  - Borders & Chart Gridlines: `#292A30` (`1px solid`, `6px` to `8px` border-radius)
  - Text Primary: `#ECE8E2`
  - Text Secondary: `#9A9895`
- **Data Visualization Palette:**
  - **Vibrant Teal:** `#0D9488`
  - **Energetic Amber:** `#D97706`
  - **Vivid Indigo:** `#4F46E5`
  - **Functional Emerald:** `#059669`
  - **Deep Rose:** `#E11D48`
