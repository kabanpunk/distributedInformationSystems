FROM python:3.11

RUN pip install poetry

WORKDIR /usr/src/app

COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

COPY app/ .

ENV PYTHONUNBUFFERED=0

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
