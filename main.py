"""
Simple Working AI Recruitment System - All in one file
"""
import streamlit as st
import os
import PyPDF2
import docx
from io import BytesIO
from dataclasses import dataclass
from typing import List, Dict, Any, TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
if not OPENAI_API_KEY or OPENAI_API_KEY == "your_openai_api_key_here":
    st.error("❌ Please set your OPENAI_API_KEY in the .env file")
    st.stop()

llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)

# Data Models
@dataclass
class JobPosting:
    title: str
    company: str
    description: str
    requirements: List[str]
    experience_level: str
    skills_required: List[str]
    location: str
    salary_range: str
    job_type: str

class ApplicationState(TypedDict):
    cv_text: str
    job_posting: str
    candidate_name: str
    experience_level: str
    skill_match: str
    technical_score: str
    response: str
    learning_recommendations: str

# CV Parser
class CVParser:
    @staticmethod
    def extract_text_from_file(file_content: bytes, file_type: str) -> str:
        try:
            if file_type == "application/pdf":
                pdf_reader = PyPDF2.PdfReader(BytesIO(file_content))
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text.strip()
            elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                doc = docx.Document(BytesIO(file_content))
                text = ""
                for paragraph in doc.paragraphs:
                    text += paragraph.text + "\n"
                return text.strip()
            elif file_type == "text/plain":
                return file_content.decode('utf-8')
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
        except Exception as e:
            st.error(f"Error parsing CV: {str(e)}")
            return ""

# Job Data
def get_sample_jobs() -> Dict[str, JobPosting]:
    return {
        "Machine Learning Engineer": JobPosting(
            title="Senior Machine Learning Engineer",
            company="TechCorp AI",
            description="We are seeking a Senior Machine Learning Engineer to join our AI research team and develop cutting-edge AI solutions.",
            requirements=[
                "5+ years of experience in machine learning and data science",
                "Strong proficiency in Python, TensorFlow, PyTorch",
                "Experience with deep learning, NLP, computer vision",
                "Knowledge of MLOps, model deployment, and scaling",
                "Master's degree in Computer Science, Mathematics, or related field",
                "Experience with cloud platforms (AWS, GCP, Azure)",
                "Strong problem-solving and analytical skills"
            ],
            experience_level="Senior-Level",
            skills_required=["Python", "TensorFlow", "PyTorch", "Machine Learning", "Deep Learning", "MLOps"],
            location="San Francisco, CA / Remote",
            salary_range="$120,000 - $180,000",
            job_type="Full-time"
        ),
        "Django Developer": JobPosting(
            title="Full Stack Django Developer",
            company="WebSolutions Inc",
            description="Join our development team to build scalable web applications using Django framework.",
            requirements=[
                "3+ years of experience with Django and Python",
                "Strong knowledge of HTML, CSS, JavaScript",
                "Experience with PostgreSQL/MySQL databases",
                "Familiarity with REST APIs and Django REST Framework",
                "Knowledge of Git, Docker, and deployment processes",
                "Understanding of software testing and debugging",
                "Bachelor's degree in Computer Science or equivalent experience"
            ],
            experience_level="Mid-Level",
            skills_required=["Django", "Python", "JavaScript", "PostgreSQL", "REST APIs", "Docker"],
            location="New York, NY / Hybrid",
            salary_range="$80,000 - $120,000",
            job_type="Full-time"
        ),
        "Python Developer": JobPosting(
            title="Python Backend Developer",
            company="StartupTech",
            description="Looking for a talented Python developer to build robust backend systems and APIs.",
            requirements=[
                "2+ years of Python development experience",
                "Knowledge of FastAPI, Flask, or Django",
                "Experience with databases (PostgreSQL, MongoDB)",
                "Understanding of REST APIs and microservices",
                "Familiarity with Docker and cloud services",
                "Knowledge of testing frameworks",
                "Good problem-solving skills"
            ],
            experience_level="Mid-Level",
            skills_required=["Python", "FastAPI", "Flask", "PostgreSQL", "MongoDB", "Docker"],
            location="Austin, TX / Remote",
            salary_range="$70,000 - $100,000",
            job_type="Full-time"
        )
    }

