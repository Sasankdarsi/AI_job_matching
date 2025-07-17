import streamlit as st
import requests
import time
from datetime import datetime
import json
import iso3166


st.set_page_config(
    page_title="Job Matching System",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Backend configuration
BACKEND_URL = "https://ai-job-matching-po0x.onrender.com"  


st.markdown("""
<style>
    /* Import font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0a0014 0%, #1a0033 25%, #2d1b69 50%, #0f0020 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide default header */
    .stAppHeader, header[data-testid="stHeader"] {
        display: none;
    }
    
    /* Main container styling */
    .main > div {
        padding-top: 2rem;
    }
    
    /* Title styling */
    .euphoria-title {
        font-size: 3.5rem;
        font-weight: 800;
        
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .euphoria-subtitle {
        text-align: center;
        color: #b794f6;
        font-size: 1.2rem;
        margin-bottom: 3rem;
        opacity: 0.8;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background: rgba(16, 0, 43, 0.8) !important;
        border: 2px solid rgba(138, 43, 226, 0.3) !important;
        border-radius: 12px !important;
        color: white !important;
        font-size: 1.1rem !important;
        padding: 12px 16px !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #8338ec !important;
        box-shadow: 0 0 20px rgba(131, 56, 236, 0.4) !important;
    }
    
    /* File uploader styling */
    .stFileUploader > div {
        background: rgba(16, 0, 43, 0.8) !important;
        border: 2px dashed rgba(138, 43, 226, 0.3) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.3s ease !important;
    }
    
    .stFileUploader > div:hover {
        border-color: #8338ec !important;
        box-shadow: 0 0 20px rgba(131, 56, 236, 0.2) !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #ff006e, #8338ec) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 32px !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 20px rgba(255, 0, 110, 0.3) !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px rgba(255, 0, 110, 0.5) !important;
        background: linear-gradient(45deg, #ff1a7a, #9146ff) !important;
    }
    
    /* Job cards */
    .job-card {
        background: rgba(16, 0, 43, 0.9);
        border: 1px solid rgba(138, 43, 226, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .job-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, #ff006e, #8338ec, #3a86ff);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .job-card:hover {
        transform: translateY(-4px);
        border-color: rgba(131, 56, 236, 0.5);
        box-shadow: 0 10px 40px rgba(131, 56, 236, 0.2);
    }
    
    .job-card:hover::before {
        opacity: 1;
    }
    
    .job-logo {
        max-width: 60px;
        max-height: 60px;
        object-fit: contain;
        border-radius: 6px;
        margin-bottom: 0.5rem;
    }
    
    .job-title {
        color: #06ffa5;
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .job-company {
        color: #8338ec;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .job-location {
        color: #b794f6;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }
    
    .job-description {
        color: #e2e8f0;
        font-size: 0.95rem;
        line-height: 1.5;
        margin-bottom: 1rem;
    }
    
    .job-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-bottom: 1rem;
    }
    
    .job-tag {
        background: rgba(131, 56, 236, 0.2);
        color: #b794f6;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        border: 1px solid rgba(131, 56, 236, 0.3);
    }
    
    .job-salary {
        color: #06ffa5;
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    /* Loading animation */
    .loading-text {
        text-align: center;
        color: #8338ec;
        font-size: 1.2rem;
        animation: pulse 1.5s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* Success message */
    .stSuccess {
        background: rgba(6, 255, 165, 0.1) !important;
        border: 1px solid rgba(6, 255, 165, 0.3) !important;
        color: #06ffa5 !important;
    }
    
    /* Error message */
    .stError {
        background: rgba(255, 0, 110, 0.1) !important;
        border: 1px solid rgba(255, 0, 110, 0.3) !important;
        color: #ff006e !important;
    }
</style>
""", unsafe_allow_html=True)

# Backend API functions
def search_jobs_api(file, query, location):
    try:
        form_data = {
            'roles': query,
            'country': location,
            'top_n': 10
        }
        files = {"resume": (file.name, file, file.type)}
        
        response = requests.post(
            f"{BACKEND_URL}/match-jobs",
            data=form_data,
            files=files,
            timeout=60
        )

        if response.status_code == 200:
            return response.json().get("results", [])
        else:
            st.error(f"❌ Backend error: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"❌ Error communicating with backend: {e}")
        return []



def render_job_card(job):
    
    # Handle both dict and object responses
    if isinstance(job, dict):
        title = job.get('title', 'Unknown Title')
        company = job.get('company', 'Unknown Company')
        location = job.get('location', 'Unknown Location')
        description = job.get('Refined_Description', 'No description available')
        tags = job.get('tags', [])
        salary = job.get('salary', 'Not specified')
        posted = job.get('datePosted', 'Unknown')
        job_url = job.get('url', '#')
        job_logo = job.get('image', './uploaded_files/logo.png')
        match_score = round(job.get('similarity_score') * 100, 2)
        improvement_tip = job.get('Improvement_Tip')
    else:
        title = getattr(job, 'title', 'Unknown Title')
        company = getattr(job, 'company', 'Unknown Company')
        location = getattr(job, 'location', 'Unknown Location')
        description = getattr(job, 'description', 'No description available')
        tags = getattr(job, 'tags', [])
        salary = getattr(job, 'salary', 'Not specified')
        posted = getattr(job, 'posted', 'Unknown')
        job_url = getattr(job, 'job_url', '#')
        job_logo = getattr(job, 'image', '#')
    
    # Truncate description if too long
    if len(description) > 200:
        description = description[:200] + "..."
    
    card_html = f"""
    <div class="job-card">
        <div class="job-title">
            <img src="{job_logo}" width="30" style="vertical-align: middle; margin-right: 8px;"> 
            {title}
        </div>
        <div class="job-company">{company}</div>
        <div class="job-location">📍 {location} • {posted}</div>
        <div class="job-description">{description}</div>
        <div class="job-tags">
            <span class="job-tag">🧠 Match Score: {match_score}%</span>
        </div>
        <div class="job-salary" style="margin-top: 0.5rem;">
            🔧 <strong>Improvement Tip:</strong> {improvement_tip}
        </div>
        <br>
        <a href="{job_url}" target="_blank" style="color: #06ffa5; text-decoration: none; font-weight: 600;">
            🔗 View Job Details
        </a>
    </div>
    """

    return card_html

def main():
    # Initialize session state
    if 'jobs' not in st.session_state:
        st.session_state.jobs = []
    if 'show_results' not in st.session_state:
        st.session_state.show_results = False
    if 'resume_skills' not in st.session_state:
        st.session_state.resume_skills = []
    
    # Header
    st.markdown('<h1 class="euphoria-title">Job Matching System</h1>', unsafe_allow_html=True)
    st.markdown('<p class="euphoria-subtitle">Find jobs that fit best for your resume</p>', unsafe_allow_html=True)
    
    # Create centered columns for better layout
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Search query input
        query = st.text_input(
            "🔍 Search for desired jobs...",
            placeholder="e.g., Machine Learning Engineer, Data Scientist, Computer Vision",
            key="job_query"
        )
        
        
        location = st.selectbox(
            "📍 Location",
            [key for key in iso3166.countries_by_name]
        )
        
        # Resume upload
        uploaded_file = st.file_uploader(
            "📄 Upload Resume",
            type=['pdf', 'doc', 'docx', 'txt'],
            help="Upload your resume to get personalized job matches"
        )
    
    # Search button
    search_col1, search_col2, search_col3 = st.columns([1, 2, 1])
    with search_col2:
        search_clicked = st.button("🚀 GET JOBS", key="search_jobs")
    
    # Handle resume upload
    # if uploaded_file is not None:
    #     if uploaded_file.name not in st.session_state.get('uploaded_files', []):
    #         with st.spinner("🤖 Analyzing resume..."):
    #             upload_result = upload_resume_api(uploaded_file)
    #             if upload_result:
    #                 st.success(f"✅ Resume uploaded: {uploaded_file.name}")
    #                 st.session_state.resume_skills = upload_result.get('extracted_skills', [])
    #                 st.session_state.uploaded_files = st.session_state.get('uploaded_files', []) + [uploaded_file.name]
                    
    #                 # Display extracted skills
    #                 if st.session_state.resume_skills:
    #                     st.info(f"🎯 Extracted skills: {', '.join(st.session_state.resume_skills[:10])}")
    
    # Search functionality
    if search_clicked:
        if query and uploaded_file:

            with st.empty():
                st.markdown('<div class="loading-text"> Analyzing opportunities...</div>', unsafe_allow_html=True)
                time.sleep(1)
            
            # Prepare search parameters
            search_location = iso3166.countries.get(location).alpha2 if location else None
            
            # Call backend API
            jobs_data = search_jobs_api(
                file=uploaded_file,
                query=query,
                location=search_location
            )

            # with open('refined_results3.json', mode='r') as file:
            #     jobs_data = json.load(file)
            
            if jobs_data:
                st.session_state.jobs = jobs_data
                st.session_state.show_results = True
            else:
                st.session_state.jobs = []
                st.session_state.show_results = True
        else:
            st.warning("⚠️ Please enter a search query and upload your resume to get started!")
    
    # Display results
    if st.session_state.show_results:
        if st.session_state.jobs:
            st.markdown(f"🎯 Found {len(st.session_state.jobs)} matching opportunities")
            
            # Display jobs in a grid
            for i in range(0, len(st.session_state.jobs), 2):
                cols = st.columns(2)
                
                # First job in row
                with cols[0]:
                    st.markdown(render_job_card(st.session_state.jobs[i]), unsafe_allow_html=True)
                
                # Second job in row (if exists)
                if i + 1 < len(st.session_state.jobs):
                    with cols[1]:
                        st.markdown(render_job_card(st.session_state.jobs[i + 1]), unsafe_allow_html=True)
        else:
            st.warning("🔍 No jobs found matching your criteria. Try different keywords!")
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<div style="text-align: center; color: #8338ec; opacity: 0.7; margin-top: 2rem;">'
        '• Powered by AI •'
        '</div>', 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
