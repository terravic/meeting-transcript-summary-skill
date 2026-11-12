# Product Requirements Document (PRD): Meeting and Presentation Transcript Summary Skill

## 1. Overview and Objective

The `meeting-transcript-summary` skill is a standardized instruction and template package that transforms raw meeting or presentation transcripts into concise, scannable, structured documentation and mode-specific interactive HTML dashboards.

Collaborative meetings and single-speaker presentations have distinct structural requirements:
- **Interactive Meetings** involve multi-participant debates, trade-offs, decisions, and task assignments that require logical topic synthesis and action item tracking.
- **Presentations** involve one or more presenters speaking sequentially (typically walking through slides or live demonstrations) without participant debate or task assignment, requiring a chronological, bullet-first record of what was presented.

This project provides a single unified skill supporting both **Meeting Mode** and **Presentation Mode**. It runs in a single turn when a transcript is pasted: it defaults to **Meeting Mode** (`"meeting"`), **No Dashboard** (`"no dashboard"`), and **No Target User Name** (`"none"`), switching to Presentation Mode, building the interactive HTML dashboard, or adding user-specific action items only when explicitly requested in the prompt. Compression guardrails ensure generated summaries remain strictly shorter than the source transcript without dropping concrete facts, metrics, decisions, or action items.

---

## 2. Supported Processing Modes

### 2.1 Mode 1: Meeting Mode (`meeting mode` - Default)
- **Activation:** Used by default whenever Presentation Mode is not explicitly specified in the prompt.
- **Target Input:** Transcripts from collaborative meetings with back-and-forth participant discussions.
- **Markdown Deliverable (Three-Part Core Structure + Optional Fourth Section):**
  1. **Document Header:** Meeting Title, Date (`YYYY-MM-DD`, defaulting to the current execution date if unstated in the transcript), and Participants list.
  2. **Section 1 - Executive Summary:** Scannable overview (`~70-130 words`) with a 1-sentence Meeting Objective (`<= 25 words`) and direct 1-line bullets (`<= 18 words/bullet`) for Key Decisions Made, Strategic Outcomes and Impact, and Critical Risks and Blockers.
  3. **Section 2 - Detailed Discussion Record and Action Items:** Bullet-first record grouped by logical topic (`Key Points`, conditional `Trade-offs & Rationale` only when alternatives were weighed, and a 1-line `Decision / Status`) with zero "he said / she said" attribution, followed by a concise 4-column Action Items table (`Action Item`, `Assigned To`, `Deadline`, `Acceptance Criteria / Target Deliverable`; `<= 15 words/cell`).
  4. **Section 3 - Five-Sentence Summary:** A single paragraph containing strictly five direct, grammatically complete sentences (`<= 18-20 words/sentence`, `~65-95 words` total) summarizing meeting purpose, core challenge, primary decision, secondary outcome/requirement, and immediate next milestone.
  5. **Section 4 - Action Items for [User Name] (Optional - Default: `none`; Included Only When User Name Is Specified):** A brief paragraph (`<= 75 words`, 1-3 sentences) appended after Section 3 combining the specific action items assigned to a given user with required deliverables and stated deadlines. If no user name is specified when invoking the skill, Section 4 is omitted.
- **Interactive Web Dashboard (`templates/meeting_dashboard_template.html` - Default: `no dashboard`; Built Only When Explicitly Requested):**
  - Self-contained offline-capable HTML5 document with four tabs: `Executive Brief` (default active tab with summary KPIs, SVG benchmark chart, coverage heatmap, and summary bento grid), `Interactive Relationship Node Map` (SVG topic topology and slide-out inspector), `Action Items` (monospace table and flat owner lanes with CSV/Markdown export), and `Discussion Record` (collapsible topic rows), populated with concise, zero-attribution copy.

### 2.2 Mode 2: Presentation Mode (`presentation mode` - Explicit Override Only)
- **Activation:** Activated **only** when the user explicitly sets the mode to presentation in the prompt (e.g., `"presentation mode"`, `"mode: presentation"`, `"in presentation mode"`).
- **Target Input:** Transcripts from presentations, keynotes, lectures, briefings, or demonstrations where presenters speak sequentially without back-and-forth meeting debate.
- **Markdown Deliverable (Chronological Structure Only):**
  1. **Document Header:** Presentation Title (`# Presentation Summary: [Title]`), Date (`YYYY-MM-DD`, defaulting to the current execution date if unstated), and `Presenter(s)`.
  2. **Chronological Presentation Summary:** Sequential, numbered segments (`### 1. [Segment Title]`, `### 2. [Segment Title]`, ...) following the exact start-to-finish chronological progression of the talk track, slides, and demonstrations. Uses 3-5 fact-dense bullets per segment (`<= 22 words/bullet`) with inline slide/visual citations and zero `"presenter explained/noted"` narration; includes `- **Presenter:**` per segment only when multiple presenters alternate.
  3. **Omitted Sections:** Explicitly omits the Executive Summary, Action Items table, Five-Sentence Summary, and User-Specific Action Items section.
