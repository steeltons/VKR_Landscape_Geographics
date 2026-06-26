import logging

import httpx
from fastapi import Request, Response


logger = logging.getLogger(__name__)


class ProxyClient:
    def __init__(self, timeout_seconds: int) -> None:
        self.timeout = httpx.Timeout(timeout_seconds)

    async def forward(
        self,
        *,
        request: Request,
        target_base_url: str,
        path: str,
    ) -> Response:
        target_url = f"{target_base_url.rstrip('/')}/{path.lstrip('/')}"

        body = await request.body()

        headers = dict(request.headers)
        headers.pop("host", None)

        logger.info(
            "PROXY %s %s -> %s",
            request.method,
            request.url.path,
            target_url,
        )

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            upstream_response = await client.request(
                method=request.method,
                url=target_url,
                params=request.query_params,
                content=body,
                headers=headers,
            )

        excluded_headers = {
            "content-encoding",
            "transfer-encoding",
            "connection",
        }

        response_headers = {
            key: value
            for key, value in upstream_response.headers.items()
            if key.lower() not in excluded_headers
        }

        return Response(
            content=upstream_response.content,
            status_code=upstream_response.status_code,
            headers=response_headers,
            media_type=upstream_response.headers.get("content-type"),
        )