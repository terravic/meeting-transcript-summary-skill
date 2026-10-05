# Meeting and Presentation Transcript Summary Skill

A standardized agent skill for extracting structured, grounded summaries and interactive visual dashboards from raw meeting or presentation transcripts. Compatible with agent platforms, assistant environments, and standalone LLM agent harnesses.

---

## Overview

Generic transcript summaries often reduce spoken content to brief bullet points, losing the technical context, quantitative metrics, and rationale behind decisions. Furthermore, collaborative meetings and single-speaker presentations require distinct summary structures.

This single unified skill (`meeting-transcript-summary`) supports **two selectable processing modes** and **always prompts the user upfront to specify the processing mode (`Meeting Mode` vs. `Presentation Mode`) and whether to create the interactive UI dashboard (`dashboard.html`) upon completion if either is not specified in the request** (along with an **optional** `user name` parameter in Meeting Mode that is never prompted for if omitted):

### Mode 1: Meeting Mode (`meeting mode`)
Designed for collaborative meetings with back-and-forth dialogue among participants. Produces a three-part core deliverable (plus a fourth user-specific section when a user name is provided) and an optional 4-tab Meeting Dashboard:
1. **Executive Summary:** Strategic briefing covering the primary objective, key decisions made, outcomes and impact, and critical blockers stated by participants.
2. **Detailed Discussion Record and Action Items:** A comprehensive narrative record organized by logical topic. Captures the specific details of what was said by participants, statements made, and the rationale (arguments exchanged, trade-offs evaluated, alternatives dismissed) without adding external explanations. Concludes with a four-column Action Items table.
3. **Five-Sentence Summary:** Exactly five complete, self-contained sentences providing a concise briefing of what was said and decided in the meeting.
4. **Action Items for [User Name] (Optional — Only When User Name Is Specified):** A brief paragraph placed after the Five-Sentence Summary combining the specific action items assigned to a given user with a concise description of what needs to be done, deliverables, and deadlines. If no user name is specified in the command, this fourth section is not created.
5. **Interactive Meeting Web Dashboard (when confirmed):** A 4-tab visual interface (`Executive Brief`, `Knowledge Graph`, `Action Items` Kanban/Table, and `Detailed Record`).

### Mode 2: Presentation Mode (`presentation mode`)
Designed for presentations, keynotes, lectures, webinars, or demonstrations where one or more presenters speak sequentially (often walking through slides) without back-and-forth meeting debate.
1. **Chronological Presentation Summary Only:** Outputs the presentation header (`Title`, `Date`, `Presenter(s)`) followed strictly by a numbered, start-to-finish **Chronological Description and Summarization** of what was presented and said (`1. [Segment Title]`, `2. [Segment Title]`, ...).
2. **Strict Omission of Meeting Sections:** Explicitly omits the Executive Summary, Action Items table, Five-Sentence Summary, and User-Specific Action Items section.
3. **Presentation Knowledge Graph Web Dashboard (when confirmed):** Opens **directly to the Interactive Presentation Knowledge Graph** (visualizing the central presentation theme, chronological progression `#1` through `#N`, conceptual links across slides/segments, and a slide-out Segment Inspector drawer) paired with a `Chronological Walkthrough` timeline tab.

Both modes operate under strict factual grounding rules: zero conversational filler, zero hallucination, and zero external topic explanations.

![Meeting and Presentation Transcript Summary Skill Workflow](assets/skill_workflow_diagram.png)

---

## Repository Structure

