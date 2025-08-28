"""
Tests for data models.
"""

import pytest
from app.models.job_posting import JobPosting


class TestJobPosting:
    """Test cases for JobPosting model."""
    
    def test_job_posting_creation(self):
        """Test JobPosting object creation."""
        job = JobPosting(
            title="Test Developer",
            company="Test Corp",
            description="A test job",
            requirements=["Python", "Testing"],
            experience_level="Mid-Level",
            skills_required=["Python", "Testing"],
            location="Remote",
            salary_range="$50,000 - $70,000",
            job_type="Full-time"
        )
        
        assert job.title == "Test Developer"
        assert job.company == "Test Corp"
        assert len(job.requirements) == 2
    
    def test_job_posting_to_text(self):
        """Test job posting text conversion."""
        job = JobPosting(
            title="Test Developer",
            company="Test Corp",
            description="A test job",
            requirements=["Python", "Testing"],
            experience_level="Mid-Level",
            skills_required=["Python", "Testing"],
            location="Remote",
            salary_range="$50,000 - $70,000",
            job_type="Full-time"
        )
        
        text = job.to_text()
        assert "Test Developer" in text
        assert "Test Corp" in text
        assert "Python" in text
