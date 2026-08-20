# Canvas UI and Interactive Visualizations Guide

This document outlines the architecture, design principles, and data contracts for rendering interactive Canvas UI dashboards in agent harnesses such as Gemini Enterprise App, Spark, and web-based artifact runtimes.

---

## 1. Canvas UI Architecture

Modern enterprise agent harnesses render dynamic user interfaces by executing self-contained HTML, CSS, and JavaScript inside a secure, sandboxed `<iframe>`. 

### Key Runtime Characteristics:
- **Zero-Dependency Self-Containment:** All styles (CSS) and logic (JavaScript) are embedded directly within a single `.html` document or code block. This avoids network timeouts, blocked external CDN requests, and version conflicts.
- **Client-Side Interactivity:** Supports full DOM manipulation, SVG/Canvas graphical rendering, tab switching, search filtering, and clipboard interactions.
- **Sandboxed Execution:** Scripts execute within standard iframe security constraints (`allow-scripts`, isolated local storage, no parent window cross-origin access).

---

## 2. Core Dashboard Components

The meeting intelligence dashboard comprises four primary interface modules:

### 2.1 Executive Overview & KPI Metrics
- **Metric Badges:** High-level counts for decisions made, topics analyzed, assigned action items, and target milestone dates.
- **Executive Summary Card:** Structured cards displaying Meeting Objectives, Approved Decisions, Strategic Impacts, and Critical Risks.
- **Five-Sentence Brief Card:** Standalone block with one-click clipboard copy functionality.

### 2.2 Interactive Topic Knowledge Graph
- **Visual Topology:** An interactive SVG node-link graph representing the central meeting objective, radiating outwards to distinct topic clusters, decision nodes, and technical rationale sub-nodes.
- **Dynamic Interaction:**
  - Clicking any node opens a slide-out Detail Inspector drawer.
  - Hover states reveal concise contextual tooltips.
  - Instant search input to filter and highlight matching nodes in real time.
- **Content Depth:** The inspector displays the full Context, In-Depth Technical Mechanism, the Rationale / Debates ("Why"), and Key Conclusions.

### 2.3 Action Items Visualizer (Multi-View)
Rather than a static table, the dashboard delivers three switchable visual representations of the action items:
1. **Gantt / Timeline View:** A chronological milestone bar chart mapping deliverables against deadlines from kickoff to cutover, with progress indicators and owner tags.
2. **Kanban by Owner Board:** Columns organized per participant (plus an `Unassigned` column for backlog tasks), presenting deliverables as actionable cards.
3. **Structured Interactive Table:** A data table with column sorting, keyword search, owner filtering, and CSV/Markdown export.

### 2.4 Detailed Narrative Discussion Explorer
- Collapsible topic accordions allowing deep reading of the complete meeting record with technical explanations preserved in full.

---

## 3. Dashboard Data Contract (JSON Schema)

The dashboard template is driven by a structured JavaScript object embedded in the document. Agents populate this object directly when generating a Canvas UI:

```json
{
  "meetingTitle": "string",
  "date": "YYYY-MM-DD",
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
  "fiveSentenceSummary": "string",
  "topics": [
    {
      "id": "topic-1",
      "title": "string",
      "context": "string",
      "explanation": "string",
      "rationale": "string",
      "conclusion": "string"
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

---

## 4. Design and Styling Standards

- **Color Palette:** High-contrast neutral slate background (`#0f172a`), clean card surfaces (`#1e293b`, `#334155`), cool blue accents (`#38bdf8`, `#0284c7`), and muted text hierarchy (`#94a3b8`, `#f8fafc`).
- **Typography:** Standard system sans-serif stack (`system-ui, -apple-system, Segoe UI, Roboto, sans-serif`).
- **No Decorative Emojis or Icons:** Visual hierarchy is communicated using geometric SVG glyphs, color badges, and clean typography tags (e.g. `[Pending]`, `[Assigned]`, `[Decision]`).
- **Responsive Layout:** CSS Grid and Flexbox layouts adapt seamlessly across full-width monitors, split-screen views, and mobile viewports.
