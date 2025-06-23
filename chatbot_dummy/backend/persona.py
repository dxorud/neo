from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path
import random, json, os, httpx
from datetime import datetime, timedelta
from uuid import uuid4
import concurrent.futures
import uvicorn
import threading
from dotenv import load_dotenv
from file_watcher import start_watching

# ✅ .env 로드
load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")

app = FastAPI()

BASE_DIR = Path(__file__).parent.parent
OUTPUT_FOLDER = BASE_DIR / "dummy_data"
OUTPUT_FOLDER.mkdir(exist_ok=True)

# ✅ LM Studio URL 환경변수
LMSTUDIO_URL = os.getenv("LMSTUDIO_URL")
print("📡 연결 시도 주소:", LMSTUDIO_URL)

TASKS = {}
executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)

# ✅ S3 감시 스레드 실행
threading.Thread(target=start_watching, daemon=True).start()

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

category_by_job = {
    '학생': ['카페', '편의점', '게임', '온라인쇼핑', '배달음식'],
    '직장인': ['카페', '점심식사', '업무비품', '패션', '스트레스 쇼핑'],
    '주부': ['마트장보기', '식료품', '반찬가게', '육아용품', '디저트'],
    '프리랜서': ['카페', '업무비품', '온라인교육', '홈오피스', '온라인구매'],
    '자영업자': ['사업자재', '식사', '업무비품', '거래처선물', '출장비']
}

price_table = {
    '카페': (4000, 7000), '편의점': (3000, 15000), '게임': (10000, 50000),
    '마트장보기': (30000, 150000), '식료품': (10000, 50000),
    '반찬가게': (10000, 30000), '육아용품': (20000, 100000),
    '패션': (50000, 300000), '스트레스 쇼핑': (30000, 500000),
    '업무비품': (10000, 200000), '온라인쇼핑': (20000, 400000),
    '배달음식': (10000, 30000), '사업자재': (50000, 1000000), '출장비': (50000, 300000)
}

def generate_realistic_price(price_range):
    base_price = random.randint(*price_range)
    noise = random.randint(-1000, 1000)
    final_price = max(1000, base_price + noise)
    last_digit = random.choice([0, 100, 500])
    return int(final_price / 1000) * 1000 + last_digit

# ✅ HTTP API 방식으로 소비내역 요청
def generate_spending_detail(category, price, current_date):
    system_prompt = """
    너는 소비 내역 생성 전문가야. 항상 현실적이고 한국인의 소비 습관을 고려해서 1문장으로 작성해.
    계절, 명절, 휴가, 기념일, 연휴, 월급일 등도 자연스럽게 반영하고, 해당 월의 특징적인 소비도 고려해줘.
    너무 길게 쓰지 말고 간결하게 작성하고, 항상 한국어로 작성해.
    """
    user_prompt = f"카테고리: {category}, 소비 금액: {price}원, 날짜: {current_date.strftime('%Y-%m-%d')}. 현실적인 상세 소비내역 한 문장 작성해줘."

    payload = {
        "model": "gemma-3-4b",  # LM Studio에서 설정한 모델 이름
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7
    }

    try:
        response = httpx.post(LMSTUDIO_URL, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"[❌ LMStudio 요청 실패]: {e}")
        return "소비 내역 생성 실패"

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

        filename = f"{input_data.name}_{start.strftime('%Y%m%d')}~{end.strftime('%Y%m%d')}.json"
        filepath = OUTPUT_FOLDER / filename

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        TASKS[task_id] = {"status": "complete", "filename": filename}

    except Exception as e:
        TASKS[task_id] = {"status": "failed", "error": str(e)}

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

if __name__ == "__main__":
    uvicorn.run("persona:app", host="0.0.0.0", port=3030, reload=True)
