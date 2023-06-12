import numpy as np 

import streamlit as st
#import streamlit_tags as sttags
from room_calc import room
from utils import basic_dict , read_db, basic_dict_2, add_row, usecase
import os
import json
from streamlit.runtime.scriptrunner.script_run_context import add_script_run_ctx


#setup of  page data:
st.set_page_config(page_title= 'Tool für Raumakustik', layout='wide',
                    initial_sidebar_state='collapsed')

#create a json file with session id as file name
state = add_script_run_ctx().streamlit_script_run_ctx.session_id +'.json'
if not os.path.isfile(state):
    #refactor all 2.WebApp.json to 2.WebApp variable
    with open(state, 'w') as init:
        json.dump({}, init)

#load the last session into session json file
if os.path.isfile('session_key.json'):
    with open('session_key.json', 'r') as file:
        last_session_keyy = json.load(file)
        last_session_key = last_session_keyy['key']
        if os.path.isfile(last_session_key + '.json'):
            with open(last_session_key + '.json', 'r') as file:
                last_session = json.load(file)
                with open(state, 'w') as init:
                    json.dump(last_session, init)

#write current session id in session_key.json
session = add_script_run_ctx().streamlit_script_run_ctx.session_id
with open('session_key.json', 'w') as init:
    json.dump({'key': session}, init)

#load data from current session
with open(state) as jsonkey:
    json_data = json.load(jsonkey)

#read material data bank
material_dict = read_db('Datenbank_Absorptionsgrade.csv')

#read starting positions of input elements from last session... 
if not (json_data == {}):
    usecase_init = json_data['usecase']         #could be done more elegantly, might change if i ever bother
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
    area_init = []
    material_init = []
    material_init_string = []
    #fill area and material data for existing walls
    for i in range(number_walls_init):
        area_init.append(json_data['wall' + str(i+1)]['area'])
        material_init_string.append(json_data['wall' + str(i+1)]['material'])
        for j in range(len(list(material_dict))):
            if list(material_dict)[j] == json_data['wall' + str(i+1)]['material']:   #what happens when key aint found?
                material_init.append(j)
    #then set data to defaults for 100 next indices, to allow adding more walls - so limiting the number of walls to 100 would be smart
    for i in range(100):
        area_init.append(1)
        material_init_string.append(list(material_dict)[0])
        material_init.append(0)
#... if there isnt a last session, set starting positions to defaults
else:
    usecase_init = 'Music'
    usecase_index = 0
    volume_init = 30
    number_walls_init = 1
    area_init = {1}
    material_init = {'Walls,hard surfaces average (brick walls, plaster, hard floors, etc.)'}


#definition of website data:
#with col1:
with st.container():
    st.title('WebApp for Roomacoustics')
    st.divider()
    st.header('Benötigt werden das Raumvolumen, die Anzahl'
        ' der Wände, deren Fläche, sowie das Material der Wandoberfläche')
    #st.write(json_data['wall' + str(1)]['material'])       #for debugging purposes
    #st.write(state)

col1, col2, col3 = st.columns(3)
with col1:
    #selection of usecase
    use = st.selectbox('Usecase nach DIN 18041', options=usecase.keys(), index=usecase_index)
    #on change save current usecase into json
    json_data['usecase'] = use
    with open(state,'w') as jsonkey:
        json.dump(json_data, jsonkey)

    #set boundaries of volume for usecase
    min_lim =  min(usecase[use])
    max_lim =  max(usecase[use])
    #check if initial values are in limits and replace them if they are
    if volume_init < min_lim:
        volume_new_init = min_lim
    elif volume_init > max_lim:
        volume_new_init = max_lim
    else:
        volume_new_init = volume_init

with col2:
    #input of volume
    vol = st.number_input('Volumen in m³', min_value=min_lim,
                        max_value=max_lim, value=volume_new_init)
    #save current key in json
    json_data['volume'] = vol
    with open(state,'w') as jsonkey:
        json.dump(json_data, jsonkey)

with col3:
    #input of amount of walls
    areas = st.number_input('Anzahl der Wandflächen die Sie eingeben möchten'
                            ,min_value=1, step=1, value=number_walls_init)
    #save current key in json
    json_data['number_walls'] = areas
    for i in range(areas):
        json_data['wall' + str(i+1)] = {"area": area_init[i], "material": material_init_string[i]}
    #delete removed walls from file
    for j in range(100):
        if j > areas and ('wall' + str(j)) in json_data:
            del json_data['wall' + str(j)]
    with open(state,'w') as jsonkey:
        json.dump(json_data, jsonkey)


area =  np.linspace(0,int(areas),int(areas)+1)
with st.container():
    col_1, col_2 = st.columns(2)
    with col_1:
        with st.form(key = 'surface'):
            #input of wall area
            surfaces = [st.number_input(f"Fläche für Wandfläche {i+1}", value=area_init[i]) for i in range(int(areas))]
            sub = st.form_submit_button('Submit')
            #save currenty wall area in json
            for i in range(int(areas)):
                json_data['wall' + str(i+1)]['area'] = surfaces[i]
            with open(state,'w') as jsonkey:
                json.dump(json_data, jsonkey)
    

    alpha = basic_dict_2()

    with col_2:
        with st.form(key = 'material'):
            #selection of wall material
            materials = [st.selectbox(label= f'Bitte wählen Sie das Material der Wand {i+1} aus.'
                                      ,options=material_dict.keys(), index = material_init[i])for i in range(int(areas))]
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

        if st.session_state["save_as"]:
            #space to input file name
            save_as_file_name = st.text_input("file name", key=key_file_name_save)
            st.session_state["save_as_name"] = st.session_state[key_file_name_save]
            #saves the json file as the input file name
            if st.button("save"):
                name = st.session_state[key_file_name_save]
                st.write(save_as_file_name + ".json saved successfully" )               #should prolly only display if save was successful, should disappear after a while
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
            #space to input file name
            save_as_file_name = st.text_input("file name (if file doesn't load properly, try refreshing the page)", key=key_file_name_open) # the reason it doesnt load properly is when you have changed an input parameter during this session, it wont go back to default position, dont think there is an easy fix
            st.session_state["open_file_name"] = st.session_state[key_file_name_open]
            #put the contents of the opened file in current session json and relaod page
            if st.button("open"):
                name = st.session_state[key_file_name_open]
                with open(name + ".json", "r") as file:                 #needs an exception if file does not exist
                    with open(state, "w") as open_json:
                        open_json.write(file.read())
                st.experimental_rerun()


          
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
