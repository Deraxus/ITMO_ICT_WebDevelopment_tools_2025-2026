from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
import requests

from parser_service.parser import parse_and_save


app = FastAPI(
    title="Travel Buddy Parser Service",
    description="Separate FastAPI service for parsing pages and saving titles to PostgreSQL",
    version="1.0.0"
)


class ParseRequest(BaseModel):
    url: HttpUrl


@app.get("/")
def root():
    return {"message": "Parser service is running"}


@app.post("/parse")
def parse(data: ParseRequest):
    try:
        return parse_and_save(str(data.url))
    except requests.RequestException as exc:
        raise HTTPException(status_code=500, detail=f"Request error: {exc}")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Parser error: {exc}")
