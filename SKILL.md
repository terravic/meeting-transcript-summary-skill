---
name: meeting-transcript-summary
description: >-
  Analyzes raw meeting or presentation transcripts from video conferencing exports,
  WebVTT, SRT, or plain text in two selectable modes: (1) Meeting Mode — produces a
  three-tier deliverable (Executive Summary, Detailed Discussion Record with Action
  Items table, and 5-Sentence Summary) plus an optional meeting dashboard; (2)
  Presentation Mode — produces strictly a chronological description and summarization
  of what the presenter(s) said (no Executive Summary, Action Items, or 5-Sentence
  Summary) plus an optional Knowledge Graph-focused presentation dashboard. Always
  prompts the user upfront to specify the processing mode and whether to create the
  interactive UI dashboard upon completion if either is not specified. Strictly
  grounded in the transcript with zero hallucination or external explanations.
---

# Meeting and Presentation Transcript Summary Skill

## Purpose

This skill transforms raw transcripts from interactive meetings or speaker presentations into structured documentation. It supports two distinct processing modes tailored to the nature of the transcript:

1. **Meeting Mode (`meeting mode`):** For interactive meetings with back-and-forth dialogue among participants. Synthesizes what was discussed into three distinct sections (Executive Summary, Detailed Logical Discussion Record with an Action Items table, and a 5-Sentence Summary) and an optional 4-tab Meeting Dashboard.
2. **Presentation Mode (`presentation mode`):** For presentations, keynotes, lectures, webinars, or demonstrations where one or more presenters speak (often alongside slides) without back-and-forth meeting debate. Produces **only** a sequential, chronological description and summarization of what was said from beginning to end (omitting the Executive Summary, Action Items table, and 5-Sentence Summary) and an optional Presentation Knowledge Graph Dashboard.

Both modes strictly capture the specific details, facts, arguments, numbers, and statements spoken in the transcript without introducing external explanations, hallucinations, or ungrounded assumptions.

---

## Operating Principles

- **Pure Factual Grounding (Zero Hallucination, Zero Making Things Up):** Strictly include only the details, facts, numbers, arguments, and statements directly and explicitly spoken in the transcript. Never make up information, invent names, fabricate numbers, or hallucinate events or slide contents not mentioned in the transcript.
- **Strictly Record What Was Said (No External Explanations):** Focus exclusively on reporting the specific details of what was spoken during the meeting or presentation. Do NOT provide external explanations, definitions, tutorials, or general background explanations about the topics discussed. Only capture the facts, arguments, constraints, visual/slide descriptions, and points explicitly articulated by the speakers.
- **Mandatory Mode and UI Dashboard Clarification (Never Assume Mode or Dashboard Preference):** Before generating any output, verify that the user has explicitly specified **both**:
  1. **Processing Mode:** `"meeting mode"` or `"presentation mode"`
  2. **UI Dashboard Creation:** Whether the interactive UI dashboard (`dashboard.html`) must be created upon completion (`yes` / `create dashboard` vs. `no` / `summary only`)
  If either or both are not explicitly specified in the user's prompt, **DO NOT assume defaults**. Immediately pause and ask the user for the missing choice(s) upfront (using the interactive `ask_question` tool if available in the agent harness, or a single concise text prompt) and wait for their response before generating the summary or dashboard.
- **Direct Factual Prose:** Deliver factual, direct, and unambiguous synthesis. Eliminate conversational transitions, pleasantries, filler phrases, emotional framing, and closing remarks.
- **Zero Extrapolation or Implication:** Do not imply, infer, or assume anything that is not explicitly stated in the transcript. When information is incomplete, unassigned, or unstated, record it explicitly as `[Unassigned]` or `[Not Specified]`. **Exception — Date Fallback:** If no date is explicitly stated in the transcript, assume today's date (the current date when the skill runs to process the input transcript text) formatted as `YYYY-MM-DD`.
- **Standard Markdown Formatting:** Structure the deliverable using standard Markdown headings, bulleted lists, and aligned tables.
- **Zero Preamble and Postamble:** Once both the mode and UI dashboard preference are confirmed, begin the summary output immediately with the document header and end immediately after the final section (emitting the `dashboard.html` artifact upon completion when requested). Do not include introductory text ("Here is the summary...") or conversational closings ("Let me know if you need changes...").
- **Missing Input Handling:** If the user invokes the skill without providing transcript text or an accessible transcript file path, respond with a single prompt requesting the transcript input (along with their preferred mode and whether to create the UI dashboard upon completion, if also unspecified) and terminate.

