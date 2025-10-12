from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from post_moderator import PostModerator

app = FastAPI()
moderator = PostModerator()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/moderate/")
def moderate(text: str):
    is_inappropriate = moderator.moderate(text)
    return {"inappropriate": is_inappropriate}