from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from typing import Optional
import json
import os
import uvicorn

app = FastAPI()

# MongoDB 연결
client = MongoClient("mongodb://192.168.1.44:27017/")
db = client["electric_car"]  # 전기차 예측 DB
charging_db = MongoClient("mongodb://192.168.1.44:27017/")["ev_data"]  # 충전소 DB
charging_collection = charging_db["ev_charging"]

# 비밀 키 로딩
def get_secret(key):
    base_path = os.path.dirname(os.path.abspath(__file__))
    secret_path = os.path.join(base_path, "..", "secret.json")
    with open(secret_path, encoding="utf-8") as f:
        secrets = json.load(f)
        return secrets.get(key)

# 🔹 1. 전기차 등록대수 조회
@app.get("/r_forecast")
def get_forecast(sido: str, sigungu: str):
    doc = db["total_ev_forecast"].find_one({"sido": sido, "sigungu": sigungu}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="예측 데이터 없음")
    return doc

# 🔹 2. 전기차 충전소 수 조회
@app.get("/r_evstation")
def get_charging_station(sido: str, sigungu: str):
    try:
        query = {
            "시도": {"$regex": sido},
            "군구": {"$regex": sigungu}
        }
        count = charging_collection.count_documents(query)
        print(f"[DEBUG] MongoDB에서 {sido} {sigungu} 충전소 수: {count}")

        return {
            "sido": sido,
            "sigungu": sigungu,
            "station_count": count
        }

    except Exception as e:
        print("[충전소 MongoDB 조회 오류]", str(e))
        raise HTTPException(status_code=500, detail="MongoDB 충전소 수 조회 실패")

# 🔹 3. 전기차 구매 시기 추천 (인구 수 제외)
@app.get("/ev_recommend")
def recommend_ev_purchase(sido: str, sigungu: str, year: Optional[int] = None):
    doc = db["total_ev_forecast"].find_one({"sido": sido, "sigungu": sigungu}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="해당 지역 예측 데이터 없음")

    # 예측 연도 선택
    all_years = sorted([int(k) for k in doc.keys() if k.isdigit()])
    if year is None:
        for y in reversed(all_years):
            try:
                y1, y2, y3 = float(doc[str(y)]), float(doc[str(y+1)]), float(doc[str(y+2)])
                year = y
                break
            except:
                continue
        if year is None:
            raise HTTPException(status_code=400, detail="3년 연속 예측 데이터 부족")

    try:
        y1 = float(doc[str(year)])
        y2 = float(doc[str(year + 1)])
        y3 = float(doc[str(year + 2)])
    except KeyError:
        raise HTTPException(status_code=400, detail="해당 연도의 예측 데이터 부족")

    # 충전소 수 조회
    try:
        station_data = get_charging_station(sido, sigungu)
        stn = station_data.get("station_count", 0)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"충전소 수 조회 실패: {str(e)}")

    # 추천 로직 (인구 수 제외)
    avg_growth = ((y2 - y1) + (y3 - y2)) / 2
    ev_per_station = y3 / stn if stn else float('inf')

    if ev_per_station < 50:
        recommend_year = year + 2
        msg = f"✅ {recommend_year}년에는 충전 인프라가 충분하여 전기차 구매에 적합합니다."
    elif avg_growth > 2500:
        recommend_year = year + 1
        msg = f"📈 전기차 보급이 빠르게 증가하고 있습니다. {recommend_year}년 구매를 추천합니다."
    else:
        recommend_year = year
        msg = f"🔋 현재도 구매해도 무난한 시기입니다. {recommend_year}년 구매를 고려해보세요."

    return {
        "result": True,
        "data": {
            "sido": sido,
            "sigungu": sigungu,
            "input_year": year,
            "forecast": {
                str(year): int(y1),
                str(year + 1): int(y2),
                str(year + 2): int(y3)
            },
            "station_count": int(stn),
            "recommendation_year": int(recommend_year),
            "recommendation": msg
        }
    }

# FastAPI 실행
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
