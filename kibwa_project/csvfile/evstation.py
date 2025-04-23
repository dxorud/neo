from pymongo import MongoClient
import pandas as pd

# 데이터 불러오기
df = pd.read_csv("evstation.csv", encoding="utf-8-sig")

# MongoDB 연결
client = MongoClient("mongodb://192.168.1.44:27017/")
db = client["ev_data"]
collection = db["ev_charging"]

# 기존 데이터 초기화
collection.delete_many({})

# 데이터 저장
collection.insert_many(df.to_dict(orient="records"))

print("✅ CSV 데이터가 MongoDB에 성공적으로 저장되었습니다.")
