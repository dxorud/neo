import uvicorn
from fastapi import FastAPI, Query
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="EV Registration API",
    description="시도 + 시군구 기반 전기차 등록대수 예측 정보 제공",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = MongoClient("mongodb://192.168.1.44:27017/")
db = client["electric_car"]
collection = db["ev_forecast"]  

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.get("/region-list")
def get_all_regions():
    try:
        regions = sorted(collection.distinct("region"))
        return {"regions": regions}
    except Exception as e:
        return {"error": "지역 목록 조회 실패", "detail": str(e)}

@app.get("/ev-registration")
def get_ev_registration(
    sido: str = Query(..., description="시도명 (예: 충청북도)"),
    sigungu: str = Query(..., description="시군구명 (예: 청주시 상당구)")
):
    try:
        full_region = f"{sido} {sigungu}".strip()
        print(f"🔍 조회 대상 지역: {full_region}")

        doc = collection.find_one({"region": full_region})

        if not doc:
            return {"message": f"'{full_region}' 지역의 전기차 등록 정보를 찾을 수 없습니다."}

        if "yearly_data" not in doc:
            return {"message": f"'{full_region}' 지역에는 'yearly_data' 필드가 없습니다."}

        return {
            "region": full_region,
            "ev_registration": doc["yearly_data"]
        }

    except Exception as e:
        return {"error": "서버 내부 오류 발생", "detail": str(e)}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
