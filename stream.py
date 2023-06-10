import numpy as np 

import streamlit as st
#import streamlit_tags as sttags
from room_calc import room
from utils import basic_dict , read_db, basic_dict_2, add_row, usecase
import os
import json
from streamlit.runtime.scriptrunner.script_run_context import add_script_run_ctx

st.set_page_config(page_title= 'Tool für Raumakustik', layout='wide',
                    initial_sidebar_state='collapsed')

#create a json file with session id as file name
state = add_script_run_ctx().streamlit_script_run_ctx.session_id +'.json'
if not os.path.isfile(state):
    #refactor all 2.WebApp.json to 2.WebApp variable
    with open(state, 'w') as init:
        json.dump({'usecase': 'Musik', 'volume': 30, 'number_walls': 1}, init) #still missing: wall parameters with variable numbers of walls, database including self-input materials

#def replaceByValue(field, oldvalue, newvalue):
#    for k in state.length:
#        if oldvalue == state[k][field]:
#            state[k][field] = newvalue

#better do with a loop for every key of the json file instead: for i in range(keys): ect.
with open(state) as jsonkey:
    json_data = json.load(jsonkey)
    #current_usecase = json.load(jsonkey)['usecase']
    #current_volume = json.load(jsonkey)['volume']
    #current_number_walls = json.load(jsonkey)['number_walls']
#with open(state) as jsonkey:
    #current_volume = json.load(jsonkey)['volume']

#with open(state) as jsonkey:
    #current_number_walls = json.load(jsonkey)['number_walls']

#with open(state) as volume_jsonkey:
#    current_usecase = json.load(volume_jsonkey)['volume']

#if st.button('button'):
#    counter += 1

#with open(state,'w') as f:
#    json.dump({'clicks': counter}, f)

#with col1:
with st.container():
    st.title('WebApp for Roomacoustics')
    st.divider()
    st.header('Benötigt werden das Raumvolumen, die Anzahl'
        ' der Wände, deren Fläche, sowie das Material der Wandoberfläche')

col1, col2, col3 = st.columns(3)
with col1:
    use = st.selectbox('Usecase nach DIN 18041', options=usecase.keys())
    #save new key every time you change it
    #if use:
    #    current_usecase = use.key
    #save current key in json
    #for item in json_data:
        #item['usecase'] = item['usecase'].replace()
    json_data['usecase'] = use
    with open(state,'w') as jsonkey:
        json.dump(json_data, jsonkey)

    min_lim =  min(usecase[use])
    max_lim =  max(usecase[use])
with col2:
    vol = st.number_input('Volumen in m³', min_value=min_lim,
                        max_value=max_lim, value=min_lim)
    #save current key in json
    json_data['volume'] = vol
    with open(state,'w') as jsonkey:
        json.dump(json_data, jsonkey)

with col3:
    areas = st.number_input('Anzahl der Wandflächen die Sie eingeben möchten'
                            ,min_value=1, step=1)
    #save current key in json
    json_data['number_walls'] = areas
    with open(state,'w') as jsonkey:
        json.dump(json_data, jsonkey)

area =  np.linspace(0,int(areas),int(areas)+1)
with st.container():
    col_1, col_2 = st.columns(2)
    with col_1:
        with st.form(key = 'surface'):
            surfaces = [st.number_input(f"Fläche für Wandfläche {i+1}", value=1) for i in range(int(areas))]
            sub = st.form_submit_button('Submit')
        #st.write(surfaces)

    alpha = basic_dict_2()

    material_dict = read_db('Datenbank_Absorptionsgrade.csv')
    with col_2:
        with st.form(key = 'material'):
            materials = [st.selectbox(label= f'Bitte wählen Sie das Material der Wand {i+1} aus.'
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
