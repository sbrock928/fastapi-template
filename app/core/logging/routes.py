"""
Routes for viewing API logs via a web-based interface.

This module provides administrative endpoints to view detailed logs
captured by the logging middleware. It includes an HTML-based viewer
that presents recent logs with formatted request and response details.

Endpoints:
    - GET /admin/logs: Renders recent API request and response logs.
    - GET /admin/logs/partial: Returns partial template for AJAX updates.

Dependencies:
    - Jinja2Templates for HTML templating.
    - Async SQLAlchemy session for asynchronous database access.
"""

from math import ceil

# FastAPI imports grouped together
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# SQLAlchemy imports
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

# Local imports
from app.core.database import get_async_session
from app.core.logging.models import APILog

router = APIRouter(prefix="/admin/logs", tags=["Logs"])
templates = Jinja2Templates(directory="app/templates")


@router.get("")
async def get_logs(
    request: Request,
    page: int = Query(1, ge=1),
    per_page: int = Query(10, le=100),
    session: AsyncSession = Depends(get_async_session),
) -> HTMLResponse:
    """Render the main logs page with paginated data."""
    # Get total count for pagination
    count_stmt = select(func.count()).select_from(APILog)  # pylint: disable=not-callable
    count_result = await session.execute(count_stmt)
    total_logs = count_result.scalar() or 0
    total_pages = max(1, ceil(total_logs / per_page))

    if page > total_pages and total_pages > 0:
        raise HTTPException(status_code=404, detail="Page not found")

    # Get paginated logs
    result = await session.execute(
        select(APILog)
        .order_by(APILog.created_at.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
    )
    logs = result.scalars().all()

    return templates.TemplateResponse(
        "logs.html",
        {
            "request": request,
            "logs": logs,
            "pagination": {
                "current_page": page,
                "total_pages": total_pages,
                "per_page": per_page,
                "total_logs": total_logs,
            },
        },
    )


@router.get("/partial", response_class=HTMLResponse)
async def get_logs_partial(
    request: Request,
    page: int = Query(1, ge=1),
    per_page: int = Query(10, le=100),
    session: AsyncSession = Depends(get_async_session),
) -> HTMLResponse:
    """Return partial template with paginated log data."""
    # Get total count for pagination
    count_stmt = select(func.count()).select_from(APILog)  # pylint: disable=not-callable
    count_result = await session.execute(count_stmt)
    total_logs = count_result.scalar() or 0
    total_pages = max(1, ceil(total_logs / per_page))

    if page > total_pages and total_pages > 0:
        raise HTTPException(status_code=404, detail="Page not found")

    # Get paginated logs
    result = await session.execute(
        select(APILog)
        .order_by(APILog.created_at.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
    )
    logs = result.scalars().all()

    return templates.TemplateResponse(
        "partials/_logs_table.html",
        {
            "request": request,
            "logs": logs,
            "pagination": {
                "current_page": page,
                "total_pages": total_pages,
                "per_page": per_page,
                "total_logs": total_logs,
            },
        },
    )
