import os
from cinesafe_openenv.models import (
    CineSafeAction,
    CineSafeObservation,
    CineSafeState,
)
from cinesafe_openenv.scenario_loader import ScenarioLoader
from cinesafe_openenv.validators import validate_action
from cinesafe_openenv.action_handlers import dispatch_action
from cinesafe_openenv.constants import NEUTRAL_OBSERVATION_REWARD
from cinesafe_openenv.reward import RewardEngine

class CineSafeEnvironment:
    def __init__(self, data_dir=None):
        self.loader = ScenarioLoader(data_dir=data_dir)
        self.reward_engine = RewardEngine()
        self._state = CineSafeState()

    def reset(self, seed=None, scenario_id=None, difficulty=None, task_id=None, **kwargs):
        scenario = self.loader.pick(
            seed=seed,
            scenario_id=scenario_id,
            difficulty=difficulty,
            task_id=task_id,
        )
        self._state = CineSafeState(
            scenario_id=scenario["scenario_id"],
            task_id=scenario["task_id"],
            difficulty=scenario["difficulty"],
            max_steps=scenario.get("max_steps", 20),
            total_budget=scenario["budget_limit"],
            remaining_budget=scenario["budget_limit"],
            total_days=scenario["day_limit"],
            remaining_days=scenario["day_limit"],
        )
        return CineSafeObservation(
            task_id=self._state.task_id,
            difficulty=self._state.difficulty,
            step_count=0,
            max_steps=self._state.max_steps,
            scenario_summary=scenario["title"],
            scenes=scenario["parsed_scenes"],
            remaining_budget=self._state.remaining_budget,
            remaining_days=self._state.remaining_days,
            unresolved_risks=[],
            assigned_departments={},
            action_history=[],
            partial_metrics={},
            message="Scenario loaded. Begin planning.",
            reward=NEUTRAL_OBSERVATION_REWARD,
            done=False,
        )

    def step(self, action: CineSafeAction):
        validate_action(action, self._state)
        result = dispatch_action(action, self._state, self.loader.current_scenario)
        reward = self.reward_engine.compute(self._state, action, result, self.loader.current_scenario)
        
        self._state.step_count += 1
        self._state.cumulative_reward += reward
        
        # Check termination condition
        if getattr(self._state, 'done', False) or self._state.step_count >= self._state.max_steps:
            self._state.done = True
            
        return CineSafeObservation(
            task_id=self._state.task_id,
            difficulty=self._state.difficulty,
            step_count=self._state.step_count,
            max_steps=self._state.max_steps,
            scenario_summary=self.loader.current_scenario["title"],
            scenes=self.loader.current_scenario["parsed_scenes"],
            remaining_budget=self._state.remaining_budget,
            remaining_days=self._state.remaining_days,
            unresolved_risks=[],
            assigned_departments=self._state.assigned_departments,
            action_history=[],
            partial_metrics=self._state.partial_scores,
            message=result.message,
            reward=reward,
            done=self._state.done,
        )

    def state(self):
        return self._state
