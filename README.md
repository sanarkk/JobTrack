# JobTrack - Stop searching. Start matching!

## Inspiration
Job hunting is overwhelming. Candidates apply to roles without knowing if they truly fit, while recruiters sift through mountains of resumes.  
**JobTrack** answers a simple question:  
*What if matching talent to opportunity could be intelligent, automated, and instant?*

It analyzes resumes, understands job postings, and connects the dots using contextual matching.

---

## What It Does
JobTrack automatically:
- Analyzes resumes and parses job postings  
- Compares skills using a contextual matching model  
- Computes match scores between candidates and jobs  
- Outputs clean, rankable results for dashboards or applications  

It focuses on compatibilities, making matches more accurate and fair.

---

## How We Built It
1. **Job Parsing** – Normalizes and structures infromation about job postings, stores position information into relational database.
2. **Resume Analysis** - Receives resume and analyzes with developed ML model, leverages skillset and experience extraction.
3. **Position-Resume Skill Matching** - Compares position's and resume's skill descriptions using own ML model via contextual matching.
4. **API Routing** - Ensures smooth operations of client with database, backend with ML, and data extraction and user authentication.
5. **User Interface** - Implements client communication with API as well as modern and pleasant UI.
6. **AI Assistant** - Provides personalized tips using user's resume context, which allows user to improve quality of the resume.
7. **Docker Conterization** - Ensures portability of API services on any host machine.
8. **Database** - PostgreSQL database, which stores user's authentication credentials, parsed jobs, resume records, and parsed job matchings.

---

## Challenges
- Messy real-world data and inconsistent skill formats 
- Complex database schemas and field mapping
- Integrating ML models with structured inputs  
- Implementing communication of API and ML model services
- Ensure consistent database tables and information storage

These challenges refined the architecture and strengthened the system.

---

## Accomplishments
- Designed and implemented a clean, modern web interface that makes job discovery intuitive and enjoyable
- Built a seamless end‑to‑end flow between the frontend, API, database, and ML matching engine
- Delivered a responsive, user‑friendly experience that feels polished, fast, and ready for real users

---

## Potential Next Steps
- Build recruiter and candidate dashboards   
- Use embeddings for deeper semantic matching
- Deploy as a real-time API for job platforms  

JobTrack is ready to evolve into a full intelligent job hunt assistant.

---

## Technical Stack
- Frontend: React, TypeScript, SCSS, React-Hot-Toast, Axios, Lucid-React-Icons
- Backend: FastAPI, Python, SQLAlchemy, Docker, JWT, requests
- ML: Python, Scikit-learn, SentenceTransformers, json, Llama
- Database: PostgreSQL, Supabase
- Parser: Playwright
