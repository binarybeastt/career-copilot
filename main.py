from fastapi import FastAPI
from graph import run_user_query

app = FastAPI()

@app.post("/career-copilot")
async def get_career_copilot(query: str):
    """Get a response from the Career Copilot system based on a user query.
    
    Args:
        query (str): The user's query
    
    Returns:
        Dict[str, str]: A dictionary containing the query's category and response
    """
    return run_user_query(query)

