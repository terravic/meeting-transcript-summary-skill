# Interactive Web Dashboard Guide

This document outlines the architecture, layout specifications, and mode-tailored data contracts for rendering interactive HTML/JS/CSS dashboards in web-based artifact runtimes.

---

## 1. Dashboard Architecture

Agent harnesses render dynamic user interfaces by executing self-contained HTML, CSS, and JavaScript inside a sandboxed `<iframe>`.

### Key Runtime Characteristics:
- **Artifact Emission Standard:** When generating or updating the interactive HTML dashboard in either mode, you MUST emit the standalone HTML file as a user-facing artifact named `dashboard.html` (using `write_to_file` with `ArtifactMetadata: { UserFacing: true, Summary: "Interactive Evaluation Dashboard", RequestFeedback: false }`). This ensures the dashboard immediately opens and renders directly in the preview pane with no need to manually copy or open links in a browser.
- **Mode-Tailored Templates:**
  - **Meeting Mode Dashboard:** Uses [templates/meeting_dashboard_template.html](templates/meeting_dashboard_template.html) to present collaborative meeting records (`Executive Brief`, `Knowledge Graph`, `Action Items` Kanban/Table, and `Detailed Record`).
  - **Presentation Mode Dashboard:** Uses [templates/presentation_dashboard_template.html](templates/presentation_dashboard_template.html) to focus directly on the **Presentation Knowledge Graph** (active on load) and the sequential **Chronological Walkthrough**, omitting meeting-specific Executive Brief metrics and Action Items.
- **Zero-Dependency Self-Containment:** All styles (CSS) and logic (JavaScript) are embedded directly within a single `.html` document or code block. This avoids network timeouts, blocked external CDN requests, and version conflicts.
- **Client-Side Interactivity:** Supports full DOM manipulation, SVG graphical rendering, tab switching, search filtering, and clipboard interactions.
- **Sandboxed Execution:** Scripts execute within standard iframe security constraints (`allow-scripts`, isolated local storage, no parent window cross-origin access).

---

## 2A. Meeting Mode Dashboard Components

When running in **Meeting Mode**, the dashboard ([templates/meeting_dashboard_template.html](templates/meeting_dashboard_template.html)) comprises four primary interface modules:

### 2A.1 Executive Overview and Metrics
- **Metric Badges:** Counts for decisions made, topics analyzed, assigned action items, and target milestone dates.
- **Executive Summary Cards:** Structured cards displaying Meeting Objectives, Approved Decisions, Strategic Impacts, and Critical Risks. (Note: The strict Five-Sentence Summary is generated exclusively in the primary text/markdown output and omitted from the interactive dashboard).

### 2A.2 Interactive Topic Knowledge Graph
- **Visual Topology and Physics Engine:** An interactive SVG node-link graph representing the central meeting objective, radiating outwards to distinct topic nodes labeled with concise, descriptive short titles (e.g. `Platform Migration`, `Protobuf Schemas`, `Security Controls`, `Staging & Cutover`).
- **Collision Avoidance and Visibility:** Employs a hard elastic collision resolution algorithm (`padding >= 28px`) and electrostatic Coulomb repulsion so nodes do not overlap or occlude one another during layout or dragging.
- **Inter-Topic Relationships:** Explicit directed edges link interdependent topics with relationship badge labels (e.g. `Enforces`, `Requires`, `Tested in`, `Gates`).
- **Node Selection and Inspector:** Clicking any node opens a slide-out Detail Inspector drawer presenting the full Context, Technical Mechanism, Rationale / Debates ("Why"), and Key Conclusions.

### 2A.3 Action Items Visualizer (Multi-View and Filter Toolbar)
- **Filtering Toolbar:** Owner Dropdown Filter (`All Owners` default), Live Search Input, CSV and Markdown export buttons, and Live Item Count.
- **Views:**
  1. **Kanban by Owner Board (Default):** Columns organized per participant (plus an `Unassigned` backlog column).
  2. **Structured Interactive Table:** A tabular view displaying all four standardized columns.

### 2A.4 Detailed Narrative Discussion Explorer
- Collapsible topic accordions allowing deep reading of the complete meeting record.

---

## 2B. Presentation Mode Dashboard Components

When running in **Presentation Mode**, there is no back-and-forth meeting debate or action item assignment. The dashboard ([templates/presentation_dashboard_template.html](templates/presentation_dashboard_template.html)) is tailored specifically to visualize the presentation's conceptual and chronological flow, comprising two focused tabs:

### 2B.1 Presentation Knowledge Graph (Default Active View on Load)
- **Immediate Graph Focus:** Opens directly to the interactive SVG Knowledge Graph (`#tab-graph` active on load) accompanied by a top **Presentation Focus** banner stating the presentation's overarching theme.
- **Chronological and Conceptual Topology:**
  - **Central Node:** Represents the `PRESENTATION CORE THEME`.
  - **Chronological Segment Nodes (`#1..#N`):** Each node displays its chronological sequence badge (`#1`, `#2`, `#3`, ...) above its concise 2–3 word `shortTitle`, enabling users to trace the presentation's progression visually.
  - **Directed Relationship Edges:** Connect sequential segments (`Leads to`, `Next: Slide 4`) as well as conceptual dependencies across slides and demonstrations (`Demonstrates`, `Benchmarks`, `Accelerated by`, `Validated in`).
