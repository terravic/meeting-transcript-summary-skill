---
name: meeting-transcript-summary
description: >-
  Analyzes raw meeting transcripts from video conferencing exports, WebVTT, SRT,
  or plain text. Produces a three-tier deliverable: an Executive Summary, a
  Detailed Discussion Record preserving the exact details of what was said, decisions, and a
  structured Action Items table, followed by a strict 5-Sentence Summary. Strictly grounded
  in the transcript with zero hallucination or external explanations.
---

# Meeting Transcript Summary Skill

## Purpose

This skill transforms raw meeting transcripts into structured, high-fidelity documentation. It synthesizes what was discussed into three distinct sections tailored for different stakeholder needs, strictly capturing the specific details, facts, arguments, decision logic, and action items spoken by participants without introducing external explanations, hallucinations, or ungrounded assumptions.

## Operating Principles

- Pure Factual Grounding (Zero Hallucination, Zero Making Things Up): Strictly include only the details, facts, numbers, arguments, and decisions directly and explicitly stated by participants in the transcript. Never make up information, invent names, fabricate numbers, or hallucinate events.
- Strictly Record What Was Said (No External Explanations): Focus exclusively on reporting the specific details of what was spoken during the meeting. Do NOT provide external explanations, definitions, tutorials, or general background explanations about the topics discussed. Only capture the facts, arguments, constraints, and points explicitly raised by the participants.
- Absolute Tone: Deliver factual, direct, and unambiguous synthesis. Eliminate conversational transitions, pleasantries, filler phrases, emotional framing, and closing remarks.
- Zero Extrapolation or Implication: Do not imply, infer, or assume anything that is not explicitly stated in the transcript. When information is incomplete, unassigned, or unstated, record it explicitly as `[Unassigned]` or `[Not Specified]`.
- Clean Professional Formatting: Structure the deliverable using standard Markdown typography, clean headings, bulleted lists, and aligned tables. Do not include graphical placeholders, decorative symbols, or emoticons.
- Zero Preamble and Postamble: Begin output immediately with the document header. End immediately after the final sentence of the third section. Do not include introductory text ("Here is the summary...") or conversational closings ("Let me know if you need changes...").
- Missing Input Handling: If the user requests a summary without providing transcript text or an accessible transcript file path, respond with a single prompt requesting the transcript input and terminate.

## Processing Workflow

Follow these steps sequentially:

```
1. Ingestion & Preprocessing
   ├── Parse speaker tags, timestamps, and diarization markers
   ├── Filter out small talk, greetings, logistics (audio checks), and off-topic banter
   └── Map main discussion topics, distinct arguments, facts, and decisions spoken by participants

2. Section 1 Synthesis: Executive Summary
   ├── Identify primary meeting objective as stated by participants
   ├── Extract strategic decisions and core outcomes agreed upon in the meeting
   └── Summarize impacts and blockers explicitly mentioned in the discussion

3. Section 2 Synthesis: Detailed Discussion Record & Action Items
   ├── Structure by logical topic discussed in the meeting
   ├── Extract and record the specific details of what was said by participants for each topic
   ├── Document the specific points, arguments, trade-offs, and rationale spoken by participants
   ├── Strictly avoid external explanations, tutorials, or unmentioned concept definitions
   └── Compile and format the Action Items table with exact column sizing

4. Section 3 Synthesis: Five-Sentence Summary
   ├── Draft exactly five grammatically complete, high-density sentences summarizing what was said
   └── Verify sentence count equals five before finalizing

5. Dashboard Generation (When Interactive Web Dashboard is requested)
   ├── Ingest the synthesized meeting data (KPIs, decisions, topics, rationale, action items)
   ├── Populate data schema into the dashboard template (SVG knowledge graph, Kanban board, topic inspector)
   └── Emit dashboard.html as a user-facing artifact via write_to_file
```

---

## Output Structure Specification

Format the generated document using standard Markdown as specified below:

