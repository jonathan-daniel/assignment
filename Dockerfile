FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./ /app/
COPY requirements.txt /
RUN pip install  pip
RUN pip install -r /requirements.txt