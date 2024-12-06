from fastapi import FastAPI, HTTPException, Query
import json
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

app = FastAPI()

# Enable CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load game data from JSON file
with open('data.json') as f:
    game_data = json.load(f)

# Minimal information for listing games with pagination, sorting, and filtering
@app.get("/games")
def list_games(
    page: int = 1,
    limit: int = 10,
    sort_by: Optional[str] = Query(None, regex="^(title|release_date)$"),
    order: Optional[str] = Query("asc", regex="^(asc|desc)$"),  # Add order parameter (default: asc)
    filter_platform: Optional[str] = None
):
    # Filtering
    filtered_games = [game for game in game_data if filter_platform is None or game["platform"] == filter_platform]
    
    # Sorting
    if sort_by:
        reverse = order == "desc"
        filtered_games.sort(key=lambda x: x[sort_by], reverse=reverse)

    # Pagination
    start = (page - 1) * limit
    end = start + limit
    paginated_games = filtered_games[start:end]

    minimal_data = [
        {"id": game["id"], "title": game["title"], "release_date": game["release_date"], "enabled": game["enabled"]}
        for game in paginated_games
    ]

    return {
        "total": len(filtered_games),
        "page": page,
        "limit": limit,
        "games": minimal_data
    }

# Fetch game details by ID
@app.get("/games/{game_id}")
def read_game(game_id: int):
    game = next((game for game in game_data if game["id"] == game_id), None)
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return {"game": game}

# Search games
@app.get("/search")
def search_games(query: str):
    searched_games = [game for game in game_data if len(query) > 0 and query.lower() in game["title"].lower()]
    if searched_games is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return {
        "games": searched_games
    }