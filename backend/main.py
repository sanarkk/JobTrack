from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.user_api import router as user_router
from backend.api.chatbot_api import router as chatbot_router
from backend.api.positions_api import router as positions_router
from backend.config import ENABLE_MATCHED_POSITIONS
from backend.services.matching_service import assert_model_ready

app = FastAPI()

if ENABLE_MATCHED_POSITIONS:
    assert_model_ready()


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

app.include_router(user_router)
app.include_router(positions_router)
app.include_router(chatbot_router)
