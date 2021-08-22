import datetime
import math
from random import randint
from typing import List, Optional

import aiofiles
from fastapi import Security, HTTPException, FastAPI, Depends, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.openapi.models import APIKey
from fastapi.security import APIKeyQuery, APIKeyHeader, APIKeyCookie
from starlette.status import HTTP_403_FORBIDDEN
from fastapi.responses import HTMLResponse

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
    weekday = date_time.weekday()
    half_hour = 2*date_time.hour + (1 if date_time.minute >= 30 else 0) + 1
    with open("holidays_new_mean_sum_dist_month.csv", "r") as f:
        for row in f.readlines():
            row = row.split(",")
            if row[1] == str(weekday) and row[2] == str(half_hour):
                return {"views": row[7]}
    return {"views": -1}


@app.post("/get_best_times/")
def get_best_times(count_needed_views: int, duration: float, player_ids: List[int],
                   api_key: APIKey = Depends(get_api_key)):
    d = {}
    for i in player_ids:
        c = randint(10, 20)
        d[i] = [{
            "unix_in": 3424234242,
            "unix_out": 3424234242 + duration * 1000,
            "predicted_count_views": math.ceil((count_needed_views / len(player_ids)) / c)
        } for j in range(c)]
    return d


# @app.get("/get_day_statistic/")
# def get_day_statistic(date: datetime.date, player_id: int,
#                       api_key: APIKey = Depends(get_api_key), response_class=HTMLResponse):
#     return {"statistic_img": "http://185.232.169.130:8080/stat"}
#
#
# @app.get("/stat", response_class=FileResponse)
# async def main():
#     return FileResponse("stat.jpg")


@app.post("/uploadfile/")
async def create_upload_file(in_file: UploadFile = File(...)):
    async with aiofiles.open(in_file.filename, 'wb') as out_file:
        content = await in_file.read()  # async read
        await out_file.write(content)  # async write
    return {"filename": in_file.filename}
