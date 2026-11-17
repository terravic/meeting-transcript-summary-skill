---
name: meeting-transcript-summary
description: >-
  Analyzes raw meeting or presentation transcripts from video conferencing exports,
  WebVTT, SRT, or plain text in two modes: (1) Meeting Mode (default) - produces a
  concise two-section core deliverable (Executive Summary and bullet-first Detailed
  Discussion Record with Action Items table), plus optional add-ons created only when
  explicitly requested: a 5-short-sentence summary (Five-Sentence Summary), a
  user-specific action plan (Action Items for [User Name] brief paragraph), and an
  interactive meeting dashboard; (2) Presentation Mode - produces strictly a concise
  chronological bullet summary of what was presented (no Executive Summary, Action
  Items, or 5-Sentence Summary) plus an optional Knowledge Graph-focused presentation
  dashboard. Executes immediately when a transcript is pasted using defaults: mode
  defaults to "meeting" (switches to "presentation" only when explicitly set),
  dashboard defaults to "no dashboard" (builds dashboard.html only when requested),
  5-sentence summary defaults to "no" (omitted unless requested), and user action plan
  defaults to "none" (omitted unless a user is specified). Enforces strict factual
  grounding, fact-first synthesis without "he said / she said" narration, and hard
  anti-bloat length guardrails so output is never longer than the source transcript.
---

# Meeting and Presentation Transcript Summary Skill

## Purpose

This skill transforms raw transcripts from interactive meetings or speaker presentations into concise, scannable, structured documentation. It supports two distinct processing modes tailored to the nature of the transcript, defaulting to **Meeting Mode** with **No Dashboard**, **No 5-Sentence Summary**, and **No User Action Plan** so you can simply invoke the skill and paste a transcript to execute immediately:

1. **Meeting Mode (`meeting mode` - Default):** For interactive meetings with back-and-forth dialogue among participants. Synthesizes discussions into **two crisp core sections by default** (`1. Executive Summary` and bullet-first `2. Detailed Discussion Record and Action Items` with a 4-column Action Items table). Three optional outputs are omitted by default and generated **only** when the user explicitly asks: an optional **5-Short-Sentence Summary** (`Five-Sentence Summary`), an optional **User Action Plan** (`Action Items for [User Name]` brief paragraph), and an optional 4-tab **Meeting Dashboard** (`dashboard.html`).
2. **Presentation Mode (`presentation mode` - Explicit Override Only):** For presentations, keynotes, lectures, webinars, or demonstrations where one or more presenters speak (often alongside slides) without back-and-forth meeting debate. Activated **only** when the mode is explicitly set to presentation in the prompt. Produces **only** a sequential, chronological, bullet-first summary of what was presented from beginning to end (omitting the Executive Summary, Action Items table, 5-Sentence Summary, and User-Specific Action Items section) and an optional Presentation Knowledge Graph Dashboard (built only when explicitly requested).

Both modes capture every concrete detail, fact, technical spec, argument, metric, and decision spoken in the transcript -- compressed into direct, to-the-point bullets without fluff, play-by-play speaker narration, external explanations, hallucinations, or ungrounded assumptions.

---

## Operating Principles

- **High-Density Conciseness & Anti-Bloat Guardrails (Never Longer Than Source):**
  - The generated Markdown summary (measured in **total words**, including headings and table cells, not just prose words) MUST ALWAYS be strictly shorter than the cleaned source transcript (never generate a "book" or expand conversational transcript text into longer prose).
  - **Compression Targets (Measured in Total Output Words vs. Cleaned Transcript):**
    - *Brief / Ultra-Short Transcripts (`< 400` cleaned words):* Target **40%-60%** (strict ceiling **<= 65%**). Scale `Executive Summary` down proportionally (`<= 35-60 words`, 1-2 tight bullets per applicable category, omitting empty bullet groups) and consolidate `Section 2` into a single compact topic block (`1-3` bullets) when single-topic so short standups or check-ins never exceed input length.
    - *Short / Dense Transcripts (`400-1,500` cleaned words):* Target **35%-55%** (strict ceiling **<= 65%** for default 2-section Meeting Mode; **< 75%** when optional 5-Sentence Summary and/or User Action Plan are requested; **<= 60%** for Presentation Mode).
    - *Medium Transcripts (`1,500-3,000` cleaned words):* Target **25%-45%** (strict ceiling **<= 50%**).
    - *Long Transcripts (`> 3,000` cleaned words, e.g., 30-60+ minute sessions):* Target **10%-25%**, generally capped at **<= 1,100 words** total (up to **~1,400 words** only for unusually dense multi-topic sessions or when optional sections are requested).
  - **Concise != Vague:** Aggressively cut filler, narrative padding, and repetition -- NEVER drop concrete numbers, technical specifications, constraints, slide visuals, trade-offs, decisions, or action items.
