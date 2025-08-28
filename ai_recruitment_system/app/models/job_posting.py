"""
Job posting data model.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class JobPosting:
    """Represents a job posting with all relevant details."""
    
    title: str
    company: str
    description: str
    requirements: List[str]
    experience_level: str
    skills_required: List[str]
    location: str
    salary_range: str
    job_type: str
    
    def to_text(self) -> str:
        """Convert job posting to text format for AI processing."""
        return f"""Title: {self.title}
Company: {self.company}
Description: {self.description}
Requirements: {' '.join(self.requirements)}"""
    
    def __str__(self) -> str:
        return f"{self.title} at {self.company}"
