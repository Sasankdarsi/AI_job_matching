# AI Job Matching System

This is an AI-powered job matching system that analyzes resumes to find tailored job opportunities using advanced language models and vector similarity. It provides personalized explanations, match scores, and improvement tips to help candidates better align with job descriptions.

## Tech Stack

* **Streamlit** – Powers the interactive web interface where users can upload resumes, search for jobs, and view AI-tailored job recommendations in real time.

* **FastAPI** – Handles backend operations including resume parsing, job fetching, vector-based matching, and AI-driven refinements with asynchronous processing for efficiency.

* **Google Gemini API** – Provides advanced language model capabilities for semantic understanding of resumes and job descriptions, embeddings generation, and personalized recommendations.

* **FAISS** – Enables high-speed vector similarity searches to accurately match resumes with job listings.

* **RapidAPI** – Supplies real-time job data based on user-specified roles and locations.



## **Workflow Overview**

![Workflow Diagram](https://drive.google.com/uc?export=view&id=1uOrBDZFYwnjBemQ0zob9qT0J7m-VfHtv)


This system processes a resume and matches it to suitable job listings through the following steps:

1. **Request Handling** – Receives the job match request, extracts the resume file extension, and saves it temporarily.
2. **Asynchronous Processing** – Parses resume data and fetches job listings from the API in parallel.
3. **Matching Workflow** – Initializes the matcher, processes raw job entries, and computes top resume-job matches.
4. **Refinement Workflow** – Loads the full resume text and refines the matched jobs for better recommendations.
5. **Response & Cleanup** – Returns the final response with matches or raises an error, followed by cleanup of temporary files.



## Project Structure

```
.
├── app.py              # Streamlit frontend
├── main.py             # FastAPI backend
├── job_fetcher.py      # Fetches jobs from external APIs
├── resume_parser.py    # Parses and embeds resumes
├── vector_matcher.py   # Matches resumes to jobs using vector similarity
├── refine_jobs.py      # Refines and explains job matches
├── models.py           # Pydantic models for structured data
├── requirements.txt    # Python dependencies
```


## Future Work & Improvements

* **Multi-Agent Framework:** Use specialized AI agents for parsing, job aggregation, matching, and feedback to improve scalability.

* **Aggregated Job Sources:** Fetch job listings from multiple APIs and platforms for broader opportunities.
* **User Authentication:** Implement login, profiles, and saved preferences for a personalized experience.
* **Enhanced UI/UX:** Redesign the interface for better navigation and interactive recommendations.
* **Feedback-Driven Matching:** Allow users to rate matches to refine AI recommendations.
* **Cloud Deployment:** Dockerize and deploy on cloud platforms with secure API key management.