- **Fact-First Synthesis (Zero "He Said / She Said" Narration):**
  - Synthesize directly by **topic, fact, technical specification, decision, and action** using crisp, scannable bullet points rather than essay prose paragraphs.
  - **NEVER narrate speaker turns or conversational play-by-play.** Ban phrasing such as *"David said..."*, *"David established..."*, *"Sarah noted that..."*, *"Marcus replied..."*, *"Elena asked..."*, *"Dr. Thorne explained..."*, *"Moving to Slide 2, he walked through..."*, *"The team discussed..."*, and *"It was mentioned that..."*.
  - **Restrict personal names strictly to:**
    1. Document header metadata (`Participants` or `Presenter(s)`).
    2. Task ownership in the `Action Items` table (`Assigned To`) and optional `Action Items for [User Name]` section.
    3. Multi-presenter handoffs in Presentation Mode (omit per-segment `Presenter:` lines for single-presenter talks since the presenter is already listed in the header).
    4. Explicit formal sign-off gates or genuine unresolved disagreements where knowing who holds a position is materially necessary.
  - **Strip throat-clearing filler:** Remove phrases like *"To provide context,"*, *"From a security standpoint,"*, *"In order to ensure..."*, *"This lack of X causes..."*, and *"It is worth noting that..."*. Lead bullets directly with strong nouns, metrics, and active verbs.
- **Zero Cross-Section Duplication (Single Source of Truth):**
  - State each technical specification, metric, and rationale **once**.
  - Keep **Section 1 (Executive Summary)** strictly high-level (crisp 1-line decisions, impacts, and blockers -- no multi-sentence technical deep dives).
  - Keep **Section 2 (Detailed Discussion Record)** as the single home for detailed specs, numbers, and trade-offs -- do NOT repeat the same facts across `Key Points`, `Trade-offs & Rationale`, and `Decision / Status`.
  - Keep **Action Items** table cells verb-first and concise without duplicating the `Action Item` text inside the `Acceptance Criteria / Target Deliverable` column.
- **Pure Factual Grounding (Zero Hallucination, Zero Making Things Up):** Strictly include only the details, facts, numbers, arguments, and statements directly and explicitly spoken in the transcript. Never make up information, invent names, fabricate numbers, or hallucinate events or slide contents not mentioned in the transcript.
- **Strictly Record What Was Said (No External Explanations):** Focus exclusively on reporting the specific details articulated during the meeting or presentation. Do NOT provide external explanations, definitions, tutorials, or general background explanations about the topics discussed.
- **Default-Driven Single-Turn Execution (Never Pause to Ask for Mode, Dashboard, 5-Sentence Summary, or User Name):** When the user invokes the skill and provides a transcript, execute immediately in a single turn by applying the following four defaults unless explicitly overridden in the prompt:
  1. **Processing Mode (Default: `"meeting"`):** Default to **Meeting Mode** (`"meeting"`). Only switch the mode to **Presentation Mode** (`"presentation"`) when the user explicitly sets the mode to presentation in the prompt (e.g., `"presentation mode"`, `"mode: presentation"`, `"in presentation mode"`).
  2. **UI Dashboard Creation (Default: `"no dashboard"`):** Default to **No Dashboard** (generate the Markdown summary only; do not build `dashboard.html`). Only build and emit the interactive UI dashboard (`dashboard.html`) when the user explicitly adds a dashboard request to the prompt (e.g., `"yes dashboard"`, `"build dashboard"`, `"create dashboard"`, `"with dashboard"`).
  3. **Five-Sentence Summary (Default: `"no"` - Meeting Mode Only):** Default to **No / Omitted** (do not generate a 5-sentence summary). Only generate the `Five-Sentence Summary` section (strictly 5 short sentences) in Meeting Mode when the user explicitly asks for it in the prompt (e.g., `"with 5 short sentence summary"`, `"include 5-sentence summary"`, `"5 sentence summary"`, `"five-sentence summary"`, `"add 5 short sentences"`).
  4. **Target User Action Plan (Default: `"none"` - Meeting Mode Only):** Default to **None / Omitted** (do not generate user-specific action items). Only generate `Action Items for [User Name]` in Meeting Mode when a participant/user name is explicitly specified in the prompt (e.g., `"for Marcus Vance"`, `"action plan for Marcus"`, `"action items for Sarah Lin"`, `"user: Sarah Lin"`).
  **Do NOT pause or prompt the user** to clarify the mode, dashboard preference, 5-sentence summary preference, or user name when a transcript is provided -- resolve any omitted parameters using their defaults and execute immediately.
