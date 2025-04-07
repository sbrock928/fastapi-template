"""
Routes for viewing API logs via a web-based interface.

This module provides administrative endpoints to view detailed logs
captured by the logging middleware. It includes an HTML-based viewer
that presents recent logs with formatted request and response details.

Endpoints:
    - GET /admin/logs: Renders recent API request and response logs.

Dependencies:
    - Jinja2Templates for HTML templating.
    - Async SQLAlchemy session for asynchronous database access.

"""

from typing import Any

from fastapi import APIRouter, Depends, Query, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.core.logging.models import APILog

router = APIRouter(prefix="/admin/logs", tags=["Logs"])
templates = Jinja2Templates(directory="app/templates")


@router.get("")
async def get_logs(
    request: Request,
    limit: int = Query(50, le=100),
    session: AsyncSession = Depends(get_async_session),
) -> Any:

    result = await session.execute(select(APILog).order_by(APILog.timestamp.desc()).limit(limit))
    logs = list(result.scalars().all())

    formatted_logs = [
        {
            "timestamp": log.timestamp.isoformat(),
            "method": log.method,
            "path": log.path,
            "query_string": log.query_string,
            "request_body": log.request_body,
            "response_body": log.response_body,
            "status_code": log.status_code,
            "duration_ms": round(log.duration_ms, 2),
            "user_id": log.user_id,
            "client_host": log.client_host,
        }
        for log in logs
    ]

    return templates.TemplateResponse("logs.html", {"request": request, "logs": formatted_logs})
