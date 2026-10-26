from typing import TypedDict , Literal
from pydantic import BaseModel


class JobCleanerState(TypedDict) : 
    raw : str
    raw : str
    skills: list[str]
    red_flags: list[str]
    polished: str
    feedback : str
    score : int
    attemtpts : int


class ExtractedJob(BaseModel) : 
    role : str
    skills : list[str]
    seniority : Literal["intern","junior","mid","senior","lead"]


class Review(BaseModel):
    score : int
    feedback:str


