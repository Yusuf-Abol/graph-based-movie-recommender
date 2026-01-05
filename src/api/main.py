
# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


import sys
import os

from ..models.models import RecommendRequest, MovieRec, RecommendResponse

# Global Variables: These will store our models & data

MODELS = {}
MOVIE_METADATA = {}
USER_ITEM_MATRIX = None
ID_MAPPING = {}



# Create the FastAPI application instance
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    
    global MODELS, MOVIE_METADATA, USER_ITEM_MATRIX, ID_MAPPINGS
    
    print("INITIALIZING RECOMMENDER SYSTEM")
    
    print("Loading models...")
    MODELS = {
        
        'gmf': "GMF model placeholder",
        'lightgcn': "LightGCN model placeholder",
        'graphrec': "GraphRec model placeholder",
        'pinsage': "PinSAGE model placeholder",
        'graphsage': "GraphSAGE model placeholder"
    }
    
    
    print("Loading movie metadata...")
    MOVIE_METADATA = {
        1: {"title": "The Matrix", "genres": ["Action", "Sci-Fi"]},
        2: {"title": "Titanic", "genres": ["Romance", "Drama"]},
        3: {"title": "The Godfather", "genres": ["Crime", "Drama"]},
        4: {"title": "Inception", "genres": ["Action", "Sci-Fi"]},
        5: {"title": "Forrest Gump", "genres": ["Drama", "Romance"]}
    }
    
    USER_ITEM_MATRIX = "User-Item Interaction Matrix Placeholder"
    ID_MAPPINGS = {
        "user_to_idx": {},
        "item_to_idx": {}
    }
    
    print(f"Loaded {len(MODELS)} models")
    print(f"Loaded {len(MOVIE_METADATA)} movies")
    print("System ready!")


# Health check endpoint
@app.get("/health")
async def health_check():
    """Simple health check to verify if the API is working"""
    return {
        "status": "healthy",
        "models_loaded": len(MODELS),
        "movies_loaded": len(MOVIE_METADATA),
        "models_available": list(MODELS.keys())
    }

@app.get("/")
async def root():
    """Root endpoint returns basic API information"""
    return {
        "service": "Graph-based Movie Recommender",
        "version": "1.0.0",
        "message": "API is running",
        "models_available": list(MODELS.keys()),
        "total_movies": len(MOVIE_METADATA)
    }



