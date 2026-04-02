import json
import os
import random
from typing import Dict, Any, Optional

class ScenarioLoader:
    def __init__(self, data_dir: str = None):
        if data_dir is None:
            self.data_dir = os.path.join(os.path.dirname(__file__), "data")
        else:
            self.data_dir = data_dir
            
        self.seed_manifest_path = os.path.join(self.data_dir, "seed_manifest.json")
        self.tasks_dir = os.path.join(self.data_dir, "tasks")
        
        self.current_scenario: Optional[Dict[str, Any]] = None

    def load_scenario_by_id(self, difficulty: str, scenario_id: str) -> Dict[str, Any]:
        """Loads a specific scenario from a JSON file."""
        file_path = os.path.join(self.tasks_dir, difficulty, f"{scenario_id}.json")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Scenario not found: {file_path}")
            
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def pick(self, 
             seed: Optional[int] = None, 
             scenario_id: Optional[str] = None, 
             difficulty: Optional[str] = "easy", 
             task_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Picks and loads a scenario based on criteria.
        Respects determinism if seed is provided by checking manifest.
        """
        # If specific scenario ID is requested
        if scenario_id:
            # We assume difficulty is correct if scenario_id is passed, or try to find it
            diffs = ["easy", "medium", "hard"] if not difficulty else [difficulty]
            for d in diffs:
                try:
                    scenario = self.load_scenario_by_id(d, scenario_id)
                    self.current_scenario = scenario
                    
                    # Convert raw dict scenes into models
                    if "scenes" in scenario:
                        from cinesafe_openenv.models import SceneCard
                        self.current_scenario["parsed_scenes"] = [SceneCard(**s) for s in scenario["scenes"]]
                    
                    return self.current_scenario
                except FileNotFoundError:
                    continue
            raise FileNotFoundError(f"Could not find scenario_id {scenario_id} in tasks dir.")

        # Fallback to seeded random choice within difficulty
        target_diff = difficulty or "easy"
        available_files = [f for f in os.listdir(os.path.join(self.tasks_dir, target_diff)) if f.endswith('.json')]
        
        if not available_files:
            raise ValueError(f"No scenarios found for difficulty {target_diff}")
            
        if seed is not None:
            random.seed(seed)
            if os.path.exists(self.seed_manifest_path):
                with open(self.seed_manifest_path, "r") as f:
                    manifest = json.load(f)
                if str(seed) in manifest and target_diff in manifest[str(seed)]:
                    scenario_candidates = manifest[str(seed)][target_diff]
                    if scenario_candidates:
                        chosen_id = random.choice(scenario_candidates)
                        self.current_scenario = self.load_scenario_by_id(target_diff, chosen_id)
                        
                        if "scenes" in self.current_scenario:
                            from cinesafe_openenv.models import SceneCard
                            self.current_scenario["parsed_scenes"] = [SceneCard(**s) for s in self.current_scenario["scenes"]]
                            
                        return self.current_scenario

        chosen_file = random.choice(available_files)
        file_path = os.path.join(self.tasks_dir, target_diff, chosen_file)
        
        with open(file_path, "r", encoding="utf-8") as f:
            self.current_scenario = json.load(f)
            
        if "scenes" in self.current_scenario:
            from cinesafe_openenv.models import SceneCard
            self.current_scenario["parsed_scenes"] = [SceneCard(**s) for s in self.current_scenario["scenes"]]

        return self.current_scenario
