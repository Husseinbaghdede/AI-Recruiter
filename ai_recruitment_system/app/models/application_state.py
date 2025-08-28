"""
Application state model for the recruitment workflow.
"""

from typing import TypedDict


class ApplicationState(TypedDict):
    """State model for the recruitment agent workflow."""
    
    cv_text: str
    job_posting: str
    candidate_name: str
    experience_level: str
    skill_match: str
    technical_score: str
    response: str
    learning_recommendations: str