---

## Processing Modes and Mode Selection

### Mode 1: Meeting Mode (`meeting mode`)
Use when processing a collaborative or decision-making meeting transcript with back-and-forth dialogue among participants.
- **Output Deliverable:** Three-part response:
  1. **Section 1: Executive Summary** (Meeting Objective, Key Decisions Made, Strategic Outcomes and Impact, Critical Risks and Blockers)
  2. **Section 2: Detailed Discussion Record and Action Items** (Organized by logical topic, followed by the 4-column Action Items table)
  3. **Section 3: Five-Sentence Summary** (Single paragraph of exactly 5 sentences)
- **Interactive Dashboard (when UI dashboard creation is confirmed):** Uses [templates/meeting_dashboard_template.html](templates/meeting_dashboard_template.html), featuring four tabs: `Executive Brief`, `Knowledge Graph`, `Action Items` (Kanban and Data Table), and `Detailed Record`.

### Mode 2: Presentation Mode (`presentation mode`)
Use when processing a presentation, keynote, lecture, demonstration, or briefing where one or more presenters speak sequentially (often walking through slides or live demonstrations).
- **Output Deliverable:** Single chronological deliverable:
  - **Document Header** (`# Presentation Summary: [Title]`, `Date`, `Presenter(s)`)
  - **Chronological Presentation Summary** (`### 1. [Segment Title]`, `### 2. [Segment Title]`, ...) describing and summarizing what was said in strict chronological order from start to finish.
  - **Strict Omissions:** Do **NOT** generate an Executive Summary, do **NOT** generate an Action Items table, and do **NOT** generate a Five-Sentence Summary.
- **Interactive Dashboard (when UI dashboard creation is confirmed):** Uses [templates/presentation_dashboard_template.html](templates/presentation_dashboard_template.html), opening **directly to the Interactive Presentation Knowledge Graph** (mapping the central presentation theme, chronological flow `#1` through `#N`, and conceptual links across slides/segments with a slide-out Segment Inspector), paired with a `Chronological Walkthrough` tab. Omits Executive Brief metrics and Action Items tabs.

### How Mode and UI Dashboard Selection Works

1. **Neither Mode nor UI Dashboard Preference Is Specified (Two-Turn Flow):**
   - If the user provides a transcript and invokes the skill without specifying the mode (`"meeting mode"` or `"presentation mode"`) or whether to create the interactive UI dashboard upon completion, **ask the user for both before processing**:
     - If the `ask_question` tool is available, call `ask_question` with two questions:
       1. Question 1: `"Which processing mode would you like to use for this transcript?"`
          - `Meeting Mode — 3-part response (Executive Summary, Detailed Logical Discussion Record + Action Items, and 5-Sentence Summary)`
          - `Presentation Mode — Chronological description and summarization of what the presenter(s) said only`
       2. Question 2: `"Should the interactive UI dashboard (dashboard.html) be created upon completion?"`
          - `Yes — Create the interactive UI dashboard upon completion`
          - `No — Generate the Markdown summary only`
     - If `ask_question` is not available, output a single direct prompt:
       > Before processing this transcript, please specify:
       > 1. **Processing Mode:**
       >    - **Meeting Mode** — 3-part summary (Executive Summary, Detailed Logical Discussion Record with Action Items, and 5-Sentence Summary)
       >    - **Presentation Mode** — Chronological description and summarization of what was said only
       > 2. **Interactive UI Dashboard:** Should the interactive UI dashboard (`dashboard.html`) be created upon completion? (**Yes** / **No**)
   - Once the user replies (e.g., `"meeting mode, yes"`, `"presentation mode, no dashboard"`, `"1, yes"`), immediately execute the chosen mode workflow and create (or skip) the UI dashboard accordingly.
2. **Only One Requirement Is Specified Upfront (Partial Specification):**
   - **Mode specified, UI Dashboard preference unspecified** (e.g., `"Summarize this transcript in meeting mode"` without mentioning the dashboard): Pause and ask **only** whether the interactive UI dashboard (`dashboard.html`) must be created upon completion (`Yes` vs. `No`), without re-asking the mode.
   - **UI Dashboard preference specified, Mode unspecified** (e.g., `"Summarize this transcript and create the UI dashboard"` or `"Summarize this transcript without a dashboard"`): Pause and ask **only** which processing mode to use (`Meeting Mode` vs. `Presentation Mode`), without re-asking the dashboard preference.
