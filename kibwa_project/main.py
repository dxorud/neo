from fastapi import FastAPI, Query, HTTPException
from pymongo import MongoClient
import requests
import json
import urllib.parse
from utils import get_secret

app = FastAPI()

# MongoDB 연결
client = MongoClient("mongodb://localhost:27017/")
db = client["electric_car"]

# 1. EV 등록대수 (MongoDB)
@app.get("/r_forecast")
def get_forecast(sido: str, sigungu: str):
    doc = db["total_ev_forecast"].find_one({"sido": sido, "sigungu": sigungu}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="예측 데이터 없음")
    return doc

# 2. 인구 수 (공공데이터 API)
@app.get("/r_population")
def get_population(sido: str, sigungu: str):
    service_key = get_secret("population_api_key")
    url = "https://apis.data.go.kr/1741000/StanReginCd/getStanReginCdList"
    params = {
        "serviceKey": service_key,
        "pageNo": "1",
        "numOfRows": "1000",
        "_type": "json"
    }
    res = requests.get(f"{url}?{urllib.parse.urlencode(params)}")
    if res.status_code != 200:
        raise HTTPException(status_code=500, detail="인구 API 실패")
    data = res.json()['response']['body']['items']['item']
    for item in data:
        if sido in item['sidoNm'] and sigungu in item['sigunguNm']:
            return {"population": item['totPopltnCnt']}
    raise HTTPException(status_code=404, detail="인구수 데이터 없음")

# 3. 충전소 수 (공공데이터 API)
@app.get("/r_charging_station")
def get_charging_station(sido: str, sigungu: str):
    service_key = get_secret("charging_api_key")
    url = "https://apis.data.go.kr/B552584/EvCharger/getChargerInfo"
    params = {
        "serviceKey": service_key,
        "zcode": sido,   # 시도코드 매핑 필요
        "pageNo": "1",
        "numOfRows": "1000",
        "_type": "json"
    }
    res = requests.get(f"{url}?{urllib.parse.urlencode(params)}")
    if res.status_code != 200:
        raise HTTPException(status_code=500, detail="충전소 API 실패")
    data = res.json()['response']['body']['items']['item']
    count = len([item for item in data if sigungu in item.get("addr", "")])
    return {"station_count": count}
