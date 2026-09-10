from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PIPELINE = ROOT / "scripts" / "pipeline_manager.py"
QUALITY_GATE = ROOT / "scripts" / "quality_gate.py"
A_GRAPH = ROOT / "research" / "cumcm_excellence" / "regression_cases" / "2026_A_problem_graph.json"


def load_quality_gate():
    spec = importlib.util.spec_from_file_location("quality_gate_under_test", QUALITY_GATE)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


class PipelinePlanTests(unittest.TestCase):
    def run_pipeline(self, cwd: Path, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(PIPELINE), *args],
            cwd=cwd,
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
        )

    def test_cumcm_questions_are_distinct_from_model_units_and_dependencies(self):
        with tempfile.TemporaryDirectory() as raw:
            cwd = Path(raw)
            result = self.run_pipeline(
                cwd, "init", "--mode", "ap", "--contest", "CUMCM",
                "--questions", "4", "--model-map", str(A_GRAPH),
            )
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            state_path = cwd / "CUMCM_Workspace" / "state" / "pipeline.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual(state["question_count"], 4)
            self.assertEqual(state["model_unit_count"], 2)
            self.assertEqual(state["question_to_model"]["Q3"], "M1")
            self.assertEqual(state["model_units"][1]["depends_on"], ["M1"])
            self.assertNotIn("model_3_build", state["stages"])

            state["stages"]["data_preprocessing"]["status"] = "approved"
            state_path.write_text(json.dumps(state), encoding="utf-8")
            suggested = self.run_pipeline(cwd, "suggest-parallel")
            self.assertEqual(suggested.stdout.strip(), "model_1_build")

            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["stages"]["model_1_build"]["status"] = "approved"
            state_path.write_text(json.dumps(state), encoding="utf-8")
            suggested = self.run_pipeline(cwd, "suggest-parallel")
            self.assertEqual(suggested.stdout.strip(), "model_1_verify")

            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["stages"]["model_1_verify"]["status"] = "approved"
            state_path.write_text(json.dumps(state), encoding="utf-8")
            suggested = self.run_pipeline(cwd, "suggest-parallel")
            self.assertEqual(suggested.stdout.strip(), "model_2_build")

    def test_mcm_keeps_legacy_stage_shape(self):
        with tempfile.TemporaryDirectory() as raw:
            cwd = Path(raw)
            result = self.run_pipeline(
                cwd, "init", "--mode", "ap", "--contest", "MCM", "--problems", "2"
            )
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            state = json.loads(
                (cwd / "CUMCM_Workspace" / "state" / "pipeline.json").read_text(encoding="utf-8")
            )
            self.assertIn("model_3_build", state["stages"])
            self.assertNotIn("question_count", state)
            self.assertNotIn("stage_order", state)


class EvidenceGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "CUMCM_Workspace"
        (self.root / "data").mkdir(parents=True)
        (self.root / "memory").mkdir(parents=True)
        (self.root / "data" / "input.xlsx").write_bytes(b"fixture")
        self.gate = load_quality_gate()
        self.gate.WORKSPACE = self.root

    def tearDown(self):
        self.temp.cleanup()

    def write_contract(self, ambiguity_status="resolved") -> Path:
        path = self.root / "memory" / "artifact_contract.json"
        path.write_text(json.dumps({
            "contest": "CUMCM",
            "inputs": [{
                "id": "input1", "path": "data/input.xlsx",
                "schema": {"columns": ["enterprise_id", "credit_rating", "revenue"]},
                "units": {"enterprise_id": "identifier", "credit_rating": "category", "revenue": "CNY"},
                "processing": ["validate identifiers and missing categories"],
            }],
            "deliverables": [{
                "id": "result1", "path": "output/result1.xlsx", "required": True,
                "schema": {"sheets": ["Sheet1"]},
                "source_evidence": ["problem.pdf#page=3"],
                "validation": ["sheet names"],
            }],
            "ambiguities": [{
                "id": "A1", "location": "problem.pdf#page=3",
                "description": "surface-column convention", "status": ambiguity_status,
            }],
        }), encoding="utf-8")
        return path

    def test_artifact_contract_warns_for_open_ambiguity(self):
        path = self.write_contract("open")
        status, message = self.gate.gate_artifact_contract(str(path))
        self.assertEqual(status, "WARN")
        self.assertIn("remains open", message)

    def test_evidence_ledger_requires_all_questions_and_deliverables(self):
        contract = self.write_contract()
        graph = self.root / "memory" / "problem_graph.json"
        graph.write_text(json.dumps({"questions": [{"id": "Q1"}]}), encoding="utf-8")
        ledger = self.root / "memory" / "evidence_ledger.json"
        ledger.write_text(json.dumps({"entries": [{
            "id": "C1", "claim": "verified result", "core": True, "status": "verified",
            "questions": ["Q1"], "deliverables": ["result1"],
            "evidence_locations": ["state/result.json:value"],
        }]}), encoding="utf-8")
        status, _ = self.gate.gate_evidence_ledger(str(ledger), str(graph), str(contract))
        self.assertEqual(status, "PASS")

        ledger.write_text(json.dumps({"entries": [{
            "id": "C1", "claim": "incomplete", "core": True, "status": "verified",
            "questions": [], "deliverables": [], "evidence_locations": ["state/result.json:value"],
        }]}), encoding="utf-8")
        status, message = self.gate.gate_evidence_ledger(str(ledger), str(graph), str(contract))
        self.assertEqual(status, "FAIL")
        self.assertIn("Q1", message)
        self.assertIn("result1", message)


if __name__ == "__main__":
    unittest.main()
