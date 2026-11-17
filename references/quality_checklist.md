# Quality and Compliance Checklist

Use this checklist to audit generated meeting and presentation summaries against required quality, conciseness, mode selection, structure, and formatting criteria.

---

## 1. Content and Fidelity Standards (Both Modes)

| Criterion | Requirement | Verification Check |
| :--- | :--- | :--- |
| **Default Parameter Resolution & Explicit Overrides (Single-Turn Execution)** | Default to **Meeting Mode** (`"meeting"`), **No Dashboard** (`"no dashboard"`), **No Five-Sentence Summary** (`"no"`), and **No User Action Plan** (`"none"`). Only switch to **Presentation Mode** when explicitly set in the prompt; only build `dashboard.html` when explicitly requested (e.g., `"yes dashboard"` or `"build dashboard"`); only add `Five-Sentence Summary` or `Action Items for [User Name]` when explicitly requested. | Confirm immediate single-turn execution without pausing to prompt for mode, dashboard preference, 5-sentence summary preference, or user name, with defaults or explicit overrides accurately applied. |
| **Anti-Bloat Compression Guardrails** | Output (measured in **total words**, including headings and table cells) MUST ALWAYS be strictly shorter than the cleaned source transcript. Enforce `<= 65%` with proportional scaling for `< 400`-word brief transcripts, target **35%-55%** (`<= 65%` default Meeting ceiling / `< 75%` with optional sections / `<= 60%` Presentation ceiling) for `400-1,500`-word transcripts, **25%-45%** (`<= 50%`) for `1,500-3,000` words, and **10%-25%** (`<= 1,100-1,400` words) for long sessions. | Verify total output word count is strictly less than the cleaned transcript word count and within per-section ceilings -- no book-length expansion. |
| **Zero "He Said / She Said" Narration** | Synthesize directly by topic, technical fact, decision, and action. Ban speaker-turn narration (`"David said"`, `"Sarah noted"`, `"Dr. Thorne explained"`, `"he walked through"`). | Confirm personal names appear only in header metadata, Action Items `Assigned To` / optional `Action Items for [User Name]`, multi-presenter transitions, or material sign-off gates/unresolved disagreements. |
| **Zero Cross-Section Duplication** | State each technical detail, metric, and rationale once. Executive Summary stays high-level; Section 2 holds detailed specs without repeating facts across sub-bullets. | Confirm Executive Summary does not duplicate multi-sentence technical deep dives from Section 2, and Action Items deliverables do not restate the task text. |
| **Complete Detail Retention (Concise != Vague)** | Specific details, metrics, technical points, constraints, slide visuals, decisions, and action items are retained in compressed form. | Zero concrete numbers, technical specifications, constraints, slide benchmarks, or tasks dropped during compression. |
| **Pure Factual Grounding and Zero Hallucination** | All statements, numbers, names, slide references, and conclusions derive strictly from what was said in the transcript. | Zero fabricated facts, invented speakers, unmentioned tools/slides, or fabricated deadlines. |
| **No External Topic Explanations** | Do not generate external explanations, definitions, tutorials, or background commentary on how topics or technologies work. | All content exclusively documents what speakers articulated during the meeting or presentation. |
| **Zero Opinion and Editorializing** | No external commentary, personal opinions, editorial assessments, or unstated implications are injected. | All content reports purely what speakers stated, proposed, presented, and decided. |
| **Organization by Mode** | **Meeting Mode:** Grouped by logical subject matter across the meeting.<br>**Presentation Mode:** Grouped in strict chronological order (`1..N`) from start to finish. | **Meeting Mode:** Related discussions are consolidated under topic headers.<br>**Presentation Mode:** Segments follow exact sequential order spoken by the presenter(s). |
| **Explicit Metadata Fallbacks** | Missing owners or dates in action items are explicitly marked; missing transcript date defaults to today's date. | Action item owners marked as `Unassigned` and deadlines marked as `Not Specified` (in Meeting Mode). If the date is not given in the transcript, assume today's date (the date the skill runs) formatted as `YYYY-MM-DD`. |

---

## 2A. Structural Standards - Meeting Mode (`meeting mode` - Default)