- **Direct Factual Prose:** Deliver direct, telegraphic, unambiguous synthesis. Eliminate conversational transitions, pleasantries, filler phrases, emotional framing, and closing remarks.
- **Zero Extrapolation or Implication:** Do not imply, infer, or assume anything that is not explicitly stated in the transcript. When information is incomplete, unassigned, or unstated, record it explicitly as `Unassigned` or `Not Specified`. **Exception - Date Fallback:** If no date is explicitly stated in the transcript, assume today's date (the current date when the skill runs to process the input transcript text) formatted as `YYYY-MM-DD`.
- **Standard Markdown Formatting:** Structure the deliverable using standard Markdown headings, crisp bulleted lists, and aligned tables.
- **Zero Preamble and Postamble:** Begin the summary output immediately with the document header and end immediately after the final section (writing `dashboard.html` upon completion only when explicitly requested in the prompt). Do not include introductory text ("Here is the summary...") or conversational closings ("Let me know if you need changes...").
- **Missing Input Handling:** If the user invokes the skill without providing transcript text or an accessible transcript file path, respond with a single prompt requesting the transcript input and terminate.

---

## Processing Modes and Parameter Defaults

### Mode 1: Meeting Mode (`meeting` - Default)
Used by default whenever the user does not explicitly specify `"presentation mode"` in the prompt. Designed for collaborative or decision-making meeting transcripts with back-and-forth dialogue among participants.
- **Default Output Deliverable (Two Core Sections Only):**
  1. **Section 1: Executive Summary** (`<= 120 words` ceiling; `~60-110 words` on standard meetings, scaling down to `<= 35-60 words` on `< 400`-word transcripts; scannable in <30 seconds: 1-sentence Objective, plus concise 1-line bullets for Key Decisions Made, Strategic Outcomes & Impact, and Critical Risks & Blockers)
  2. **Section 2: Detailed Discussion Record and Action Items** (Bullet-first topic sections with exact facts/specs, conditional Trade-offs & Rationale, and 1-line Decision/Status -- followed by the 4-column Action Items table)
- **Optional Add-On Sections (Omitted by Default; Included ONLY When User Explicitly Asks):**
  - **Five-Sentence Summary (Optional - Default: `no`):** Single paragraph of strictly 5 short, crisp, complete sentences (`<= 18 words/sentence`, `<= 85 words` total). Included as `## 3. Five-Sentence Summary` **only** when the user explicitly requests a 5-sentence summary in the prompt.
  - **Action Items for [User Name] (Optional - Default: `none`):** Single tight brief paragraph (`<= 75 words`) combining the action items assigned to the specified user with required deliverables and deadlines. Included **only** when a user name is explicitly provided in the prompt (numbered `## 3. Action Items for [User Name]` if Five-Sentence Summary is omitted, or `## 4. Action Items for [User Name]` if both optional sections are requested).
- **Interactive Dashboard (Default: `no dashboard`; Built Only When Explicitly Requested):** Skipped by default. When explicitly requested in the prompt (e.g., `"yes dashboard"`, `"build dashboard"`, `"create dashboard"`, `"with dashboard"`), uses [templates/meeting_dashboard_template.html](templates/meeting_dashboard_template.html), featuring four tabs: `Executive Brief`, `Knowledge Graph`, `Action Items` (Kanban and Data Table), and `Detailed Record`.

### Mode 2: Presentation Mode (`presentation` - Explicit Override Only)
Activated **only** when the user explicitly sets the mode to presentation in the prompt (e.g., `"presentation mode"`, `"mode: presentation"`, `"in presentation mode"`). Designed for a presentation, keynote, lecture, demonstration, or briefing where one or more presenters speak sequentially (often walking through slides or live demonstrations).
- **Output Deliverable:** Single concise chronological deliverable:
  - **Document Header** (`# Presentation Summary: [Title]`, `Date`, `Presenter(s)`)
  - **Chronological Presentation Summary** (`### 1. [Segment Title]`, `### 2. [Segment Title]`, ...) using crisp, direct, fact-dense bullets capturing what was presented in strict chronological order from start to finish -- zero `"presenter explained/noted"` narration.
  - **Strict Omissions:** Do **NOT** generate an Executive Summary, do **NOT** generate an Action Items table, do **NOT** generate a Five-Sentence Summary, and do **NOT** generate a User-Specific Action Items section.
- **Interactive Dashboard (Default: `no dashboard`; Built Only When Explicitly Requested):** Skipped by default. When explicitly requested in the prompt (e.g., `"yes dashboard"`, `"build dashboard"`, `"create dashboard"`, `"with dashboard"`), uses [templates/presentation_dashboard_template.html](templates/presentation_dashboard_template.html), opening **directly to the Interactive Presentation Knowledge Graph** (mapping the central presentation theme, chronological flow `#1` through `#N`, and conceptual links across slides/segments with a slide-out Segment Inspector), paired with a `Chronological Walkthrough` tab. Omits Executive Brief metrics and Action Items tabs.

### How Parameter Defaults and Explicit Overrides Work (Single-Turn Flow)

Whenever a transcript is provided, resolve the four execution parameters directly from the user's prompt and execute immediately without asking follow-up questions:

