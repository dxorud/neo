import streamlit as st
import requests

st.set_page_config(page_title="나의 금융데이터", page_icon="💳")
st.title("💳 나의 금융 소비 더미데이터 생성기")

if "loading" not in st.session_state:
    st.session_state.loading = False

if st.button("📥 나의 금융데이터 가져오기"):
    st.session_state.loading = True
    with st.spinner("금융데이터 가져오는 중..."):
        try:
            res = requests.post("http://localhost:8080/generate_data")
            st.session_state.loading = False

            if res.status_code == 200:
                result = res.json()
                file_name = result["file"]
                st.success(f"✅ 데이터 가져오기 성공!\n📁 저장 파일: `{file_name}`")

                st.subheader("📄 생성된 소비일기 데이터")
                st.json(result["file"])  # 여기에 파일 내용 보여주기 (예: st.json(result["data"]) 가능)

            else:
                st.error("❌ 요청 실패")
                st.text(res.text)

        except Exception as e:
            st.session_state.loading = False
            st.error("❌ 서버에 연결할 수 없습니다.")
            st.exception(e)