| Section | Mandatory Elements | Common Failures to Avoid |
| :--- | :--- | :--- |
| **Document Header** | Meeting Topic, Date (from transcript, or today's date when the skill runs if not given), Participant List. | Missing participants or omitting date instead of defaulting to today's date. |
| **1. Executive Summary (Default)** | Scannable (`<= 120 words` ceiling; `<= 35-60 words` on `< 400`-word brief transcripts): 1-sentence Meeting Objective (`<= 25 words`), plus direct 1-line bullets (`<= 18 words/bullet`) for Key Decisions Made (max 3-5), Strategic Outcomes & Impact (max 2-4), Critical Risks & Blockers (max 2-4). | Padding short transcripts up to 70+ words, multi-sentence paragraphs, bloated bullets (`> 25 words`), or duplicating full Section 2 technical explanations. |
| **2. Detailed Discussion Record (Default)** | Bullet-first subheadings per logical topic (consolidated into 1 topic on brief single-subject meetings): `Key Points` (2-5 concise bullets, `<= 22 words` each; 1-3 on brief transcripts), conditional `Trade-offs & Rationale` (only when options were weighed), and 1-line `Decision / Status` (`<= 18 words`). | Walls of narrative prose, `"David did/said..."` attribution, repeating the same point across all sub-blocks, or injecting external tutorials. |
| **Action Items Table (Default)** | 4 columns: `Action Item`, `Assigned To`, `Deadline`, `Acceptance Criteria / Target Deliverable` with tight verb-first cells (`<= 15 words/cell`). | Verbose table cells, duplicating task wording in deliverables, broken table alignment, or fabricating assignees/deadlines. |
| **Five-Sentence Summary (Conditional - Default: `no`; Only When User Explicitly Asks)** | Omitted by default. Included as `## 3. Five-Sentence Summary` **only** if explicitly requested in the prompt. Strictly five short, direct, grammatically complete sentences in a single paragraph (`<= 18 words/sentence`, `<= 85 words` total). | Generating the 5-sentence summary when the user did not ask for it, generating 4 or 6 sentences, bloated compound run-ons, or exceeding 85 words. |
| **Action Items for [User Name] (Conditional - Default: `none`; Only When User Name Is Specified)** | Omitted by default. Included **only** if a user name was specified in the prompt (numbered `## 3. Action Items for [User Name]` when 5-Sentence Summary is omitted, or `## 4. Action Items for [User Name]` when both optional sections are requested). Single brief paragraph (`<= 75 words`, 1-3 sentences) combining tasks, deliverables, and deadlines (or one factual sentence if zero tasks). | Generating this section when no user name was provided, skipping `## 3.` to `## 4.` when 5-Sentence Summary is omitted, exceeding 75 words, using a bullet list/table instead of a brief paragraph, or fabricating tasks. |
| **Meeting Mode Dashboard (Conditional - Default: `no dashboard`)** | Skipped by default. When explicitly requested (`"yes dashboard"` / `"build dashboard"`), uses `templates/meeting_dashboard_template.html` with 4 tabs (`Executive Brief`, `Interactive Relationship Node Map`, `Action Items`, `Discussion Record`) and concise, zero-attribution `MEETING_DATA` copy. | Building `dashboard.html` when not requested in the prompt, verbose speaker-narrated JSON strings, or emitting a presentation-only dashboard for an interactive meeting. |

---

## 2B. Structural Standards - Presentation Mode (`presentation mode` - Explicit Override Only)

| Section | Mandatory Elements | Common Failures to Avoid |
| :--- | :--- | :--- |
| **Document Header** | Presentation Title (`# Presentation Summary: [Title]`), Date (from transcript, or today's date if not given), Presenter(s) List. | Using `Participants` instead of `Presenter(s)` or omitting the date. |
| **Chronological Presentation Summary** | Sequential numbered subheadings (`### 1. [Segment Title]`, `### 2. [Segment Title]`, ...) with 3-5 fact-dense bullets (`<= 22 words` each) and inline slide/visual references. Include `- **Presenter:**` ONLY when multiple presenters alternate. | Dense prose paragraphs, `"Dr. Thorne explained..."` / `"he walked through..."` narration, repeating `Presenter:` per segment for a single speaker, reordering chronologically, or omitting spoken metrics. |
| **Strict Omission of Meeting Sections** | Must **NOT** include an Executive Summary, Action Items table, Five-Sentence Summary, or User-Specific Action Items section. | Including an Executive Summary, fabricating an Action Items table, appending a 5-Sentence Summary, or adding user-specific action items in Presentation Mode. |
| **Presentation Mode Dashboard (Conditional - Default: `no dashboard`)** | Skipped by default. When explicitly requested (`"yes dashboard"` / `"build dashboard"`), uses `templates/presentation_dashboard_template.html` opening **directly to the Interactive Relationship Node Map** (with `#1..#N` sequence nodes and Segment Inspector) plus the `Chronological Walkthrough` tab using concise, zero-attribution `PRESENTATION_DATA` copy. | Building `dashboard.html` when not requested in the prompt, verbose speaker-narrated JSON strings, or including Executive Brief metrics / Action Items views in a Presentation Mode dashboard. |

---

## 3. Formatting Standards

- **Markdown Structure:** Standard Markdown formatting, consistent headers, bulleted lists, and aligned tables.
- **Direct Framing:** Output must begin immediately with the document header and conclude directly after the final section without conversational preambles or closings.
- **Direct, Telegraphic Factual Style:** Active, fact-first bullets with zero filler phrases or speaker play-by-play narration across all sections.
- **Valid Markdown Syntax:** Headers, tables, and lists must render accurately across standard Markdown renderers.
- **Interactive Dashboard Output:** When explicitly requested in the prompt (`"yes dashboard"`, `"build dashboard"`, etc.), write the standalone HTML document to `dashboard.html`.
