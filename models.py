from pydantic import BaseModel, Field
from typing import List, Optional

class Information(BaseModel):
    name: str = Field(description="Extract the name of the Candidate.")
    Roles: List[str] = Field(description="Determine four job roles to which the candidate is suitable.")


class RefinedJobs(BaseModel):
    Refined_Description: str = Field(
        description="A concise summary of the job description, limited to 3–4 lines. Focus on key responsibilities and required skills."
    )
    Explanation: str = Field(
        description="A brief justification (2–3 lines) explaining why this job is a good fit for the candidate based on their resume."
    )
    Match_Confidence: int = Field(
        ge=1, le=100,
        description="An integer percentage indicating how well the candidate’s resume aligns with the job requirements."
    )
    Improvement_Tip: Optional[str] = Field(
        default=None,
        description="One actionable suggestion to improve the resume's relevance for this specific job (e.g., adding a missing skill or clarifying experience)."
    )

