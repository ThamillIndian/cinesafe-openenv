from .risk_grader import run_risk_grader
from .department_grader import run_department_grader
from .schedule_grader import run_schedule_grader
from .llm_judge import GeminiGrader
from cinesafe_openenv.constants import SCORING_WEIGHTS

def compute_terminal_score(state, scenario) -> dict:
    gold = scenario.get("gold", {})
    r_res = run_risk_grader(state.detected_risks, gold)
    d_res = run_department_grader(state.assigned_departments, gold)
    s_res = run_schedule_grader(state.schedule_order, gold)
    
    # AI Qualitative Grading
    ai_grader = GeminiGrader()
    ai_res = ai_grader.grade_qualitative(state, scenario)
    
    # Defaults for budget/mitigation to not block baseline 
    b_score = 1.0 
    
    final_score = (
        SCORING_WEIGHTS["risk"] * r_res["score"] +
        SCORING_WEIGHTS["department"] * d_res["score"] +
        SCORING_WEIGHTS["schedule"] * s_res["score"] +
        SCORING_WEIGHTS["budget"] * b_score +
        SCORING_WEIGHTS["mitigation"] * ai_res["mitigation_score"]
    )
    
    # Optional logic to clamp if catastrophic failure in schedule or safety
    if not r_res["passed"]:
        final_score = min(final_score, 0.4)
        
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
