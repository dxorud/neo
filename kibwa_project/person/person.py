import requests

def get_population_from_api(region_name: str):
    API_KEY = "uRxtGHwjuKfwiIL%2FcO1h9SCukQS25Vtbd%2BvJWArG4uhk0hA1Kro%2ByTLMjUxWw3xVYmbEBxxPqECLDWcVBOFXHA%3D%3D"
    base_url = "https://apis.data.go.kr/1741000/StanReginCd/getStanReginCdList"
    
    params = {
        "serviceKey": API_KEY,
        "locatadd_nm": region_name,
        "type": "json"
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if 'data' in data and len(data['data']) > 0:
            population = data['data'][0].get('tot_popltn_cnt')
            return int(population.replace(',', ''))
        else:
            return None
    except Exception as e:
        print(f"인구 수 API 호출 중 오류 발생: {e}")
        return None