| Parameter | Default (When Not Mentioned in Prompt) | How to Override in Prompt | Resulting Behavior |
| :--- | :--- | :--- | :--- |
| **Mode** | **`meeting`** (`Meeting Mode`) | Explicitly specify `"presentation mode"`, `"mode: presentation"`, or `"in presentation mode"` | Runs **Meeting Mode** (2 core sections) by default; switches to **Presentation Mode** only when explicitly set in the prompt. |
| **Dashboard** | **`no dashboard`** (Markdown summary only) | Explicitly add `"yes dashboard"`, `"build dashboard"`, `"create dashboard"`, or `"with dashboard"` | Outputs only the Markdown summary by default; builds and emits `dashboard.html` only when explicitly requested. |
| **5-Sentence Summary** | **`no`** (Omitted) | Explicitly request in Meeting Mode (e.g., `"with 5 short sentence summary"`, `"include 5-sentence summary"`, `"add 5 sentence summary"`) | Omitted by default; appends `## 3. Five-Sentence Summary` (5 short sentences) in Meeting Mode only when requested. |
| **User Action Plan** | **`none`** (Omitted) | Explicitly specify a participant name in Meeting Mode (e.g., `"for Marcus Vance"`, `"action plan for Marcus"`, `"user: Sarah Lin"`) | Omitted by default; appends `Action Items for [User Name]` (`## 3.` if alone, or `## 4.` after 5-Sentence Summary) only when a user name is provided. |

1. **Pasting Transcript Only (Zero Flags Specified):**
   - If the user simply invokes the skill and pastes (or attaches) the transcript without specifying any flags, immediately execute **Meeting Mode** (`mode = meeting`), generate **only the 2 core sections** (`1. Executive Summary` and `2. Detailed Discussion Record and Action Items`), omit both `Five-Sentence Summary` and `Action Items for [User Name]`, and do **not** generate `dashboard.html`.
2. **Explicit 5-Sentence Summary Override (`with 5 short sentence summary` in Meeting Mode):**
   - If the prompt asks for a 5-sentence summary (e.g., `"include 5 short sentence summary"`, `"with 5-sentence summary"`), generate Sections 1, 2, and `## 3. Five-Sentence Summary`.
3. **Explicit User Action Plan Override (`for [User Name]` in Meeting Mode):**
   - If the prompt specifies a target user name without asking for a 5-sentence summary, generate Sections 1, 2, and `## 3. Action Items for [User Name]`. If the prompt asks for **both** a 5-sentence summary and a target user name, generate Sections 1, 2, `## 3. Five-Sentence Summary`, and `## 4. Action Items for [User Name]`.
4. **Explicit Mode Override (`presentation mode`):**
   - If the prompt explicitly requests Presentation Mode (e.g., `"presentation mode"`), execute **Presentation Mode** and output only the chronological presentation summary (plus the Presentation Knowledge Graph `dashboard.html` if and only if dashboard creation is also explicitly requested in the prompt).
5. **Explicit Dashboard Override (`yes dashboard` / `build dashboard`):**
   - If the prompt explicitly requests a dashboard (e.g., `"yes dashboard"`, `"build dashboard"`, `"create dashboard"`, `"with dashboard"`), generate the Markdown summary for the active mode **and** write `dashboard.html` upon completion.

---

## Processing Workflow

Follow these steps sequentially:

```text
1. Ingestion and Default/Override Parameter Resolution (Single-Turn Execution)
   |-- Verify transcript text or file path is provided (if missing, prompt for transcript input and terminate)
   |-- Resolve Processing Mode (Default = "meeting"):
   |   |-- Use "Meeting Mode" by default
   |   `-- Switch to "Presentation Mode" ONLY if explicitly specified in the prompt (e.g., "presentation mode", "mode: presentation")
   |-- Resolve UI Dashboard Creation (Default = "no dashboard"):
   |   |-- Default to "No Dashboard" (Markdown summary only)
   |   `-- Set UI Dashboard = "Yes" ONLY if explicitly requested in the prompt (e.g., "yes dashboard", "build dashboard", "create dashboard", "with dashboard")
   |-- Resolve Five-Sentence Summary (Default = "no", Meeting Mode only):
   |   |-- Default to "no" (omit Five-Sentence Summary)
   |   `-- Enable Five-Sentence Summary ONLY if explicitly requested in the prompt (e.g., "with 5 short sentence summary", "include 5-sentence summary", "5 sentence summary")
   |-- Resolve Target User Action Plan (Default = "none", Meeting Mode only):
   |   |-- Default to "none" (omit Action Items for [User Name])
   |   `-- Enable Action Items for [User Name] ONLY if a target user name is explicitly specified in the prompt (e.g., "for Marcus Vance", "action plan for Marcus")
   |-- Parse speaker tags, timestamps, slide transitions, and diarization markers
   |-- Extract the date from the transcript, or default to today's date (the date the skill runs) in YYYY-MM-DD format if no date is given
   |-- Filter out small talk, greetings, audio/screen-share checks, and off-topic logistics
   `-- Estimate cleaned transcript word count to enforce strict total-word anti-bloat ceilings (<= 65% with proportional scaling for < 400 words; <= 65% default / < 75% with optional sections / <= 60% Presentation for 400-1,500 words; 25%-45% / <= 50% for 1,500-3,000 words; 10%-25% / <= 1,100-1,400 words for > 3,000 words)

