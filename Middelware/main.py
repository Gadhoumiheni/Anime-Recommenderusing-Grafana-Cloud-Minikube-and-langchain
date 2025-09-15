from src.app import get_anime_recommendation
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Anime Recommender API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or replace "*" with ["http://localhost:3000"] for Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserRequest(BaseModel):
    query: str

@app.post("/recommend")
def recommend_anime(request: UserRequest):
    try:
        result = get_anime_recommendation(request.query)
        response = {
            "answer": result["result"],
            "sources": [doc.page_content for doc in result["source_documents"]],
        }
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
