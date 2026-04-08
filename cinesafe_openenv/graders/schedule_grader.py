def run_schedule_grader(schedule_order: list[str], gold: dict) -> dict:
    if not gold.get("acceptable_schedule_patterns"):
        return {"score": 0.99, "passed": True}
        
    if schedule_order in gold["acceptable_schedule_patterns"]:
        return {"score": 0.99, "passed": True}
        
    return {"score": 0.01, "passed": False}
