"""
Constants and enumerations for CineSafe OpenEnv
"""

# Difficulties
DIFFICULTIES = ["easy", "medium", "hard"]

# Tasks
TASK_IDS = [
    "scene_risk_triage",
    "multi_scene_planning",
    "disruption_recovery"
]

# Risk features and labels
RISK_CATEGORIES = [
    "stunt", "water", "crowd", "vehicle", "animal",
    "weather", "location", "permit", "vfx", "special", "electrical"
]

SEVERITY_LEVELS = ["low", "medium", "high", "critical"]

# Departments
DEPARTMENTS = [
    "stunts", "camera", "lighting", "sfx", "vfx", 
    "medical", "animal_handling", "marine", "security", "art", "wardrobe"
]

# Scoring Weights for Final Aggregation
SCORING_WEIGHTS = {
    "risk": 0.30,
    "department": 0.20,
    "schedule": 0.20,
    "budget": 0.15,
    "mitigation": 0.15
}

# Risk Amplifiers
RISK_AMPLIFIERS = {
    ("night_shoot", "water", "stunt"): 1.4,
    ("night_shoot", "crowd", "vehicle"): 1.3,
    ("weather_dependent", "tight_schedule"): 1.25,
    ("water", "animals", "crowd"): 1.3,
    ("stunts", "vehicle_chase", "crowd"): 1.35,
}

# AI Grading
GEMINI_MODEL = "gemini-3-flash-preview"

