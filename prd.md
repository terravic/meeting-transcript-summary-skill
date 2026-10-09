# Product Requirements Document (PRD): Meeting and Presentation Transcript Summary Skill

## 1. Overview and Objective

The `meeting-transcript-summary` skill is a standardized instruction and template package that transforms raw meeting or presentation transcripts into structured, grounded documentation and mode-specific interactive HTML dashboards.

Collaborative meetings and single-speaker presentations have distinct structural requirements:
- **Interactive Meetings** involve multi-participant debates, trade-offs, decisions, and task assignments that require logical topic synthesis and action item tracking.
- **Presentations** involve one or more presenters speaking sequentially (typically walking through slides or live demonstrations) without participant debate or task assignment, requiring a chronological record of what was presented and said.

This project provides a single unified skill supporting both **Meeting Mode** and **Presentation Mode**. It is designed for immediate, single-turn execution when a transcript is pasted: it defaults to **Meeting Mode** (`"meeting"`), **No Dashboard** (`"no dashboard"`), and **No Target User Name** (`"none"`), switching to Presentation Mode, building the interactive UI dashboard, or adding user-specific action items only when explicitly requested in the prompt.

---

## 2. Supported Processing Modes

### 2.1 Mode 1: Meeting Mode (`meeting mode` - Default)
- **Activation:** Used by default whenever Presentation Mode is not explicitly specified in the prompt.
- **Target Input:** Transcripts from collaborative meetings with back-and-forth participant discussions.
- **Markdown Deliverable (Three-Part Core Structure + Optional Fourth Section):**
  1. **Document Header:** Meeting Title, Date (`YYYY-MM-DD`, defaulting to the current execution date if unstated in the transcript), and Participants list.
  2. **Section 1 - Executive Summary:** Meeting Objective, Key Decisions Made, Strategic Outcomes and Impact, and Critical Risks and Blockers.
  3. **Section 2 - Detailed Discussion Record and Action Items:** Narrative record grouped by logical topic (capturing Discussion Details of what was said, Points Raised and Rationale, and Key Conclusions), followed by a four-column Action Items table (`Action Item`, `Assigned To`, `Deadline`, `Acceptance Criteria / Target Deliverable`).
  4. **Section 3 - Five-Sentence Summary:** A single paragraph containing strictly five grammatically complete sentences summarizing the meeting purpose, core challenge, primary decision, secondary outcome, and immediate next milestone.
  5. **Section 4 - Action Items for [User Name] (Optional - Default: `none`; Included Only When User Name Is Specified):** A brief paragraph appended after Section 3 combining the specific action items assigned to a given user with a concise description of what needs to be done, relevant discussion context, deliverables, and stated deadlines. If the user does not specify a user name when invoking the skill, Section 4 is omitted.
- **Interactive Web Dashboard (`templates/meeting_dashboard_template.html` - Default: `no dashboard`; Built Only When Explicitly Requested):**
  - Four-tab interface: `Executive Brief` (default active tab with summary metrics and cards), `Knowledge Graph` (SVG topic node-link topology and slide-out inspector), `Action Items` (Kanban by Owner board and filterable data table with CSV/Markdown export), and `Detailed Record` (collapsible topic accordions).

### 2.2 Mode 2: Presentation Mode (`presentation mode` - Explicit Override Only)
- **Activation:** Activated **only** when the user explicitly sets the mode to presentation in the prompt (e.g., `"presentation mode"`, `"mode: presentation"`, `"in presentation mode"`).
- **Target Input:** Transcripts from presentations, keynotes, lectures, briefings, or demonstrations where presenters speak sequentially without back-and-forth meeting debate.
- **Markdown Deliverable (Chronological Structure Only):**
  1. **Document Header:** Presentation Title (`# Presentation Summary: [Title]`), Date (`YYYY-MM-DD`, defaulting to the current execution date if unstated), and `Presenter(s)`.
  2. **Chronological Presentation Summary:** Sequential, numbered segments (`### 1. [Segment Title]`, `### 2. [Segment Title]`, ...) following the exact start-to-finish chronological progression of the talk track, slides, and demonstrations. Records the presenter name and a detailed description and summarization of what was said, including spoken references to slide visuals, charts, architectures, and metrics.
  3. **Omitted Sections:** Explicitly omits the Executive Summary, Action Items table, Five-Sentence Summary, and User-Specific Action Items section.
