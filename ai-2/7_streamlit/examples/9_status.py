import streamlit as st
import time

progress_bar = st.progress(0)

for percent in range(0, 101, 10):
    time.sleep(0.2)
    progress_bar.progress(percent)

with st.spinner('Wait for it...'):
    time.sleep(5)
st.success('Done!')

st.balloons()

sh.show()

st.success('Success!')

st.error('Error!')

st.warning('Warning!')

st.info('Info!')

st.exception(Exception('Exception!'))