```text
meeting-transcript-summary-skill/
├── SKILL.md                                        # Primary agent instruction file supporting Meeting & Presentation modes
├── prd.md                                          # Product Requirements Document (PRD)
├── README.md                                       # End-user documentation and integration guides
├── LICENSE                                         # Apache 2.0 License
├── assets/
│   ├── skill_workflow_diagram.png                  # Architecture and workflow diagram
│   ├── user_interaction_diagram.png                # Execution parameters & user-specific Section 4 flow diagram
│   ├── dashboard_executive_brief.png               # Executive Brief screenshot (Meeting Mode)
│   ├── dashboard_knowledge_graph.png               # Topic Knowledge Graph screenshot (Meeting Mode)
│   ├── dashboard_action_items.png                  # Action Items Kanban screenshot (Meeting Mode)
│   └── dashboard_presentation_knowledge_graph.png  # Presentation Knowledge Graph screenshot (Presentation Mode)
├── templates/
│   ├── meeting_dashboard_template.html             # 4-tab interactive dashboard template for Meeting Mode
│   └── presentation_dashboard_template.html        # Knowledge Graph-focused dashboard template for Presentation Mode
├── references/
│   ├── dashboard_ui_guide.md                       # Guide for Meeting & Presentation interactive dashboards and data schemas
│   ├── transcript_formats.md                       # Reference guide for caption and transcript formats
│   └── quality_checklist.md                        # Verification rubric used to audit output quality across both modes
├── examples/
│   ├── sample_meeting_transcript.txt               # Sample meeting transcript (Meeting Mode, synthetic data)
│   ├── sample_output_summary.md                    # Expected output for Meeting Mode (including optional Section 4)
│   ├── sample_meeting_dashboard.html               # Working interactive dashboard example for Meeting Mode
│   ├── sample_presentation_transcript.txt          # Sample presentation transcript (Presentation Mode, synthetic data)
│   ├── sample_presentation_summary.md              # Expected chronological output for Presentation Mode
│   └── sample_presentation_dashboard.html          # Working Knowledge Graph dashboard example for Presentation Mode
└── scripts/
    └── clean_transcript.py                         # Standalone Python utility to strip caption timestamps
```

---

## Non-Technical User Guide: How to Use This Skill

You do not need any programming experience to use this skill. Follow the steps below to turn a raw recording transcript into a structured summary and optional interactive UI dashboard.

### Step 1: Obtain Your Transcript

Export or copy the text transcript from your video call recording, webinar platform, or transcription tool. The skill accepts:
- Plain text copied and pasted directly into the chat window
- Attached text files (`.txt`)
- Exported subtitle or caption files (`.vtt` or `.srt`)

### Step 2: Provide the Transcript, Choose a Mode, Specify UI Dashboard Creation, and Optionally Provide a User Name

Before generating any output, the assistant checks for **two required settings** and **one optional setting**:
1. **Processing Mode (Required):** `Meeting Mode` or `Presentation Mode`
2. **Interactive UI Dashboard (`dashboard.html`) (Required):** Whether the UI dashboard must be created upon completion (`Yes` or `No`)
3. **User Name (Optional — Meeting Mode Only):** A participant's name (for example, `Marcus Vance`). If specified in Meeting Mode, the assistant adds a **fourth section (`## 4. Action Items for [User Name]`)** after the 5-sentence summary with a brief paragraph combining the action items assigned to that user and a concise description of what needs to be done. Because this parameter is optional, the assistant will **never** prompt you for a user name if you omit it—it simply generates the 3 standard sections.

![Skill Execution Parameters and User-Specific Action Items Interaction](assets/user_interaction_diagram.png)

You can either **paste the transcript first and let the assistant prompt you** for the mode and UI dashboard preference, or **specify your settings directly in your initial message**.

#### Option A: Paste the Transcript First, Answer the Prompt After (Two-Step Flow)
If you provide a transcript without specifying the mode or whether to create the UI dashboard upon completion, the assistant will not guess. It will pause and ask you **only** for the missing required choice(s) (`Mode` and/or `UI Dashboard`)—never asking for a user name—before generating output.

**Real-World Example 1 — Weekly Team Planning Call (Pasting Transcript Only, Creating Dashboard + Optional User Name in Reply):**
1. **You paste into chat:**
   ```text
   Use the meeting-transcript-summary skill on this transcript:

   Sarah Lin (10:01 AM): Let's finalize our Q4 database migration schedule.
   Marcus Vance (10:02 AM): Staging tests completed with zero data loss. I can run the production cutover on October 3.
   Sarah Lin (10:03 AM): Approved. Marcus, please publish the cutover runbook by Friday.
   ```