- **Interactive Web Dashboard (`templates/presentation_dashboard_template.html` - Default: `no dashboard`; Built Only When Explicitly Requested):**
  - Self-contained offline-capable HTML5 document with two tabs tailored for presentations:
    1. `Interactive Relationship Node Map` (default active tab on load): Visualizes the central `CORE THEME` node connected to numbered chronological segment nodes (`#1` through `#N`) with directed edges representing sequential slide progression and conceptual links, paired with a slide-out Segment Inspector drawer (`What Was Presented & Said`, `Slide Visuals, Demos & Metrics Cited`, and `Stated Key Takeaway`).
    2. `Chronological Walkthrough`: Sequential numbered timeline accordions (`#01` through `#0N`) with Expand/Collapse controls and one-click Markdown export.

---

## 3. Functional Requirements

### 3.1 Execution Parameters and Default-Driven Single-Turn Resolution
- **Execution Parameters and Defaults:**
  1. **Processing Mode (Default: `"meeting"`):** Defaults to **Meeting Mode** (`"meeting"`). Switches to **Presentation Mode** (`"presentation"`) **only** when explicitly specified in the prompt (e.g., `"presentation mode"`, `"mode: presentation"`, `"in presentation mode"`).
  2. **UI Dashboard Flag (Default: `"no dashboard"`):** Defaults to **No Dashboard** (Markdown summary only). Builds and writes `dashboard.html` **only** when the user explicitly adds a dashboard request to the prompt (e.g., `"yes dashboard"`, `"build dashboard"`, `"create dashboard"`, `"with dashboard"`).
  3. **User Name (Default: `"none"` - Meeting Mode Only):** Defaults to **None** (omits Section 4). When a target participant/user name is explicitly specified in the prompt in Meeting Mode (e.g., `"for user Marcus Vance"`, `"for Marcus"`), triggers generation of `Section 4: Action Items for [User Name]` after Section 3.
- **Immediate Single-Turn Execution:** Whenever the user invokes the skill and provides transcript text or a valid file path, unspecified parameters resolve to their defaults (`mode = meeting`, `dashboard = no dashboard`, `user = none`) and execution completes in a single turn without asking clarifying questions.
- **Missing Transcript Handling:** If the skill is invoked without transcript text or a valid file path, prompt once for the transcript input and terminate.

### 3.2 Transcript Ingestion and Normalization
- **Supported Formats:** Plain text dialogue blocks, WebVTT (`.vtt`), SubRip (`.srt`), segmented timestamp exports, and inline diarized transcripts as documented in [references/transcript_formats.md](references/transcript_formats.md).
- **Preprocessing Utility:** [scripts/clean_transcript.py](scripts/clean_transcript.py) strips caption headers, cue indices, and timestamp markers while consolidating consecutive utterances by the same speaker.
- **Metadata Fallbacks:**
  - Unstated meeting or presentation date defaults to the current date when the skill processes the transcript (`YYYY-MM-DD`).
  - Unstated action item owners in Meeting Mode are recorded as `Unassigned`.
  - Unstated action item deadlines in Meeting Mode are recorded as `Not Specified`.

### 3.3 Factual Grounding, Conciseness, and Content Constraints
- **Anti-Bloat Compression Guardrails:** Generated summaries must always be strictly shorter than the cleaned source transcript (targeting **40%-65%** with `< 80%` Meeting / `<= 60%` Presentation ceiling for `< 1,500`-word dense transcripts, **25%-50%** for `1,500-3,000` words, and **10%-25%** / generally `<= 1,200-1,500 words` for long sessions) while retaining 100% of concrete facts, metrics, technical specs, decisions, and action items.
- **Fact-First Synthesis (Zero "He Said / She Said"):** Synthesize directly by topic, fact, and outcome using direct scannable bullets -- never narrate speaker turns (`"X said"`, `"Y noted"`, `"he explained"`). Restrict personal names strictly to header lists, Action Items `Assigned To` / Section 4, multi-presenter transitions, or material sign-off gates/unresolved disagreements.
- **Zero Cross-Section Duplication:** State each technical spec and metric once without repeating details across Executive Summary, Section 2 sub-bullets, and Action Items deliverable cells.
- **Zero Hallucination:** Every fact, metric, name, decision, slide reference, and takeaway must originate directly from the source transcript.
- **No External Explanations:** The output must only report what speakers articulated during the session without injecting external definitions, tutorials, or background commentary.
- **Zero Preamble or Postamble:** Output starts immediately with the Markdown header and ends immediately after the final section.

