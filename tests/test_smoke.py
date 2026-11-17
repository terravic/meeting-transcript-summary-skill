#!/usr/bin/env python3
"""Automated smoke, security, and accessibility verification suite."""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "scripts"))

import clean_transcript  # noqa: E402


class TestCleanTranscript(unittest.TestCase):
    def test_vtt_cleaning_and_consolidation(self):
        raw_vtt = (
            "WEBVTT\n\n"
            "1\n"
            "00:00:01.000 --> 00:00:04.500\n"
            "Jane Doe: Welcome everyone.\n\n"
            "2\n"
            "00:00:05.000 --> 00:00:08.000\n"
            "Jane Doe: Today we review Q3 goals.\n\n"
            "3\n"
            "00:00:09.000 --> 00:00:12.000\n"
            "John Smith: Latency dropped to 14ms.\n\n"
            "4\n"
            "00:00:13.000 --> 00:00:15.000\n"
            "John Smith: Throughput reached 65k QPS.\n"
        )
        cleaned = clean_transcript.clean_transcript(raw_vtt)
        self.assertNotIn("WEBVTT", cleaned)
        self.assertNotIn("-->", cleaned)
        self.assertIn("Jane Doe: Welcome everyone.", cleaned)
        self.assertIn("John Smith: Latency dropped to 14ms. Throughput reached 65k QPS.", cleaned)

    def test_srt_cleaning(self):
        raw_srt = (
            "1\n"
            "00:00:01,000 --> 00:00:04,500\n"
            "Alice: First point.\n\n"
            "2\n"
            "00:00:05,000 --> 00:00:09,000\n"
            "Bob: Second point.\n"
        )
        cleaned = clean_transcript.clean_transcript(raw_srt)
        self.assertNotIn("00:00:01,000", cleaned)
        self.assertIn("Alice: First point.", cleaned)
        self.assertIn("Bob: Second point.", cleaned)

    def test_cli_stdout_output_and_size_guard(self):
        sample_in = os.path.join(REPO_ROOT, "examples", "sample_meeting_transcript.txt")
        script_path = os.path.join(REPO_ROOT, "scripts", "clean_transcript.py")
        proc = subprocess.run(
            [sys.executable, script_path, sample_in],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("Sarah Lin:", proc.stdout)
        self.assertNotIn("[00:00:02]", proc.stdout)

        with tempfile.NamedTemporaryFile("r+", suffix=".txt", delete=True) as tmp:
            subprocess.run(
                [sys.executable, script_path, sample_in, "--output", tmp.name],
                capture_output=True,
                text=True,
                check=True,
            )
            self.assertIn("Marcus Vance:", tmp.read())

        env = dict(os.environ, CLEAN_TRANSCRIPT_MAX_BYTES="128")
        rejected = subprocess.run(
            [sys.executable, script_path, sample_in],
            capture_output=True,
            text=True,
            env=env,
        )
        self.assertNotEqual(rejected.returncode, 0)
        self.assertIn("exceeds limit", rejected.stderr)


class TestSkillAndDashboardContracts(unittest.TestCase):
    HTML_FILES = [
        "dashboard.html",
        "templates/meeting_dashboard_template.html",
        "templates/presentation_dashboard_template.html",
        "examples/sample_meeting_dashboard.html",
        "examples/sample_presentation_dashboard.html",
    ]

    def test_skill_frontmatter_and_sections(self):
        skill_path = os.path.join(REPO_ROOT, "SKILL.md")
        with open(skill_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertTrue(content.startswith("---\nname: meeting-transcript-summary\n"))
        self.assertIn("## 1. Executive Summary", content)
        self.assertIn("## 2. Detailed Discussion Record and Action Items", content)
        self.assertIn("## Chronological Presentation Summary", content)

    def test_html_security_and_wcag_contracts(self):
        for rel in self.HTML_FILES:
            full = os.path.join(REPO_ROOT, rel)
            self.assertTrue(os.path.isfile(full), f"Missing {rel}")
            with open(full, "r", encoding="utf-8") as f:
                html = f.read()
            self.assertIn("<!DOCTYPE html>", html)
            self.assertIn('http-equiv="Content-Security-Policy"', html)
            self.assertIn("connect-src 'none'", html)
            self.assertIn("font-src 'none'", html)
            self.assertIn("function escapeHtml(", html)
            self.assertIn("function sanitizeHexColor(", html)
            self.assertIn("function sanitizeCsvCell(", html)
            self.assertNotIn("DM Sans", html)
            self.assertNotIn("fonts.googleapis.com", html)
            self.assertNotIn("fonts.gstatic.com", html)
            self.assertIn('role="tablist"', html)
            self.assertIn('role="tab"', html)
            self.assertIn('role="tabpanel"', html)
            self.assertIn(":focus-visible", html)
            self.assertIn("<footer", html)
            self.assertEqual(len(re.findall(r"<h1\b", html)), 1, f"Expected single h1 in {rel}")

    def test_headless_browser_dom_and_xss_neutralization(self):
        chrome_bin = shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
        if not chrome_bin:
            self.skipTest("Headless Chromium binary not available")

        # 1. Verify all 5 dashboards render cleanly in headless Chromium
        for rel in self.HTML_FILES:
            full = os.path.join(REPO_ROOT, rel)
            dom = subprocess.check_output(
                [chrome_bin, "--headless=new", "--disable-gpu", "--no-sandbox", "--dump-dom", f"file://{full}"],
                stderr=subprocess.DEVNULL,
                text=True,
            )
            self.assertIn('id="display-title"', dom)
            self.assertIn('id="graph-nodes-layer"', dom)

        # 2. Inject adversarial XSS + CSV formula payload into meeting template and verify escaping
        tpl_path = os.path.join(REPO_ROOT, "templates", "meeting_dashboard_template.html")
        with open(tpl_path, "r", encoding="utf-8") as f:
            tpl_html = f.read()

        adversarial_data = {
            "mode": "meeting",
            "meetingTitle": "<img src=x onerror=\"document.body.dataset.pwned='1'\">",
            "date": "2026-08-14",
            "participants": ["<script>document.body.dataset.pwned='2'</script>"],
            "metrics": {"decisionsCount": 1, "topicsCount": 1, "actionsCount": 1, "targetCutover": "2026-10-03"},
            "executiveSummary": {
                "objective": "Verify escaping",
                "decisions": ["<svg onload=\"document.body.dataset.pwned='3'\">"],
                "impacts": ["Safe impact"],
                "risks": ["Safe risk"],
            },
            "topics": [
                {
                    "id": "topic-1",
                    "title": "<b onmouseover=alert(1)>Topic</b>",
                    "shortTitle": "<img src=x>",
                    "color": "javascript:alert(1)",
                    "context": "<iframe src='https://example.com'></iframe>",
                    "explanation": "Details",
                    "rationale": "Rationale",
                    "conclusion": "Done",
                }
            ],
            "relationships": [],
            "actionItems": [
                {
                    "id": "act-1",
                    "description": "=CMD|' /C calc'!A0",
                    "assignee": "<img src=x onerror=alert(1)>",
                    "deadline": "2026-09-01",
                    "deliverable": "@SUM(1+1)",
                }
            ],
        }

        injected_html = re.sub(
            r"const MEETING_DATA = \{[\s\S]*?\n    \};",
            "const MEETING_DATA = " + json.dumps(adversarial_data) + ";\n"
            "    window.addEventListener('DOMContentLoaded', () => {\n"
            "      document.body.setAttribute('data-csv-check', sanitizeCsvCell(MEETING_DATA.actionItems[0].description));\n"
            "    });",
            tpl_html,
            count=1,
        )

        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tmp_html:
            tmp_html.write(injected_html)
            tmp_html_path = tmp_html.name

        try:
            dom = subprocess.check_output(
                [chrome_bin, "--headless=new", "--disable-gpu", "--no-sandbox", "--dump-dom", f"file://{tmp_html_path}"],
                stderr=subprocess.DEVNULL,
                text=True,
            )
            self.assertNotIn("data-pwned=", dom)
            self.assertNotIn("<iframe src=", dom)
            self.assertIn("&lt;svg onload=", dom)
            self.assertIn("data-csv-check=\"'&#39;=CMD|", dom.replace("'", "&#39;"))
        finally:
            os.unlink(tmp_html_path)


if __name__ == "__main__":
    unittest.main(verbosity=2)
