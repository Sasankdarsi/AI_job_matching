from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from typing import List, Dict
from resume_parser import ResumeParser
from models import RefinedJobs
import json

class RefineJobs:
    def __init__(self, model_name: str = "gemini-2.5-flash-lite-preview-06-17", temperature: float = 0.3):
        
        self.llm = ChatGoogleGenerativeAI(model=model_name, temperature=temperature)
        self.output_parser = PydanticOutputParser(pydantic_object=RefinedJobs)

        self.prompt = PromptTemplate(
            input_variables=["resume_text", "title", "company", "location", "description"],
            partial_variables={"format_instructions": self.output_parser.get_format_instructions()},
            template="""
You are an AI assistant that evaluates how well a candidate's resume fits a job.

Your tasks:
1. Summarize the job description in 3–4 lines.
2. Explain in 2–3 lines why the resume is or isn't a good fit.
3. Rate the match from 1 (poor) to 5 (excellent).
4. Suggest one improvement in the resume to improve fit.

{format_instructions}

Resume:
{resume_text}

Job Title: {title}
Company: {company}
Location: {location}
Job Description:
{description}
"""
        )

        
        self.chain = (
            {
                "resume_text": lambda x: x["resume_text"],
                "title": lambda x: x["title"],
                "company": lambda x: x.get("company", "N/A"),
                "location": lambda x: x.get("location", "Unspecified"),
                "description": lambda x: x["description"]
            }
            | self.prompt
            | self.llm
            | self.output_parser
        )

    def refine_jobs(self, resume_text: str, jobs: List[Dict]) -> List[Dict]:
        refined_jobs = []

        for job in jobs:
            try:
                input_data = {
                    "resume_text": resume_text,
                    "title": job.get("title", ""),
                    "company": job.get("company", ""),
                    "location": job.get("location", ""),
                    "description": job.get("description", "")
                }

                result = self.chain.invoke(input_data).model_dump()
                job["Explanation"] = result["Explanation"]
                job["Refined_Description"] = result["Refined_Description"]
                job["Match_Confidence"] = result["Match_Confidence"]
                job["Improvement_Tip"] = result["Improvement_Tip"]
                refined_jobs.append(job)
            except Exception as e:
                print(f"Error refining job '{job.get('title')}': {e}")

        return refined_jobs


