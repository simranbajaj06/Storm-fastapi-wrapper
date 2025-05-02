from fastapi import APIRouter
from fastapi.responses import StreamingResponse, JSONResponse
from src.wrapstorm.api.models import StormRequest
from src.wrapstorm.core.storm_wrapper import run_storm_query_stream
import json 

router = APIRouter()

@router.post("/query")
async def query_storm(payload: StormRequest):
    generator = run_storm_query_stream(payload)

    if payload.stream:
        def stream_result():
            for chunk in generator:
                yield chunk  # Each chunk is a newline-terminated JSON object
        return StreamingResponse(stream_result(), media_type="application/json")

    # Non-streaming: Merge chunks into a single dict
    result = {}
    for chunk in generator:
        item = json.loads(chunk)
        result.update(item)

    return JSONResponse(content=result)
