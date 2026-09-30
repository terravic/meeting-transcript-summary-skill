# Product Requirements Document (PRD): Meeting and Presentation Transcript Summary Skill

## 1. Overview and Objective

The `meeting-transcript-summary` skill is a standardized instruction and template package that transforms raw meeting or presentation transcripts into structured, grounded documentation and mode-specific interactive HTML dashboards.

Collaborative meetings and single-speaker presentations have distinct structural requirements:
- **Interactive Meetings** involve multi-participant debates, trade-offs, decisions, and task assignments that require logical topic synthesis and action item tracking.
- **Presentations** involve one or more presenters speaking sequentially (typically walking through slides or live demonstrations) without participant debate or task assignment, requiring a chronological record of what was presented and said.

This project provides a single unified skill supporting both **Meeting Mode** and **Presentation Mode**, enforcing explicit mode selection whenever a user provides a transcript without specifying a mode.

---

## 2. Supported Processing Modes

### 2.1 Mode 1: Meeting Mode (`meeting mode`)
- **Target Input:** Transcripts from collaborative meetings with back-and-forth participant discussions.
- **Markdown Deliverable (Three-Part Structure):**
  1. **Document Header:** Meeting Title, Date (`YYYY-MM-DD`, defaulting to the current execution date if unstated in the transcript), and Participants list.
  2. **Section 1 — Executive Summary:** Meeting Objective, Key Decisions Made, Strategic Outcomes and Impact, and Critical Risks and Blockers.
  3. **Section 2 — Detailed Discussion Record and Action Items:** Narrative record grouped by logical topic (capturing Discussion Details of what was said, Points Raised and Rationale, and Key Conclusions), followed by a four-column Action Items table (`Action Item`, `Assigned To`, `Deadline`, `Acceptance Criteria / Target Deliverable`).
  4. **Section 3 — Five-Sentence Summary:** A single paragraph containing strictly five grammatically complete sentences summarizing the meeting purpose, core challenge, primary decision, secondary outcome, and immediate next milestone.
- **Interactive Web Dashboard (`templates/meeting_dashboard_template.html`):**
  - Four-tab interface: `Executive Brief` (default active tab with summary metrics and cards), `Knowledge Graph` (SVG topic node-link topology and slide-out inspector), `Action Items` (Kanban by Owner board and filterable data table with CSV/Markdown export), and `Detailed Record` (collapsible topic accordions).

### 2.2 Mode 2: Presentation Mode (`presentation mode`)
- **Target Input:** Transcripts from presentations, keynotes, lectures, briefings, or demonstrations where presenters speak sequentially without back-and-forth meeting debate.
- **Markdown Deliverable (Chronological Structure Only):**
  1. **Document Header:** Presentation Title (`# Presentation Summary: [Title]`), Date (`YYYY-MM-DD`, defaulting to the current execution date if unstated), and `Presenter(s)`.
  2. **Chronological Presentation Summary:** Sequential, numbered segments (`### 1. [Segment Title]`, `### 2. [Segment Title]`, ...) following the exact start-to-finish chronological progression of the talk track, slides, and demonstrations. Records the presenter name and a detailed description and summarization of what was said, including spoken references to slide visuals, charts, architectures, and metrics.
  3. **Omitted Sections:** Explicitly omits the Executive Summary, Action Items table, and Five-Sentence Summary.
- **Interactive Web Dashboard (`templates/presentation_dashboard_template.html`):**
  - Two-tab interface tailored for presentations:
    1. `Presentation Knowledge Graph` (default active tab on load): Visualizes the central `PRESENTATION CORE THEME` node connected to numbered chronological segment nodes (`#1` through `#N`) with directed edges representing sequential slide progression and conceptual links, paired with a slide-out Segment Inspector drawer (`What Was Presented & Said`, `Slide Visuals, Demos & Metrics Cited`, and `Stated Key Takeaway`).
    2. `Chronological Walkthrough`: Sequential numbered timeline accordions (`#1` through `#N`) with Expand/Collapse controls and one-click Markdown export.

---

## 3. Functional Requirements

### 3.1 Mandatory Mode Selection Gate
- **Explicit Mode Invocation:** If the user specifies `"meeting mode"` or `"presentation mode"` when invoking the skill (either alongside the transcript or in a subsequent message), the agent executes the specified mode directly.
- **Unspecified Mode Handling:** If the user invokes the skill and provides transcript text or a file path without specifying which mode to use, the agent **must not assume a default mode**. It must prompt the user to select between `Meeting Mode` and `Presentation Mode` (using the interactive question tool when supported, or a direct text prompt) and wait for confirmation before generating output.
- **Missing Transcript Handling:** If the user invokes the skill without providing transcript text or a valid file path, the agent prompts the user to provide the transcript input and terminates.

