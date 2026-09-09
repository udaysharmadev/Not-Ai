import subprocess
import sys
import unittest
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


if __name__ == "__main__":
    unittest.main()