2A. Meeting Mode Workflow (Default, or when "Meeting Mode" is specified)
   |-- Step 1 - Section 1 Synthesis: Concise Executive Summary (<= 120 words ceiling; <= 35-60 words if transcript < 400 words)
   |   |-- State primary meeting objective in 1 crisp sentence (<= 25 words)
   |   |-- List top decisions and core outcomes as tight 1-line bullets (<= 18 words each)
   |   `-- List critical risks/blockers concisely without duplicating Section 2 technical details
   |-- Step 2 - Section 2 Synthesis: Bullet-First Detailed Discussion Record and Action Items
   |   |-- Group by logical topic discussed in the meeting (consolidate into 1 topic block on brief single-topic < 400-word transcripts)
   |   |-- Extract exact technical facts, specs, metrics, and constraints as direct Key Points bullets (no "he said / she said")
   |   |-- Include Trade-offs & Rationale ONLY when options/alternatives were weighed; close with a 1-line Decision / Status
   |   |-- Strictly avoid external explanations, tutorials, or unmentioned concept definitions
   |   `-- Compile the 4-column Action Items table using tight verb-first phrasing (<= 15 words/cell)
   |-- Step 3 - Optional Five-Sentence Summary Synthesis (Conditional - Default: no; ONLY when explicitly requested)
   |   |-- Draft strictly five short, crisp, grammatically complete sentences (<= 18 words each, <= 85 words total)
   |   `-- Emit as "## 3. Five-Sentence Summary" and verify sentence count equals exactly five before finalizing (omit completely if not requested)
   |-- Step 4 - Optional Action Items for [User Name] Synthesis (Conditional - Default: none; ONLY when a User Name is explicitly specified)
   |   |-- Match the specified user name (full or partial/first name) to the corresponding participant in the transcript
   |   |-- Identify all action items and responsibilities assigned to that user in the transcript
   |   |-- Draft a single tight brief paragraph (<= 75 words) combining tasks, deliverables/acceptance criteria, and deadlines
   |   |-- Number sequentially as "## 3. Action Items for [User Name]" (if Five-Sentence Summary was omitted) or "## 4. Action Items for [User Name]" (if Five-Sentence Summary was included)
   |   `-- If zero action items were assigned to the user, state so explicitly in one factual sentence (omit completely if no user name was specified)
   `-- Step 5 - Meeting Dashboard Generation (Conditional - Default: no dashboard; ONLY when explicitly requested via "yes dashboard" / "build dashboard")
       |-- Populate concise, fact-first meeting data into templates/meeting_dashboard_template.html
       `-- Write standalone HTML output to dashboard.html

2B. Presentation Mode Workflow (ONLY when "Presentation Mode" is explicitly specified in the prompt)
   |-- Step 1 - Chronological Segmentation
   |   |-- Partition the transcript into sequential segments in exact chronological order
   |   `-- Align segment boundaries with slide transitions, agenda sections, architecture steps, or demo stages stated aloud
   |-- Step 2 - Concise Chronological Bullet Summarization
   |   |-- For each segment, list 3-5 fact-dense bullets (<= 22 words each) capturing all facts, technical mechanisms, metrics, slide visual/chart references inline, demo steps, and stated takeaways
   |   |-- Eliminate all "presenter said / explained / noted / walked through" narration; include Presenter: tag ONLY when multiple presenters alternate
   |   |-- Strictly avoid external explanations, tutorials, or unmentioned concept definitions
   |   `-- Strictly omit Executive Summary, Action Items table, Five-Sentence Summary, and User-Specific Action Items section
   `-- Step 3 - Presentation Dashboard Generation (Conditional - Default: no dashboard; ONLY when explicitly requested via "yes dashboard" / "build dashboard")
       |-- Populate concise, fact-first PRESENTATION_DATA schema into templates/presentation_dashboard_template.html
       `-- Write standalone HTML output to dashboard.html
```

---

## Output Structure Specification

Format the generated document using standard Markdown according to the selected mode below.

### Mode 1: Meeting Mode Output Structure (Default: Sections 1 and 2 Only)

By default, output **only** the document header, `## 1. Executive Summary`, and `## 2. Detailed Discussion Record and Action Items`. Do **NOT** output `Five-Sentence Summary` or `Action Items for [User Name]` unless the user explicitly asks for them in the prompt.

