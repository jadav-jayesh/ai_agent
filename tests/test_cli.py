import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "bin" / "ai-agent"


class AgentCliTests(unittest.TestCase):
    def run_cli(self, *args, env=None, cwd=None):
        merged_env = os.environ.copy()
        merged_env["AI_AGENT_HOME"] = str(ROOT)
        merged_env["GROQ_API_KEY"] = merged_env.get("GROQ_API_KEY", "dummy")
        if env:
            merged_env.update(env)
        return subprocess.run(["python3", str(CLI), *args], cwd=cwd or ROOT, env=merged_env, text=True, capture_output=True)

    def test_agents_lists_markdown_agents(self):
        result = self.run_cli("agents")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("planner", result.stdout)
        self.assertIn("docs", result.stdout)

    def test_analyze_works_on_another_project(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            (temp / "src").mkdir()
            (temp / "src" / "main.py").write_text("print('hi')\n", encoding="utf-8")
            (temp / "requirements.txt").write_text("fastapi==0.1\n", encoding="utf-8")
            result = self.run_cli("analyze", "--project", str(temp))
            self.assertEqual(result.returncode, 0, result.stderr)
            parsed = json.loads(result.stdout)
            self.assertIn("python", parsed["languages"])
            self.assertIn("FastAPI", parsed["frameworks"])

    def test_doctor_passes_with_dummy_env(self):
        result = self.run_cli("doctor")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Configuration looks good", result.stdout)


if __name__ == "__main__":
    unittest.main()