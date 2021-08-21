FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code

RUN pip install -r requirements.txt

COPY . /app
