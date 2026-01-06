
# main.


from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware


import sys
import os

from ..models.models import RecommendRequest, MovieRec, RecommendResponse

# store our models & data

MODELS = {}
MOVIE_METADATA = {}
USER_MOVIE_MATRIX = None
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
    
    USER_MOVIE_MATRIX = "User-Movie Interaction Matrix Placeholder"
    ID_MAPPINGS = {
        "user_to_idx": {},
        "movie_to_idx": {}
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


#  model endpoint
@app.get("/models")
async def get_available_models():
    """Get list of available recommendation models"""
    return {
        "available_models": list(MODELS.keys()),
        "model_count": len(MODELS)
    }



# recommendation endpoint (core functionality)
@app.post("/recommend", response_model=RecommendResponse)
async def recommend(request: RecommendRequest):
    """
    Generate movie recommendations for a user
    This is where the recommendation logic will go
    """
    print(f"\nRECEIVED RECOMMENDATION REQUEST:")
    print(f"- User ID: {request.user_id}")
    print(f"- Model Type: {request.model_type}")
    print(f"- Top K: {request.top_k}")
    print(f"- Exclude Rated: {request.exclude_rated}")
    
    # Validate that the requested model exists
    if request.model_type not in MODELS:
        raise HTTPException(
            status_code=400,
            detail=f"Model '{request.model_type}' not available. Available models: {list(MODELS.keys())}"
        )
    
    # Validate that we have movie data
    if not MOVIE_METADATA:
        raise HTTPException(
            status_code=500,
            detail="No movie metadata available"
        )
    
    # Validate that top_k is not larger than available movies
    max_recommendations = min(request.top_k, len(MOVIE_METADATA))
    
    print(f"Generating {max_recommendations} recommendations using {request.model_type}...")
    

    
    # Get all movie IDs
    all_movie_ids = list(MOVIE_METADATA.keys())
    
    # For demo purposes, we'll return the first 'max_recommendations' movies
    # In reality, the model would calculate scores for each movie for this user
    selected_movie_ids = all_movie_ids[:max_recommendations]
    
    # Create recommendation objects
    recommendations = []
    for i, movie_id in enumerate(selected_movie_ids):
        movie_info = MOVIE_METADATA[movie_id]
        # Simulate predicted ratings (in real app, model would calculate these)
        predicted_rating = 5.0 - (i * 0.1)  # Slightly decreasing ratings
        
        recommendations.append(MovieRec(
            movie_id=movie_id,
            title=movie_info["title"],
            predicted_rating=predicted_rating,
            genres=movie_info["genres"]
        ))
    
    print(f"✓ Generated {len(recommendations)} recommendations!")
    
    # Return the structured response
    return RecommendResponse(
        user_id=request.user_id,
        model_used=request.model_type,
        recommendations=recommendations,
        total_considered=len(MOVIE_METADATA)
    )

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



