# Quality and Compliance Checklist

Use this checklist to audit generated meeting and presentation summaries against required quality, conciseness, mode selection, structure, and formatting criteria.

---

## 1. Content and Fidelity Standards (Both Modes)

| Criterion | Requirement | Verification Check |
| :--- | :--- | :--- |
| **Default Parameter Resolution & Explicit Overrides (Single-Turn Execution)** | Default to **Meeting Mode** (`"meeting"`), **No Dashboard** (`"no dashboard"`), and **No Target User Name** (`"none"`). Only switch to **Presentation Mode** when explicitly set in the prompt; only build `dashboard.html` when explicitly requested (e.g., `"yes dashboard"` or `"build dashboard"`); only add Section 4 when a user name is specified. | Confirm the agent executed immediately in a single turn without pausing to prompt for mode, dashboard preference, or user name, and accurately applied defaults or explicit overrides. |
| **Anti-Bloat Compression Guardrails** | Output MUST ALWAYS be strictly shorter than the cleaned source transcript. Target **40%–65%** (`< 80%` hard ceiling in Meeting Mode / `≤ 60%` in Presentation Mode) for `< 1,500`-word dense transcripts, **25%–50%** for `1,500–3,000` words, and **10%–25%** (`≤ 1,200–1,500` words) for long sessions. | Verify total output prose word count is strictly less than the cleaned transcript word count and within per-section budgets—no "book-length" expansion. |
| **Zero "He Said / She Said" Narration** | Synthesize directly by topic, technical fact, decision, and action. Ban speaker-turn narration (`"David said"`, `"Sarah noted"`, `"Dr. Thorne explained"`, `"he walked through"`). | Confirm personal names appear only in header metadata, Action Items `Assigned To` / Section 4, multi-presenter transitions, or material sign-off gates/unresolved disagreements. |
| **Zero Cross-Section Duplication** | State each technical detail, metric, and rationale once. Executive Summary stays high-level; Section 2 holds detailed specs without repeating facts across sub-bullets. | Confirm Executive Summary does not duplicate multi-sentence technical deep dives from Section 2, and Action Items deliverables do not restate the task text. |
| **Complete Detail Retention (Concise ≠ Vague)** | Specific details, metrics, technical points, constraints, slide visuals, decisions, and action items are retained in compressed form. | Zero concrete numbers, technical specifications, constraints, slide benchmarks, or tasks dropped during compression. |
| **Pure Factual Grounding and Zero Hallucination** | All statements, numbers, names, slide references, and conclusions derive strictly from what was said in the transcript. | Zero hallucinated facts, invented speakers, unmentioned tools/slides, or fabricated deadlines. |
| **No External Topic Explanations** | Do not generate external explanations, definitions, tutorials, or background commentary on how topics or technologies work. | All content exclusively documents what speakers articulated during the meeting or presentation. |
| **Zero Opinion and Editorializing** | No external commentary, personal opinions, editorial assessments, or unstated implications are injected. | All content reports purely what speakers stated, proposed, presented, and decided. |
| **Organization by Mode** | **Meeting Mode:** Grouped by logical subject matter across the meeting.<br>**Presentation Mode:** Grouped in strict chronological order (`1..N`) from start to finish. | **Meeting Mode:** Related discussions are consolidated under topic headers.<br>**Presentation Mode:** Segments follow exact sequential order spoken by the presenter(s). |
| **Explicit Metadata Fallbacks** | Missing owners or dates in action items are explicitly marked; missing transcript date defaults to today's date. | Action item owners marked as `Unassigned` and deadlines marked as `Not Specified` (in Meeting Mode). If the date is not given in the transcript, assume today's date (the date the skill runs) formatted as `YYYY-MM-DD`. |

---

## 2A. Structural Standards - Meeting Mode (`meeting mode` - Default)

