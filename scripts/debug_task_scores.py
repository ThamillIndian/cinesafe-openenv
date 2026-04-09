#!/usr/bin/env python3
"""
Audit task scores for strict open interval (0, 1) — excludes 0.0 and 1.0.

Run from repo root:
  python scripts/debug_task_scores.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

# Repo root (parent of scripts/)
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cinesafe_openenv.models import CineSafeAction
from cinesafe_openenv.server.environment import CineSafeEnvironment
from cinesafe_openenv.graders import compute_terminal_score


def _in_open_unit_interval(x: float) -> bool:
    return 0.0 < float(x) < 1.0


def audit_final_scores(d: dict) -> list[tuple[str, float]]:
    bad: list[tuple[str, float]] = []
    for k, v in d.items():
        if isinstance(v, (int, float)) and not _in_open_unit_interval(float(v)):
            bad.append((f"final_scores.{k}", float(v)))
    return bad


def audit_breakdown(b: dict) -> list[tuple[str, float]]:
    bad: list[tuple[str, float]] = []
    for comp in ("risk", "department", "schedule"):
        block = b.get(comp) or {}
        s = block.get("score")
        if isinstance(s, (int, float)) and not _in_open_unit_interval(float(s)):
            bad.append((f"breakdown.{comp}.score", float(s)))
        det = block.get("details")
        if isinstance(det, dict):
            for dk, dv in det.items():
                if isinstance(dv, (int, float)) and not _in_open_unit_interval(float(dv)):
                    bad.append((f"breakdown.{comp}.details.{dk}", float(dv)))
    ai = b.get("ai") or {}
    for ak in ("mitigation_score", "rationale_score"):
        v = ai.get(ak)
        if isinstance(v, (int, float)) and not _in_open_unit_interval(float(v)):
            bad.append((f"breakdown.ai.{ak}", float(v)))
    return bad


def main() -> int:
    env = CineSafeEnvironment()
    exit_code = 0
    for difficulty in ("easy", "medium", "hard"):
        env.reset(difficulty=difficulty)
        env.step(CineSafeAction(action_type="submit_final_plan"))
        state = env.state()
        scenario = env.loader.current_scenario
        terminal = compute_terminal_score(state, scenario)

        fs_bad = audit_final_scores(dict(state.final_scores))
        br_bad = audit_breakdown(terminal.get("breakdown", {}))
        fs = terminal.get("final_score")
        if isinstance(fs, (int, float)) and not _in_open_unit_interval(float(fs)):
            fs_bad.append(("terminal.final_score", float(fs)))

        print(f"--- {difficulty} task_id={state.task_id} ---")
        print("state.final_scores:", json.dumps(state.final_scores, indent=2))
        print("terminal.final_score:", terminal.get("final_score"))
        if fs_bad or br_bad:
            exit_code = 1
            print("VIOLATIONS (must be strictly between 0 and 1):")
            for path, val in fs_bad + br_bad:
                print(f"  {path} = {val!r}")
        else:
            print("OK: no boundary scores detected in audited fields.")
        print()
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
