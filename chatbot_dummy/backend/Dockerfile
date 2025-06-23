# Python 3.11 경량 이미지
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 먼저 복사 및 설치
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 전체 backend 코드 복사
COPY backend/ ./

# 외부 dummy_data 폴더 복사 (backend 밖에 위치)
COPY dummy_data/ ./dummy_data/

# 포트 오픈 (선택)
EXPOSE 3030

# FastAPI 서버 실행
CMD ["uvicorn", "persona:app", "--host", "0.0.0.0", "--port", "3030"]
