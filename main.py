from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from graph import run_user_query

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins; replace with a list for specific domains
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

@app.post("/career-copilot")
async def get_career_copilot(query: str):
    """Get a response from the Career Copilot system based on a user query.
    
    Args:
        query (str): The user's query
    
    Returns:
        Dict[str, str]: A dictionary containing the query's category and response
    """
    return run_user_query(query)

