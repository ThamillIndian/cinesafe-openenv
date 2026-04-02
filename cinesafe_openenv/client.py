import httpx
from typing import Optional, Dict, Any
from .models import CineSafeAction, CineSafeObservation

class CineSafeEnvClient:
    """
    A client wrapper to interact with the CineSafe environment server.
    This is the primary entry point for agents.
    """
    def __init__(self, base_url: str = "http://localhost:7860"):
        self.base_url = base_url.rstrip("/")

    def reset(self, 
              seed: Optional[int] = None, 
              scenario_id: Optional[str] = None, 
              difficulty: Optional[str] = None) -> CineSafeObservation:
        params = {}
        if seed is not None: params["seed"] = seed
        if scenario_id: params["scenario_id"] = scenario_id
        if difficulty: params["difficulty"] = difficulty
        
        response = httpx.post(f"{self.base_url}/reset", params=params, timeout=30.0)
        response.raise_for_status()
        return CineSafeObservation(**response.json())

    def step(self, action: CineSafeAction) -> CineSafeObservation:
        response = httpx.post(f"{self.base_url}/step", json=action.model_dump(), timeout=30.0)
        response.raise_for_status()
        return CineSafeObservation(**response.json())

    def state(self) -> Dict[str, Any]:
        response = httpx.get(f"{self.base_url}/state", timeout=30.0)
        response.raise_for_status()
        return response.json()
