from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
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

@app.post("/add_pattern/")
def add_pattern(pattern: str):
    moderator.add_inappropriate_pattern(pattern)
    return {"status": "Pattern added"}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)