```markdown
# Meeting Summary: [Insert Meeting Topic / Project Name]

**Date:** [YYYY-MM-DD - Use the date stated in the transcript; if no date is given, assume today's date (the date the skill runs)]  
**Participants:** [Comma-separated list of active participants identified in transcript]

---

## 1. Executive Summary

Provide a crisp, scannable overview (`<= 120 words` ceiling; `~60-110 words` on standard meetings, scaling down to `<= 35-60 words` on `< 400`-word transcripts; readable in <30 seconds) grounded strictly in the transcript -- no deep technical repetition from Section 2:
- **Meeting Objective:** [1 direct sentence (<= 25 words) stating the primary goal.]
- **Key Decisions Made:**
  - [Max 3-5 concise 1-line bullets (<= 18 words each; 1-2 bullets on brief transcripts) stating approved choices and paths forward.]
- **Strategic Outcomes & Impact:**
  - [Max 2-4 concise 1-line bullets (<= 18 words each) citing explicit metrics, savings, or operational impacts.]
- **Critical Risks & Blockers:**
  - [Max 2-4 concise 1-line bullets (<= 18 words each) listing explicit unresolved blockers or gates; write `None stated` if none.]

---

## 2. Detailed Discussion Record and Action Items

Create a dense, bullet-first record organized by logical topic. Preserve every concrete specification, metric, constraint, alternative, and decision -- without "he said / she said" attribution, narrative fluff, repetition, or external explanations.

### Topic 1: [Descriptive Topic Title]

- **Key Points:**
  - [2-5 crisp, fact-first bullets (<= 22 words each; 1-3 bullets on brief < 400-word transcripts) capturing specific facts, numbers, configurations, constraints, or options -- no speaker-turn narration.]
- **Trade-offs & Rationale:** *(Include ONLY when alternatives were actually weighed or debated; omit on straightforward topics)* [1-3 concise bullets or 1 tight line explaining why the selected approach beat dismissed options.]
- **Decision / Status:** [1 crisp line (<= 18 words) stating the final agreement, decision, or open status.]

### Topic 2: [Descriptive Topic Title]
[Repeat this concise bullet-first structure for each substantial topic discussed; consolidate into a single topic on brief single-subject meetings.]

### Action Items

Conclude Section 2 with a Markdown table containing all concrete deliverables, tasks, and follow-ups assigned during the meeting. Adhere strictly to the column layout below:

| Action Item | Assigned To | Deadline | Acceptance Criteria / Target Deliverable |
| :--- | :--- | :--- | :--- |
| [Concise verb-first task (<= 15 words)] | [Owner Name or Unassigned] | [Date / Milestone or Not Specified] | [Specific deliverable or outcome (<= 15 words)] |
```

#### Meeting Mode Formatting & Conciseness Rules:
1. Always include all four columns in the Action Items table; keep cells tight (`<= 15 words`) and do not repeat the task phrasing inside `Acceptance Criteria / Target Deliverable`.
2. If an action item has no designated owner stated in the transcript, write `Unassigned`. Do not guess names or make up assignees.
3. If no timeline or target date was agreed upon, write `Not Specified`. Do not invent deadlines.
4. Keep personal names out of `Key Points` and `Trade-offs & Rationale` unless documenting a material formal sign-off gate or an unresolved disagreement where stance ownership matters.
5. Ensure Markdown table syntax is valid and cleanly aligned.

#### Conditional Optional Section: Five-Sentence Summary (Include ONLY When User Explicitly Asks):

If and only if the user explicitly asks for a 5-sentence / 5-short-sentence summary in the prompt (e.g., `"with 5 short sentence summary"`, `"include 5-sentence summary"`, `"add 5 sentence summary"`), append `## 3. Five-Sentence Summary` immediately after Section 2. If the user does not ask for it, **do not output this section**.

```markdown
---

## 3. Five-Sentence Summary

A single paragraph containing strictly five short, crisp, complete sentences (`<= 18 words/sentence`, `<= 85 words` total; no run-on compound sentences):

[Sentence 1: Primary purpose and scope.] [Sentence 2: Core technical or operational problem addressed.] [Sentence 3: Primary architectural or strategic decision.] [Sentence 4: Key security/secondary requirement or quantified impact.] [Sentence 5: Immediate milestone and target timeline.]
```

#### Conditional Optional Section: Action Items for [User Name] (Include ONLY When a User Name Is Specified):

If and only if the user specifies a target user name when invoking the skill (e.g., `"for Marcus Vance"`, `"action plan for Marcus"`, `"user: Sarah Lin"`), append `Action Items for [User Name]` at the end of the summary. Use sequential heading numbering:
- Use `## 3. Action Items for [User Name]` when the optional Five-Sentence Summary is **omitted** (default).
- Use `## 4. Action Items for [User Name]` when **both** the Five-Sentence Summary (`## 3.`) and User Action Plan are requested.
If no user name is specified, **do not output this section**.

```markdown
---

## [3 or 4]. Action Items for [User Name]

[Single tight brief paragraph (<= 75 words, 1-3 crisp sentences) stating the specific tasks assigned to the user, target deliverables/acceptance criteria, and deadlines -- without re-summarizing meeting history.]
```

