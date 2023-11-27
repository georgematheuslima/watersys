FROM python:3.11.2-slim-bullseye

RUN apt-get update && apt-get install -y postgresql-client curl

WORKDIR /app

RUN mkdir -p logs && touch logs/user.logs

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
