from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from datetime import date

app = FastAPI()

CSV_FILE_PATH = "202001_202504_전기차등록현황.csv"  

class QueryParams(BaseModel):
    location: str
    date: date

@app.get('/get_data_by_location_and_date')
async def get_data_by_location_and_date(params: QueryParams):
    try:
        df = pd.read_csv(CSV_FILE_PATH)
    except Exception:
        
        return {"message": "데이터를 불러오는 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요."}

    df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce').dt.date

    filtered_data = df[(df['LOCATION'] == params.location) & (df['DATE'] == params.date)]

    if filtered_data.empty:
        return {"message": "해당 지역과 날짜에 대한 데이터가 없습니다."}

    if 'REGISTERED_CARS' in filtered_data.columns:
        total_registered_cars = filtered_data['REGISTERED_CARS'].sum()
    else:
        return {"message": "차량 등록대수 정보를 찾을 수 없습니다."}

    return {
        "location": params.location,
        "date": params.date,
        "total_registered_cars": total_registered_cars
    }
