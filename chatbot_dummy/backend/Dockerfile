FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .
COPY dummy_data/ ./dummy_data/

CMD ["uvicorn", "persona:app", "--host", "0.0.0.0", "--port", "3030"]
