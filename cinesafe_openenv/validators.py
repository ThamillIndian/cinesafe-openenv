from cinesafe_openenv.models import CineSafeAction, CineSafeState

def validate_action(action: CineSafeAction, state: CineSafeState):
    """
    Validates if an action is semantically correct given the current state.
    Raises ValueError if action is invalid.
    """
    valid_actions = [
        "analyze_scene", "flag_risk", "assign_departments", 
        "estimate_scene_cost", "cluster_scenes", "reorder_schedule", 
        "propose_mitigation", "request_more_context", "submit_final_plan"
    ]
    
    if action.action_type not in valid_actions:
        raise ValueError(f"Unknown action type: {action.action_type}")
        
    if state.done:
        raise ValueError("Scenario is already done. Cannot submit action.")
