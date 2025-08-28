"""
Custom exceptions for the AI Recruitment System.
"""


class RecruitmentSystemError(Exception):
    """Base exception for recruitment system errors."""
    pass


class ConfigurationError(RecruitmentSystemError):
    """Raised when configuration is invalid or missing."""
    pass


class CVParseError(RecruitmentSystemError):
    """Raised when CV parsing fails."""
    pass


class AgentWorkflowError(RecruitmentSystemError):
    """Raised when agent workflow execution fails."""
    pass


class FileProcessingError(RecruitmentSystemError):
    """Raised when file processing fails."""
    pass
