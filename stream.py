import numpy as np 

import streamlit as st
#import streamlit_tags as sttags
from room_calc import room
from utils import basic_dict , read_db, basic_dict_2, add_row, usecase


st.set_page_config(page_title= 'Tool für Raumakustik', layout='wide',
                    initial_sidebar_state='collapsed')

# """Eingabe der Parameter"""


with st.container():
    st.title('WebApp for Roomacoustics')
    st.divider()
    st.header('Benötigt werden das Raumvolumen, die Anzahl'
        ' der Wände, deren Fläche, sowie das Material der Wandoberfläche')

col1, col2, col3 = st.columns(3)
with col1:
    use = st.selectbox('Usecase nach DIN 18041', options=usecase.keys())
    min_lim =  min(usecase[use])
    max_lim =  max(usecase[use])
with col2:
    vol = st.number_input('Volumen in m³', min_value=min_lim,
                        max_value=max_lim, value=min_lim)
with col3:
    areas = st.number_input('Anzahl der Wandflächen die Sie eingeben möchten'
                            ,min_value=1, step=1)
area =  np.linspace(0,int(areas),int(areas)+1)
with st.container():
    col_1, col_2 = st.columns(2)
    with col_1:
        with st.form(key = 'surface'):
            surfaces = [st.number_input(
                f"Fläche für Wandfläche {i+1}", value=1) for i in range(int(areas))]
            sub = st.form_submit_button('Submit')
        #st.write(surfaces)

    alpha = basic_dict_2()

    material_dict = read_db()
    with col_2:
        with st.form(key = 'material'):
            materials = [st.selectbox(
                label= f'Bitte wählen Sie das Material der Wand {i+1} aus.'
                ,options=material_dict.keys())for i in range(int(areas))]
            sub = st.form_submit_button('Submit')

          
for ind, octaveBands in enumerate(alpha):
    for material in materials:
        alpha[octaveBands].append(material_dict[material][ind])

#Erstellen des Objektes Raum der Klasse room
raum = room(volume=vol, surface=surfaces, alpha=alpha, use='Musik')
#Plots erstellen

st.divider()
st.subheader('Ergebnisse')
st.divider()
tab1, tab2 = st.tabs(['Nachhallzeit', 'Vergleich der Nachhallzeit'])
with tab1:
    fig1 = raum.plot_reverberationTime()
    st.plotly_chart(fig1)

with tab2:
    fig2 = raum.plot_reverberationTime_ratio()

    st.plotly_chart(fig2)
