import streamlit as st

st.title('스트림릿에서의 체크 박스 사용 예')

checked1 = st.checkbox('checknox 1')
st.write('checkbox 1 Status: ', checked1)

if checked1:
    st.write('checkbox 1 was clicked')
else:
    st.write('checkbox 1 was not clicked')

checked2 = st.checkbox('checkbox 2')
st.write('checkbox 2 Status: ', checked2)

if checked2:
    st.write('checkbox 2 was clicked')
else:
    st.write('checkbox 2 was not clicked')