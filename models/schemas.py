from pydantic import BaseModel
from typing import List


class CandidateProfile(BaseModel):
    name: str
    email: str
    phone: str
    skills: List[str]
    education: str
    experience_years: int
    projects: List[str]