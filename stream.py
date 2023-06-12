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
        json.dump({}, init)

#load the last session
if os.path.isfile('session_key.json'):
    with open('session_key.json', 'r') as file:
        last_session_keyy = json.load(file)
        last_session_key = last_session_keyy['key']
        with open(last_session_key + '.json', 'r') as file:
            last_session = json.load(file)
            with open(state, 'w') as init:
                json.dump(last_session, init)

#create a json file with session id
session = add_script_run_ctx().streamlit_script_run_ctx.session_id
with open('session_key.json', 'w') as init:
    json.dump({'key': session}, init)


with open(state) as jsonkey:
    json_data = json.load(jsonkey)

if not (json_data == '{}'):
    usecase_init = json_data['usecase']
    if usecase_init == 'Musik':
        usecase_index = 0
    elif usecase_init == 'Sprache/Vortrag':
        usecase_index = 1
    elif usecase_init == 'Sprache/Vortrag inklusiv':
        usecase_index = 2
    elif usecase_init == 'Unterricht/Kommunikation':
        usecase_index = 3
    elif usecase_init == 'Sport':
        usecase_index = 4

    volume_init = json_data['volume']
    number_walls_init = json_data['number_walls']
    length = 0
    for i in range(100):
        if 'wall' + str(i) in json_data:
            length += 1
    #area_init = np.zeros(length)
    #material_init = np.zeros(length)
    #for i in range(length):
        #area_init[i] = json_data['wall' + str(i+1)]['area']
        #material_init[i] = json_data['wall' + str(i+1)]['material']
else:
    usecase_init = 'Music'
    usecase_index = 0
    volume_init = 30
    number_walls_init = 1
    area_init = {1}
    material_init = {'Walls,hard surfaces average (brick walls, plaster, hard floors, etc.)'}

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
    use = st.selectbox('Usecase nach DIN 18041', options=usecase.keys(), index=usecase_index)
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
                        max_value=max_lim, value=volume_init)
    #save current key in json
    json_data['volume'] = vol
    with open(state,'w') as jsonkey:
        json.dump(json_data, jsonkey)

with col3:
    areas = st.number_input('Anzahl der Wandflächen die Sie eingeben möchten'
                            ,min_value=1, step=1, value=number_walls_init)
    #save current key in json
    json_data['number_walls'] = areas
    for i in range(areas):
        json_data['wall' + str(i+1)] = {"area": 1, "material": "Walls,hard surfaces average (brick walls, plaster, hard floors, etc.)"} #needs to be implemented that wall gets removed when deleted and changed stuff actually stays changed
    for j in range(100):                                                                                   #<-something like this? as answer to that ^
        if j > areas and ('wall' + str(j)) in json_data:
            del json_data['wall' + str(j)]
    with open(state,'w') as jsonkey:
        json.dump(json_data, jsonkey)
        #with open(state, "r") as jsonkey:
            #json_data
        #with open(state, "a") as jsonkey:
            #json.dump({'wall' + str(i) + 'area': 1, 'wall' + str(i)+ 'material': 'Walls,hard surfaces average (brick walls, plaster, hard floors, etc.)'}, jsonkey)

area =  np.linspace(0,int(areas),int(areas)+1)
with st.container():
    col_1, col_2 = st.columns(2)
    with col_1:
        with st.form(key = 'surface'):
            
            surfaces = [st.number_input(f"Fläche für Wandfläche {i+1}", value=1) for i in range(int(areas))]
            sub = st.form_submit_button('Submit')
            #save currenty wall area in json
            for i in range(int(areas)):
                json_data['wall' + str(i+1)]['area'] = surfaces[i]
            with open(state,'w') as jsonkey:
                json.dump(json_data, jsonkey)
                
        #st.write(surfaces)
    

    alpha = basic_dict_2()

    material_dict = read_db('Datenbank_Absorptionsgrade.csv')
    with col_2:
        with st.form(key = 'material'):
            materials = [st.selectbox(label= f'Bitte wählen Sie das Material der Wand {i+1} aus.'
                                      ,options=material_dict.keys())for i in range(int(areas))]
            sub = st.form_submit_button('Submit')
            #save current wall material in json
            for i in range(int(areas)):
                json_data['wall' + str(i+1)]['material'] = materials[i]
            with open(state,'w') as jsonkey:
                json.dump(json_data, jsonkey)


with st.container():
    col_1, col_2 = st.columns(2)
    with col_1:
        #create a save as button that unlocks a text input space
        if "save_as_name" not in st.session_state:
            st.session_state["save_as_name"] = ""

        if "save_as" not in st.session_state:
            st.session_state["save_as"] = False

        if st.button("save as"):
            st.session_state["save_as"] = not st.session_state["save_as"]

        key_file_name_save = " "
        #name = ""
        if st.session_state["save_as"]:
            save_as_file_name = st.text_input("file name", key=key_file_name_save)
            st.session_state["save_as_name"] = st.session_state[key_file_name_save]
            #saves the json file as the input file name
            if st.button("save"):
                name = st.session_state[key_file_name_save]
                with open(name + ".json", "w") as file:
                    with open(state, "r") as open_json:
                        file.write(open_json.read())

    with col_2:
        #create an open file button that unlocks a text input space
        if "open_file_name" not in st.session_state:
            st.session_state["open_file_name"] = ""

        if "open_file" not in st.session_state:
            st.session_state["open_file"] = False

        if st.button("open file"):
            st.session_state["open_file"] = not st.session_state["open_file"]

        key_file_name_open = ""
        if st.session_state["open_file"]:
            save_as_file_name = st.text_input("file name", key=key_file_name_open)
            st.session_state["open_file_name"] = st.session_state[key_file_name_open]
            #saves the json file as the input file name
            if st.button("open"):
                name = st.session_state[key_file_name_open]
                with open(name + ".json", "r") as file:                 #needs an exception if file does not exist
                    with open(state, "w") as open_json:
                        open_json.write(file.read())


          
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