3. **Both Mode and UI Dashboard Preference Are Specified Upfront (One-Turn Flow):**
   - If the user includes both the mode (`"meeting mode"` or `"presentation mode"`) and their UI dashboard preference (e.g., `"and create the UI dashboard"`, `"with dashboard"`, `"no dashboard"`, `"without UI dashboard"`, or `"summary only"`) in their initial prompt, proceed directly to the corresponding workflow without asking follow-up questions.

---

## Processing Workflow

Follow these steps sequentially:

```text
1. Ingestion, Mode, and UI Dashboard Verification
   ├── Verify transcript text or file path is provided (if missing, prompt for transcript + mode + dashboard preference and terminate)
   ├── Check if user specified "Meeting Mode" or "Presentation Mode"
   ├── Check if user specified whether the interactive UI dashboard must be created upon completion ("Yes" or "No")
   │   └── If either or both are unspecified: Prompt user upfront for the missing choice(s) and wait (DO NOT assume defaults)
   ├── Parse speaker tags, timestamps, slide transitions, and diarization markers
   ├── Extract the date from the transcript, or default to today's date (the date the skill runs) in YYYY-MM-DD format if no date is given
   └── Filter out small talk, greetings, audio/screen-share checks, and off-topic logistics

2A. Meeting Mode Workflow (When "Meeting Mode" is selected)
   ├── Step 1 — Section 1 Synthesis: Executive Summary
   │   ├── Identify primary meeting objective as stated by participants
   │   ├── Extract strategic decisions and core outcomes agreed upon in the meeting
   │   └── Summarize impacts and blockers explicitly mentioned in the discussion
   ├── Step 2 — Section 2 Synthesis: Detailed Discussion Record and Action Items
   │   ├── Structure by logical topic discussed in the meeting
   │   ├── Extract and record the specific details of what was said by participants for each topic
   │   ├── Document the specific points, arguments, trade-offs, and rationale spoken by participants
   │   ├── Strictly avoid external explanations, tutorials, or unmentioned concept definitions
   │   └── Compile and format the 4-column Action Items table
   ├── Step 3 — Section 3 Synthesis: Five-Sentence Summary
   │   ├── Draft exactly five grammatically complete sentences summarizing what was said
   │   └── Verify sentence count equals five before finalizing
   └── Step 4 — Meeting Dashboard Generation (When user confirmed UI Dashboard creation = Yes)
       ├── Ingest synthesized meeting data (metrics, decisions, topics, rationale, action items)
       ├── Populate data schema into templates/meeting_dashboard_template.html
       └── Emit dashboard.html as a user-facing artifact via write_to_file

2B. Presentation Mode Workflow (When "Presentation Mode" is selected)
   ├── Step 1 — Chronological Segmentation
   │   ├── Partition the transcript into sequential segments in the exact chronological order spoken
   │   └── Align segment boundaries with slide transitions, agenda sections, architecture walkthrough steps, or demonstration stages stated by the presenter(s)
   ├── Step 2 — Chronological Description and Summarization
   │   ├── For each segment in chronological order, describe and summarize what the presenter(s) said
   │   ├── Capture all specific facts, technical mechanisms, numbers, benchmarks, slide visuals/charts explicitly described aloud, demonstrations, and stated takeaways
   │   ├── Strictly avoid external explanations, tutorials, or unmentioned concept definitions
   │   └── Strictly omit Executive Summary, Action Items table, and Five-Sentence Summary
   └── Step 3 — Presentation Dashboard Generation (When user confirmed UI Dashboard creation = Yes)
       ├── Ingest chronological presentation segments, core presentation theme, and conceptual/chronological relationships
       ├── Populate PRESENTATION_DATA schema into templates/presentation_dashboard_template.html (opening directly to the Presentation Knowledge Graph + Chronological Walkthrough tab)
       └── Emit dashboard.html as a user-facing artifact via write_to_file
```

---

## Output Structure Specification

Format the generated document using standard Markdown according to the selected mode below.

### Mode 1: Meeting Mode Output Structure