- **Slide / Segment Detail Inspector Drawer:** Clicking any node slides out the Presentation Inspector displaying:
  - **Segment Sequence and Presenter:** e.g., `Segment #2: Two-Tier Hybrid Storage - Presenter: Dr. Aris Thorne`
  - **What Was Presented and Said:** Detailed chronological summary of what the presenter explained.
  - **Slide Visuals, Demos and Metrics Cited:** Specific benchmarks, diagrams, architectures, or live demonstration outputs explicitly referenced aloud by the presenter.
  - **Stated Key Takeaway:** The primary takeaway stated by the presenter for that segment.

### 2B.2 Chronological Walkthrough Timeline (Tab 2)
- Sequential, numbered accordion cards (`#1` through `#N`) presenting the chronological description and summarization of what was said from beginning to end.
- Includes `Expand All`, `Collapse All`, and `Copy Chronological Markdown` toolbar actions.

---

## 3. Dashboard Data Contracts (JSON Schemas)

### 3A. Meeting Mode Data Contract (`MEETING_DATA`)
Used in [templates/meeting_dashboard_template.html](templates/meeting_dashboard_template.html):

```json
{
  "mode": "meeting",
  "meetingTitle": "string",
  "date": "YYYY-MM-DD (use transcript date; if no date is given, assume today's date when the skill runs)",
  "participants": ["string"],
  "metrics": {
    "decisionsCount": 0,
    "topicsCount": 0,
    "actionsCount": 0,
    "targetCutover": "YYYY-MM-DD"
  },
  "executiveSummary": {
    "objective": "string",
    "decisions": ["string"],
    "impacts": ["string"],
    "risks": ["string"]
  },
  "topics": [
    {
      "id": "topic-1",
      "title": "string",
      "shortTitle": "string (2-3 words for node label)",
      "context": "string",
      "explanation": "string",
      "rationale": "string",
      "conclusion": "string"
    }
  ],
  "relationships": [
    {
      "from": "topic-1",
      "to": "topic-2",
      "label": "string (e.g. Enforces, Requires, Tested in, Gates)"
    }
  ],
  "actionItems": [
    {
      "id": "act-1",
      "description": "string",
      "assignee": "string",
      "deadline": "YYYY-MM-DD",
      "deliverable": "string",
      "status": "Assigned | In Progress | Unassigned"
    }
  ]
}
```

### 3B. Presentation Mode Data Contract (`PRESENTATION_DATA`)
Used in [templates/presentation_dashboard_template.html](templates/presentation_dashboard_template.html):

```json
{
  "mode": "presentation",
  "presentationTitle": "string",
  "date": "YYYY-MM-DD (use transcript date; if no date is given, assume today's date when the skill runs)",
  "presenters": ["string"],
  "coreTheme": "string (1-2 sentence overview of what the presentation covers as stated by the presenter)",
  "segments": [
    {
      "id": "seg-1",
      "order": 1,
      "title": "string (Full chronological segment / slide title)",
      "shortTitle": "string (2-3 words for graph node label)",
      "presenter": "string",
      "summary": "string (Detailed chronological description and summarization of what was said)",
      "visualsAndMetrics": "string (Slides, charts, architectures, live demos, or numbers explicitly cited aloud)",
      "takeaway": "string (Key conclusion or takeaway stated by the presenter for this segment)"
    }
  ],
  "relationships": [
    {
      "from": "seg-1",
      "to": "seg-2",
      "label": "string (e.g. Solved by, Accelerated by, Next: Slide 4, Validated in)"
    }
  ]
}
```

---

## 4. Design and Styling Standards

- **Light and Dark Mode Toggle:** The header in both templates contains a theme toggle button (`#theme-toggle-btn`) that switches state between Light and Dark modes, toggling between Sun and Moon SVG graphics. Theme preferences are persisted via `localStorage` and dynamically re-render SVG knowledge graph elements.
- **Dual Color Palettes:**
  - **Dark Mode (Default):** Neutral slate background (`#0f172a`), card surfaces (`#1e293b`, `#334155`), blue accents (`#38bdf8`, `#0284c7`), and clear text hierarchy (`#94a3b8`, `#f8fafc`).
  - **Light Mode:** Slate background (`#f8fafc`), white card surfaces (`#ffffff`, `#f1f5f9`), blue accents (`#0284c7`, `#0369a1`), and dark text hierarchy (`#475569`, `#0f172a`).
- **Typography:** Standard system sans-serif stack (`system-ui, -apple-system, Segoe UI, Roboto, sans-serif`).
- **Visual Hierarchy:** Visual hierarchy is communicated using typography, geometric SVG indicators, color badges, sequence numbers (`#1..#N` in Presentation Mode), and status labels.
- **Responsive Layout:** CSS Grid and Flexbox layouts adapt across full-width monitors, split-screen views, and mobile viewports.
