"""
File upload components for CV processing.
"""

import streamlit as st
from ...services.cv_parser import CVParser
from ...core.exceptions import CVParseError, FileProcessingError


def render_file_upload() -> tuple[str, str]:
    """
    Render file upload component and return extracted text and file type.
    
    Returns:
        Tuple of (extracted_text, file_type)
    """
    st.header("📤 Submit Your Application")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload your CV/Resume",
        type=['pdf', 'docx', 'txt'],
        help="Supported formats: PDF, DOCX, TXT"
    )
    
    cv_text = ""
    file_type = ""
    
    if uploaded_file:
        try:
            # Validate file type
            if not CVParser.validate_file_type(uploaded_file.type):
                st.error(f"❌ Unsupported file type: {uploaded_file.type}")
                return cv_text, file_type
            
            # Extract text
            file_content = uploaded_file.read()
            cv_text = CVParser.extract_text_from_file(file_content, uploaded_file.type)
            file_type = uploaded_file.type
            
            if cv_text:
                st.success("✅ CV processed successfully!")
                with st.expander("Preview Extracted Text"):
                    st.text_area("Extracted text:", cv_text[:500] + "...", height=100)
            else:
                st.warning("⚠️ No text could be extracted from the file.")
                
        except CVParseError as e:
            st.error(f"❌ CV parsing error: {str(e)}")
        except FileProcessingError as e:
            st.error(f"❌ File processing error: {str(e)}")
        except Exception as e:
            st.error(f"❌ Unexpected error: {str(e)}")
    
    return cv_text, file_type


def render_submit_button(cv_text: str, selected_job: str) -> bool:
    """
    Render submit button and return whether it was clicked.
    
    Args:
        cv_text: Extracted CV text
        selected_job: Selected job key
        
    Returns:
        True if submit button was clicked, False otherwise
    """
    return st.button(
        "🚀 Submit Application", 
        type="primary", 
        disabled=not (cv_text and selected_job),
        help="Upload a CV and select a job position to enable submission"
    )
