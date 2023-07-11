import streamlit as st
import copy
from utils import usecase
from stream import raum
import pickle 

fileObj = open('raum.obj', 'rb')
raum_fine = pickle.load(fileObj)
fileObj.close()

st.set_page_config(page_title= 'Feinauslegung', layout='wide')
with st.container():
    st.title('Tool für die Feinauslegung einer Wandfläche Raums')
    st.text('Führen Sie zunächst die generelle Berechnung für den Raum durch')
    st.divider()

col1, col2, col3 = st.columns(3)
with col1:
    wall = st.selectbox('Wähle die zu bearbeitende Hauptfläche aus', options=st.session_state['main_walls'])

with col2:
    sub_surface_count = len(raum_fine.sub_surface[wall])
    sub_wall_list = [f'Subflaeche {i+1}' for i in range(sub_surface_count)]
    sub_wallmaterial = st.selectbox('Wähle die Subwandfläche aus', options=sub_wall_list)