# Agent Workflow
class RecruitmentAgent:
    def __init__(self):
        self.workflow = StateGraph(ApplicationState)
        self._setup_workflow()
        self.app = self.workflow.compile()
    
    def _setup_workflow(self):
        self.workflow.add_node("extract_info", self.extract_candidate_info)
        self.workflow.add_node("categorize_experience", self.categorize_experience)
        self.workflow.add_node("assess_skills", self.assess_skills)
        self.workflow.add_node("technical_evaluation", self.technical_evaluation)
        self.workflow.add_node("schedule_interview", self.schedule_interview)
        self.workflow.add_node("escalate_to_recruiter", self.escalate_to_recruiter)
        self.workflow.add_node("reject_with_feedback", self.reject_with_feedback)
        
        self.workflow.add_edge(START, "extract_info")
        self.workflow.add_edge("extract_info", "categorize_experience")
        self.workflow.add_edge("categorize_experience", "assess_skills")
        self.workflow.add_edge("assess_skills", "technical_evaluation")
        
        self.workflow.add_conditional_edges(
            "technical_evaluation",
            self.route_application,
            {
                "schedule_interview": "schedule_interview",
                "escalate_to_recruiter": "escalate_to_recruiter",
                "reject_with_feedback": "reject_with_feedback"
            }
        )
        
        self.workflow.add_edge("schedule_interview", END)
        self.workflow.add_edge("escalate_to_recruiter", END)
        self.workflow.add_edge("reject_with_feedback", END)
    
    def extract_candidate_info(self, state: ApplicationState) -> ApplicationState:
        try:
            prompt = ChatPromptTemplate.from_template(
                "Extract the candidate's name from this CV. Return only the name: {cv_text}"
            )
            chain = prompt | llm
            result = chain.invoke({"cv_text": state['cv_text'][:1000]})
            return {"candidate_name": result.content.strip()}
        except:
            return {"candidate_name": "Unknown Candidate"}
    
    def categorize_experience(self, state: ApplicationState) -> ApplicationState:
        try:
            prompt = ChatPromptTemplate.from_template("""
            Categorize experience level based on CV and job posting.
            Reply ONLY with: 'Entry-Level', 'Mid-Level', or 'Senior-Level'
            
            CV: {cv_text}
            Job: {job_posting}
            """)
            chain = prompt | llm
            result = chain.invoke({
                "cv_text": state['cv_text'][:1500],
                "job_posting": state['job_posting'][:1000]
            })
            return {"experience_level": result.content.strip()}
        except:
            return {"experience_level": "Mid-Level"}
    
    def assess_skills(self, state: ApplicationState) -> ApplicationState:
        try:
            prompt = ChatPromptTemplate.from_template("""
            Assess skill match between CV and job requirements.
            Reply ONLY with: 'Strong Match', 'Partial Match', or 'No Match'
            
            CV: {cv_text}
            Job: {job_posting}
            """)
            chain = prompt | llm
            result = chain.invoke({
                "cv_text": state['cv_text'][:1500],
                "job_posting": state['job_posting'][:1000]
            })
            return {"skill_match": result.content.strip()}
        except:
            return {"skill_match": "Partial Match"}
    
    def technical_evaluation(self, state: ApplicationState) -> ApplicationState:
        try:
            prompt = ChatPromptTemplate.from_template("""
            Rate technical competency 1-10. Reply ONLY with the number.
            
            CV: {cv_text}
            Experience: {experience_level}
            Skills: {skill_match}
            """)
            chain = prompt | llm
            result = chain.invoke({
                "cv_text": state['cv_text'][:1500],
                "experience_level": state['experience_level'],
                "skill_match": state['skill_match']
            })
            return {"technical_score": result.content.strip()}
        except:
            return {"technical_score": "5"}
    
    def route_application(self, state: ApplicationState) -> str:
        try:
            score = float(state['technical_score'])
            if score >= 7:
                return 'schedule_interview'
            elif state['experience_level'] == 'Senior-Level' and score >= 6:
                return 'escalate_to_recruiter'
            else:
                return 'reject_with_feedback'
        except:
            return 'reject_with_feedback'
    
    def schedule_interview(self, state: ApplicationState) -> ApplicationState:
        return {
            "response": f"🎉 Congratulations {state['candidate_name']}! You have been selected for an interview. Our HR team will contact you within 2 business days."
        }
    
    def escalate_to_recruiter(self, state: ApplicationState) -> ApplicationState:
        return {
            "response": f"Hello {state['candidate_name']}, your application shows strong potential and has been forwarded to our senior recruitment team for detailed review."
        }
    
    def reject_with_feedback(self, state: ApplicationState) -> ApplicationState:
        try:
            prompt = ChatPromptTemplate.from_template("""
            Create learning recommendations for this rejected candidate.
            Be encouraging and specific about courses, projects, and skills to develop.
            
            Candidate: {candidate_name}
            Experience: {experience_level}
            Skills: {skill_match}
            Score: {technical_score}
            Job: {job_posting}s
            also below dont mention  something like this ever Sincerely,
[Your Name]
[Your Position
            """)
            chain = prompt | llm
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
        except:
            return {
                "response": f"Thank you for your interest, {state['candidate_name']}. Please continue developing your skills.",
                "learning_recommendations": "Focus on building relevant experience and skills for this role."
            }
    
    def process_application(self, cv_text: str, job_posting: str) -> Dict[str, Any]:
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

