from celery.result import AsyncResult
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, HttpUrl
import httpx

from app.celery_app import celery_app
from app.core.config import settings
from app.tasks import parse_url_task


router = APIRouter(prefix="/parser", tags=["Parser"] )


class ParseRequest(BaseModel):
    url: HttpUrl


@router.post("/parse")
def parse_via_http(data: ParseRequest):
    """Синхронный вызов отдельного parser_service по HTTP."""
    try:
        response = httpx.post(
            f"{settings.parser_service_url}/parse",
            json={"url": str(data.url)},
            timeout=20.0
        )
        response.raise_for_status()
        return response.json()
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Parser service error: {exc}"
        )


@router.post("/parse-async", status_code=status.HTTP_202_ACCEPTED)
def parse_via_queue(data: ParseRequest):
    """Асинхронный вызов парсера через очередь Celery + Redis."""
    task = parse_url_task.delay(str(data.url))
    return {
        "message": "Parsing task has been added to queue",
        "task_id": task.id,
        "status": task.status
    }


@router.get("/tasks/{task_id}")
def get_task_status(task_id: str):
    task = AsyncResult(task_id, app=celery_app)

    result = {
        "task_id": task_id,
        "status": task.status
    }

    if task.successful():
        result["result"] = task.result
    elif task.failed():
        result["error"] = str(task.result)

    return result