#### Optional Sections Formatting and Grounding Rules:
1. **Strictly Opt-In:** Never generate `Five-Sentence Summary` or `Action Items for [User Name]` unless explicitly requested in the user's prompt. Never prompt the user to ask if they want either section.
2. **Short Five-Sentence Rule:** When `Five-Sentence Summary` is requested, write strictly 5 complete short sentences (`<= 18 words/sentence`, `<= 85 words` total) in one paragraph.
3. **Tight User Action Plan Paragraph:** When `Action Items for [User Name]` is requested, write a cohesive, brief prose paragraph (`<= 75 words`, not a bulleted list or table) combining the user's assigned action items, concrete deliverables, and stated deadlines.
4. **Participant Name Resolution:** If a partial or first name is given (e.g., `"Marcus"`), resolve it to the full participant name from the transcript (e.g., `"Marcus Vance"`) if unambiguous.
5. **Zero-Task Fallback:** If a user name is specified in the request, still generate `Action Items for [User Name]`, but if that user has zero assigned action items in the transcript, state explicitly in a single factual sentence that no action items were assigned to `[User Name]` during the meeting. Never invent tasks.

---

### Mode 2: Presentation Mode Output Structure

When running in **Presentation Mode**, output **only** the document header and the concise chronological bullet summary of what was presented. Do **NOT** output an Executive Summary, Action Items table, Five-Sentence Summary, or User-Specific Action Items section.

```markdown
# Presentation Summary: [Insert Presentation Title / Topic]

**Date:** [YYYY-MM-DD - Use the date stated in the transcript; if no date is given, assume today's date (the date the skill runs)]  
**Presenter(s):** [Comma-separated list of presenter(s) identified in transcript, or [Not Specified] if unnamed]

---

## Chronological Presentation Summary

Provide a sequential, start-to-finish chronological summary grouped into numbered segments following slide transitions, agenda sections, or demonstration steps. Write direct, fact-dense bullets -- NEVER narrate speaker actions ("Presenter explained...", "Moving to Slide 2, he detailed...").

### 1. [First Chronological Segment / Slide Topic Title]

- **Presenter:** [Name -- include ONLY when multiple presenters share the stage; OMIT for single-presenter presentations]
- [Direct, fact-dense bullet (<= 22 words) capturing facts, technical architecture, metrics, slide visual/chart citations inline (e.g., "(Slide 1 chart)"), demo steps, or stated takeaways.]
- [3-5 concise bullets per segment; zero filler transitions or speaker attribution.]

### 2. [Second Chronological Segment / Slide Topic Title]

- [Continue with crisp, direct chronological bullets through the end of the presentation...]
```

#### Presentation Mode Rules:
1. **Strict Chronological Order:** Segments must follow the exact sequential order presented from start to finish (do not reorder or merge disparate timestamps into non-chronological thematic buckets).
2. **Fact-First Bullets (No Speaker Narration):** Omit `- **Presenter:**` inside segments for single-presenter talks (already stated in the header). Never open bullets with *"Dr. Thorne noted..."*, *"Presenting Slide N, he described..."*, or *"She walked through..."* -- state the facts, architecture, numbers, and takeaways directly.
3. **Slide and Visual References:** Cite slides, charts, architecture diagrams, code walkthroughs, or live demos concisely inline (e.g., `(Slide 3 pipeline diagram)`). Never fabricate visual details not mentioned in the transcript.
4. **No Meeting-Mode Sections:** Never include an Executive Summary, Key Decisions list, Action Items table, Five-Sentence Summary, or User-Specific Action Items section in Presentation Mode.

---

## Output Format Modes

Within either processing mode (`Meeting Mode` or `Presentation Mode`), the skill supports four delivery formats based on user requirements:

1. **Rendered Markdown (Default Text Output):** Output standard Markdown directly to the chat stream. Standard Markdown renderers automatically parse and renders this into rich text with headers, bullet lists, and tables.
2. **Raw Markdown Code Block:** When prompted for "raw markdown", wrap the complete output inside a fenced code block (` ```markdown ... ``` `) with a copy button, allowing immediate transfer into code repositories or `.md` files.
3. **Dual Output Mode:** When prompted for "dual output" or "both rendered and raw", deliver the complete rendered output first, followed by a divider and a fenced code block containing the exact raw Markdown.
4. **Interactive Web Dashboard Mode (Default: `no dashboard`; Built Only When Explicitly Requested):** By default, no dashboard is built (`dashboard = no dashboard`). Only when the user explicitly adds a dashboard request to the prompt (e.g., `"yes dashboard"`, `"build dashboard"`, `"create dashboard"`, `"with dashboard"`), generate a self-contained HTML/JS/CSS document tailored to the active processing mode following [references/dashboard_ui_guide.md](references/dashboard_ui_guide.md), populating `MEETING_DATA` or `PRESENTATION_DATA` with the same concise, zero-attribution copy:
   - **In Meeting Mode:** Use [templates/meeting_dashboard_template.html](templates/meeting_dashboard_template.html) to render the 4-tab Meeting Dashboard (`Executive Brief`, `Knowledge Graph`, `Action Items` Kanban/Table, and `Detailed Record`).
   - **In Presentation Mode:** Use [templates/presentation_dashboard_template.html](templates/presentation_dashboard_template.html) to render the Presentation Knowledge Graph Dashboard, which opens **directly to the Interactive Presentation Knowledge Graph** (visualizing the central presentation theme, chronological progression `#1` through `#N`, conceptual links across segments, and a slide-out Segment Inspector drawer) alongside a `Chronological Walkthrough` timeline tab, with no Executive Brief metrics or Action Items views.
   - **Dashboard File Output Requirement:** When generating or updating the interactive HTML dashboard in either mode, write the standalone HTML document to `dashboard.html` in the active output directory.

