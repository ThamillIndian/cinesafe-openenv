import os
import sys

# Ensure package is resolvable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from cinesafe_openenv.server.environment import CineSafeEnvironment
from cinesafe_openenv.models import CineSafeAction

def run_baseline_on_scenario(difficulty: str, scenario_id: str):
    env = CineSafeEnvironment()
    obs = env.reset(difficulty=difficulty, scenario_id=scenario_id)
    print(f"\n--- Running baseline on {difficulty}/{scenario_id} ---")
    
    # Analyze all scenes
    scene_ids = [s.scene_id for s in obs.scenes]
    env.step(CineSafeAction(action_type="analyze_scene", scene_ids=scene_ids))
    
    # Flag risks based on simple rules
    for scene in obs.scenes:
        risks = []
        deps = ["camera", "lighting"]
        if scene.stunt_required:
            risks.append("stunt")
            deps.append("stunts")
            deps.append("medical")
        if getattr(scene, "animals", False):
            risks.append("animal")
            deps.append("animal_handling")
        if getattr(scene, "child_actor", False):
            risks.append("child_actor")
        if scene.time_of_day == "night":
            risks.append("night_shoot")
        if getattr(scene, "weather_dependency", False):
            risks.append("weather")
        if getattr(scene, "special_fx", False):
            risks.append("electrical_sparks")
            risks.append("glass_break") # hacky baseline for "special"
            deps.append("sfx")
            
        if risks:
            env.step(CineSafeAction(action_type="flag_risk", scene_ids=[scene.scene_id], risk_labels=risks))
        env.step(CineSafeAction(action_type="assign_departments", scene_ids=[scene.scene_id], departments=deps))
        
        # simple baseline: apply generic mitigations to everything
        env.step(CineSafeAction(
            action_type="propose_mitigation", 
            scene_ids=[scene.scene_id], 
            mitigation_notes="safety briefing, protective equipment, medic on standby, breakaway glass handling, child labor law compliance, animal handler present"
        ))

    # Cluster scenes by location
    location_groups = {}
    for scene in obs.scenes:
        loc = scene.location
        if loc not in location_groups:
            location_groups[loc] = []
        location_groups[loc].append(scene.scene_id)
        
    for group, s_ids in location_groups.items():
        env.step(CineSafeAction(action_type="cluster_scenes", scene_ids=s_ids))
        
    # Reorder schedule sequentially
    env.step(CineSafeAction(action_type="reorder_schedule", schedule_order=scene_ids))
    
    # Submit finally
    env.step(CineSafeAction(action_type="submit_final_plan"))
    
    state = env.state()
    print(f"Cumulative Reward: {state.cumulative_reward:.3f}")
    if state.final_scores:
        scores = state.final_scores
        print(f"Final Scores: Passed={scores.get('passed', False)}")
        print(f" - Risk Score: {scores.get('risk', {}).get('score', 0):.2f}")
        print(f" - Dept Score: {scores.get('department', {}).get('score', 0):.2f}")
        
        # AI Qualitative Feedback
        ai = scores.get('ai', {})
        print(f" - AI Mitigation Score: {ai.get('mitigation_score', 0):.2f}")
        print(f" - AI Rationale Score: {ai.get('rationale_score', 0):.2f}")
        print(f" - AI Feedback: {ai.get('ai_feedback', 'No feedback')}")
        
    print(f"Done Reason: {state.done_reason}")
    return state.cumulative_reward, state.final_scores

if __name__ == "__main__":
    print("Evaluating Baseline Rule-Based Planner")
    run_baseline_on_scenario("easy", "easy_001")
    run_baseline_on_scenario("medium", "medium_001")
    run_baseline_on_scenario("hard", "hard_001")