### 3.4 Output Delivery Formats and Visual Design Standards
Both processing modes support four delivery formats:
1. **Rendered Markdown (Default):** Standard Markdown emitted directly to the response stream.
2. **Raw Markdown Code Block:** Complete output wrapped in a fenced ` ```markdown ` block.
3. **Dual Output Mode:** Rendered Markdown followed by a divider and a fenced raw Markdown code block.
4. **Interactive Web Dashboard Mode (Default: `no dashboard`; Built Only When Explicitly Requested):** Standalone, offline-capable HTML/CSS/JavaScript document written to `dashboard.html` in accordance with [DESIGN.md](DESIGN.md) and [references/dashboard_ui_guide.md](references/dashboard_ui_guide.md). Dashboards use native system typography (`system-ui, sans-serif` and `ui-monospace, monospace`), flat solid light/dark themes with a plain-text `Light` / `Dark` switcher, and a 5-color semantic visualization palette without external stylesheet dependencies.

---

## 4. Technical Architecture and Repository Structure

All project files use relative paths originating from the repository root:

```text
meeting-transcript-summary-skill/
|-- SKILL.md                                        # Core skill definition and mode workflows
|-- DESIGN.md                                       # Visual, theme, and technical dashboard design specification
|-- prd.md                                          # Product Requirements Document
|-- README.md                                       # End-user guide, architecture, and integration documentation
|-- LICENSE                                         # Apache 2.0 License
|-- dashboard.html                                  # Top-level working interactive Meeting Mode dashboard
|-- assets/
|   |-- skill_workflow_diagram.png                  # System workflow diagram covering both modes
|   |-- user_interaction_diagram.png                # Execution parameters and user-specific Section 4 diagram
|   |-- dashboard_executive_brief.png               # Meeting Mode Executive Brief view
|   |-- dashboard_knowledge_graph.png               # Meeting Mode Interactive Relationship Node Map view
|   |-- dashboard_action_items.png                  # Meeting Mode Action Items view
|   `-- dashboard_presentation_knowledge_graph.png  # Presentation Mode Relationship Node Map view
|-- templates/
|   |-- meeting_dashboard_template.html             # Self-contained 4-tab Meeting Mode dashboard template
|   `-- presentation_dashboard_template.html        # Self-contained 2-tab Presentation Mode dashboard template
|-- references/
|   |-- dashboard_ui_guide.md                       # UI architecture and JSON data schemas for both modes
|   |-- transcript_formats.md                       # Supported caption/transcript formats and parsing rules
|   `-- quality_checklist.md                        # Verification rubric for Meeting and Presentation modes
|-- examples/
|   |-- sample_meeting_transcript.txt               # Synthetic multi-participant meeting transcript
|   |-- sample_output_summary.md                    # Reference output for Meeting Mode (including optional Section 4)
|   |-- sample_meeting_dashboard.html               # Working interactive dashboard example for Meeting Mode
|   |-- sample_presentation_transcript.txt          # Synthetic single-presenter keynote transcript
|   |-- sample_presentation_summary.md              # Reference chronological output for Presentation Mode
|   `-- sample_presentation_dashboard.html          # Working interactive dashboard example for Presentation Mode
`-- scripts/
    `-- clean_transcript.py                         # Python CLI utility to normalize .vtt, .srt, and .txt files
```

---

## 5. Verification and Acceptance Criteria

All outputs generated by the skill are verified against [references/quality_checklist.md](references/quality_checklist.md) and [DESIGN.md](DESIGN.md):
1. **Default Parameter Resolution and Explicit Overrides (Single-Turn Execution):** When invoked with a transcript, execution completes in a single turn without prompting for parameters -- defaulting to `Meeting Mode` (`"meeting"`), `No Dashboard` (`"no dashboard"`), and `User Name = none`, and switching to `Presentation Mode`, building `dashboard.html`, or adding Section 4 only when explicitly requested in the prompt.
2. **Anti-Bloat Compression and Zero Attribution Narration:** Total summary prose word count is strictly shorter than the cleaned source transcript (**40%-65%** target and `< 80%` Meeting / `<= 60%` Presentation ceiling for `< 1,500`-word dense transcripts; **25%-50%** for `1,500-3,000` words; **10%-25%** / generally `<= 1,200-1,500` words for `> 3,000` words) with zero "he said / she said" narration and zero cross-section duplication.
3. **Meeting Mode Structural Accuracy:** Contains the Header, Section 1 (scannable Executive Summary `~70-130 words`), Section 2 (bullet-first Logical Topic Record + 4-Column Action Items Table), Section 3 (strictly 5 complete sentences), and -- if and only if a user name was specified in the prompt -- Section 4 (`Action Items for [User Name]`, formatted as a brief paragraph `<= 75 words`).
4. **Presentation Mode Structural Accuracy:** Contains only the Presentation Header and numbered `Chronological Presentation Summary` segments (`1..N`) formatted as direct, fact-dense bullets (omitting per-segment `Presenter:` tags for single-presenter talks), with zero Executive Summary, Action Items table, 5-Sentence Summary, or User-Specific Action Items section.
5. **Dashboard Mode and Design Compliance:** Meeting Mode dashboards use `templates/meeting_dashboard_template.html`; Presentation Mode dashboards use `templates/presentation_dashboard_template.html` and open directly to the `Interactive Relationship Node Map` tab. Both are standalone HTML5 files with zero external network dependencies, a plain-text `Light` / `Dark` switcher, and concise, zero-attribution JSON copy.
6. **Strict Grounding:** Zero fabricated metrics, unmentioned concepts, or external explanations, while preserving 100% of substantive facts, numbers, and decisions.
