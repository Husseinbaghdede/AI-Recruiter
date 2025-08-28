"""
Workflow nodes for the recruitment agent.
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from typing import Dict, Any

from ..models.application_state import ApplicationState
from ..core.config import Config


class RecruitmentNodes:
    """Collection of workflow nodes for the recruitment process."""
    
    def __init__(self):
        self.llm = ChatOpenAI(model=Config.OPENAI_MODEL, api_key=Config.OPENAI_API_KEY)
    
    def extract_candidate_info(self, state: ApplicationState) -> ApplicationState:
        """Extract candidate name from CV text."""
        try:
            prompt = ChatPromptTemplate.from_template(
                "Extract the candidate's name from this CV. Return only the name: {cv_text}"
            )
            chain = prompt | self.llm
            result = chain.invoke({"cv_text": state['cv_text'][:1000]})
            return {"candidate_name": result.content.strip()}
        except Exception:
            return {"candidate_name": "Unknown Candidate"}
    
    def categorize_experience(self, state: ApplicationState) -> ApplicationState:
        """Categorize candidate experience level."""
        try:
            prompt = ChatPromptTemplate.from_template("""
            Categorize experience level based on CV and job posting.
            Reply ONLY with: 'Entry-Level', 'Mid-Level', or 'Senior-Level'
            
            CV: {cv_text}
            Job: {job_posting}
            """)
            chain = prompt | self.llm
            result = chain.invoke({
                "cv_text": state['cv_text'][:1500],
                "job_posting": state['job_posting'][:1000]
            })
            return {"experience_level": result.content.strip()}
        except Exception:
            return {"experience_level": "Mid-Level"}
    
    def assess_skills(self, state: ApplicationState) -> ApplicationState:
        """Assess skill match between CV and job requirements."""
        try:
            prompt = ChatPromptTemplate.from_template("""
            Assess skill match between CV and job requirements.
            Reply ONLY with: 'Strong Match', 'Partial Match', or 'No Match'
            
            CV: {cv_text}
            Job: {job_posting}
            """)
            chain = prompt | self.llm
            result = chain.invoke({
                "cv_text": state['cv_text'][:1500],
                "job_posting": state['job_posting'][:1000]
            })
            return {"skill_match": result.content.strip()}
        except Exception:
            return {"skill_match": "Partial Match"}
    
    def technical_evaluation(self, state: ApplicationState) -> ApplicationState:
        """Evaluate technical competency score."""
        try:
            prompt = ChatPromptTemplate.from_template("""
            Rate technical competency 1-10. Reply ONLY with the number.
            
            CV: {cv_text}
            Experience: {experience_level}
            Skills: {skill_match}
            """)
            chain = prompt | self.llm
            result = chain.invoke({
                "cv_text": state['cv_text'][:1500],
                "experience_level": state['experience_level'],
                "skill_match": state['skill_match']
            })
            return {"technical_score": result.content.strip()}
        except Exception:
            return {"technical_score": "5"}
    
    def schedule_interview(self, state: ApplicationState) -> ApplicationState:
        """Generate interview scheduling response."""
        return {
            "response": f"🎉 Congratulations {state['candidate_name']}! You have been selected for an interview. Our HR team will contact you within 2 business days."
        }
    
    def escalate_to_recruiter(self, state: ApplicationState) -> ApplicationState:
        """Generate escalation response."""
        return {
            "response": f"Hello {state['candidate_name']}, your application shows strong potential and has been forwarded to our senior recruitment team for detailed review."
        }
    
    def reject_with_feedback(self, state: ApplicationState) -> ApplicationState:
        """Generate rejection response with learning recommendations."""
        try:
            prompt = ChatPromptTemplate.from_template("""
            Create learning recommendations for this rejected candidate.
            Be encouraging and specific about courses, projects, and skills to develop.
            
            Candidate: {candidate_name}
            Experience: {experience_level}
            Skills: {skill_match}
            Score: {technical_score}
            Job: {job_posting}
            """)
            chain = prompt | self.llm
            result = chain.invoke({
                "candidate_name": state['candidate_name'],
                "experience_level": state['experience_level'],
                "skill_match": state['skill_match'],
                "technical_score": state['technical_score'],
                "job_posting": state['job_posting'][:1000]
            })
            
            return {
                "response": f"Thank you for your interest, {state['candidate_name']}. While you weren't selected for this position, we believe in your potential.",
                "learning_recommendations": result.content
            }
        except Exception:
            return {
                "response": f"Thank you for your interest, {state['candidate_name']}. Please continue developing your skills.",
                "learning_recommendations": "Focus on building relevant experience and skills for this role."
            }
    
    def route_application(self, state: ApplicationState) -> str:
        """Route application based on evaluation results."""
        try:
            score = float(state['technical_score'])
            if score >= 7:
                return 'schedule_interview'
            elif state['experience_level'] == 'Senior-Level' and score >= 6:
                return 'escalate_to_recruiter'
            else:
                return 'reject_with_feedback'
        except Exception:
            return 'reject_with_feedback'
