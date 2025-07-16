import os
import json
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

class MatchingSystem:
    
    def __init__(self, api_key: Optional[str] = None):
        
        
        load_dotenv()
        
        
        if api_key:
            os.environ["GOOGLE_API_KEY"] = api_key
        elif "GOOGLE_API_KEY" not in os.environ:
            os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
            
        # Initialize embedding model
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, 
            chunk_overlap=200
        )
        
        # Initialize vectorstores
        self.resume_db = None
        self.jobs_db = None
        
        # Storage for original job data
        self.job_data = []
    
        
    def process_jobs(self, jobs: List[Dict[str, Any]], jobs_path: str = "./jobs_db"):
        
        # Store the original job data for later retrieval
        self.job_data = jobs
        
        # Convert jobs to documents
        job_docs = []
        for i, job in enumerate(jobs):
            # Create a combined text representation of the job
            job_text = f"Title: {job.get('title', '')}\n"
            job_text += f"Description: {job.get('description', '')}\n"
            job_text += f"Requirements: {job.get('requirements', '')}\n"
            job_text += f"Company: {job.get('company', '')}\n"
            job_text += f"Location: {job.get('location', '')}\n"
            
            # Create a document with the job index in metadata
            job_docs.append(Document(
                page_content=job_text,
                metadata={"source": "job", "type": "job", "index": i}
            ))
        
        # Split into chunks if needed
        job_chunks = self.text_splitter.split_documents(job_docs)
        
        # Create and save the vector store
        self.jobs_db = FAISS.from_documents(
            documents=job_chunks,
            embedding=self.embeddings
        )
        
        # # Save to disk
        # self.jobs_db.save_local(jobs_path)
        print(f"Jobs processed and embeddings generated")
        
    def load_databases(self, 
                      resume_embed: str):
        
        # Load resume database if it exists
        self.resume_db = resume_embed

        print("Resume and Job embeddings are loaded")



    def match_resume_to_jobs(self, top_n: int = 5):
        
        if not self.resume_db or not self.jobs_db:
            raise ValueError("Resume and jobs databases should be added first")
        
        if not self.job_data:
            raise ValueError("Original job data is not available")
        
        # Get the resume text to use as query
        resume_docs = self.resume_db.similarity_search(
            query="",  # Empty query to get all documents
            k=1000  # Large number to get all chunks
        )
        
        # Combine all resume chunks into one query
        resume_query = " ".join([doc.page_content for doc in resume_docs])
        
        # Find the most similar jobs
        job_matches = self.jobs_db.similarity_search_with_score(
            query=resume_query,
            k=top_n * 3  # Get more than needed to account for duplicates
        )
        
        # Extract job indices and deduplicate
        seen_indices = set()
        matched_jobs = []
        
        for doc, score in job_matches:
            job_index = doc.metadata.get("index")
            
            # Skip if we've already seen this job or index is invalid
            if job_index is None or job_index in seen_indices:
                continue
                
            # Get the original job data
            if 0 <= job_index < len(self.job_data):
                job = self.job_data[job_index].copy()
                job["similarity_score"] = float(score)  # Add the score
                matched_jobs.append(job)
                seen_indices.add(job_index)
                
                # Stop once we have enough matches
                if len(matched_jobs) >= top_n:
                    break
        
        # Sort by similarity score (lower is better)
        matched_jobs.sort(key=lambda x: x["similarity_score"], reverse = False)
        
        return matched_jobs
    
    def analyze_match(self, job: Dict[str, Any]) -> Dict[str, Any]:
        
        if not self.resume_db:
            raise ValueError("Resume database must be loaded first")
            
        # Create a combined job text for analysis
        job_text = f"Title: {job.get('title', '')}\n"
        job_text += f"Description: {job.get('description', '')}\n"
        job_text += f"Requirements: {job.get('requirements', '')}\n"
        
        # Get the resume chunks
        resume_chunks = self.resume_db.similarity_search(
            query="",
            k=1000
        )
        resume_text = " ".join([doc.page_content for doc in resume_chunks])
        
        # Embed both texts
        job_embedding = self.embeddings.embed_query(job_text)
        resume_embedding = self.embeddings.embed_query(resume_text)
        
        # Convert to numpy arrays for computation
        job_array = np.array(job_embedding)
        resume_array = np.array(resume_embedding)
        
        # Compute cosine similarity
        dot_product = np.dot(job_array, resume_array)
        job_norm = np.linalg.norm(job_array)
        resume_norm = np.linalg.norm(resume_array)
        cosine_similarity = dot_product / (job_norm * resume_norm)
        
        # Return analysis
        return {
            "job_title": job.get("title", ""),
            "similarity_score": job.get("similarity_score", 0.0),
            "cosine_similarity": float(cosine_similarity),
            "match_confidence": f"{float(cosine_similarity) * 100:.1f}%"
        }

