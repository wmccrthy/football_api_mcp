"""
Objective of this file is to setup an MCP server to link to Cursor s.t it can
easily query the football API I am using for my pet project; my thinking is 
that if Cursor can query the API, it will have a much easier time helping me build
the backend, linking the frontend to this backend, and debugging accordingly. Generally,
it will provide it much better context as to the format of this API's responses and thus
be able to better determine appropriate querying approaches and frontend solutions.
"""
from typing import Any
# import asyncio
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("football")

# Constants
FOOTBALL_API_BASE = "http://v3.football.api-sports.io"

async def make_api_request(endpoint: str):
    headers = {
        'x-rapidapi-host': FOOTBALL_API_BASE,
        'x-rapidapi-key': ""
    }

    async with httpx.AsyncClient() as conn:
        try:
            response = await conn.get(FOOTBALL_API_BASE + endpoint, headers = headers, timeout = 30.0)
            response.raise_for_status()
            return response.json()['response']
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            print(f"Request error: {str(e)}")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
        
"""
Functions for formatting data returned from common API requests
"""
def list_json(data):
    return [obj for obj in data]


"""
Functions for querying specific endpoints
"""

@mcp.tool()
async def search_play(name_search: str):
    """
    Queries football api players endpoint with a search

    Args:
        name_search: player name in any format (first, last, full, etc)
    """
    endpoint = f'/players/profiles?search={name_search}'
    data = await make_api_request(endpoint)
    if not data:
        return f"Unable to fetch player data with search: {name_search}"
    return data

@mcp.tool()
async def search_leagues(name_search: str):
    """
    Queries football api leagues endpoint with a search

    Args:
        name_search: league name/country query string
    """
    endpoint = f'/leagues?search={name_search}'
    data = await make_api_request(endpoint)
    
    if not data:
        return f"Unable to fetch leagues data with search: {name_search}"
    return data

if __name__ == "__main__":
    # Initalize and run MCP server
    mcp.run(transport='stdio')

"""
Some testing code
"""
# asyncio.run(search_play("yamal"))


