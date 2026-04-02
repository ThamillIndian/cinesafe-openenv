from typing import Dict, Any, List

def run_department_grader(state_deps: Dict[str, List[str]], gold: Dict[str, Any]) -> Dict[str, Any]:
    required = gold.get("required_departments", [])
    if not required:
        return {"score": 1.0, "passed": True, "details": "No required departments"}
        
    found_deps = set()
    for deps in state_deps.values():
        found_deps.update(deps)
        
    matched = sum(1 for d in required if d in found_deps)
    score = matched / len(required)
    
    # Penalty for massive over-assignment could be added here
    passed = score >= 0.8
    
    return {
        "score": score,
        "passed": passed,
        "details": {"score": score, "assigned": list(found_deps)}
    }