```markdown
# Meeting Summary: [Insert Meeting Topic / Project Name]

**Date:** [YYYY-MM-DD — Use the date stated in the transcript; if no date is given, assume today's date (the date the skill runs)]  
**Participants:** [Comma-separated list of active participants identified in transcript]

---

## 1. Executive Summary

Provide a concise, high-level overview based strictly on what was stated in the meeting:
- **Meeting Objective:** State the primary goal and context of the meeting in 1-2 direct sentences as articulated by participants.
- **Key Decisions Made:** Bulleted list of definitive choices, approved proposals, and agreed paths forward made during the meeting.
- **Strategic Outcomes & Impact:** Bulleted list detailing the specific impacts, metrics, or outcomes explicitly stated by participants.
- **Critical Risks & Blockers:** Any unresolved blockers, dependencies, or concerns explicitly raised by participants during the call.

---

## 2. Detailed Discussion Record and Action Items

Create a comprehensive narrative record organized by topic. This section must document the specific details of what was said and discussed by participants during the meeting without introducing external background explanations, generic concept definitions, or hallucinated details.

### Topic 1: [Descriptive Topic Title]

- **Discussion Details (What Was Said):** Record the specific details, facts, technical points, configurations, numbers, constraints, and statements articulated by participants. Strictly report what speakers said during the meeting rather than explaining how tools or concepts work in general.
- **Points Raised and Rationale:** Chronicle the specific arguments exchanged by participants. Detail the stated reasons why specific approaches were favored, what alternatives were discussed and dismissed, what trade-offs and concerns were raised, and how consensus was reached.
- **Key Conclusions:** The definitive agreement, decision, or status reached by participants for this topic.

### Topic 2: [Descriptive Topic Title]
[Repeat structured format for each substantial topic discussed during the meeting.]

### Action Items

Conclude Section 2 with a Markdown table containing all concrete deliverables, tasks, and follow-ups assigned during the meeting. Adhere strictly to the column layout below:

| Action Item | Assigned To | Deadline | Acceptance Criteria / Target Deliverable |
| :--- | :--- | :--- | :--- |
| [Clear, actionable description of the task] | [Owner Name or Unassigned] | [Date / Milestone or Not Specified] | [Specific deliverable, link, or outcome required] |
```

#### Meeting Mode Table Formatting Rules:
1. Always include all four columns.
2. If an action item has no designated owner stated in the transcript, write `Unassigned`. Do not guess names or make up assignees.
3. If no timeline or target date was agreed upon, write `Not Specified`. Do not invent deadlines.
4. Ensure Markdown table syntax is valid and cleanly aligned.

```markdown
---

## 3. Five-Sentence Summary

A single paragraph containing exactly five complete sentences summarizing what was said, key decisions, and next steps:

[Sentence 1: Context and primary purpose of the meeting.] [Sentence 2: Core technical or strategic challenge addressed.] [Sentence 3: Primary decision or consensus reached.] [Sentence 4: Major secondary outcome, resource commitment, or architectural shift.] [Sentence 5: Immediate next milestone and critical path timeline.]
```

---

### Mode 2: Presentation Mode Output Structure

When running in **Presentation Mode**, output **only** the document header and the chronological description and summarization of what was said. Do **NOT** output an Executive Summary, Action Items table, or Five-Sentence Summary.

```markdown
# Presentation Summary: [Insert Presentation Title / Topic]

**Date:** [YYYY-MM-DD — Use the date stated in the transcript; if no date is given, assume today's date (the date the skill runs)]  
**Presenter(s):** [Comma-separated list of presenter(s) identified in transcript, or [Not Specified] if unnamed]

---

## Chronological Presentation Summary

Provide a sequential, chronological description and summarization of what was said and presented from beginning to end. Group the transcript into numbered chronological segments following the exact progression of the presentation (e.g., by slide transitions, section transitions, demonstration steps, or sequential topics covered by the presenter):

### 1. [First Chronological Segment / Slide Topic Title]

- **Presenter:** [Presenter Name — include if speaker is named or when multiple presenters share the stage; omit if a single unnamed presenter]
- **What Was Presented & Said:** Record a detailed, factual description and summarization of what the presenter said during this segment. Include all specific facts, architectural or conceptual descriptions spoken aloud, metrics, numbers, slide visuals or diagrams explicitly referenced by the presenter, live demonstration steps, and stated takeaways.

### 2. [Second Chronological Segment / Slide Topic Title]

- **Presenter:** [Presenter Name]
- **What Was Presented & Said:** [Continue describing and summarizing what was said in strict chronological order...]

### 3. [Third Chronological Segment / Slide Topic Title]
[Repeat sequentially for each chronological segment through the end of the presentation.]
```

