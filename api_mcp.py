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
async def search_player(name_search: str):
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
async def search_player_teams(player_id: str | int):
    """
    Queries football api players/team endpoint given a player id

    Args:
        player_id: player ID as designated by football API (can retrieve via players/profiles query)
    """
    player_id = str(player_id) #cast as str in case of int input

    endpoint = f'/players/teams?player={player_id}'
    data = await make_api_request(endpoint)
    if not data:
        return f"Unable to fetch player team data with player ID: {player_id}"
    return data
    return

@mcp.tool()
async def search_player_statistics(player_id: str | int , team_id: str | int, season: str | int):
    player_id, team_id, season = str(player_id), str(team_id), str(season) #cast as str in case of int input
    endpoint = f'/players/statistics?player={player_id}'
    data = await make_api_request(endpoint)
    if not data:
        return f"Unable to fetch player statistics data with player ID: {player_id}, team ID: {team_id}, and season: {season}"
    return data

"""
For most organized stats retrieval, I'm going to want to use the following players endpoints:
    - /profiles
    - /teams
    These two endpoints to get playerID, then teamIDs and associate seasons with teamIDs
    Then to actually get statistics we need to query the players/statistics endpoint with the following params: player_id, team_id, season (4digit year)
    - /statistics

    Assuming we return a list of [(team_id, [seasons])] tuples from our player/teams query, we can have a loop similar to the following:
    
        for team_id, seasons in list:
            for season in seasons:
                query players/statistics for: player_id, team_id, seasons 

Will probably want a backend function to better parse the retrieved information since it will arrive in an out of sorts manner



"""


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


