from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from datetime import datetime, timedelta
import json
import lmstudio
import uvicorn

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# LLM 초기화 (Docker 환경이면 host.docker.internal 명시 가능)
llm = lmstudio.llm("gemma-3-4b-it")  

# 저장 폴더 설정
DATA_DIR = Path(__file__).resolve().parents[1] / "real_dummy"
DATA_DIR.mkdir(exist_ok=True)

@app.post("/generate_data")
def generate_merged_data():
    # 사용자 페르소나
    user = {
        "이름": "김하나",
        "성별": "여",
        "나이": 27,
        "직업": "마케팅AE",
        "월소득": 3600000,
        "소득형태": "월급",
        "경험": {
            "결혼여부": "미혼",
            "자녀유무": False,
            "반려동물유무": True
        },
        "주거형태": "월세",
        "고정지출": {
            "주거비": 600000,
            "교통비": 80000,
            "통신비": 70000,
            "구독료": 15000
        },
        "쇼핑스타일": "충동형",
        "결제수단": "간편결제",
        "절약목표": False,
        "감정트리거": ["스트레스", "자기보상", "지루함"]
    }

    # 날짜 설정
    start_date = datetime.strptime("2025-06-11", "%Y-%m-%d")
    end_date = datetime.strptime("2025-06-18", "%Y-%m-%d")
    delta = (end_date - start_date).days + 1

    소비일기 = {
        "시작일": start_date.strftime("%Y-%m-%d"),
        "종료일": end_date.strftime("%Y-%m-%d"),
        "소비기록": []
    }

    for i in range(delta):
        day = start_date + timedelta(days=i)
        day_str = day.strftime("%Y-%m-%d")

        prompt = f"""
다음은 감정소비 기반의 하루 소비 일기 JSON입니다. 사용자 정보에 기반하여 아래 형식을 그대로 따르세요.

[사용자 정보]
- 이름: {user['이름']}
- 성별: {user['성별']}
- 나이: {user['나이']}
- 직업: {user['직업']}
- 월소득: {user['월소득']}원
- 소득형태: {user['소득형태']}
- 결혼여부: {user['경험']['결혼여부']}
- 자녀 유무: {'있음' if user['경험']['자녀유무'] else '없음'}
- 반려동물 유무: {'있음' if user['경험']['반려동물유무'] else '없음'}
- 주거형태: {user['주거형태']}
- 고정지출:
    - 주거비: {user['고정지출']['주거비']}원
    - 교통비: {user['고정지출']['교통비']}원
    - 통신비: {user['고정지출']['통신비']}원
    - 구독료: {user['고정지출']['구독료']}원
- 쇼핑스타일: {user['쇼핑스타일']}
- 결제수단: {user['결제수단']}
- 절약목표: {'있음' if user['절약목표'] else '없음'}
- 감정 트리거: {', '.join(user['감정트리거'])}
- 날짜: {day_str}

📌 지켜야 할 조건:
- 너는 소비 내역 생성 전문가야. 항상 현실적이고 한국인의 소비 습관을 고려해서 1문장으로 작성해.
- 소비목록은 최소 2개 이상, 감정개입은 다양한 감정 중에서 랜덤하게 작성
- 각 소비 내역은 실제로 존재할 법한 문장으로 작성

[JSON 형식]
{{
    "날짜": "{day_str}",
    "소비목록": [
        {{
            "시간": "HH:MM",
            "분류": "지출",
            "항목": "카페",
            "금액": 4800,
            "금액표시": "4,800원",
            "상세내역": "감정적 배경이 담긴 소비 설명",
            "감정개입": "지루함"
        }}
    ]
}}
※ 설명 없이 JSON만 출력
        """

        # LM Studio 응답
        chat = lmstudio.Chat(prompt)
        response = llm.respond(chat)
        result = response.content.strip()

        try:
            day_data = json.loads(result)
        except json.JSONDecodeError:
            day_data = {
                "날짜": day_str,
                "소비목록": [],
                "raw_output": result
            }

        소비일기["소비기록"].append(day_data)

    # 파일 저장
    file_name = f"{user['성별']}_{user['나이']}_{user['직업']}_{start_date.strftime('%Y-%m-%d')}_to_{end_date.strftime('%Y-%m-%d')}.json"
    file_path = DATA_DIR / file_name
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(소비일기, f, ensure_ascii=False, indent=2)

    return {
        "message": f"✅ {delta}일치 소비일기 파일 생성 완료",
        "file": file_name
    }

if __name__ == "__main__":
    uvicorn.run("generate_data:app", host="0.0.0.0", port=8080, reload=True)
