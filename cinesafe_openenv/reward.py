from cinesafe_openenv.models import CineSafeAction, CineSafeState
from typing import Dict, Any
from cinesafe_openenv.graders import compute_terminal_score

class RewardEngine:
    def __init__(self):
        pass
        
    def compute(self, state: CineSafeState, action: CineSafeAction, result, scenario: Dict[str, Any]) -> float:
        """Computes partial/dense rewards for step interactions."""
        reward = 0.0
        
        # Intermediate shaping logic (dense rewards)
        if action.action_type == "flag_risk":
            reward += 0.05
        elif action.action_type == "assign_departments":
            reward += 0.05
        elif action.action_type == "cluster_scenes":
            reward += 0.08
        elif action.action_type == "propose_mitigation":
            reward += 0.05
        elif action.action_type == "submit_final_plan":
            terminal_results = compute_terminal_score(state, scenario)
            # Log the scores onto the state object
            state.final_scores = terminal_results["breakdown"]
            reward += terminal_results["final_score"]
        else:
            reward += 0.01
            
        return reward
