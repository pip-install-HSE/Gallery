import datetime
import math
from random import randint
from typing import List, Optional

import aiofiles
from fastapi import Security, HTTPException, FastAPI, Depends, UploadFile, File
from fastapi.openapi.models import APIKey
from fastapi.security import APIKeyQuery, APIKeyHeader, APIKeyCookie
from starlette.status import HTTP_403_FORBIDDEN

app = FastAPI()

ALLOWED_API_KEYS = ["lfsdgffsdhgsd"]
API_KEY_NAME = "token"

api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
api_key_cookie = APIKeyCookie(name=API_KEY_NAME, auto_error=False)


async def get_api_key(
        api_key_query: str = Security(api_key_query),
        api_key_header: str = Security(api_key_header),
        api_key_cookie: str = Security(api_key_cookie),
):
    if api_key_query in ALLOWED_API_KEYS:
        return api_key_query
    elif api_key_header in ALLOWED_API_KEYS:
        return api_key_header
    elif api_key_cookie in ALLOWED_API_KEYS:
        return api_key_cookie
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )


@app.get("/get_math_prediction/")
def get_math_prediction(date_time: datetime.datetime, player_id: str, api_key: APIKey = Depends(get_api_key)):
    return {"views": 300}


@app.post("/get_best_times/")
def get_best_times(count_needed_views: int, duration: float, player_ids: List[int],
                   api_key: APIKey = Depends(get_api_key)):
    d = {}
    for i in player_ids:
        d[i] = [{
            "unix_in": 3424234242,
            "unix_out": 3424234242 + duration * 1000,
            "predicted_count_views": math.ceil(count_needed_views / len(player_ids))
        } for j in range(randint(10, 20))]
    return d


@app.post("/uploadfile/")
async def create_upload_file(in_file: UploadFile = File(...)):
    async with aiofiles.open(in_file.filename, 'wb') as out_file:
        content = await in_file.read()  # async read
        await out_file.write(content)  # async write
    return {"filename": in_file.filename}