# Meeting Summary: [Insert Meeting Topic / Project Name]

**Date:** [YYYY-MM-DD or As Stated in Transcript]  
**Participants:** [Comma-separated list of active participants identified in transcript]

---

## 1. Executive Summary

Provide a concise, high-level overview for leadership and key stakeholders based strictly on what was stated in the meeting:
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

#### Table Formatting Rules:
1. Always include all four columns.
2. If an action item has no designated owner stated in the transcript, write `Unassigned`. Do not guess names or make up assignees.
3. If no timeline or target date was agreed upon, write `Not Specified`. Do not invent deadlines.
4. Ensure Markdown table syntax is valid and cleanly aligned.

---

## 3. Five-Sentence Summary

A single paragraph containing exactly five complete, high-density sentences summarizing what was said, key decisions, and next steps:

[Sentence 1: Context and primary purpose of the meeting.] [Sentence 2: Core technical or strategic challenge addressed.] [Sentence 3: Primary decision or consensus reached.] [Sentence 4: Major secondary outcome, resource commitment, or architectural shift.] [Sentence 5: Immediate next milestone and critical path timeline.]

---

## Output Format Modes

The skill supports four delivery modes based on user requirements:

1. **Rendered Markdown (Default):** Output standard Markdown directly to the chat stream. The host agent harness automatically parses and renders this into visual rich text with styled headers, structured bullet lists, and graphical tables. This format is optimized for non-technical users to select, copy, and paste directly into document editors, wikis, or email without losing styling.
2. **Raw Markdown Code Block:** When prompted for "raw markdown", wrap the complete output inside a fenced code block (` ```markdown ... ``` `) with a one-click copy button, allowing immediate transfer into code repositories or `.md` files.
3. **Dual Output Mode:** When prompted for "dual output" or "both rendered and raw", deliver the complete rendered output first, followed by a divider and a fenced code block containing the exact raw Markdown.
4. **Interactive Web Dashboard Mode:** When prompted for "dashboard", "visual UI", or "interactive summary", generate a self-contained HTML/JS/CSS document implementing the interactive Executive Overview, SVG Knowledge Graph with Topic Inspector, Multi-View Action Items (Kanban board by owner and sortable data table), and a Light/Dark Mode toggle button (SVG toggle for seamless theme switching) following the reference guide in `references/dashboard_ui_guide.md` and template in `templates/meeting_dashboard_template.html`.
   - **Artifact Emission Requirement:** When generating or updating the interactive HTML dashboard, you MUST emit the standalone HTML file as a user-facing artifact named `dashboard.html` (using `write_to_file` with `ArtifactMetadata: { UserFacing: true, Summary: "Interactive Evaluation Dashboard", RequestFeedback: false }`). This ensures the dashboard immediately opens and renders directly in the agent harness preview pane with no need to manually copy or open links in a browser.

---

## Content Evaluation Rubric

Before outputting the response, verify compliance against these standards:

1. **Sentence Count:** Confirm that Section 3 contains exactly 5 terminal periods corresponding to 5 complete sentences.
2. **Details of What Was Said:** Verify that Section 2 captures the precise details, facts, numbers, and statements spoken by participants, rather than generic summaries.
3. **No External Explanations or Hallucinations:** Verify that zero external explanations, definitions, unmentioned concepts, or hallucinated facts have been added. Everything in the summary must be directly traceable to participant dialogue in the transcript.
4. **Preservation of Spoken Rationale:** Confirm that the reasoning, trade-offs, and counter-arguments explicitly stated by participants are accurately documented.
5. **Tone and Style Check:** Verify that the output maintains an objective business tone with zero conversational pleasantries and zero meta-commentary.
6. **Pure Factual Grounding & Zero Opinion:** Verify that all facts, numbers, dates, technical claims, arguments, and deliverables derive solely from what was said in the transcript. Confirm that zero personal opinions, editorial interpretations, external advice, or unstated implications were added.