- **Interactive Web Dashboard (`templates/presentation_dashboard_template.html` - Default: `no dashboard`; Built Only When Explicitly Requested):**
  - Two-tab interface tailored for presentations:
    1. `Presentation Knowledge Graph` (default active tab on load): Visualizes the central `PRESENTATION CORE THEME` node connected to numbered chronological segment nodes (`#1` through `#N`) with directed edges representing sequential slide progression and conceptual links, paired with a slide-out Segment Inspector drawer (`What Was Presented & Said`, `Slide Visuals, Demos & Metrics Cited`, and `Stated Key Takeaway`).
    2. `Chronological Walkthrough`: Sequential numbered timeline accordions (`#1` through `#N`) with Expand/Collapse controls and one-click Markdown export.

---

## 3. Functional Requirements

### 3.1 Execution Parameters and Default-Driven Single-Turn Resolution
- **Execution Parameters and Defaults:**
  1. **Processing Mode (Default: `"meeting"`):** Defaults to **Meeting Mode** (`"meeting"`). Switches to **Presentation Mode** (`"presentation"`) **only** when explicitly specified in the prompt (e.g., `"presentation mode"`, `"mode: presentation"`, `"in presentation mode"`).
  2. **UI Dashboard Flag (Default: `"no dashboard"`):** Defaults to **No Dashboard** (Markdown summary only). Builds and emits the interactive UI dashboard (`dashboard.html`) **only** when the user explicitly adds a dashboard request to the prompt (e.g., `"yes dashboard"`, `"build dashboard"`, `"create dashboard"`, `"with dashboard"`).
  3. **User Name (Default: `"none"` - Meeting Mode Only):** Defaults to **None** (omits Section 4). When a target participant/user name is explicitly specified in the prompt in Meeting Mode (e.g., `"for user Marcus Vance"`, `"for Marcus"`), triggers generation of `Section 4: Action Items for [User Name]` after Section 3.
- **Immediate Single-Turn Execution:** Whenever the user invokes the skill and provides transcript text or a valid file path, the agent resolves any unspecified parameters to their defaults (`mode = meeting`, `dashboard = no dashboard`, `user = none`) and executes immediately in a single turn. The agent **must not pause or ask clarifying questions** for mode, dashboard preference, or user name.
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
- **Zero Preamble or Postamble:** Output starts immediately with the Markdown header and ends immediately after the final section.

### 3.4 Output Delivery Formats
Both processing modes support four delivery formats:
1. **Rendered Markdown (Default):** Standard Markdown emitted directly to the response stream.
2. **Raw Markdown Code Block:** Complete output wrapped in a fenced ` ```markdown ` block.
3. **Dual Output Mode:** Rendered Markdown followed by a divider and a fenced raw Markdown code block.
4. **Interactive Web Dashboard Mode (Default: `no dashboard`; Built Only When Explicitly Requested):** Self-contained HTML/CSS/JavaScript document emitted upon completion (only when explicitly requested via phrases such as `"yes dashboard"` or `"build dashboard"`) as a user-facing artifact named `dashboard.html` (`UserFacing: true`, `Summary: "Interactive Evaluation Dashboard"`, `RequestFeedback: false`).

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
│   ├── user_interaction_diagram.png                # Execution parameters & user-specific Section 4 flow diagram
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
│   ├── sample_output_summary.md                    # Reference output for Meeting Mode (including optional Section 4)
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
1. **Default Parameter Resolution and Explicit Overrides (Single-Turn Execution):** When invoked with a transcript, the agent executes immediately in a single turn without prompting for parameters-defaulting to `Meeting Mode` (`"meeting"`), `No Dashboard` (`"no dashboard"`), and `User Name = none`, and switching to `Presentation Mode`, building `dashboard.html`, or adding Section 4 only when explicitly requested in the prompt.
2. **Meeting Mode Structural Accuracy:** Contains the Header, Section 1 (Executive Summary), Section 2 (Logical Topic Record + 4-Column Action Items Table), Section 3 (strictly 5 sentences), and-if and only if a user name was specified in the prompt-Section 4 (`Action Items for [User Name]`, formatted as a brief paragraph combining the user's assigned action items with a description of what needs to be done).
3. **Presentation Mode Structural Accuracy:** Contains only the Presentation Header and numbered `Chronological Presentation Summary` segments (`1..N`), with zero Executive Summary, Action Items table, 5-Sentence Summary, or User-Specific Action Items section.
4. **Dashboard Mode Alignment:** Meeting Mode dashboards use `templates/meeting_dashboard_template.html`; Presentation Mode dashboards use `templates/presentation_dashboard_template.html` and open directly to the `Presentation Knowledge Graph` tab.
5. **Strict Grounding:** Zero fabricated metrics, unmentioned concepts, or external explanations.
