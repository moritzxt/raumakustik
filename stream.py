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

surfaces = []
materials = []
names = [f'Wandfläche {i+1}' for i in range(areas)]
subAreas = 0

tabs = st.tabs(names)

for tab, name in zip(tabs, names):
    with tab:
        with st.container():
            col_1, col_2, col_3 = st.columns(3)
            with col_1:
                #with st.form(key = f'MainSurface {name}'):
                surfaces.append(st.number_input(
                    f"Fläche für {name}", value=1))
                if st.button('Add Subwandfläche', key = f'subArea {name}'):
                    subAreas += 1

                    #subAreas = st.number_input('Anzahl der Subwandflächen', min_value=0, step=1, value=0)
                    #sub = st.form_submit_button('Submit')
                #st.write(surfaces)

            with col_2:
                with st.form(key = f'subSurface {name}'):
                    subsurfaces = [st.number_input(
                    f"Fläche für Subwandfläche {i+1}", value=1) for i in range(int(subAreas))]
                    sub = st.form_submit_button('Submit')
            

            material_dict = read_db()
            with col_3:
                with st.form(key = f'subMaterial {name}'):
                    materials.append(st.selectbox(label =  f'Bitte wählen Sie das Material der {name} aus.'
                        ,options=material_dict.keys()))
                    subMaterials = [st.selectbox(
                        label= f'Bitte wählen Sie das Material der Subwand {i+1} aus.'
                        ,options=material_dict.keys())for i in range(int(subAreas))]
                    sub = st.form_submit_button('Submit')

alpha = basic_dict_2()

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