#### Presentation Mode Rules:
1. **Strict Chronological Order:** Segments must follow the exact sequential order in which the presenter(s) spoke from start to finish (do not reorder or merge disparate timestamps into non-chronological thematic buckets).
2. **Slide and Visual References:** If the presenter explicitly mentions slides, charts, architecture diagrams, code walkthroughs, or live demonstrations (e.g., *"On slide 4, you can see the latency curve..."*), describe what the presenter stated about those visuals. Never fabricate visual details that were not spoken or included in the transcript.
3. **No Meeting-Mode Sections:** Never include an Executive Summary, Key Decisions list, Action Items table, or Five-Sentence Summary in Presentation Mode.

---

## Output Format Modes

Within either processing mode (`Meeting Mode` or `Presentation Mode`), the skill supports four delivery formats based on user requirements:

1. **Rendered Markdown (Default Text Output):** Output standard Markdown directly to the chat stream. The host agent harness automatically parses and renders this into rich text with headers, bullet lists, and tables.
2. **Raw Markdown Code Block:** When prompted for "raw markdown", wrap the complete output inside a fenced code block (` ```markdown ... ``` `) with a copy button, allowing immediate transfer into code repositories or `.md` files.
3. **Dual Output Mode:** When prompted for "dual output" or "both rendered and raw", deliver the complete rendered output first, followed by a divider and a fenced code block containing the exact raw Markdown.
4. **Interactive Web Dashboard Mode (Created Upon Completion When Confirmed):** When the user confirms that the interactive UI dashboard must be created upon completion (either upfront in their prompt or in response to the confirmation question), generate a self-contained HTML/JS/CSS document tailored to the active processing mode following [references/dashboard_ui_guide.md](references/dashboard_ui_guide.md):
   - **In Meeting Mode:** Use [templates/meeting_dashboard_template.html](templates/meeting_dashboard_template.html) to render the 4-tab Meeting Dashboard (`Executive Brief`, `Knowledge Graph`, `Action Items` Kanban/Table, and `Detailed Record`).
   - **In Presentation Mode:** Use [templates/presentation_dashboard_template.html](templates/presentation_dashboard_template.html) to render the Presentation Knowledge Graph Dashboard, which opens **directly to the Interactive Presentation Knowledge Graph** (visualizing the central presentation theme, chronological progression `#1` through `#N`, conceptual links across segments, and a slide-out Segment Inspector drawer) alongside a `Chronological Walkthrough` timeline tab, with no Executive Brief metrics or Action Items views.
   - **Artifact Emission Requirement:** When generating or updating the interactive HTML dashboard in either mode, you MUST emit the standalone HTML file as a user-facing artifact named `dashboard.html` (using `write_to_file` with `ArtifactMetadata: { UserFacing: true, Summary: "Interactive Evaluation Dashboard", RequestFeedback: false }`). This ensures the dashboard immediately opens and renders directly in the preview pane.

---

## Content Evaluation Rubric

Before outputting the response, verify compliance against these standards:

1. **Mode and UI Dashboard Verification Check:** Confirm that the user either explicitly specified both (a) the processing mode (`"meeting mode"` or `"presentation mode"`) and (b) whether the interactive UI dashboard must be created upon completion (`Yes` / `No`), or was prompted upfront to specify the missing choice(s) before generation.
2. **Mode-Specific Structural Compliance:**
   - **If Meeting Mode:** Confirm all 3 sections are present (`1. Executive Summary`, `2. Detailed Discussion Record and Action Items` with the 4-column table, and `3. Five-Sentence Summary` containing exactly 5 terminal periods / 5 complete sentences), and topics are grouped logically with spoken rationale/trade-offs preserved.
   - **If Presentation Mode:** Confirm the output contains **only** the Presentation Summary header and the `Chronological Presentation Summary` organized in strict start-to-finish chronological order, and confirm that **zero** Executive Summary, Action Items table, or 5-Sentence Summary sections are included.
3. **Details of What Was Said:** Verify that the summary captures the precise details, facts, numbers, and statements spoken in the transcript, rather than vague or generic summaries.
4. **No External Explanations or Hallucinations:** Verify that zero external explanations, definitions, unmentioned concepts, or hallucinated facts have been added. Everything in the summary must be directly traceable to spoken dialogue in the transcript.
5. **Factual Prose Check:** Verify that the output maintains an objective, direct structure with zero conversational pleasantries and zero meta-commentary.
6. **Pure Factual Grounding and Zero Opinion:** Verify that all facts, numbers, dates, technical claims, arguments, and takeaways derive solely from what was said in the transcript. Confirm that zero personal opinions, editorial interpretations, external advice, or unstated implications were added.
