import httpx

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse, Response


app = FastAPI()

services = {
    # Add more services as needed
    "service1": "https://service.first:8001",
    "service2": "https://service.second:8002",
}


async def forward_request(
    service_url: str, method: str, path: str, body=None, headers=None
):
    async with httpx.AsyncClient() as client:
        url = f"{service_url}{path}"
        try:
            return await client.request(method, url, json=body, headers=headers)
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Error forwading request: {str(e)}.",
            )


@app.api_route(
    "/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"]
)
async def gateway(service: str, path: str, request: Request):
    if service not in services:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Service not found"
        )

    service_url = services[service]
    body = await request.json() if request.method in ["POST", "PUT", "PATCH"] else None
    headers = dict(request.headers)

    response = await forward_request(
        service_url, request.method, f"/{path}", body, headers
    )

    content_type = response.headers.get("content-type", "")
    if "application/json" in content_type:
        return JSONResponse(status_code=response.status_code, content=response.json())
    return Response(
        status_code=response.status_code,
        content=response.content,
        media_type=content_type,
    )
