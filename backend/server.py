from fastapi import FastAPI, Request
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

@app.post("/moderate")
async def moderate(request: Request):
    data = await request.json()
    text = data.get("text", "")
    is_inappropriate = moderator.moderate(text)
    return {"inappropriate": is_inappropriate}

@app.post("/report")
async def report(request: Request):
    data = await request.json()
    pattern = data.get("text", "")
    moderator.add_inappropriate_pattern(pattern)
    return {"status": "Pattern added"}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)