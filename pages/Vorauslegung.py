import streamlit as st
from utils import usecase

st.set_page_config(page_title= 'Grobauslegung', layout='wide')
with st.container():
    st.title('Tool für die Grobauslegung des Raums')
    st.divider()

col1, col2, col3 = st.columns(3)
with col1:
    use = st.selectbox('Usecase nach DIN 18041', options=usecase.keys())
    min_lim =  min(usecase[use])
    max_lim =  max(usecase[use])
with col2:
    vol = st.number_input('Volumen in m³', min_value=min_lim,
                        max_value=max_lim, value=min_lim)