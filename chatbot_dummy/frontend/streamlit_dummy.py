import streamlit as st
import requests
from datetime import datetime
import time

# ✅ 도커 환경에서는 컨테이너 이름으로 백엔드 접근
API_BASE_URL = "http://backend:3030"

st.title("🎯 감정소비 페르소나 기반 더미데이터 생성기")

# ① 기본 인적 사항
st.header("① 기본 정보")
name = st.text_input("이름을 입력하세요")
age = st.number_input("나이", min_value=10, max_value=100, value=20)
gender = st.radio("성별", ["남", "여"])
married = st.radio("결혼 여부", ["미혼", "기혼"])
has_child = st.checkbox("자녀가 있다")
has_pet = st.checkbox("반려동물을 키운다")

# ② 직업 및 소득
st.header("② 직업 및 소득 정보")
job = st.radio("직업", ["학생", "직장인", "주부", "프리랜서", "자영업자"])
income_type = st.radio("소득 형태", ["월급", "용돈", "생활비 지원", "사업소득"])
monthly_income = st.number_input("월소득 (만원)", 10, 2000, 300) * 10000
housing = st.radio("주거 형태", ["자가", "전세", "월세"])

# ③ 고정 지출
st.header("③ 고정 지출")
fixed_expenses = {
    "주거비": st.number_input("주거비 (만원)", 0, 500, 50) * 10000,
    "교통비": st.number_input("교통비 (만원)", 0, 100, 10) * 10000,
    "통신비": st.number_input("통신비 (만원)", 0, 100, 10) * 10000,
    "구독료": st.number_input("구독료 (만원)", 0, 50, 5) * 10000
}

# ④ 소비 성향
st.header("④ 소비 성향")
spending_style = st.radio("소비 성향", ["절약형", "일반형", "플렉스형"])
shopping_style = st.radio("쇼핑 스타일", ["계획형", "충동형", "혼합형"])
payment_method = st.radio("결제 수단", ["카드", "현금", "간편결제"])
saving_goal = st.checkbox("절약 목표")

# ⑤ 감정소비 성향
st.header("⑤ 감정소비 성향")
emotion_sensitive = st.slider("감정소비 민감도", 0, 100, 30)
emotion_triggers = st.multiselect(
    "감정 트리거", ["스트레스", "외로움", "불안", "지루함", "자기보상", "분노", "기쁨"]
)

# ⑥ 소비 기간
st.header("⑥ 소비 기간")
period = st.date_input(
    "소비 생성 기간", (datetime(2024, 1, 1), datetime(2024, 1, 31))
)

# 🚀 생성 버튼
if st.button("🚀 더미데이터 생성하기"):
    with st.spinner("⏳ 생성 요청 전송 중..."):
        payload = {
            "name": name,
            "age": age,
            "gender": gender,
            "married": married,
            "has_child": has_child,
            "has_pet": has_pet,
            "job": job,
            "income_type": income_type,
            "monthly_income": monthly_income,
            "housing": housing,
            "fixed_expenses": fixed_expenses,
            "spending_style": spending_style,
            "shopping_style": shopping_style,
            "payment_method": payment_method,
            "saving_goal": saving_goal,
            "emotion_sensitive": emotion_sensitive,
            "emotion_triggers": emotion_triggers,
            "period_start": period[0].strftime("%Y-%m-%d"),
            "period_end": period[1].strftime("%Y-%m-%d"),
        }

        try:
            response = requests.post(f"{API_BASE_URL}/generate", json=payload, timeout=60)
            response.raise_for_status()
            task_id = response.json().get("task_id")

            max_attempts = 720  # 최대 60분까지 기다림
            interval_seconds = 5

            for attempt in range(max_attempts):
                time.sleep(interval_seconds)
                status_response = requests.get(f"{API_BASE_URL}/status/{task_id}", timeout=20)
                status = status_response.json()

                if status["status"] == "complete":
                    filename = status["filename"]
                    st.success("✅ 데이터 생성 완료!")
                    download_url = f"{API_BASE_URL}/download/{filename}"
                    st.markdown(f"[📥 JSON 파일 다운로드]({download_url})")
                    break

                elif status["status"] == "failed":
                    st.error("❌ 데이터 생성 실패!")
                    st.write(status.get("error", "알 수 없는 에러"))
                    break

                else:
                    if (attempt + 1) % 12 == 0:
                        minutes = (attempt + 1) * interval_seconds // 60
                        st.info(f"🔄 데이터 생성 중... ({minutes}분 경과)")

            else:
                st.error("⚠ 데이터 생성이 제한시간 내 완료되지 않았습니다.")

        except requests.exceptions.RequestException as e:
            st.error(f"❌ 서버 통신 에러: {e}")
        except Exception as e:
            st.error(f"❌ 알 수 없는 에러: {e}")
