# backend/persona.py (최종 통합버전)

from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path
import random, json
from datetime import datetime, timedelta
from uuid import uuid4
import lmstudio as lms
import concurrent.futures
import uvicorn

app = FastAPI()

# 📌 폴더 경로 (backend 폴더 기준으로 안전하게)
BASE_DIR = Path(__file__).parent.parent
OUTPUT_FOLDER = BASE_DIR / "dummy_data"
OUTPUT_FOLDER.mkdir(exist_ok=True)

# 모델 초기화
model = lms.llm("ws://host.docker.internal:1234/llm")
TASKS = {}
executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)

# 입력 데이터 스키마
class InputData(BaseModel):
    name: str
    age: int
    gender: str
    married: str
    has_child: bool
    has_pet: bool
    job: str
    income_type: str
    monthly_income: int
    housing: str
    fixed_expenses: dict
    spending_style: str
    shopping_style: str
    payment_method: str
    saving_goal: bool
    emotion_sensitive: int
    emotion_triggers: list
    period_start: str
    period_end: str

# 직업별 소비 카테고리
category_by_job = {
    '학생': ['카페', '편의점', '게임', '온라인쇼핑', '배달음식'],
    '직장인': ['카페', '점심식사', '업무비품', '패션', '스트레스 쇼핑'],
    '주부': ['마트장보기', '식료품', '반찬가게', '육아용품', '디저트'],
    '프리랜서': ['카페', '업무비품', '온라인교육', '홈오피스', '온라인구매'],
    '자영업자': ['사업자재', '식사', '업무비품', '거래처선물', '출장비']
}

# 카테고리별 금액범위
price_table = {
    '카페': (4000, 7000), '편의점': (3000, 15000), '게임': (10000, 50000),
    '마트장보기': (30000, 150000), '식료품': (10000, 50000),
    '반찬가게': (10000, 30000), '육아용품': (20000, 100000),
    '패션': (50000, 300000), '스트레스 쇼핑': (30000, 500000),
    '업무비품': (10000, 200000), '온라인쇼핑': (20000, 400000),
    '배달음식': (10000, 30000), '사업자재': (50000, 1000000), '출장비': (50000, 300000)
}

# 금액 생성 (100원 단위로 깔끔)
def generate_realistic_price(price_range):
    base_price = random.randint(*price_range)
    noise = random.randint(-1000, 1000)
    final_price = max(1000, base_price + noise)
    last_digit = random.choice([0, 100, 500])
    final_price = int(final_price / 1000) * 1000 + last_digit
    return final_price

# 상세 내역 (모델 호출)
def generate_spending_detail(category, price, current_date):
    system_prompt = """
    너는 소비 내역 생성 전문가야. 항상 현실적이고 한국인의 소비 습관을 고려해서 1문장으로 작성해.
    계절, 명절, 휴가, 기념일, 연휴, 월급일 등도 자연스럽게 반영하고, 해당 월의 특징적인 소비도 고려해줘.
    너무 길게 쓰지 말고 간결하게 작성하고, 항상 한국어로 작성해.
    """
    user_prompt = f"카테고리: {category}, 소비 금액: {price}원, 날짜: {current_date.strftime('%Y-%m-%d')}. 현실적인 상세 소비내역 한 문장 작성해줘."
    chat = lms.Chat(system_prompt)
    chat.add_user_message(user_prompt)
    prediction = model.respond(chat)
    return prediction.content.strip()

# 더미데이터 생성
def generate_dummy_data(input_data: InputData, task_id: str):
    try:
        result = []
        start = datetime.strptime(input_data.period_start, "%Y-%m-%d")
        end = datetime.strptime(input_data.period_end, "%Y-%m-%d")
        delta = (end - start).days + 1

        for i in range(delta):
            current_date = start + timedelta(days=i)
            daily_logs = []

            if current_date.day == 25:
                daily_logs.append({
                    "시간": "09:00", "분류": "수입", "항목": "월급",
                    "금액": input_data.monthly_income,
                    "금액표시": f"{input_data.monthly_income:,}원"
                })

            if random.random() < 0.4:
                result.append({"날짜": current_date.strftime("%Y-%m-%d"), "소비목록": daily_logs})
                continue

            futures = []
            num_spending = random.choices([1, 2, 3, 4], weights=[30, 40, 20, 10])[0]

            for _ in range(num_spending):
                category_list = category_by_job.get(input_data.job, ['기타'])
                category = random.choice(category_list)
                price = generate_realistic_price(price_table.get(category, (10000, 50000)))
                emotion_flag = random.choice(input_data.emotion_triggers) if random.randint(0, 100) < input_data.emotion_sensitive else ""
                future = executor.submit(generate_spending_detail, category, price, current_date)
                futures.append((future, category, price, emotion_flag))

            for future, category, price, emotion_flag in futures:
                detail = future.result()
                daily_logs.append({
                    "시간": f"{random.randint(8, 22)}:{random.choice(['00','30'])}",
                    "분류": "지출", "항목": category, "금액": price,
                    "금액표시": f"{price:,}원", "상세내역": detail, "감정개입": emotion_flag
                })

            result.append({"날짜": current_date.strftime("%Y-%m-%d"), "소비목록": daily_logs})

        filename = f"{input_data.gender}_{input_data.age}_{input_data.job}_{task_id}.json"
        filepath = OUTPUT_FOLDER / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        TASKS[task_id] = {"status": "complete", "filename": filename}

    except Exception as e:
        TASKS[task_id] = {"status": "failed", "error": str(e)}

# API 엔드포인트

@app.post("/generate")
def start_generation(data: InputData, background_tasks: BackgroundTasks):
    task_id = str(uuid4())
    TASKS[task_id] = {"status": "processing"}
    background_tasks.add_task(generate_dummy_data, data, task_id)
    return {"task_id": task_id}

@app.get("/status/{task_id}")
def check_status(task_id: str):
    return TASKS.get(task_id, {"status": "not_found"})

@app.get("/download/{filename}")
def download(filename: str):
    filepath = OUTPUT_FOLDER / filename
    return FileResponse(filepath, media_type='application/json', filename=filename)

# 개발 시 편리하게 실행
if __name__ == "__main__":
    uvicorn.run("persona:app", host="0.0.0.0", port=3030, reload=True)
