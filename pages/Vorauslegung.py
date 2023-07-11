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
    sub_wall = st.selectbox('Wähle die Subwandfläche aus', options=sub_wall_list)
    sub_wall_ind =  sub_wall_list.index(sub_wall)

with col3:
    max_area =  float(raum_fine.surface[wall] - sum(raum_fine.sub_surface[wall]))
    raum_fine.sub_surface[wall][sub_wall_ind] = st.slider(label= 'Fläche der Subwandfläche',min_value=.0,max_value=max_area, key='SubAreaSlider', step=0.1) 

tab1, tab2 = st.tabs(['Nachhallzeit', 'Vergleich der Nachhallzeit'])

with tab1:
    fig1 = raum_fine.plot_reverberationTime()
    st.plotly_chart(fig1)

with tab2:
    fig2 = raum_fine.plot_reverberationTime_ratio()
    st.plotly_chart(fig2)