# UI Functions
def setup_page():
    st.set_page_config(
        page_title="AI Recruitment System",
        page_icon="🤖",
        layout="wide"
    )

def render_header():
    st.markdown("""
    <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 10px; color: white; text-align: center; margin-bottom: 2rem;">
        <h1>🤖 AI Recruitment System</h1>
        <p>Intelligent CV screening and candidate evaluation platform</p>
    </div>
    """, unsafe_allow_html=True)

def render_job_details(job: JobPosting):
    st.header("📄 Job Description")
    
    st.markdown(f"""
    ### {job.title}
    **📍 {job.company}**
    
    **Description:**  
    {job.description}
    
    **Requirements:**
    """)
    
    for req in job.requirements:
        st.markdown(f"• {req}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Experience Level:** {job.experience_level}")
        st.markdown(f"**Location:** {job.location}")
    with col2:
        st.markdown(f"**Job Type:** {job.job_type}")
        st.markdown(f"**Salary:** {job.salary_range}")
    
    st.markdown(f"**Required Skills:** {', '.join(job.skills_required)}")

def render_results(result: Dict[str, Any]):
    st.header("📊 Application Results")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("👤 Candidate", result.get('candidate_name', 'Unknown'))
    with col2:
        st.metric("⭐ Experience", result.get('experience_level', 'Unknown'))
    with col3:
        st.metric("🎯 Skill Match", result.get('skill_match', 'Unknown'))
    with col4:
        score = result.get('technical_score', 'N/A')
        st.metric("📈 Technical Score", f"{score}/10")
    
    # Decision
    st.subheader("📋 Final Decision")
    response = result.get('response', '')
    
    if "Congratulations" in response:
        st.success(response)
    elif "forwarded to our senior recruitment team" in response:
        st.warning(response)
    else:
        st.error(response)
    
    # Learning recommendations
    recommendations = result.get('learning_recommendations', '')
    if recommendations and recommendations.strip():
        st.subheader("📚 Learning Recommendations")
        st.info(recommendations)
        st.success("💡 Don't give up! Use these recommendations to improve and apply again!")

# Main App
def main():
    setup_page()
    render_header()
    
    # Initialize
    if 'agent' not in st.session_state:
        st.session_state.agent = RecruitmentAgent()
    if 'jobs' not in st.session_state:
        st.session_state.jobs = get_sample_jobs()
    
    # Sidebar
    with st.sidebar:
        st.header("📋 Available Positions")
        selected_job = st.selectbox(
            "Select a position:",
            options=list(st.session_state.jobs.keys())
        )
        
        if selected_job:
            job = st.session_state.jobs[selected_job]
            st.markdown(f"**Company:** {job.company}")
            st.markdown(f"**Location:** {job.location}")
            st.markdown(f"**Salary:** {job.salary_range}")
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if selected_job:
            render_job_details(st.session_state.jobs[selected_job])
        else:
            st.info("Please select a job position from the sidebar")
    
    with col2:
        st.header("📤 Submit Your Application")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Upload your CV/Resume",
            type=['pdf', 'docx', 'txt']
        )
        
        cv_text = ""
        if uploaded_file:
            file_content = uploaded_file.read()
            cv_text = CVParser.extract_text_from_file(file_content, uploaded_file.type)
            
            if cv_text:
                st.success("✅ CV processed successfully!")
                with st.expander("Preview"):
                    st.text_area("Extracted text:", cv_text[:500] + "...", height=100)
        
        # Submit button
        if st.button("🚀 Submit Application", type="primary", disabled=not (cv_text and selected_job)):
            if cv_text and selected_job:
                with st.spinner("Processing your application..."):
                    try:
                        job = st.session_state.jobs[selected_job]
                        job_text = f"Title: {job.title}\nCompany: {job.company}\nDescription: {job.description}\nRequirements: {' '.join(job.requirements)}"
                        
                        result = st.session_state.agent.process_application(cv_text, job_text)
                        render_results(result)
                        
                    except Exception as e:
                        st.error(f"Error processing application: {str(e)}")

if __name__ == "__main__":
    main()