from pymongo import MongoClient

client = MongoClient("mongodb://192.168.1.44:27017/")

db = client["electric_car"]

source_collections = [
    "chungbuk_ev_forecast",
    "gyeonggi_ev_forecast",
    "incheon_ev_actual",
    "seoul_ev_forecast",
    "jeonnam_ev_forecast"
]

target_collection = db["ev_forecast"]

total_inserted = 0

for col_name in source_collections:
    source = db[col_name]
    for doc in source.find():
        doc.pop("_id", None)  
        doc["original_collection"] = col_name  
        target_collection.insert_one(doc)
        total_inserted += 1

print(f"병합 완료: {total_inserted}건 → electric_car.ev_forecast")
