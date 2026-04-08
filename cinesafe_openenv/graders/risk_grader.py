from typing import Dict, Any, List

def run_risk_grader(state_risks: Dict[str, List[str]], gold: Dict[str, Any]) -> Dict[str, Any]:
    critical = gold.get("critical_risks", [])
    if not critical:
        return {"score": 0.99, "passed": True, "details": "No critical risks needed"}
        
    found_critical = 0
    all_agent_risks = set()
    for s_risks in state_risks.values():
        all_agent_risks.update(s_risks)
        
    for cr in critical:
        if cr in all_agent_risks:
            found_critical += 1
            
    recall = found_critical / len(critical) if critical else 1.0
    recall = max(0.01, min(0.99, recall))
    passed = recall > 0.5
    
    return {
        "score": recall,
        "passed": passed,
        "details": {"recall": recall, "found": list(all_agent_risks)}
    }