2. **The assistant asks you for the two required settings (Mode and UI Dashboard):**
   > Before processing this transcript, please specify:
   > 1. **Processing Mode:**
   >    - **Meeting Mode** — 3-part summary (Executive Summary, Detailed Logical Discussion Record with Action Items, and 5-Sentence Summary; plus optional Section 4 if a user name is specified)
   >    - **Presentation Mode** — Chronological description and summarization of what was said only
   > 2. **Interactive UI Dashboard:** Should the interactive UI dashboard (`dashboard.html`) be created upon completion? (**Yes** / **No**)
3. **You reply (either with or without an optional user name):**
   - **Standard 3-section reply (no user name):**
     ```text
     meeting mode, yes create the UI dashboard
     ```
     The assistant generates the 3-part meeting summary (Sections 1–3) and creates the interactive 4-tab `dashboard.html` artifact upon completion.
   - **User-specific 4-section reply (with optional user name):**
     ```text
     meeting mode, yes create the UI dashboard, for user Marcus Vance
     ```
     The assistant generates all 3 core sections **plus** `## 4. Action Items for Marcus Vance` (a brief paragraph detailing what Marcus Vance needs to do) and creates the interactive `dashboard.html` artifact upon completion.

**Real-World Example 2 — Recorded Slide Presentation or Webinar (Pasting Transcript First, Summary Only):**
1. **You paste or attach the transcript:**
   ```text
   Apply the meeting-transcript-summary skill to the attached recording transcript.
   ```
2. **The assistant asks you to select the Processing Mode (`Meeting Mode` vs. `Presentation Mode`) and whether to create the interactive UI dashboard (`Yes` vs. `No`).**
3. **You reply:**
   ```text
   presentation mode, no dashboard
   ```
   The assistant generates only the start-to-finish chronological walkthrough of what the presenter said on each slide or section (without an Executive Summary, Action Items table, 5-Sentence Summary, User Action Items section, or HTML dashboard).

**Real-World Example 3 — Specifying Mode and Optional User Name Upfront (Assistant Prompts Only for UI Dashboard Preference):**
1. **You write in chat:**
   ```text
   Summarize the attached transcript using the meeting-transcript-summary skill in meeting mode for user Sarah Lin.
   ```
2. **Because the mode (and optional user name) were already provided, the assistant asks only the remaining required question:**
   > Should the interactive UI dashboard (`dashboard.html`) be created upon completion? (**Yes** / **No**)
3. **You reply:**
   ```text
   No
   ```
   The assistant proceeds with Meeting Mode, generates Sections 1–3 plus `## 4. Action Items for Sarah Lin`, and skips the HTML dashboard.

---

#### Option B: Specify Mode and UI Dashboard Preference (Plus Optional User Name) in Your First Message (One-Step Flow)

If you already know both your preferred mode and whether you want the UI dashboard created upon completion (plus an optional user name if you want Section 4), include them in your initial prompt to run in a single step without follow-up prompts:

- **Example 4 — Meeting Mode + UI Dashboard + User Name Specified (4 Sections + Dashboard):**
  ```text
  Summarize the attached transcript using the meeting-transcript-summary skill in meeting mode, create the UI dashboard upon completion, and include action items for user Marcus Vance.
  ```
- **Example 5 — Meeting Mode + No UI Dashboard + User Name Specified (4 Sections, Summary Only):**
  ```text
  Summarize the attached transcript using the meeting-transcript-summary skill in meeting mode without creating the UI dashboard, for user Marcus Vance.
  ```
- **Example 6 — Meeting Mode + UI Dashboard, No User Name (3 Sections + Dashboard):**
  ```text
  Summarize the attached transcript using the meeting-transcript-summary skill in meeting mode and create the UI dashboard upon completion.
  ```
- **Example 7 — Meeting Mode + No UI Dashboard, No User Name (3 Sections, Summary Only):**
  ```text
  Summarize the attached transcript using the meeting-transcript-summary skill in meeting mode without creating the UI dashboard.
  ```
- **Example 8 — Presentation Mode + Knowledge Graph UI Dashboard Upon Completion:**
  ```text
  Summarize the following transcript using the meeting-transcript-summary skill in presentation mode and create the UI dashboard upon completion:

  [Paste presentation transcript here]
  ```
