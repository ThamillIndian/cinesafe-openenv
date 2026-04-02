import os
from typing import Dict, Any, Optional
from google import genai
from google.genai import types
from cinesafe_openenv.constants import GEMINI_MODEL
from dotenv import load_dotenv

load_dotenv()

class GeminiGrader:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.client = None
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)

    def grade_qualitative(self, state: Any, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """
        Grades qualitative aspects using Gemini 3 Flash.
        Returns scores for mitigation and rationale.
        """
        if not self.client:
            return {
                "mitigation_score": 0.5, # Default neutral if no API
                "rationale_score": 0.5,
                "ai_feedback": "AI Grading skipped: GEMINI_API_KEY not set."
            }

        prompt = f"""
        You are a professional Film Production Safety Auditor.
        Grade the following film production plan based on Safety Mitigations and Rationale.

        SCENARIO: {scenario.get('title')}
        SCENES: {scenario.get('scenes')}
        AGENT'S MITIGATION PLANS: {state.mitigation_plans}
        AGENT'S RATIONALE: {getattr(state, 'rationale', 'No rationale provided.')}

        Return a JSON object with:
        1. "mitigation_score": (0.0 to 1.0) based on completeness and realism of safety steps.
        2. "rationale_score": (0.0 to 1.0) based on professional sound logic for scheduling and risk handling.
        3. "feedback": A brief explanation of the score.
        """

        try:
            response = self.client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    thinking_config=types.ThinkingConfig(thinking_level="medium")
                )
            )
            
            import json
            result = json.loads(response.text)
            return {
                "mitigation_score": result.get("mitigation_score", 0.5),
                "rationale_score": result.get("rationale_score", 0.5),
                "ai_feedback": result.get("feedback", "AI evaluation complete.")
            }
        except Exception as e:
            return {
                "mitigation_score": 0.5,
                "rationale_score": 0.5,
                "ai_feedback": f"AI Grading error: {str(e)}"
            }
