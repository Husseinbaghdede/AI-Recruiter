"""
LangGraph workflow for the recruitment agent.
"""

from langgraph.graph import StateGraph, START, END
from typing import Dict, Any

from ..models.application_state import ApplicationState
from .nodes import RecruitmentNodes


class RecruitmentWorkflow:
    """Main workflow orchestrator for the recruitment process."""
    
    def __init__(self):
        self.nodes = RecruitmentNodes()
        self.workflow = StateGraph(ApplicationState)
        self._setup_workflow()
        self.app = self.workflow.compile()
    
    def _setup_workflow(self):
        """Setup the workflow graph with nodes and edges."""
        # Add nodes
        self.workflow.add_node("extract_info", self.nodes.extract_candidate_info)
        self.workflow.add_node("categorize_experience", self.nodes.categorize_experience)
        self.workflow.add_node("assess_skills", self.nodes.assess_skills)
        self.workflow.add_node("technical_evaluation", self.nodes.technical_evaluation)
        self.workflow.add_node("schedule_interview", self.nodes.schedule_interview)
        self.workflow.add_node("escalate_to_recruiter", self.nodes.escalate_to_recruiter)
        self.workflow.add_node("reject_with_feedback", self.nodes.reject_with_feedback)
        
        # Add edges
        self.workflow.add_edge(START, "extract_info")
        self.workflow.add_edge("extract_info", "categorize_experience")
        self.workflow.add_edge("categorize_experience", "assess_skills")
        self.workflow.add_edge("assess_skills", "technical_evaluation")
        
        # Add conditional edges
        self.workflow.add_conditional_edges(
            "technical_evaluation",
            self.nodes.route_application,
            {
                "schedule_interview": "schedule_interview",
                "escalate_to_recruiter": "escalate_to_recruiter",
                "reject_with_feedback": "reject_with_feedback"
            }
        )
        
        # Add final edges
        self.workflow.add_edge("schedule_interview", END)
        self.workflow.add_edge("escalate_to_recruiter", END)
        self.workflow.add_edge("reject_with_feedback", END)
    
    def process_application(self, cv_text: str, job_posting: str) -> Dict[str, Any]:
        """
        Process a job application through the complete workflow.
        
        Args:
            cv_text: Extracted text from candidate's CV
            job_posting: Job posting text
            
        Returns:
            Dictionary containing evaluation results
        """
        initial_state = {
            "cv_text": cv_text,
            "job_posting": job_posting,
            "candidate_name": "",
            "experience_level": "",
            "skill_match": "",
            "technical_score": "",
            "response": "",
            "learning_recommendations": ""
        }
        return self.app.invoke(initial_state)
