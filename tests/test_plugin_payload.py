import subprocess
import sys
import unittest
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/not-ai"


class PluginPayloadTests(unittest.TestCase):
    def test_plugin_contains_its_runtime_gate(self):
        self.assertTrue((PLUGIN / "tools/gate.py").is_file())
        self.assertTrue((PLUGIN / "tools/not_ai_core/gate.py").is_file())

    def test_skill_documents_the_bundled_tool(self):
        skill = (PLUGIN / "skills/not-ai/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("tools/gate.py", skill)

    def test_skill_requires_source_grounded_editing(self):
        skill = (PLUGIN / "skills/not-ai/SKILL.md").read_text(encoding="utf-8")
        self.assertIn(
            "Never invent an experience, opinion, uncertainty, quote, source, result, name, "
            "number, or sensory detail if given.",
            skill,
        )
        self.assertIn("AI-detector scores", skill)
        self.assertIn("Do not force a rewrite", skill)
        self.assertIn("Never add Em Dashes", skill)
        self.assertIn("before sending newly authored prose, check for the `—` character", skill)
        self.assertIn("replace every instance", skill)
        self.assertIn("Default to the fullest useful result", skill)
        self.assertIn("write a complete, detailed draft from scratch", skill)
        self.assertIn("rewrite it to its full potential", skill)
        self.assertNotIn("Default to `fast`", skill)
        self.assertIn("Do not ask for writing samples", skill)
        self.assertIn("Use `student` when running the bundled gate", skill)
        self.assertNotIn("scores 0-5%", skill)
        self.assertNotIn("micro-imperfection", skill)

    def test_references_do_not_turn_population_patterns_into_targets(self):
        references = PLUGIN / "skills/not-ai/reference"
        combined = "\n".join(
            path.read_text(encoding="utf-8") for path in sorted(references.glob("*.md"))
        )
        self.assertNotIn('"Ceiling" is the target', combined)
        self.assertNotIn('"Floor" is the target', combined)
        self.assertNotIn("for dating suspected text", combined)
        self.assertNotIn("Zero em dashes", combined)
        self.assertNotIn("ZeroGPT", combined)

    def test_local_skill_copy_matches_canonical_skill(self):
        local_copy = (ROOT / ".claude/skills/not-ai.md").read_text(encoding="utf-8")
        canonical = (PLUGIN / "skills/not-ai/SKILL.md").read_text(encoding="utf-8")
        self.assertEqual(local_copy, canonical)

    def test_sync_skill_check_passes(self):
        completed = subprocess.run(
            [sys.executable, str(ROOT / "scripts/sync_skill.py"), "--check"],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)

    def test_repository_wrapper_runs_the_plugin_tool(self):
        completed = subprocess.run(
            [sys.executable, str(ROOT / "scripts/gate.py"), "--stdin", "--json"],
            input="A short, plain sentence.",
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn('"passed": true', completed.stdout)

    def test_repository_wrapper_enforces_explicit_protected_text(self):
        completed = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/gate.py"),
                "--stdin",
                "--json",
                "--protect",
                "Nagpur",
            ],
            input="The event happened on Tuesday.",
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 1, completed.stderr)
        self.assertIn('"rule": "protected-content"', completed.stdout)

    def test_benchmark_corpus_covers_rewrite_and_no_change(self):
        completed = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/benchmark.py"),
                "--corpus",
                str(ROOT / "benchmarks/corpus"),
                "--json",
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        results = json.loads(completed.stdout)
        actions = {
            item["expected_action_check"]["expected_action"]: item["expected_action_check"]
            for item in results
        }
        self.assertEqual(actions["no-change"]["assessment"], "matched")
        self.assertEqual(actions["rewrite"]["assessment"], "matched")


if __name__ == "__main__":
    unittest.main()
