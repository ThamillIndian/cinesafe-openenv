import pytest
from cinesafe_openenv.server.environment import CineSafeEnvironment
from cinesafe_openenv.models import CineSafeAction

def test_reset():
    env = CineSafeEnvironment()
    obs = env.reset(difficulty="easy")
    assert obs.task_id == "scene_risk_triage"
    assert obs.difficulty == "easy"
    assert obs.step_count == 0
    assert len(obs.scenes) > 0

def test_step():
    env = CineSafeEnvironment()
    env.reset(difficulty="easy")
    
    # Test a few actions
    action1 = CineSafeAction(action_type="analyze_scene", scene_ids=["S1"])
    obs = env.step(action1)
    assert obs.step_count == 1
    assert "Analyzed scenes S1" in obs.message
    
    action2 = CineSafeAction(action_type="flag_risk", scene_ids=["S1"], risk_labels=["stunt"])
    obs = env.step(action2)
    assert obs.step_count == 2
    assert "stunt" in env.state().detected_risks["S1"]

def test_final_submission():
    env = CineSafeEnvironment()
    env.reset(difficulty="easy")
    
    # Analyze, Flag, and Submit
    env.step(CineSafeAction(action_type="analyze_scene", scene_ids=["S1"]))
    env.step(CineSafeAction(action_type="flag_risk", scene_ids=["S1"], risk_labels=["stunt", "glass"]))
    env.step(CineSafeAction(action_type="assign_departments", scene_ids=["S1"], departments=["stunts", "medical"]))
    env.step(CineSafeAction(action_type="submit_final_plan"))
    
    assert env.state().done is True
    assert env.state().cumulative_reward > 0.0

def test_max_steps():
    env = CineSafeEnvironment()
    env.reset(difficulty="easy")
    env._state.max_steps = 2
    
    env.step(CineSafeAction(action_type="analyze_scene", scene_ids=["S1"]))
    obs = env.step(CineSafeAction(action_type="analyze_scene", scene_ids=["S1"]))
    
    assert obs.done is True
    assert obs.step_count == 2