| Section | Mandatory Elements | Common Failures to Avoid |
| :--- | :--- | :--- |
| **Document Header** | Meeting Topic, Date (from transcript, or today's date when the skill runs if not given), Participant List. | Missing participants or omitting date instead of defaulting to today's date. |
| **1. Executive Summary** | Scannable (`~70–130 words`): 1-sentence Meeting Objective (`≤ 25 words`), plus crisp 1-line bullets (`≤ 18 words/bullet`) for Key Decisions Made (max 3–5), Strategic Outcomes & Impact (max 2–4), Critical Risks & Blockers (max 2–4). | Multi-sentence paragraphs, bloated bullets (`> 25 words`), or duplicating full Section 2 technical explanations. |
| **2. Detailed Discussion Record** | Bullet-first subheadings per logical topic: `Key Points` (2–5 crisp bullets, `≤ 22 words` each), conditional `Trade-offs & Rationale` (only when options were weighed), and 1-line `Decision / Status` (`≤ 18 words`). | Walls of narrative prose, `"David did/said..."` attribution, repeating the same point across all sub-blocks, or injecting external tutorials. |
| **Action Items Table** | 4 columns: `Action Item`, `Assigned To`, `Deadline`, `Acceptance Criteria / Target Deliverable` with tight verb-first cells (`≤ 15 words/cell`). | Verbose table cells, duplicating task wording in deliverables, broken table alignment, or hallucinating assignees/deadlines. |
| **3. Five-Sentence Summary** | Strictly five crisp, grammatically complete sentences in a single paragraph (`≤ 18–20 words/sentence`, `~65–95 words` total). | Generating 4 or 6 sentences, bloated compound run-ons, or exceeding ~100 words. |
| **4. Action Items for [User Name] (Conditional - Default: `none`; Only When User Name Is Specified)** | Included after Section 3 **only** if a user name was specified in the prompt; omitted by default when no user name is specified. Single tight brief paragraph (`≤ 75 words`, 1–3 sentences) combining tasks, deliverables, and deadlines (or one factual sentence if zero tasks). | Exceeding 75 words, re-summarizing meeting history, generating Section 4 when no user name was provided, using a bullet list/table instead of a brief paragraph, or fabricating tasks. |
| **Meeting Mode Dashboard (Conditional - Default: `no dashboard`)** | Skipped by default. When explicitly requested (`"yes dashboard"` / `"build dashboard"`), uses `templates/meeting_dashboard_template.html` with 4 tabs (`Executive Brief`, `Knowledge Graph`, `Action Items`, `Detailed Record`) and concise, zero-attribution `MEETING_DATA` copy. | Building `dashboard.html` when not requested in the prompt, verbose speaker-narrated JSON strings, or emitting a presentation-only dashboard for an interactive meeting. |

---

## 2B. Structural Standards - Presentation Mode (`presentation mode` - Explicit Override Only)

| Section | Mandatory Elements | Common Failures to Avoid |
| :--- | :--- | :--- |
| **Document Header** | Presentation Title (`# Presentation Summary: [Title]`), Date (from transcript, or today's date if not given), Presenter(s) List. | Using `Participants` instead of `Presenter(s)` or omitting the date. |
| **Chronological Presentation Summary** | Sequential numbered subheadings (`### 1. [Segment Title]`, `### 2. [Segment Title]`, ...) with 3–5 crisp, fact-dense bullets (`≤ 22 words` each) and inline slide/visual references. Include `- **Presenter:**` ONLY when multiple presenters alternate. | Dense prose paragraphs, `"Dr. Thorne explained..."` / `"he walked through..."` narration, repeating `Presenter:` per segment for a single speaker, reordering chronologically, or omitting spoken metrics. |
| **Strict Omission of Meeting Sections** | Must **NOT** include an Executive Summary, Action Items table, Five-Sentence Summary, or User-Specific Action Items section. | Including an Executive Summary, fabricating an Action Items table, appending a 5-Sentence Summary, or adding Section 4 in Presentation Mode. |
| **Presentation Mode Dashboard (Conditional - Default: `no dashboard`)** | Skipped by default. When explicitly requested (`"yes dashboard"` / `"build dashboard"`), uses `templates/presentation_dashboard_template.html` opening **directly to the Presentation Knowledge Graph** (with `#1..#N` sequence nodes and Segment Inspector) plus the `Chronological Walkthrough` tab using concise, zero-attribution `PRESENTATION_DATA` copy. | Building `dashboard.html` when not requested in the prompt, verbose speaker-narrated JSON strings, or including Executive Brief metrics / Action Items Kanban/Table views in a Presentation Mode dashboard. |

---

## 3. Formatting Standards

- **Markdown Structure:** Standard Markdown formatting, clean headers, crisp bulleted lists, and aligned tables.
- **Direct Framing:** Output must begin immediately with the document header and conclude directly after the final section without conversational preambles or closings.
- **Direct, Telegraphic Factual Style:** Active, fact-first bullets with zero filler phrases or speaker play-by-play narration across all sections.
- **Valid Markdown Syntax:** Headers, tables, and lists must render cleanly across standard Markdown renderers.
- **Interactive Dashboard Artifact Emission:** When explicitly requested in the prompt (`"yes dashboard"`, `"build dashboard"`, etc.), emit the standalone HTML file as a user-facing artifact named `dashboard.html` (`write_to_file` with `ArtifactMetadata: { UserFacing: true, Summary: "Interactive Evaluation Dashboard", RequestFeedback: false }`).
