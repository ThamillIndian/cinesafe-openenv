from .risk_grader import run_risk_grader
from .department_grader import run_department_grader
from .schedule_grader import run_schedule_grader
from .llm_judge import GeminiGrader
from cinesafe_openenv.constants import SCORING_WEIGHTS

def compute_terminal_score(state, scenario) -> dict:
    def _clamp_open_interval(score: float) -> float:
        return max(0.01, min(0.99, float(score)))

    gold = scenario.get("gold", {})
    r_res = run_risk_grader(state.detected_risks, gold)
    d_res = run_department_grader(state.assigned_departments, gold)
    s_res = run_schedule_grader(state.schedule_order, gold)
    
    # AI Qualitative Grading
    ai_grader = GeminiGrader()
    ai_res = ai_grader.grade_qualitative(state, scenario)
    
    # Defaults for budget/mitigation to not block baseline.
    b_score = 0.99
    ai_mitigation = _clamp_open_interval(ai_res.get("mitigation_score", 0.5))

    # Clamp all grader scores to satisfy strict (0,1) validator checks.
    r_res["score"] = _clamp_open_interval(r_res["score"])
    d_res["score"] = _clamp_open_interval(d_res["score"])
    s_res["score"] = _clamp_open_interval(s_res["score"])
    ai_res["mitigation_score"] = ai_mitigation
    
    final_score = (
        SCORING_WEIGHTS["risk"] * r_res["score"] +
        SCORING_WEIGHTS["department"] * d_res["score"] +
        SCORING_WEIGHTS["schedule"] * s_res["score"] +
        SCORING_WEIGHTS["budget"] * b_score +
        SCORING_WEIGHTS["mitigation"] * ai_mitigation
    )
    # Ensure score is strictly between 0 and 1 (exclusive) for validation
    final_score = max(0.01, min(0.99, final_score))
    
    return {
        "final_score": final_score,
        "passed": final_score > 0.7,
        "breakdown": {
            "risk": r_res,
            "department": d_res,
            "schedule": s_res,
            "ai": ai_res
        }
    }
