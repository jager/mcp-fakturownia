import httpx
import logging

async def get_request(url: str, user_agent: str = "") -> dict | None:
    
    """Make a request to fakturownia.pl API"""

    headers = {
        "User-Agent": user_agent,
        "Accept": "application/json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(e)
            return None
        
async def post_request(url: str, data: dict, user_agent: str = "") -> dict | None:
    """Make a POST request to fakturownia.pl API"""

    headers = {
        "User-Agent": user_agent,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=data, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(e)
            return None
        
async def put_request(url: str, data: dict, user_agent: str = "") -> dict | None:
    """Make a POST request to fakturownia.pl API"""

    headers = {
        "User-Agent": user_agent,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.put(url, json=data, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(e)
            return None