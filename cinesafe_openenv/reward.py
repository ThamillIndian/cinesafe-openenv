from cinesafe_openenv.models import CineSafeAction, CineSafeState
from typing import Dict, Any
from cinesafe_openenv.graders import compute_terminal_score

class RewardEngine:
    def __init__(self):
        pass
        
    def compute(self, state: CineSafeState, action: CineSafeAction, result, scenario: Dict[str, Any]) -> float:
        """Computes partial/dense rewards for step interactions."""
        reward = 0.0
        
        # We switch to "Sparse Rewards" to ensure compliance with the 
        # [0.01, 0.99] total score requirement. 
        # Intermediate steps return 0.0, and the final plan returns the full score.
        
        if action.action_type == "submit_final_plan":
            terminal_results = compute_terminal_score(state, scenario)
            # Keep the full terminal payload so downstream consumers can read
            # both pass/fail and grader breakdown.
            state.final_scores = terminal_results
            reward = terminal_results["final_score"]
        else:
            reward = 0.0
            
        return reward
