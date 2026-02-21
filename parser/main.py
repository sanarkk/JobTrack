from fastapi.middleware.cors import CORSMiddleware
import fastapi
from parser.resume.resume_processor import parser_router


app = fastapi.FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(parser_router, prefix="/parse_resume", tags=["parser"])