- **Example 9 — Presentation Mode + Chronological Summary Only (No UI Dashboard):**
  ```text
  Summarize the attached transcript using the meeting-transcript-summary skill in presentation mode, summary only (no UI dashboard).
  ```
- **Example 10 — Requesting Dual Output (Rendered + Raw Markdown) with User Name and Dashboard Preference:**
  ```text
  Summarize the attached transcript using the meeting-transcript-summary skill in meeting mode with no UI dashboard, for user Elena Rostova. Provide dual output with both rendered markdown and a raw markdown code block.
  ```

### Step 3: Use or Share the Output

- **Copying into Word Processors, Docs, or Email:** Highlight and copy the rendered summary directly from the chat window. Headings, bullet lists, and tables retain their formatting when pasted.
- **Copying into Wikis or Markdown Files:** Request `"raw markdown"` or `"dual output"` and click the copy button on the code block.
- **Exploring the Interactive Dashboard:** When you confirm UI dashboard creation, the assistant opens an interactive `dashboard.html` panel upon completion where you can click nodes on the Knowledge Graph, inspect slide or topic details, filter tasks by owner, or toggle between dark and light themes.

---

## Platform Deployment and Integration

### 1. Workspace Skill Integration

To register this skill in a local or shared workspace:

1. Copy the skill directory into your environment's skills path (for example, `.agents/skills/meeting-transcript-summary/` relative to the workspace root).
2. Reference the skill in chat with the required **mode** and **UI dashboard flag**, plus an optional **user name**:
   ```text
   # 3-section summary + UI dashboard (no user name specified)
   Use the meeting-transcript-summary skill in meeting mode and create the UI dashboard upon completion for examples/sample_meeting_transcript.txt

   # 4-section summary (with Section 4 for Marcus Vance) + UI dashboard
   Use the meeting-transcript-summary skill in meeting mode, create the UI dashboard upon completion, and generate action items for user Marcus Vance on examples/sample_meeting_transcript.txt
   ```

### 2. Assistant Configuration Interface

To configure this skill in a web-based assistant environment:

1. Open the skills or custom instructions configuration panel.
2. Create a skill named `meeting-transcript-summary`.
3. Copy the contents of [SKILL.md](SKILL.md) into the instruction body.
4. Optionally attach [references/transcript_formats.md](references/transcript_formats.md), [references/dashboard_ui_guide.md](references/dashboard_ui_guide.md), and [references/quality_checklist.md](references/quality_checklist.md) as reference documents.

### 3. Command Line Preprocessing and Agent Harness CLI Usage

Use the included Python script to strip WebVTT or SRT timestamps before passing a transcript to an automated CLI agent runner. Always pass the required **mode** (`meeting mode` or `presentation mode`) and **UI dashboard flag** (`with UI dashboard` or `no UI dashboard`) in your CLI prompt so the agent runs non-interactively in a single turn, and optionally include a **user name** (`for user "<Name>"`) when you want the fourth section generated in Meeting Mode:

```bash
# 1. Normalize raw WebVTT or SRT files into consolidated speaker blocks
python3 scripts/clean_transcript.py raw_recording.vtt --output cleaned_transcript.txt

# 2A. Meeting Mode (3 sections, no UI dashboard, no user name specified)
cat cleaned_transcript.txt | agent-cli --prompt "Execute meeting-transcript-summary in meeting mode with no UI dashboard"

# 2B. Meeting Mode + Optional User Name (4 sections including Section 4 for Marcus Vance, no UI dashboard)
cat cleaned_transcript.txt | agent-cli --prompt "Execute meeting-transcript-summary in meeting mode with no UI dashboard for user Marcus Vance"

# 2C. Meeting Mode + UI Dashboard + Optional User Name (4 sections + emits dashboard.html)
cat cleaned_transcript.txt | agent-cli --prompt "Execute meeting-transcript-summary in meeting mode and create the UI dashboard for user Marcus Vance"

# 2D. Presentation Mode (chronological summary only, no UI dashboard)
cat cleaned_transcript.txt | agent-cli --prompt "Execute meeting-transcript-summary in presentation mode with no UI dashboard"
```

---

## Detailed Output Specifications

