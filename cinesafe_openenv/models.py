from typing import Literal, Dict, List, Optional
from pydantic import BaseModel, Field

class SceneCard(BaseModel):
    scene_id: str
    heading: str
    location: str
    time_of_day: str
    cast: List[str] = Field(default_factory=list)
    stunt_required: bool = False
    special_fx: bool = False
    child_actor: bool = False
    animals: bool = False
    weather_dependency: bool = False
    summary: str

class CineSafeAction(BaseModel):
    action_type: Literal[
        "analyze_scene",
        "flag_risk",
        "assign_departments",
        "estimate_scene_cost",
        "cluster_scenes",
        "reorder_schedule",
        "propose_mitigation",
        "request_more_context",
        "submit_final_plan"
    ]
    scene_ids: List[str] = Field(default_factory=list)
    risk_labels: List[str] = Field(default_factory=list)
    priority: Optional[str] = None
    departments: List[str] = Field(default_factory=list)
    estimated_cost: Optional[float] = None
    schedule_order: List[str] = Field(default_factory=list)
    mitigation_notes: Optional[str] = None
    rationale: Optional[str] = None

class CineSafeObservation(BaseModel):
    task_id: str
    difficulty: Literal["easy", "medium", "hard"]
    step_count: int
    max_steps: int
    scenario_summary: str
    scenes: List[SceneCard]
    remaining_budget: float
    remaining_days: int
    unresolved_risks: List[str] = Field(default_factory=list)
    assigned_departments: Dict[str, List[str]] = Field(default_factory=dict)
    action_history: List[str] = Field(default_factory=list)
    partial_metrics: Dict[str, float] = Field(default_factory=dict)
    message: str
    reward: float = 0.0
    done: bool = False

class CineSafeState(BaseModel):
    episode_id: Optional[str] = None
    scenario_id: Optional[str] = None
    task_id: str = ""
    difficulty: str = ""
    step_count: int = 0
    max_steps: int = 0
    total_budget: float = 0.0
    remaining_budget: float = 0.0
    total_days: int = 0
    remaining_days: int = 0
    scene_status: Dict[str, dict] = Field(default_factory=dict)
    detected_risks: Dict[str, List[str]] = Field(default_factory=dict)
    priorities: Dict[str, str] = Field(default_factory=dict)
    assigned_departments: Dict[str, List[str]] = Field(default_factory=dict)
    cost_estimates: Dict[str, float] = Field(default_factory=dict)
    scene_clusters: Dict[str, List[str]] = Field(default_factory=dict)
    schedule_order: List[str] = Field(default_factory=list)
    mitigation_plans: Dict[str, str] = Field(default_factory=dict)
    partial_scores: Dict[str, float] = Field(default_factory=dict)
    cumulative_reward: float = 0.0
    final_scores: Dict[str, float] = Field(default_factory=dict)
    available_context_keys: List[str] = Field(default_factory=list)
    revealed_context_keys: List[str] = Field(default_factory=list)
    done: bool = False
    done_reason: Optional[str] = None
