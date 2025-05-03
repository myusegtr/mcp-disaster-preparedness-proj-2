from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("disaster_alerts")

# Constants
NWS_API_BASE = "https://api.weather.gov"
USGS_API_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_day.geojson"
USER_AGENT = "disaster-app/1.0"

# Shared NWS request
async def make_nws_request(url: str) -> dict[str, Any] | None:
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

def format_alert(feature: dict) -> str:
    props = feature["properties"]
    return f"""
    Event: {props.get('event', 'Unknown')}
    Area: {props.get('areaDesc', 'Unknown')}
    Severity: {props.get('severity', 'Unknown')}
    City_description: {props.get('city_description', 'Unknown')}
    Description: {props.get('description', 'No description available')}
    Instructions: {props.get('instruction', 'No specific instructions provided')}
    """

@mcp.tool()
async def get_weather_alerts(state: str) -> str:
    """Get weather alerts for a US state."""
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."
    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)


@mcp.tool()
async def get_earthquake_alerts() -> str:
    """Get recent significant earthquake alerts (past 24h)."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(USGS_API_URL, timeout=30.0)
            response.raise_for_status()
            data = response.json()
        except Exception:
            return "Failed to fetch earthquake data."

    features = data.get("features", [])
    if not features:
        return "No significant earthquakes reported in the past 24 hours."

    alerts = []
    for quake in features:
        props = quake["properties"]
        alerts.append(
            f"""
            Location: {props.get('place', 'Unknown')}
            Country: {props.get('country', 'Unknown')}
            City: {props.get('city', 'Unknown')}
            Magnitude: {props.get('mag', 'N/A')}
            Time: {props.get('time', 'N/A')}
            More Info: {props.get('url', 'N/A')}
            """
        )
    return "\n---\n".join(alerts)


@mcp.resource("echo://{message}")
def echo_resource(message: str) -> str:
    return f"Resource echo: {message}"

if __name__ == "__main__":
    mcp.run()