### 3.2 Transcript Ingestion and Normalization
- **Supported Formats:** Plain text dialogue blocks, WebVTT (`.vtt`), SubRip (`.srt`), segmented timestamp exports, and inline diarized transcripts as documented in [references/transcript_formats.md](references/transcript_formats.md).
- **Preprocessing Utility:** [scripts/clean_transcript.py](scripts/clean_transcript.py) strips caption headers, cue indices, and timestamp markers while consolidating consecutive utterances by the same speaker.
- **Metadata Fallbacks:**
  - Unstated meeting or presentation date defaults to the current date when the skill processes the transcript (`YYYY-MM-DD`).
  - Unstated action item owners in Meeting Mode are recorded as `Unassigned`.
  - Unstated action item deadlines in Meeting Mode are recorded as `Not Specified`.

### 3.3 Factual Grounding and Content Constraints
- **Zero Hallucination:** Every fact, metric, name, decision, slide reference, and takeaway must originate directly from the source transcript.
- **No External Explanations:** The output must only report what speakers articulated during the session. It must never inject external definitions, tutorials, or background commentary on concepts or tools mentioned.
- **Zero Preamble or Postamble:** Once the mode is selected, output starts immediately with the Markdown header and ends immediately after the final section.

### 3.4 Output Delivery Formats
Both processing modes support four delivery formats:
1. **Rendered Markdown (Default):** Standard Markdown emitted directly to the response stream.
2. **Raw Markdown Code Block:** Complete output wrapped in a fenced ` ```markdown ` block.
3. **Dual Output Mode:** Rendered Markdown followed by a divider and a fenced raw Markdown code block.
4. **Interactive Web Dashboard Mode:** Self-contained HTML/CSS/JavaScript document emitted as a user-facing artifact named `dashboard.html` (`UserFacing: true`, `Summary: "Interactive Evaluation Dashboard"`, `RequestFeedback: false`).

---

## 4. Technical Architecture and Repository Structure

All project files use relative paths originating from the repository root:

```text
meeting-transcript-summary-skill/
├── SKILL.md                                        # Core skill definition and mode workflows
├── prd.md                                          # Product Requirements Document
├── README.md                                       # User guide, architecture, and integration documentation
├── LICENSE                                         # Apache 2.0 License
├── assets/
│   ├── skill_workflow_diagram.png                  # System workflow diagram covering both modes
│   ├── dashboard_executive_brief.png               # Meeting Mode Executive Brief view
│   ├── dashboard_knowledge_graph.png               # Meeting Mode Topic Knowledge Graph view
│   ├── dashboard_action_items.png                  # Meeting Mode Action Items Kanban view
│   └── dashboard_presentation_knowledge_graph.png  # Presentation Mode Knowledge Graph view
├── templates/
│   ├── meeting_dashboard_template.html             # Self-contained 4-tab Meeting Mode dashboard template
│   └── presentation_dashboard_template.html        # Self-contained 2-tab Presentation Mode dashboard template
├── references/
│   ├── dashboard_ui_guide.md                       # UI architecture and JSON data schemas for both modes
│   ├── transcript_formats.md                       # Supported caption/transcript formats and parsing rules
│   └── quality_checklist.md                        # Verification rubric for Meeting and Presentation modes
├── examples/
│   ├── sample_meeting_transcript.txt               # Synthetic multi-participant meeting transcript
│   ├── sample_output_summary.md                    # Reference 3-part output for Meeting Mode
│   ├── sample_meeting_dashboard.html               # Working interactive dashboard for Meeting Mode
│   ├── sample_presentation_transcript.txt          # Synthetic single-presenter keynote transcript
│   ├── sample_presentation_summary.md              # Reference chronological output for Presentation Mode
│   └── sample_presentation_dashboard.html          # Working interactive dashboard for Presentation Mode
└── scripts/
    └── clean_transcript.py                         # Python CLI utility to normalize .vtt, .srt, and .txt files
```

---

## 5. Verification and Acceptance Criteria

All outputs generated by the skill are verified against [references/quality_checklist.md](references/quality_checklist.md):
1. **Mode Confirmation:** When invoked without an explicit mode, the agent prompts the user to select `Meeting Mode` or `Presentation Mode` prior to processing.
2. **Meeting Mode Structural Accuracy:** Contains the Header, Section 1 (Executive Summary), Section 2 (Logical Topic Record + 4-Column Action Items Table), and Section 3 (strictly 5 sentences).
3. **Presentation Mode Structural Accuracy:** Contains only the Presentation Header and numbered `Chronological Presentation Summary` segments (`1..N`), with zero Executive Summary, Action Items table, or 5-Sentence Summary.
4. **Dashboard Mode Alignment:** Meeting Mode dashboards use `templates/meeting_dashboard_template.html`; Presentation Mode dashboards use `templates/presentation_dashboard_template.html` and open directly to the `Presentation Knowledge Graph` tab.
5. **Strict Grounding:** Zero fabricated metrics, unmentioned concepts, or external explanations.
