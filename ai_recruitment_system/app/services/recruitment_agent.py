"""
Main recruitment agent service that orchestrates the entire process.
"""

from typing import Dict, Any

from ..agents.workflow import RecruitmentWorkflow
from ..core.exceptions import AgentWorkflowError


class RecruitmentAgent:
    """Main service for processing job applications."""
    
    def __init__(self):
        """Initialize the recruitment agent with workflow."""
        self.workflow = RecruitmentWorkflow()
    
    def process_application(self, cv_text: str, job_posting: str) -> Dict[str, Any]:
        """
        Process a job application through the complete AI workflow.
        
        Args:
            cv_text: Extracted text from candidate's CV
            job_posting: Job posting text
            
        Returns:
            Dictionary containing evaluation results
            
        Raises:
            AgentWorkflowError: If workflow execution fails
        """
        try:
            return self.workflow.process_application(cv_text, job_posting)
        except Exception as e:
            raise AgentWorkflowError(f"Failed to process application: {str(e)}")
    
    def get_workflow_graph(self):
        """Get the workflow graph for visualization."""
        return self.workflow.app.get_graph()
