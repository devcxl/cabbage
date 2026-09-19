from importlib import resources
import re
import unittest

import yaml


CORE_TEMPLATE_HEADINGS = {
    "prd.md": [
        "# Goal",
        "# Users and Use Cases",
        "# Scope",
        "# Requirements",
        "# Acceptance Criteria",
        "# Success Metrics",
        "# Dependencies and Constraints",
        "# Risks",
        "# Open Questions",
    ],
    "impact.md": [
        "# Change Summary",
        "# Impact Matrix",
        "# Impact Details",
        "# Risks",
        "# Documentation Updates",
    ],
    "tech-spec.md": [
        "# Context",
        "# Requirements",
        "# Design",
        "# Alternatives",
        "# Security and Privacy",
        "# Observability",
        "# Failure Modes",
        "# Rollout",
        "# Rollback",
        "# Open Questions",
    ],
    "test-plan.md": [
        "# Strategy",
        "# Test Environment and Data",
        "# Cases",
        "# Regression Coverage",
        "# Non-functional Testing",
        "# Entry and Exit Criteria",
        "# Risks",
    ],
    "tasks.md": ["# Preparation", "# Tasks", "# Verification"],
    "release-plan.md": [
        "# Release Summary",
        "# Preconditions",
        "# Deployment",
        "# Rollback",
        "# Verification",
        "# Monitoring",
        "# Communication",
    ],
}

SPECIALIZED_TEMPLATE_HEADINGS = {
    "adr.md": [
        "# Status",
        "# Context",
        "# Decision Drivers",
        "# Considered Options",
        "# Decision",
        "# Consequences",
        "# Validation",
    ],
    "api-design.md": [
        "# Overview",
        "# Contract",
        "# Error Model",
        "# Compatibility",
        "# Security",
        "# Observability",
    ],
    "database-design.md": [
        "# Summary",
        "# Schema",
        "# Migration",
        "# Data Verification",
        "# Compatibility and Operations",
        "# Rollback",
    ],
    "security-review.md": [
        "# Scope and Assets",
        "# Threats",
        "# Controls",
        "# Residual Risks",
        "# Verification",
    ],
    "rfc.md": [
        "# Summary",
        "# Problem",
        "# Goals and Non-goals",
        "# Proposal",
        "# Alternatives",
        "# Compatibility and Migration",
        "# Risks",
        "# Open Questions",
    ],
    "incident.md": [
        "# Incident Metadata",
        "# Impact",
        "# Detection",
        "# Timeline",
        "# Mitigation",
        "# Recovery Verification",
        "# Communications",
    ],
    "postmortem.md": [
        "# Summary",
        "# Impact and Detection",
        "# Root Cause",
        "# Contributing Factors",
        "# Response Assessment",
        "# Corrective Actions",
        "# Lessons Learned",
    ],
    "generic.md": ["# Summary", "# Content", "# Decisions and Follow-up"],
}


class TemplateTest(unittest.TestCase):
    def assert_heading(self, text, heading):
        pattern = rf"^#+\s+{re.escape(heading.lstrip('# '))}\s*$"
        self.assertRegex(text, re.compile(pattern, flags=re.M | re.I))

    def test_core_templates_contain_review_structure(self):
        template_dir = resources.files("cabbage_cli").joinpath("assets", "templates")

        for filename, headings in CORE_TEMPLATE_HEADINGS.items():
            with self.subTest(template=filename):
                text = template_dir.joinpath(filename).read_text(encoding="utf-8")
                for heading in headings:
                    self.assert_heading(text, heading)
                self.assertIn("<!-- CABBAGE:", text)

    def test_templates_satisfy_workflow_heading_contracts(self):
        assets = resources.files("cabbage_cli").joinpath("assets")

        for workflow_path in assets.joinpath("workflows").iterdir():
            if workflow_path.suffix != ".yaml":
                continue
            workflow = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))
            for stage in workflow["stages"]:
                template = assets.joinpath("templates", stage["template"])
                text = template.read_text(encoding="utf-8")
                for heading in stage.get("required_headings", []):
                    pattern = rf"^#+\s+{re.escape(heading)}\s*$"
                    self.assertRegex(text, re.compile(pattern, flags=re.M | re.I))

    def test_impact_template_preserves_sync_rows(self):
        from cabbage_cli.scaffold import IMPACT_FIELDS
        template = resources.files("cabbage_cli").joinpath(
            "assets", "templates", "impact.md"
        )
        text = template.read_text(encoding="utf-8")
        sync_labels = {
            "product": "Product",
            "architecture": "Architecture",
            "api": "API",
            "database": "Database",
            "security": "Security",
            "testing": "Testing",
            "deployment": "Deployment",
            "operations": "Operations",
            "performance": "Performance",
        }
        # Every declared impact field needs a syncable table row, and the
        # template must not carry rows for fields the CLI no longer accepts.
        for field in IMPACT_FIELDS:
            with self.subTest(field=field):
                self.assertIn(field, sync_labels, "no table label for this impact field")
                self.assertRegex(text, rf"(?m)^\| {sync_labels[field]} \| (?:Yes|No) \|")
        self.assertEqual(set(IMPACT_FIELDS), set(sync_labels))
        self.assertNotRegex(text, r"(?m)^\| Data \| (?:Yes|No) \|")

    def test_specialized_templates_contain_review_structure(self):
        template_dir = resources.files("cabbage_cli").joinpath("assets", "templates")

        for filename, headings in SPECIALIZED_TEMPLATE_HEADINGS.items():
            with self.subTest(template=filename):
                text = template_dir.joinpath(filename).read_text(encoding="utf-8")
                for heading in headings:
                    self.assert_heading(text, heading)
                self.assertIn("<!-- CABBAGE:", text)


if __name__ == "__main__":
    unittest.main()
