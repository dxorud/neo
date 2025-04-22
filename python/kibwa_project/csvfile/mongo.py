from pymongo import MongoClient

client = MongoClient('mongodb://192.168.1.44:27017/')
db = client['electric_car']

collection_names = [
    'seoul_ev_forecast',
    'gyeonggi_ev_forecast',
    'incheon_ev_forecast',
    'chungbuk_ev_forecast',
    'jeonnam_ev_forecast',
    'gyeongnam_ev_forecast'
]

merged_collection = db['total_ev_forecast']
total_inserted = 0

for name in collection_names:
    source_col = db[name]
    docs = list(source_col.find({}, {'_id': 0})) 

    inserted_count = 0
    for doc in docs:
        sido = doc.get('sido', '').strip()
        sigungu = doc.get('sigungu', '').strip()

        if not sido or not sigungu:
            continue  

        filter_key = {'sido': sido, 'sigungu': sigungu}

        result = merged_collection.update_one(
            filter_key,
            {'$set': doc},
            upsert=True
        )

        if result.upserted_id or result.modified_count:
            inserted_count += 1

    total_inserted += inserted_count
    print(f"{name} → 통합 완료: {inserted_count}건")

print(f"\n총 통합된 문서 수: {total_inserted}건")
