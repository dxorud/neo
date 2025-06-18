import streamlit as st
import requests

st.set_page_config(page_title="감정소비 일기 생성기", page_icon="🧾")
st.title("🧾 감정소비 기반 금융 더미데이터 생성")

# 버튼 클릭 상태를 저장
if "loading" not in st.session_state:
    st.session_state.loading = False

# FastAPI 엔드포인트 설정
FASTAPI_URL = "http://localhost:8080/generate_data"  # 또는 Docker용이면 호스트에 맞게 변경

if st.button("📥 나의 소비일기 생성하기"):
    st.session_state.loading = True
    with st.spinner("소비일기 생성 중..."):
        try:
            res = requests.post(FASTAPI_URL)
            st.session_state.loading = False

            if res.status_code == 200:
                result = res.json()
                st.success(result["message"])
                st.write(f"📂 저장된 파일명: `{result['file']}`")

                # 저장된 파일 내용 일부 미리보기 (옵션)
                download_path = f"http://localhost:8080/download/{result['file']}"
                preview_res = requests.get(download_path)
                if preview_res.status_code == 200:
                    st.subheader("📋 소비일기 미리보기")
                    st.json(preview_res.json())

            else:
                st.error("❌ 요청 실패")
                st.text(res.text)

        except Exception as e:
            st.session_state.loading = False
            st.error("❌ 서버에 연결할 수 없습니다.")
            st.exception(e)
