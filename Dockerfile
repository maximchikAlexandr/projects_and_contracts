FROM python:3.11

SHELL ["/bin/bash", "-c"]

ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  POETRY_VERSION=1.6.1


RUN pip install --upgrade pip
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app
COPY . .

RUN poetry config virtualenvs.create false && poetry install --no-root
RUN echo 'alias pc="python /app/main.py"' >> ~/.bashrc