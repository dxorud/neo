FROM python:3.11-slim

WORKDIR /app

COPY frontend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY frontend/ .

# 로그 실시간 출력
ENV PYTHONUNBUFFERED=1

# Streamlit 실행
CMD ["streamlit", "run", "streamlit_dummy.py", "--server.port=8501", "--server.address=0.0.0.0"]
