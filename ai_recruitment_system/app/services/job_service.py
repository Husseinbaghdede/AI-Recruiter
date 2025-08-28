"""
Job management service for handling job postings.
"""

from typing import Dict
from ..models.job_posting import JobPosting


class JobService:
    """Service for managing job postings and data."""
    
    @staticmethod
    def get_sample_jobs() -> Dict[str, JobPosting]:
        """Get sample job postings for demonstration."""
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
    
    @staticmethod
    def get_job_by_key(jobs: Dict[str, JobPosting], job_key: str) -> JobPosting:
        """Get a specific job posting by key."""
        if job_key not in jobs:
            raise ValueError(f"Job key '{job_key}' not found")
        return jobs[job_key]
    
    @staticmethod
    def get_job_keys(jobs: Dict[str, JobPosting]) -> list:
        """Get list of available job keys."""
        return list(jobs.keys())
