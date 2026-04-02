# CineSafe-OpenEnv

**CineSafe-OpenEnv** is a real-world Reinforcement Learning (RL) environment designed for the Meta x PyTorch Hackathon. It simulates risk-aware film production planning, where an AI agent must analyze scenes, detect hazards, assign departments, and optimize schedules for safety and cost-efficiency.

## Environment Overview

Film productions are complex operational environments. Bad scheduling or missed hazards can lead to budget overruns, delays, or serious safety incidents. This environment challenges agents to act as a "Production Safety Coordinator & Planner."

### Tasks & Difficulty
*   **Easy: Scene Risk Triage** — Analyze a single scene (e.g., an indoor fight) and identify critical hazards (stunts, glass).
*   **Medium: Multi-Scene Planning** — Sequence 5-8 scenes while minimizing location changes and respecting time/budget constraints.
*   **Hard: Disruption Recovery** — Adapt an existing production plan after a major disruption (e.g., weather alert or actor unavailability).

## Action Space

The agent interacts via structured `CineSafeAction` objects:
*   `analyze_scene`: Mark scenes as reviewed.
*   `flag_risk`: Attach hazard labels (stunt, animal, night, etc.).
*   `assign_departments`: Assign specialized crew (Stunts, Medic, SFX).
*   `cluster_scenes`: Group scenes by location for efficiency.
*   `reorder_schedule`: Set the final shooting order.
*   `submit_final_plan`: Terminates the episode and triggers terminal grading.

## Observation Space

Per step, the agent receives a `CineSafeObservation`:
*   `scenes`: Full metadata for all scenes in the current scenario.
*   `remaining_budget` / `remaining_days`: Current resource limits.
*   `unresolved_risks`: Feedback on what hasn't been addressed.
*   `partial_metrics`: Real-time score signals.

## Reward Design

The environment uses **Dense Rewards**:
*   `+0.05` for correct risk detection.
*   `+0.08` for efficient location clustering.
*   `+1.0` (Terminal) based on aggregate grader performance (safety, budget, feasibility).
*   Penalties for unsafe schedule patterns or missed "must-have" mitigations.

## 📝 Submission Checklist Compliance (Meta x PyTorch Round 1)

This repository is 100% compliant with the OpenEnv Mandatory Submission Requirements:

- [x] **OpenEnv Spec Compliance**: Implements `step()`, `reset()`, and `state()` endpoints in `cinesafe_openenv/server/app.py`.
- [x] **3+ Tasks with Graders**: 18 Tasks included across **Easy**, **Medium**, and **Hard** difficulties with 0.0-1.0 scoring logic.
- [x] **Mandatory Inference Script**: `inference.py` is in the root directory and emits required `[START]`, `[STEP]`, and `[END]` stdout logs.
- [x] **LLM Integration**: `inference.py` uses the `OpenAI` client (via `google-genai` or standard HF Router) and respects `API_BASE_URL`, `MODEL_NAME`, and `HF_TOKEN`.
- [x] **Deployment Ready**: Includes `Dockerfile`, `openenv.yaml`, and `pyproject.toml`.
- [x] **Validator**: `validate-submission.sh` is provided in the root to verify compliance locally.

## Running the Inference Baseline

To run the mandatory inference script:
```bash
export HF_TOKEN="your_token"
export API_BASE_URL="https://router.huggingface.co/v1"
export MODEL_NAME="Qwen/Qwen2.5-72B-Instruct"
python inference.py
```

## Quickstart

### Installation
```bash
pip install -e .
```

### Local Dev Server
```bash
uvicorn cinesafe_openenv.server.app:app --host 0.0.0.0 --port 7860
```

## Deployment

The environment is set up for easy deployment to **Hugging Face Spaces** using the included `Dockerfile` and `openenv.yaml` manifest.

```bash
openenv push
```

## License
MIT
