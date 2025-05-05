from pydantic import BaseModel
from typing import List, Optional

class ExperienceItem(BaseModel):
    title: str
    company: str
    location: Optional[str] = ""
    dates: Optional[str] = ""
    responsibilities: Optional[str] = ""

class EducationItem(BaseModel):
    school: str
    degree: Optional[str] = ""
    field: Optional[str] = ""
    dates: Optional[str] = ""

class Candidate(BaseModel):
    name: str
    email: Optional[str] = ""
    phone: Optional[str] = ""
    location: Optional[str] = ""
    skills: List[str] = []
    certifications: List[str] = []
    experience: List[ExperienceItem] = []
    education: List[EducationItem] = []
    embedding: Optional[List[float]] = None
    source_file: Optional[str] = ""
