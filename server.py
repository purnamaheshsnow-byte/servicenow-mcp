from mcp.server.fastmcp import FastMCP
from sn_client import ServiceNowClient
from fastapi import FastAPI

app = FastAPI()
# Create MCP Server
mcp = FastMCP("ServiceNow MCP")
# Initialize ServiceNow Client
snow = ServiceNowClient()


@mcp.tool()
async def get_open_incidents(limit: int = 10):
    """
    Get recent incidents from ServiceNow.
    """

    incidents = await snow.get_incidents(limit)

    return [
        {
            "number": incident.get("number"),
            "state": incident.get("state"),
            "priority": incident.get("priority"),
            "short_description": incident.get("short_description")
        }
        for incident in incidents
    ]


@mcp.tool()
async def get_incident_details(incident_number: str):
    """
    Get details for a specific incident.
    Example: INC0012345
    """

    incident = await snow.get_incident(incident_number)

    if not incident:
        return f"Incident {incident_number} not found"
    #print(f"get_incident_details result: {incident}",flush=True)
    return incident


@mcp.tool()
async def create_incident(
    short_description: str,
    description: str = ""
):
    """
    Create a new ServiceNow incident.
    """

    result = await snow.create_incident(
        short_description,
        description
    )

    return {
        "number": result.get("number"),
        "sys_id": result.get("sys_id"),
        "message": "Incident created successfully"
    }


@mcp.tool()
async def search_knowledge(keyword: str):
    """
    Search ServiceNow Knowledge Base.
    """

    articles = await snow.search_kb(keyword)

    return [
        {
            "number": article.get("number"),
            "title": article.get("short_description")
        }
        for article in articles
    ]


@mcp.tool()
async def get_change_requests():
    """
    Retrieve Change Requests.
    """

    changes = await snow.get_change_requests()

    return [
        {
            "number": change.get("number"),
            "state": change.get("state"),
            "short_description":
                change.get("short_description")
        }
        for change in changes
    ]


mcp_app = mcp.streamable_http_app()

app = FastAPI(
    title="ServiceNow MCP",
    lifespan=mcp_app.router.lifespan_context
)

app.mount("/mcp", mcp_app, name="mcp")

@app.get("/health")
async def health_check():
    """
    Verify MCP Server is running.
    """

    return {
        "status": "healthy",
        "server": "ServiceNow MCP"
    }

@app.get("/test-snow")
async def test_snow():
    incidents = await snow.get_incidents(1)
    return incidents

@app.get("/")
async def root():
    return {"status": "server is running..."}

# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run(
#         app,
#         host="0.0.0.0",
#         port=8000
#     )

# if __name__ == "__main__":
#     mcp.run(
#         transport="http",
#         host="0.0.0.0",
#         port=8000
#     )

import os

if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000))
    )
