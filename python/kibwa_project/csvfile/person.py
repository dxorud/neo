import requests
import json
from urllib.parse import urlencode
import time

# ✅ API 기본 설정
API_KEY = "uRxtGHwjuKfwiIL%2FcO1h9SCukQS25Vtbd%2BvJWArG4uhk0hA1Kro%2ByTLMjUxWw3xVYmbEBxxPqECLDWcVBOFXHA%3D%3D"
BASE_URL = "https://apis.data.go.kr/1741000/StanReginCd/getStanReginCdList"
yyyymm = "202403"

# ✅ 반복 호출 관련 설정
page = 1
num_of_rows = 1000
all_data = []

while True:
    params = {
        "serviceKey": API_KEY,
        "yyyymm": yyyymm,
        "resultType": "json",
        "pageNo": page,
        "numOfRows": num_of_rows
    }

    url = f"{BASE_URL}?{urlencode(params)}"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"❌ 요청 실패 (페이지 {page})")
        break

    try:
        data = response.json()
        rows = data["StanReginCd"]["row"]
        total_count = int(data["StanReginCd"]["totalCount"])

        # ✅ adm_cd 필드 제거
        for row in rows:
            row.pop("adm_cd", None)  # adm_cd가 있으면 제거
            all_data.append(row)

        print(f"✅ 페이지 {page} 수집 완료 ({len(rows)}건 누적: {len(all_data)}건)")

        if page * num_of_rows >= total_count:
            break

        page += 1
        time.sleep(0.2)

    except Exception as e:
        print(f"❌ JSON 파싱 실패: {e}")
        break

# ✅ JSON 파일로 저장
filename = f"population_data_no_admcd_{yyyymm}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump({"population": all_data}, f, ensure_ascii=False, indent=4)

print(f"\n🎉 adm_cd 없는 인구 데이터 저장 완료: {filename}")
