from fastapi import FastAPI, HTTPException
from cinesafe_openenv.server.environment import CineSafeEnvironment
from cinesafe_openenv.models import CineSafeAction

app = FastAPI(title="CineSafe OpenEnv Server")
env = CineSafeEnvironment()

@app.post("/reset")
async def reset(seed: int = None, scenario_id: str = None, difficulty: str = None):
    try:
        obs = env.reset(seed=seed, scenario_id=scenario_id, difficulty=difficulty)
        return obs.model_dump()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/step")
async def step(action: CineSafeAction):
    try:
        obs = env.step(action)
        return obs.model_dump()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/state")
async def state():
    return env.state().model_dump()

@app.get("/")
async def root():
    return {"status": "CineSafe Environment is running", "tasks": ["scene_risk_triage", "multi_scene_planning", "disruption_recovery"]}
