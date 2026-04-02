import os
import json
import asyncio
from typing import List, Optional
from openai import OpenAI
from cinesafe_openenv.server.environment import CineSafeEnvironment
from cinesafe_openenv.models import CineSafeAction

# Mandatory Env Vars
API_BASE_URL = os.getenv("API_BASE_URL") or "https://generativelanguage.googleapis.com/v1beta/openai/"
MODEL_NAME = os.getenv("MODEL_NAME") or "gemini-3-flash-preview"
API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("HF_TOKEN") or os.getenv("OPEN_AI_API_KEY")

client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

async def run_inference():
    env = CineSafeEnvironment()
    # Configuration
    difficulty = os.getenv("CINESAFE_DIFFICULTY", "easy")
    max_steps = 10
    
    # [START]
    obs = env.reset(difficulty=difficulty)
    print(f"[START] task_id={obs.task_id} difficulty={obs.difficulty}")
    
    total_reward = 0
    rewards_history = []
    
    for i in range(max_steps):
        # 1. Prepare prompt for LLM
        prompt = f"""
        You are a film production safety agent. 
        Current Observation: {obs.model_dump_json()}
        Available Actions: analyze_scene, flag_risk, assign_departments, submit_final_plan.
        
        Choose the next action in JSON format: {{"action_type": "...", "scene_ids": [...], "risk_labels": [...], "departments": [...]}}
        """
        
        # 2. Call LLM (Mandatory OpenAI Client usage)
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                response_format={ "type": "json_object" }
            )
            action_data = json.loads(response.choices[0].message.content)
            action = CineSafeAction(**action_data)
        except Exception as e:
            # Fallback for baseline if LLM fails
            print(f"LLM Error: {e}. Falling back to submission.")
            action = CineSafeAction(action_type="submit_final_plan")

        # 3. Step Environment
        obs = env.step(action)
        total_reward += obs.reward
        rewards_history.append(obs.reward)
        
        # [STEP]
        print(f"[STEP] step={obs.step_count} action={action.action_type} reward={obs.reward:.2f}")
        
        if obs.done:
            break
            
    # [END]
    success = env.state().final_scores.get("passed", False) if hasattr(env.state(), "final_scores") else True
    rewards_str = ",".join([f"{r:.2f}" for r in rewards_history])
    print(f"[END] success={str(success).lower()} steps={obs.step_count} rewards={rewards_str}")

if __name__ == "__main__":
    if not API_KEY:
        print("Warning: API_KEY/HF_TOKEN not set. Running in pseudo-inference mode.")
    asyncio.run(run_inference())
