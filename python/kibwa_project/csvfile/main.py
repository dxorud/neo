from fastapi import FastAPI, Query, HTTPException
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="EV Forecast API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = MongoClient("mongodb://192.168.1.44:27017/")
db = client["electric_car"]
collection = db["total_ev_forecast"]

@app.get("/")
def root():
    return {"message": "전기차 예측 API입니다. /forecast?sido=서울특별시&sigungu=강남구"}

@app.get("/forecast")
def get_forecast(
    sido: str = Query(..., description="시도명 예: 서울특별시"),
    sigungu: str = Query(..., description="시군구명 예: 강남구")
):
    region = f"{sido.strip()} {sigungu.strip()}"
    doc = collection.find_one({"region": region}, {"_id": 0})

    if not doc:
        raise HTTPException(status_code=404, detail=f"{region} 데이터가 없습니다.")

    return {
        "region": doc["region"],
        "forecast": {k: v for k, v in doc.items() if k != "region"}
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)
