# Quality and Compliance Checklist

Use this checklist to audit generated meeting summaries against required quality, structure, and style criteria.

---

## 1. Content and Fidelity Standards

| Criterion | Requirement | Verification Check |
| :--- | :--- | :--- |
| **Pure Factual Grounding & Zero Hallucination** | All statements, numbers, names, and conclusions derive strictly from what was said in the transcript. | Zero hallucinated facts, invented participants, unmentioned tools, or fabricated deadlines. |
| **No External Topic Explanations** | Do not generate external explanations, definitions, tutorials, or background commentary on how topics or technologies work. | All content exclusively documents what participants articulated during the meeting. |
| **Details of What Was Said** | Specific details, metrics, technical points, constraints, and statements made by participants are recorded. | Detailed points spoken by participants are preserved rather than replaced by vague summaries or external definitions. |
| **Preservation of the "Why"** | Debates, trade-offs, discarded alternatives, and reasoning spoken by participants are explicitly documented. | The narrative explains why decisions were made as articulated in the meeting, not merely what was decided. |
| **Zero Opinion & Editorializing** | No external commentary, personal opinions, editorial assessments, or unstated implications are injected. | All content reports purely what participants stated, proposed, and decided. |
| **Topic-Based Organization** | Discussions are grouped by logical subject matter rather than chronological transcript order. | Related discussions across different time points in the meeting are consolidated cleanly under relevant topic headers. |
| **Explicit Metadata Fallbacks** | Missing owners or dates in action items are explicitly marked; missing meeting date defaults to today's date. | Action item owners marked as `Unassigned` and deadlines marked as `Not Specified` when unstated. If the meeting date is not given in the transcript, assume today's date (the date the skill runs) formatted as `YYYY-MM-DD`. |

---

## 2. Structural Standards

| Section | Mandatory Elements | Common Failures to Avoid |
| :--- | :--- | :--- |
| **Document Header** | Meeting Topic, Date (from transcript, or today's date when the skill runs if not given), Participant List. | Missing participants or omitting date instead of defaulting to today's date. |
| **1. Executive Summary** | Meeting Objective, Key Decisions Made, Strategic Outcomes & Impact, Critical Risks & Blockers. | Blending decisions into running paragraphs without clear structure. |
| **2. Detailed Discussion Record** | Subheadings per topic with Discussion Details (What Was Said), Points Raised and Rationale, and Key Conclusions. | Providing external topic tutorials instead of documenting what was said, or hallucinating details. |
| **Action Items Table** | 4 columns: `Action Item`, `Assigned To`, `Deadline`, `Acceptance Criteria / Target Deliverable`. | Missing columns, broken table alignment, or hallucinating assignees/deadlines. |
| **3. Five-Sentence Summary** | Exactly five grammatically complete sentences in a single paragraph. | Generating 4 or 6 sentences, or using run-on compound sentences separated by semicolons. |

---

## 3. Formatting and Tone Standards

- **Professional Typography:** Standard markdown formatting, clean headers, and structured tables without decorative embellishments.
- **Direct Framing:** The output must begin immediately with the document header and conclude directly after the final sentence without conversational preambles or closings.
- **Direct Business Language:** Professional, factual, and direct prose.
- **Valid Markdown Syntax:** Headers, tables, and lists must render cleanly across standard Markdown renderers.
- **Interactive Dashboard Artifact Emission:** When generating or updating the interactive dashboard, emit the file as a user-facing artifact named `dashboard.html` (`write_to_file` with `ArtifactMetadata: { UserFacing: true, Summary: "Interactive Evaluation Dashboard", RequestFeedback: false }`).