---

## Content Evaluation Rubric

Before outputting the response, verify compliance against these standards:

1. **Default Parameter Resolution and Explicit Override Check (Single-Turn Execution):** Confirm that the agent executes immediately in a single turn when a transcript is provided without pausing to ask for mode, dashboard preference, 5-sentence summary preference, or user name:
   - **Mode:** Defaults to `"meeting"` (`Meeting Mode`) and switches to `"presentation"` (`Presentation Mode`) **only** when explicitly set in the prompt.
   - **Dashboard:** Defaults to `"no dashboard"` (Markdown summary only) and builds `dashboard.html` **only** when explicitly requested in the prompt (e.g., `"yes dashboard"`, `"build dashboard"`, `"create dashboard"`, `"with dashboard"`).
   - **Five-Sentence Summary:** Defaults to `"no"` (omitted) and generates `## 3. Five-Sentence Summary` in Meeting Mode **only** when explicitly requested in the prompt.
   - **User Action Plan:** Defaults to `"none"` (omitted) and generates `Action Items for [User Name]` in Meeting Mode **only** when a target user name is explicitly provided in the prompt (`## 3.` if 5-Sentence Summary is omitted; `## 4.` if both are requested).
2. **Anti-Bloat Compression & Section Budget Check:**
   - Confirm **total output word count** (including headings and table cells) is **strictly shorter** than the cleaned source transcript: `<= 65%` with proportional scaling for `< 400`-word brief transcripts; target **35%-55%** with hard ceiling **`<= 65%`** default (`< 75%` with optional sections; **`<= 60%`** Presentation) for `400-1,500` words; **25%-45%** (`<= 50%`) for `1,500-3,000` words; **10%-25%** and generally **`<= 1,100-1,400 words`** for `> 3,000`-word sessions.
   - Confirm Executive Summary stays `<= 120 words` (`<= 35-60 words` on `< 400`-word transcripts), Section 2 uses concise scannable bullets (not prose walls) with zero cross-section duplication, optional `Five-Sentence Summary` (when requested) has strictly 5 short sentences (`<= 18 words/sentence`, `<= 85 words` total), and optional `Action Items for [User Name]` (when requested) is `<= 75 words`.
3. **Zero "He Said / She Said" Attribution & Fluff Check:**
   - Verify zero speaker-turn narration (`"X said"`, `"Y noted"`, `"he explained"`, `"she walked through"`, `"The team discussed"`) appears in discussion or presentation bullets.
   - Confirm personal names appear only in header metadata, Action Items `Assigned To` / optional `Action Items for [User Name]`, multi-presenter transitions, or material sign-off gates/unresolved disagreements.
4. **Mode-Specific Structural Compliance:**
   - **If Meeting Mode:** Confirm **only** the 2 core sections (`1. Executive Summary` and `2. Detailed Discussion Record and Action Items` with the 4-column table) are emitted by default; confirm topics use the concise bullet-first structure (`Key Points`, conditional `Trade-offs & Rationale`, 1-line `Decision / Status`); and confirm `Five-Sentence Summary` and `Action Items for [User Name]` are omitted unless explicitly requested in the prompt (numbered sequentially as `## 3.` or `## 3.` + `## 4.` when included).
   - **If Presentation Mode:** Confirm the output contains **only** the Presentation Summary header and the `Chronological Presentation Summary` formatted as concise chronological bullets (`1..N`) with single-presenter per-segment tags omitted, and confirm **zero** Executive Summary, Action Items table, Five-Sentence Summary, or User-Specific Action Items sections are included.
5. **Complete Detail Retention (Concise != Vague):** Verify that despite aggressive fluff removal, every concrete fact, metric, technical specification, constraint, slide reference, decision, trade-off, and action item from the transcript is retained.
6. **Pure Factual Grounding, Zero External Explanations, and Zero Opinion:** Verify that zero external explanations, definitions, unmentioned concepts, personal opinions, editorial interpretations, or hallucinated facts have been added. Output must begin immediately with the document header and end immediately after the final section.
