"""
CV parsing service for extracting text from various file formats.
"""

import streamlit as st
import PyPDF2
import docx
from io import BytesIO
from typing import Union

from ..core.exceptions import CVParseError


class CVParser:
    """Service for parsing CV files and extracting text content."""
    
    @staticmethod
    def extract_text_from_file(file_content: bytes, file_type: str) -> str:
        """
        Extract text from uploaded file content.
        
        Args:
            file_content: Raw file content as bytes
            file_type: MIME type of the file
            
        Returns:
            Extracted text content
            
        Raises:
            CVParseError: If file parsing fails
        """
        try:
            if file_type == "application/pdf":
                return CVParser._extract_from_pdf(file_content)
            elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                return CVParser._extract_from_docx(file_content)
            elif file_type == "text/plain":
                return file_content.decode('utf-8')
            else:
                raise CVParseError(f"Unsupported file type: {file_type}")
        except Exception as e:
            raise CVParseError(f"Error parsing CV: {str(e)}")
    
    @staticmethod
    def _extract_from_pdf(file_content: bytes) -> str:
        """Extract text from PDF file."""
        pdf_reader = PyPDF2.PdfReader(BytesIO(file_content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    
    @staticmethod
    def _extract_from_docx(file_content: bytes) -> str:
        """Extract text from DOCX file."""
        doc = docx.Document(BytesIO(file_content))
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text.strip()
    
    @staticmethod
    def validate_file_type(file_type: str) -> bool:
        """Validate if file type is supported."""
        supported_types = [
            "application/pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "text/plain"
        ]
        return file_type in supported_types
