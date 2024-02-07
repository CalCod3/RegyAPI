FROM python:3.9

WORKDIR /

COPY ./requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

COPY ./db /db

COPY ./tests /tests


CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "80", "--reload"]