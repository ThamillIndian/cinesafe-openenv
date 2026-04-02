from cinesafe_openenv.models import CineSafeAction, CineSafeState
from typing import Dict, Any

class HandlerResult:
    def __init__(self, message: str, success: bool):
        self.message = message
        self.success = success

def dispatch_action(action: CineSafeAction, state: CineSafeState, scenario: Dict[str, Any]) -> HandlerResult:
    handler_map = {
        "analyze_scene": handle_analyze_scene,
        "flag_risk": handle_flag_risk,
        "assign_departments": handle_assign_departments,
        "estimate_scene_cost": handle_estimate_scene_cost,
        "cluster_scenes": handle_cluster_scenes,
        "reorder_schedule": handle_reorder_schedule,
        "propose_mitigation": handle_propose_mitigation,
        "request_more_context": handle_request_more_context,
        "submit_final_plan": handle_submit_final_plan,
    }
    
    handler = handler_map.get(action.action_type)
    if not handler:
        return HandlerResult(f"No handler for {action.action_type}", False)
        
    return handler(action, state, scenario)

def handle_analyze_scene(action: CineSafeAction, state: CineSafeState, scenario: Dict[str, Any]) -> HandlerResult:
    for s_id in action.scene_ids:
        if s_id not in state.scene_status:
            state.scene_status[s_id] = {"analyzed": True}
        else:
            state.scene_status[s_id]["analyzed"] = True
    return HandlerResult(f"Analyzed scenes {' '.join(action.scene_ids)}", True)

def handle_flag_risk(action: CineSafeAction, state: CineSafeState, scenario: Dict[str, Any]) -> HandlerResult:
    for s_id in action.scene_ids:
        current_risks = state.detected_risks.get(s_id, [])
        for r in action.risk_labels:
            if r not in current_risks:
                current_risks.append(r)
        state.detected_risks[s_id] = current_risks
        
    if action.priority and action.scene_ids:
        for s_id in action.scene_ids:
            state.priorities[s_id] = action.priority
            
    return HandlerResult(f"Flagged risks {action.risk_labels} for {action.scene_ids}", True)

def handle_assign_departments(action: CineSafeAction, state: CineSafeState, scenario: Dict[str, Any]) -> HandlerResult:
    for s_id in action.scene_ids:
        current_deps = state.assigned_departments.get(s_id, [])
        for d in action.departments:
            if d not in current_deps:
                current_deps.append(d)
        state.assigned_departments[s_id] = current_deps
    return HandlerResult(f"Assigned departments {action.departments} for {action.scene_ids}", True)

def handle_estimate_scene_cost(action: CineSafeAction, state: CineSafeState, scenario: Dict[str, Any]) -> HandlerResult:
    for s_id in action.scene_ids:
        state.cost_estimates[s_id] = action.estimated_cost
    return HandlerResult(f"Estimated cost {action.estimated_cost} for {action.scene_ids}", True)

def handle_cluster_scenes(action: CineSafeAction, state: CineSafeState, scenario: Dict[str, Any]) -> HandlerResult:
    cluster_id = f"C{len(state.scene_clusters) + 1}"
    state.scene_clusters[cluster_id] = action.scene_ids
    return HandlerResult(f"Clustered scenes into {cluster_id}", True)

def handle_reorder_schedule(action: CineSafeAction, state: CineSafeState, scenario: Dict[str, Any]) -> HandlerResult:
    state.schedule_order = action.schedule_order
    return HandlerResult(f"Reordered schedule to {action.schedule_order}", True)

def handle_propose_mitigation(action: CineSafeAction, state: CineSafeState, scenario: Dict[str, Any]) -> HandlerResult:
    for s_id in action.scene_ids:
        state.mitigation_plans[s_id] = action.mitigation_notes
    return HandlerResult(f"Proposed mitigation for {action.scene_ids}", True)

def handle_request_more_context(action: CineSafeAction, state: CineSafeState, scenario: Dict[str, Any]) -> HandlerResult:
    revealed = list(scenario.get("hidden_context", {}).keys())
    state.revealed_context_keys = revealed
    return HandlerResult(f"Revealed hidden context: {revealed}", True)

def handle_submit_final_plan(action: CineSafeAction, state: CineSafeState, scenario: Dict[str, Any]) -> HandlerResult:
    state.done = True
    state.done_reason = "Agent submitted final plan."
    return HandlerResult("Submitted final plan. Episode complete.", True)
