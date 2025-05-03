from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("multi_alert_system")

# Constants
NWS_API_BASE = "https://api.weather.gov"
USGS_API_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_day.geojson"
USER_AGENT = "disaster-mcp-app/2.0"

# Generic HTTP GET
async def fetch_json(url: str, headers: dict = None) -> dict[str, Any] | None:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers or {}, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

# Weather alert formatter
def format_weather_alert(feature: dict) -> str:
    props = feature["properties"]
    return f"""🔔 **Weather Alert**
- **Event**: {props.get('event', 'N/A')}
- **Area**: {props.get('areaDesc', 'N/A')}
- **Severity**: {props.get('severity', 'N/A')}
- **Headline**: {props.get('headline', 'N/A')}
- **Description**: {props.get('description', 'N/A')}
- **Instructions**: {props.get('instruction', 'N/A')}
"""

# Earthquake alert formatter
def format_quake_alert(feature: dict) -> str:
    props = feature["properties"]
    return f"""🌍 **Earthquake Alert**
- **Location**: {props.get('place', 'Unknown')}
- **Magnitude**: {props.get('mag', 'N/A')}
- **Time**: {props.get('time', 'N/A')}
- **More Info**: {props.get('url', 'N/A')}
"""

# MCP Tools

@mcp.tool()
async def get_weather_alerts(state: str) -> str:
    """Get active weather alerts for a US state."""
    url = f"{NWS_API_BASE}/alerts/active/area/{state.upper()}"
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    data = await fetch_json(url, headers)

    if not data or "features" not in data:
        return "❌ Could not fetch weather alerts."
    if not data["features"]:
        return "✅ No active alerts for this state."

    return "\n---\n".join(format_weather_alert(f) for f in data["features"])

@mcp.tool()
async def get_earthquake_alerts() -> str:
    """Get recent significant earthquakes (last 24 hours)."""
    data = await fetch_json(USGS_API_URL)

    if not data or "features" not in data:
        return "❌ Failed to retrieve earthquake data."
    if not data["features"]:
        return "✅ No significant earthquakes in the past 24 hours."

    return "\n---\n".join(format_quake_alert(f) for f in data["features"])

@mcp.tool()
async def travel_weather_risk(city: str, state: str) -> str:
    """Check weather risks before travel."""
    state_alerts = await get_weather_alerts(state)
    return f"🧳 **Travel Risk for {city}, {state}**\n\n{state_alerts}"

@mcp.tool()
async def logistics_route_alerts(start_state: str, end_state: str) -> str:
    """Predict delivery issues across a route."""
    start_alerts = await get_weather_alerts(start_state)
    end_alerts = await get_weather_alerts(end_state)

    return f"""🚚 **Logistics Alert Report**
Route: {start_state} ➜ {end_state}

📍 Start State Alerts:
{start_alerts}

📍 End State Alerts:
{end_alerts}
"""

@mcp.tool()
async def event_weather_check(city: str, state: str) -> str:
    """Check alerts for upcoming events in a location."""
    alerts = await get_weather_alerts(state)
    return f"🎪 **Event Risk Check in {city}, {state}**\n\n{alerts}"

@mcp.tool()
async def agriculture_weather_check(state: str) -> str:
    """Farmer-specific weather alert assistant."""
    alerts = await get_weather_alerts(state)
    return f"🌾 **Agriculture Weather Report for {state}**\n\n{alerts}"

@mcp.tool()
async def smart_home_conditions(state: str) -> str:
    """Trigger automation if rain/storm forecasted."""
    url = f"{NWS_API_BASE}/alerts/active/area/{state.upper()}"
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    data = await fetch_json(url, headers)

    if not data or "features" not in data or not data["features"]:
        return "✅ No weather-based automation needed."

    triggers = []
    for feature in data["features"]:
        event = feature["properties"].get("event", "").lower()
        if "rain" in event or "storm" in event:
            triggers.append("⛔ Detected precipitation alert! Consider disabling sprinklers or securing outdoors.")

    return "\n".join(triggers) if triggers else "✅ No automation triggers detected."

@mcp.resource("echo://{message}")
def echo_resource(message: str) -> str:
    return f"🔁 Echo: {message}"

# Start FastMCP Server
# if __name__ == "__main__":
#     mcp.run()
