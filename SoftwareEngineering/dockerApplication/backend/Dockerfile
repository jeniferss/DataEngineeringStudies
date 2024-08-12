FROM python:3.12-alpine

WORKDIR /api 

COPY ./requirements.txt /api/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /api/requirements.txt

COPY . /api

CMD ["fastapi", "dev", "main.py"]
