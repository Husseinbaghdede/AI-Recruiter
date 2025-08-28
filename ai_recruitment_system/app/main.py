"""
Main Streamlit application for the AI Recruitment System.
"""

import streamlit as st
from typing import Dict, Any

from .core.config import Config
from .core.exceptions import ConfigurationError, AgentWorkflowError
from .services.recruitment_agent import RecruitmentAgent
from .services.job_service import JobService
from .ui.components.job_display import render_job_details, render_job_sidebar
from .ui.components.file_upload import render_file_upload, render_submit_button
from .ui.components.results_display import render_results, render_processing_spinner, render_error_message


def setup_page():
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title=Config.APP_TITLE,
        page_icon=Config.APP_ICON,
        layout=Config.APP_LAYOUT
    )


def render_header():
    """Render application header."""
    st.markdown("""
    <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 10px; color: white; text-align: center; margin-bottom: 2rem;">
        <h1>🤖 AI Recruitment System</h1>
        <p>Intelligent CV screening and candidate evaluation platform</p>
    </div>
    """, unsafe_allow_html=True)


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'agent' not in st.session_state:
        st.session_state.agent = RecruitmentAgent()
    if 'jobs' not in st.session_state:
        st.session_state.jobs = JobService.get_sample_jobs()
    if 'selected_job' not in st.session_state:
        st.session_state.selected_job = list(st.session_state.jobs.keys())[0]


def process_application(cv_text: str, selected_job: str) -> Dict[str, Any]:
    """
    Process job application through the AI workflow.
    
    Args:
        cv_text: Extracted CV text
        selected_job: Selected job key
        
    Returns:
        Evaluation results
    """
    job = st.session_state.jobs[selected_job]
    job_text = job.to_text()
    
    return st.session_state.agent.process_application(cv_text, job_text)


def main():
    """Main application function."""
    # Setup page
    setup_page()
    
    # Check configuration
    error_message = Config.get_error_message()
    if error_message:
        st.error(error_message)
        st.stop()
    
    # Render header
    render_header()
    
    # Initialize session state
    initialize_session_state()
    
    # Render sidebar
    st.session_state.selected_job = render_job_sidebar(
        st.session_state.jobs, 
        st.session_state.selected_job
    )
    
    # Main content layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Job details
        if st.session_state.selected_job:
            render_job_details(st.session_state.jobs[st.session_state.selected_job])
        else:
            st.info("Please select a job position from the sidebar")
    
    with col2:
        # File upload and application submission
        cv_text, file_type = render_file_upload()
        
        # Submit button
        if render_submit_button(cv_text, st.session_state.selected_job):
            if cv_text and st.session_state.selected_job:
                with render_processing_spinner():
                    try:
                        result = process_application(cv_text, st.session_state.selected_job)
                        render_results(result)
                    except AgentWorkflowError as e:
                        render_error_message(str(e))
                    except Exception as e:
                        render_error_message(f"Unexpected error: {str(e)}")


if __name__ == "__main__":
    main()
