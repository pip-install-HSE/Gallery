import datetime
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
def get_math_prediction(date_time: datetime.datetime, player_id: str,  api_key: APIKey = Depends(get_api_key)):
    return {"views": 300}


@app.post("/uploadfile/")
async def create_upload_file(in_file: UploadFile = File(...)):
    async with aiofiles.open(in_file.filename, 'wb') as out_file:
        content = await in_file.read()  # async read
        await out_file.write(content)  # async write
    return {"filename": in_file.filename}
