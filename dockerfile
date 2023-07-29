FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONNUNBUFFERED 1

WORKDIR /service/

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src src

EXPOSE 8080
