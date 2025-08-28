"""
Job display components for the Streamlit UI.
"""

import streamlit as st
from ...models.job_posting import JobPosting


def render_job_details(job: JobPosting):
    """Render detailed job posting information."""
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


def render_job_sidebar(jobs: dict, selected_job: str):
    """Render job selection sidebar."""
    with st.sidebar:
        st.header("📋 Available Positions")
        selected_job = st.selectbox(
            "Select a position:",
            options=list(jobs.keys()),
            index=list(jobs.keys()).index(selected_job) if selected_job in jobs else 0
        )
        
        if selected_job:
            job = jobs[selected_job]
            st.markdown(f"**Company:** {job.company}")
            st.markdown(f"**Location:** {job.location}")
            st.markdown(f"**Salary:** {job.salary_range}")
    
    return selected_job