### Mode 1: Meeting Mode (`meeting mode`)

#### 1. Executive Summary
- **Meeting Objective:** 1 to 2 direct sentences defining the primary purpose of the meeting as stated by participants.
- **Key Decisions Made:** Bulleted list of final agreements and approved proposals.
- **Strategic Outcomes and Impact:** Quantifiable benefits, architectural shifts, or operational impacts mentioned in the transcript.
- **Critical Risks and Blockers:** Unresolved technical, security, or scheduling dependencies.

#### 2. Detailed Discussion Record and Action Items
- **Logical Topic Organization:** Groups dialogue by subject matter rather than chronological order.
- **Details of What Was Said:** Captures specific statements, technical details, configurations, benchmarks, numbers, and constraints spoken by participants without adding external explanations.
- **Points Raised and Rationale:** Documents the arguments exchanged, trade-offs evaluated, and reasons why alternatives were rejected.
- **Action Items Table:** Four aligned columns:
  - `Action Item`: Concrete task description.
  - `Assigned To`: Designated owner name or `Unassigned` if not stated.
  - `Deadline`: Stated date, milestone, or `Not Specified`.
  - `Acceptance Criteria / Target Deliverable`: Specific artifact, sign-off, or outcome required.

#### 3. Five-Sentence Summary
- Exactly 5 complete sentences in a single paragraph summarizing the meeting purpose, core challenge, primary decision, secondary outcome, and immediate next milestone.

#### 4. Action Items for [User Name] (Optional — Only When User Name Is Specified)
- Generated immediately after Section 3 **only** if a user name is specified when executing the skill (omitted if no user name is provided).
- Consists of a single brief paragraph combining the action items assigned to that user with a concise description of what needs to be done, incorporating relevant discussion context, target deliverables/acceptance criteria, and stated deadlines (or stating explicitly in one factual sentence if no action items were assigned to that user).

---

### Mode 2: Presentation Mode (`presentation mode`)

#### Chronological Presentation Summary
- **Header Metadata:** Presentation Title (`# Presentation Summary: [Title]`), Date (`YYYY-MM-DD`), and `Presenter(s)`.
- **Strict Start-to-Finish Chronological Order:** Segments the transcript into sequential numbered sections (`### 1. [Segment Title]`, `### 2. [Segment Title]`, ...) matching the exact chronological order spoken by the presenter(s).
- **What Was Presented and Said:** Detailed, factual description and summarization of what the presenter(s) said in each segment, including spoken explanations of slide visuals, diagrams, live demonstrations, metrics, benchmarks, and stated takeaways.
- **Omitted Sections:** Does not include an Executive Summary, Action Items table, Five-Sentence Summary, or User-Specific Action Items section.

---

## Interactive Web Dashboards (Tailored by Mode)

When the user confirms that the interactive UI dashboard must be created upon completion, the skill emits a self-contained HTML/CSS/JavaScript file named `dashboard.html` (`UserFacing: true`, `Summary: "Interactive Evaluation Dashboard"`, `RequestFeedback: false`).

### 1. Meeting Mode Dashboard ([templates/meeting_dashboard_template.html](templates/meeting_dashboard_template.html))
Includes four tabs designed for multi-participant meetings:
- **Executive Overview and Metric Cards:** Displays counts for decisions, topics covered, action items, and target cutover date, followed by cards for Meeting Objective, Key Decisions Made, Strategic Outcomes, and Critical Risks.
  ![Executive Brief](assets/dashboard_executive_brief.png)
- **Interactive Topic Knowledge Graph:** SVG node-link topology connecting the core meeting goal to discussed topics with directed relationship edges (`Enforces`, `Requires`, `Gates`) and a slide-out Detail Inspector drawer.
  ![Knowledge Graph](assets/dashboard_knowledge_graph.png)
- **Action Items Visualizer and Toolbar:** Owner filter dropdown, search input, CSV/Markdown clipboard export, Kanban by Owner board, and data table.
  ![Action Items Kanban](assets/dashboard_action_items.png)
- **Detailed Discussion Record:** Expandable topic accordions containing the full narrative record.

