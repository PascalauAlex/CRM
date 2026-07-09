from fastmcp import FastMCP
import os
from typing import Any
import httpx
from fastmcp.exceptions import ToolError
from fastmcp.server.dependencies import get_http_headers

mcp = FastMCP(name="crm_mcp_server")

REST_BASE_URL = os.getenv("CRM_REST_BASE_URL", "http://127.0.0.1:8000")
MCP_HOST = os.getenv("MCP_HOST", "127.0.0.1")
MCP_PORT = int(os.getenv("MCP_PORT", "8001"))
HTTP_TIMEOUT = float(os.getenv("CRM_REST_TIMEOUT", "15"))
TOOL_ERROR_MESSAGE = "REST API responded with"

def _auth_header() -> dict[str, str]:
    headers = get_http_headers(include_all=True)  
    token = headers.get("authorization")
    if not token:
        raise ToolError("Request without token")
    return {"Authorization": token}

def _unwrap_results(payload: Any) -> tuple[list, int | None]:
    """Normalizeaza raspunsul DRF: paginat ({results, count}) sau lista simpla."""
    if isinstance(payload, dict) and "results" in payload:
        return payload["results"], payload.get("count")
    if isinstance(payload, list):
        return payload, len(payload)
    return [payload], 1

def over_400_status(resp):
    if resp.status_code > 400:
        raise ToolError(f"{TOOL_ERROR_MESSAGE} {resp}")


_client = None
def get_client() -> httpx.AsyncClient:
    global _client
    if _client is None:
        _client = httpx.AsyncClient(timeout=HTTP_TIMEOUT,follow_redirects=True)
    return _client


# LEADS 
@mcp.tool(name="list_all_leads",description="Show all leads corresponding to a team")
async def list_all_leads():
    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT, follow_redirects=True) as client:
        resp = await client.get(f"{REST_BASE_URL}/api/v1/leads/fetchAllLeads/", headers=_auth_header())
    if resp.status_code >= 400:
        raise ToolError(f"REST API responded with {resp.status_code}: {resp.text[:200]}")
    results, count = _unwrap_results(payload=resp.json())
    return {"count": count, "leads":results}


@mcp.tool(name="leads_by_status",description="Get the leads by the status, eg.new, contacted, in progress, lost, won, inactive")
async def get_lead_by_status(status: str):
    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT, follow_redirects=True) as client:
        resp = await client.get(f"{REST_BASE_URL}/api/v1/leads?status={status}",headers=_auth_header())
    if resp.status_code >= 400:
        raise ToolError(f"REST API responded with {resp.status_code} : {resp.text[:200]}")
    results, count = _unwrap_results(payload=resp.json())
    return {"count":count, "leads":results}

@mcp.tool(name="get_lead_by_company",description="Get a particular lead by the company name")
async def get_lead_by_company(company:str):
    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT,follow_redirects=True) as client:
        resp = await client.get(f"{REST_BASE_URL}/api/v1/leads?company={company}",headers=_auth_header())
    if resp.status_code > 400:
        raise ToolError(f"REST API responded with {resp.status_code}: {resp.text[:200]}")
    results, count = _unwrap_results(payload=resp.json())
    return {"count":count, "leads":results}

@mcp.tool(name="get_leads_by_priority",description="Get the leads by priority, eg. low, medium, high")
async def get_leads_by_priority(priority:str):
    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT, follow_redirects=True) as client:
        resp = await client.get(f"{REST_BASE_URL}/api/v1/leads?priority={priority}",headers=_auth_header())
    over_400_status(resp)
    results, count = _unwrap_results(payload=resp.json())
    return {"count":count, "leads":results}
    


@mcp.tool(name="list_all_clients",description="Get all the clients coresponding to a team")
async def list_all_clients():
    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT, follow_redirects=True) as client:
        resp = await client.get(f"{REST_BASE_URL}/api/v1/clients/",headers=_auth_header())
    if resp.status_code > 400:
        raise ToolError(f"{TOOL_ERROR_MESSAGE} {resp.status_code}: {resp.text[:200]}")
    results, count = _unwrap_results(payload=resp.json())
    return {"count":count, "clients":results}

@mcp.tool(description="List all task from the current team.")
async def list_all_tasks():
    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT,follow_redirects=True) as client:
        resp = await client.get(f"{REST_BASE_URL}/api/v1/tasks",headers=_auth_header())
    over_400_status(resp)
    results, count = _unwrap_results(payload=resp.json())
    return {"count":count,"tasks":results}

@mcp.tool(description="Get leads, clients, team, tasks statistics")
async def get_stats():
    client = get_client()
    resp = await client.get(f"{REST_BASE_URL}/api/v1/dashboard-statistics",headers=_auth_header())
    over_400_status(resp)
    results, count = _unwrap_results(payload=resp.json())
    return {"count":count,"tasks":results}

@mcp.tool(description="Get task by status eg. open, closed, inprogress")
async def get_task_by_status(status:str):
    client = get_client()
    resp = await client.get(f"{REST_BASE_URL}/api/v1/tasks?status={status}",headers=_auth_header())
    over_400_status(resp)
    results, count = _unwrap_results(payload=resp.json())
    return {"count":count,"tasks":results}

@mcp.tool(description="Get all products or services")
async def get_all_products_or_services():
    client = get_client()
    resp = await client.get(f"{REST_BASE_URL}/api/v1/products",headers=_auth_header())
    over_400_status(resp)
    results, count = _unwrap_results(payload=resp.json())
    return {"count":count, "products":results}












    




if __name__ == "__main__":
    mcp.run(transport="http", host=MCP_HOST, port=MCP_PORT, stateless_http=True)








