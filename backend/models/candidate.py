from pydantic import BaseModel
from typing import List, Optional
from typing import Union

class ExperienceItem(BaseModel):
    title: str
    company: str
    location: Optional[str] = ""
    dates: Optional[str] = ""
    responsibilities: Union[str, list[str]]

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
    certifications: Union[list[Union[str, dict]], None] = []
    experience: List[ExperienceItem] = []
    education: List[EducationItem] = []
    embedding: Optional[List[float]] = None
    source_file: Optional[str] = ""

class SearchRequest(BaseModel):
    prompt: str
    top_k: int = 25
    owner: str | None = None  # 👈 add this line