### 2. Presentation Mode Dashboard ([templates/presentation_dashboard_template.html](templates/presentation_dashboard_template.html))
Tailored specifically for presentations where the focus is on the conceptual structure and chronological progression rather than meeting action items:
- **Presentation Knowledge Graph (Default Active Tab on Load):**
  - Opens directly to the interactive SVG Knowledge Graph with a top **Presentation Focus** banner.
  - Connects the central `PRESENTATION CORE THEME` node to chronological segment nodes labeled with sequence badges (`#1`, `#2`, `#3`, ...) and concise titles.
  - Displays sequential progression edges (`Next: Slide 4`, `Solved by`) and conceptual links (`Accelerated by`, `Validated in`).
  - Clicking any node opens the **Slide / Segment Detail Inspector Drawer** showing **What Was Presented & Said**, **Slide Visuals, Demos & Metrics Cited**, and **Stated Key Takeaway**.
- **Chronological Walkthrough (Tab 2):**
  - Sequential numbered timeline accordions (`#1` through `#N`) presenting the start-to-finish chronological summary, with Expand/Collapse controls and one-click Markdown export.
- **Omitted Meeting Views:** Does not include Executive Brief metric cards or Action Items tabs.

![Presentation Mode Knowledge Graph Dashboard](assets/dashboard_presentation_knowledge_graph.png)

### Templates and Reference Guides:
- Product Requirements Document: [prd.md](prd.md)
- Meeting Mode Template: [templates/meeting_dashboard_template.html](templates/meeting_dashboard_template.html)
- Presentation Mode Template: [templates/presentation_dashboard_template.html](templates/presentation_dashboard_template.html)
- Working Meeting Dashboard Example: [examples/sample_meeting_dashboard.html](examples/sample_meeting_dashboard.html)
- Working Presentation Dashboard Example: [examples/sample_presentation_dashboard.html](examples/sample_presentation_dashboard.html)
- UI Architecture Guide: [references/dashboard_ui_guide.md](references/dashboard_ui_guide.md)

---

## Core Rules and Constraints

- **Mandatory Mode and UI Dashboard Clarification (Optional User Name):** Before generating output, the agent verifies that both required settings—the processing mode (`"meeting mode"` or `"presentation mode"`) and whether to create the interactive UI dashboard (`dashboard.html`) upon completion—are specified. If either or both are omitted, the agent prompts the user upfront before processing. The `user name` parameter is optional and is never prompted for if omitted.
- **Pure Factual Grounding (Zero Hallucination):** Output contains strictly facts, decisions, numbers, slide descriptions, and arguments directly stated in the source transcript.
- **Strictly Record What Was Said (No External Explanations):** Documents exclusively what speakers articulated during the meeting or presentation without adding external definitions or tutorials.
- **Direct Factual Prose:** Eliminates conversational filler phrases, pleasantries, and introductory or closing framing.
- **Zero Extrapolation:** Unstated owners or deadlines in Meeting Mode are recorded explicitly as `Unassigned` or `Not Specified`; unstated transcript dates default to the current date (`YYYY-MM-DD`).

---

## Quality Audit and Examples

Generated outputs are verified against [references/quality_checklist.md](references/quality_checklist.md). Complete synthetic reference inputs, summaries, and interactive dashboards for both modes are available in `examples/`:

### Meeting Mode Examples:
- Input Transcript: [examples/sample_meeting_transcript.txt](examples/sample_meeting_transcript.txt)
- Output Summary (with optional Section 4 for Marcus Vance): [examples/sample_output_summary.md](examples/sample_output_summary.md)
- Interactive Meeting Dashboard: [examples/sample_meeting_dashboard.html](examples/sample_meeting_dashboard.html)

### Presentation Mode Examples:
- Input Presentation Transcript: [examples/sample_presentation_transcript.txt](examples/sample_presentation_transcript.txt)
- Chronological Output Summary: [examples/sample_presentation_summary.md](examples/sample_presentation_summary.md)
- Interactive Presentation Knowledge Graph Dashboard: [examples/sample_presentation_dashboard.html](examples/sample_presentation_dashboard.html)

---

## License

This project is licensed under the Apache License, Version 2.0. See the [LICENSE](LICENSE) file for details.
