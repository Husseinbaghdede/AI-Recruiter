"""
Results display components for application evaluation.
"""

import streamlit as st
from typing import Dict, Any


def render_results(result: Dict[str, Any]):
    """Render application evaluation results."""
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


def render_processing_spinner():
    """Render processing spinner context manager."""
    return st.spinner("Processing your application...")


def render_error_message(error_message: str):
    """Render error message."""
    st.error(f"❌ Error processing application: {error_message}")
