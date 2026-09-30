# Quality and Compliance Checklist

Use this checklist to audit generated meeting and presentation summaries against required quality, mode selection, structure, and formatting criteria.

---

## 1. Content and Fidelity Standards (Both Modes)

| Criterion | Requirement | Verification Check |
| :--- | :--- | :--- |
| **Mandatory Mode Clarification** | Never assume a default mode if the user only provides a transcript without specifying `"meeting mode"` or `"presentation mode"`. | Confirm the agent asked the user to choose `Meeting Mode` or `Presentation Mode` if unspecified in the prompt. |
| **Pure Factual Grounding and Zero Hallucination** | All statements, numbers, names, slide references, and conclusions derive strictly from what was said in the transcript. | Zero hallucinated facts, invented speakers, unmentioned tools/slides, or fabricated deadlines. |
| **No External Topic Explanations** | Do not generate external explanations, definitions, tutorials, or background commentary on how topics or technologies work. | All content exclusively documents what speakers articulated during the meeting or presentation. |
| **Details of What Was Said** | Specific details, metrics, technical points, constraints, slide walkthroughs, and statements made by speakers are recorded. | Detailed points spoken in the transcript are preserved rather than replaced by vague summaries or external definitions. |
| **Zero Opinion and Editorializing** | No external commentary, personal opinions, editorial assessments, or unstated implications are injected. | All content reports purely what speakers stated, proposed, presented, and decided. |
| **Organization by Mode** | **Meeting Mode:** Grouped by logical subject matter across the meeting.<br>**Presentation Mode:** Grouped in strict chronological order (`1..N`) from start to finish. | **Meeting Mode:** Related discussions are consolidated under topic headers.<br>**Presentation Mode:** Segments follow exact sequential order spoken by the presenter(s). |
| **Explicit Metadata Fallbacks** | Missing owners or dates in action items are explicitly marked; missing transcript date defaults to today's date. | Action item owners marked as `Unassigned` and deadlines marked as `Not Specified` (in Meeting Mode). If the date is not given in the transcript, assume today's date (the date the skill runs) formatted as `YYYY-MM-DD`. |

---

## 2A. Structural Standards — Meeting Mode (`meeting mode`)

| Section | Mandatory Elements | Common Failures to Avoid |
| :--- | :--- | :--- |
| **Document Header** | Meeting Topic, Date (from transcript, or today's date when the skill runs if not given), Participant List. | Missing participants or omitting date instead of defaulting to today's date. |
| **1. Executive Summary** | Meeting Objective, Key Decisions Made, Strategic Outcomes & Impact, Critical Risks & Blockers. | Blending decisions into running paragraphs without clear structure. |
| **2. Detailed Discussion Record** | Subheadings per logical topic with Discussion Details (What Was Said), Points Raised and Rationale, and Key Conclusions. | Providing external topic tutorials instead of documenting what was said, or hallucinating details. |
| **Action Items Table** | 4 columns: `Action Item`, `Assigned To`, `Deadline`, `Acceptance Criteria / Target Deliverable`. | Missing columns, broken table alignment, or hallucinating assignees/deadlines. |
| **3. Five-Sentence Summary** | Exactly five grammatically complete sentences in a single paragraph. | Generating 4 or 6 sentences, or using run-on compound sentences separated by semicolons. |
| **Meeting Mode Dashboard** | Uses `templates/meeting_dashboard_template.html` with 4 tabs (`Executive Brief`, `Knowledge Graph`, `Action Items`, `Detailed Record`). | Emitting a presentation-only dashboard for an interactive meeting. |

---

## 2B. Structural Standards — Presentation Mode (`presentation mode`)

| Section | Mandatory Elements | Common Failures to Avoid |
| :--- | :--- | :--- |
| **Document Header** | Presentation Title (`# Presentation Summary: [Title]`), Date (from transcript, or today's date if not given), Presenter(s) List. | Using `Participants` instead of `Presenter(s)` or omitting the date. |
| **Chronological Presentation Summary** | Sequential numbered subheadings (`### 1. [Segment Title]`, `### 2. [Segment Title]`, ...) with `Presenter` and `What Was Presented & Said`. | Reordering topics non-chronologically or omitting details/metrics spoken during slide walkthroughs. |
| **Strict Omission of Meeting Sections** | Must **NOT** include an Executive Summary, Action Items table, or Five-Sentence Summary. | Including an Executive Summary, fabricating an Action Items table, or appending a 5-Sentence Summary in Presentation Mode. |
| **Presentation Mode Dashboard** | Uses `templates/presentation_dashboard_template.html` opening **directly to the Presentation Knowledge Graph** (with `#1..#N` sequence nodes and Segment Inspector) plus the `Chronological Walkthrough` tab. | Including Executive Brief metrics or Action Items Kanban/Table views in a Presentation Mode dashboard. |

---

## 3. Formatting Standards

- **Markdown Structure:** Standard Markdown formatting, clean headers, bulleted lists, and aligned tables.
- **Direct Framing:** Once the mode is selected, the output must begin immediately with the document header and conclude directly after the final section without conversational preambles or closings.
- **Direct Technical Prose:** Factual and direct language throughout all sections.
- **Valid Markdown Syntax:** Headers, tables, and lists must render cleanly across standard Markdown renderers.
- **Interactive Dashboard Artifact Emission:** When generating or updating the interactive dashboard in either mode, emit the file as a user-facing artifact named `dashboard.html` (`write_to_file` with `ArtifactMetadata: { UserFacing: true, Summary: "Interactive Evaluation Dashboard", RequestFeedback: false }`).
