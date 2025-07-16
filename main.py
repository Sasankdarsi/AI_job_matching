from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import tempfile, shutil, os, asyncio
import json

from resume_parser import ResumeParser
from job_fetcher import RapidJobs          
from vector_matcher import MatchingSystem  
from refine_jobs import RefineJobs         



app = FastAPI()
app.add_middleware(
    CORSMiddleware, allow_origins=["*"],
    allow_methods=["*"], allow_headers=["*"]
)

@app.post("/match-jobs")
async def match_jobs(
    resume: UploadFile = File(...),
    roles: str        = Form(...),  
    country: str      = Form(...),
    top_n: int        = Form(...)
):
    # Saving the uploaded file to a temp location
    suffix = os.path.splitext(resume.filename)[1] or ".pdf"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(resume.file, tmp)
        tmp_path = tmp.name
    await resume.close()

    # Fetching Jobs and parsing resume
    parser   = ResumeParser()
    fetcher  = RapidJobs()

    async def parse_resume():
        
        return await asyncio.to_thread(parser.parse, tmp_path)

    async def fetch_jobs():
        role_list = [r.strip() for r in roles.split(", ")]
        
        return await asyncio.to_thread(fetcher.get_jobs, role_list, country)

    # Parsing resume and fetching jobs asynchronously
    try:
        resume_embed, jobs_json = await asyncio.gather(parse_resume(), fetch_jobs())
        jobs = jobs_json["jobs"]          

        # Matching resume to jobs
        matcher = MatchingSystem()
        jobs_embed = matcher.process_jobs(jobs)        
        matcher.load_databases(resume_embed=resume_embed, jobs_embed=jobs_embed)          
        matches = matcher.match_resume_to_jobs(top_n=top_n)

        # Further refining the jobs
        refiner  = RefineJobs()
        resume_text = parser.load_document(tmp_path)
        refined  = refiner.refine_jobs(resume_text, matches)

        with open('refined_results3.json', mode='w') as file:
            json.dump(refined, file, indent=4)


        return {"results": refined}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        os.remove(tmp_path)


   

        