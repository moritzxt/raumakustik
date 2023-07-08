import numpy as np 

import streamlit as st
#import streamlit_tags as sttags
from room_calc import room
from utils import basic_dict , read_db, basic_dict_2, add_row, usecase, sub_alpha_dict, flatten_dict
import os
import json
from streamlit.runtime.scriptrunner.script_run_context import add_script_run_ctx
from session_utils import write_session_file, load_session_file, write_session_key, init_starting_values, sync_session, load_session, negate_checkbox, write_json


#setup of  page data:
st.set_page_config(page_title= 'Tool für Raumakustik', layout='wide',
                    initial_sidebar_state='collapsed')

# """Eingabe der Parameter"""
tabs_list = []
main_surfaces = {} # Dict enthält den Flächeninhalte der Hauptfläche, korrespondierend zum Key (name der Hauptfläche)
main_materials = [] # Materialien 
material_dict = read_db('Datenbank_DIN18041.csv')
material_dict_flattened = flatten_dict(material_dict)

person_dict = read_db('equivalentAbsorptionSurface_people_data.csv')
sub_surfaces = {}
sub_materials = {}
numberOfPeople = []
peopleDescription = []

#create a json file with session id as file name
state = add_script_run_ctx().streamlit_script_run_ctx.session_id +'.json'
write_session_file(state)

#load the last session into session json file
load_session_file(state)

#write current session id in session_key.json
session = add_script_run_ctx().streamlit_script_run_ctx.session_id
write_session_key(session)

#load data from current session
with open(state) as jsonkey:
    json_data = json.load(jsonkey)

#read material data bank
#material_dict = read_db('Datenbank_Absorptionsgrade.csv')

load_session(state)
#read starting positions of input elements from last session... 
init_data = init_starting_values(json_data,material_dict,person_dict)
#if 'volume' not in st.session_state:
#    st.session_state['volume'] = init_data['volume']
#if 'usecase' not in st.session_state:
#    st.session_state['usecase'] = init_data['usecase']

#def _update_volume():
#    name = st.session_state['file_name_open']
##    name = st.session_state[key_file_name_open]
#    with open(name + ".json", "r") as file:
#        test = json.load(file)
#    st.session_state['volume'] = test['volume']
#sync_session(state)
#st.write(st.session_state['volume'])
#definition of website data:
#with col1:
with st.container():
    st.title('WebApp for Roomacoustics')
    st.divider()
    st.header('Benötigt werden das Raumvolumen, die Anzahl'
        ' der Wände, deren Fläche, sowie das Material der Wandoberfläche')
    #testvar = []
    #for keys in st.session_state:
    #    testvar.append([keys, st.session_state[keys]])
    #st.write(testvar)
    #st.write(init_data['sub_area'])       #for debugging purposes
    #st.write(state)
    #import random
    #def _update_slider(value):
    #    st.session_state["test_slider"] = value
    #if "test_slider" not in st.session_state:
    #    st.session_state["test_slider"] = 0
    #st.slider("slider", key="test_slider", min_value = 0, max_value = 100)

    #if "number_input" not in st.session_state:
    #    st.session_state["number_input"] = 0
    #st.number_input("Value", key="number_input", min_value = 0, max_value = 100)
    #st.write(st.session_state["number_input"])
    #st.button("upadte", on_click = _update_slider, kwargs={"value":st.session_state["number_input"]})
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        #selection of usecase
        #use = st.selectbox('Usecase nach DIN 18041', options=usecase.keys(), key='usecase_index', index=init_data['usecase_index'], on_change = sync_session, kwargs = {"state":state})
        use = st.selectbox('Usecase nach DIN 18041', options=usecase.keys(), index=init_data['usecase_index'],)
        #on change save current usecase into json
        json_data['usecase'] = use
        with open(state,'w') as jsonkey:
            json.dump(json_data, jsonkey)

        #set boundaries of volume for usecase
        min_lim =  min(usecase[use])
        max_lim =  max(usecase[use])

        if 'volume' not in st.session_state:
            st.session_state['volume'] = init_data['volume']
        #check if initial values are in limits and replace them if they aren't
        if init_data['volume'] < min_lim:
            volume_new_init = min_lim
        elif init_data['volume'] > max_lim:
            volume_new_init = max_lim
        else:
            volume_new_init = init_data['volume']
        if st.session_state['volume'] < min_lim:
            st.session_state['volume'] = min_lim
        elif st.session_state['volume'] > max_lim:
            st.session_state['volume'] = max_lim

    with col2:
        #st.write(st.session_state['volume'])
        #input of volume
        vol = st.number_input('Volumen in m³', min_value=min_lim,
                            max_value=max_lim,  key='volume', on_change = sync_session, kwargs ={"state": state})
        #save current key in json
        json_data['volume'] = vol
        with open(state,'w') as jsonkey:
            json.dump(json_data, jsonkey)
        #st.write(st.session_state['volume'])
        #sync_session(state)

        
    with col3:
        if 'number_walls' not in st.session_state:
            st.session_state['number_walls'] = init_data['number_walls']
        #input of amount of walls
        #areas = st.number_input('Anzahl der Wandflächen die Sie eingeben möchten'
        #                        ,min_value=1, step=1, key = 'number_walls')
        areas = st.number_input('Anzahl der Wandflächen die Sie eingeben möchten'
                                ,min_value=1, step=1, value=init_data['number_walls'])
        #areas = st.number_input('Anzahl der Wandflächen die Sie eingeben möchten'
        #                        ,min_value=1, step=1, key='number_walls', value=init_data['number_walls'], on_change = sync_session, kwargs ={"state": state})
        #save current key in json
        json_data['number_walls'] = areas
        for i in range(areas):
            json_data['wall' + str(i+1)] = {"area": init_data['area'][i], "material": init_data['material_string'][i], "number_subareas":0}
        #delete removed walls from file
        for j in range(100):
            if j > areas and ('wall' + str(j)) in json_data:
                del json_data['wall' + str(j)]
        with open(state,'w') as jsonkey:
            json.dump(json_data, jsonkey)
    with col4:
        st.empty()
        #st.write(st.session_state['personen'])
        #checkboxvar = json_data['persons']
        #st.session_state['personen'] = init_data['persons']
        #st.write(init_data['persons'])
        json_data['persons'] = init_data['persons']
        if st.checkbox(label='Personen', key='personen', label_visibility='visible', on_change = negate_checkbox, kwargs = {"json_data": json_data, "state": state}):
            tabs_list = ['Personen']
        #json_data['persons'] = checkboxvar
        #st.write(st.session_state['personen'])
    #json_data['persons'] = not json_data['persons']
        #json_data['persons'] = st.session_state['personen']
    
    #st.write(json_data['persons'])
    



area =  np.linspace(0,int(areas),int(areas)+1)



main_walls = [f'Grundflaeche {i+1}' for i in range(areas)]
subAreas = []

numPeople = init_data['persons'] # Anzahl der Personengruppen im Raum 
tabs_list.extend(main_walls)

for key in main_walls:
    sub_surfaces[key] = []
    sub_materials[key] = []
    main_surfaces[key] = None

tabs = st.tabs(tabs_list)


# Tabs für die jeweiligen Flächen und die 
# Personen

for tab, name in zip(tabs, tabs_list):
    with tab:
    
        if name == 'Personen':
            col_11, col_12 = st.columns(2)

            if 'add_persons' not in st.session_state:
                st.session_state['add_persons'] = numPeople

            if st.button('Add Personen', key ='button_add_persons'):
                st.session_state['add_persons'] += 1

            #for i in range(st.session_state['add_persons']):
            #    peopleDescription.append(init_data['type'][i])
            numPeople = st.session_state['add_persons']
            json_data['number_people'] = numPeople
            for i in range(numPeople):
                if 'person_type' + str(i+1) not in json_data:
                    json_data['person_type' + str(i+1)] = {}
                #json_data['person_type' + str(i+1)]['amount'] = init_data['amount'][i]
                #json_data['person_type' + str(i+1)]['type'] = init_data['type_string'][i]
            with open(state,'w') as jsonkey:
                json.dump(json_data, jsonkey)

            for num in range(0, numPeople):
                
                    #st.session_state[f'people{num}'] = init_data['amount'][num]
                    #st.session_state[f'Beschreibung{num}'] = 
                    #if f'people{num}' not in st.session_state:   {"amount": init_data['amount'][i], "type": init_data['type_string'][i]}
                    #    st.session_state[f'people{num}'] = int(init_data['amount'][0])
                    #st.session_state[f'people{num}'] = init_data['amount'][num]
                   
                    with col_11:
                        numberOfPeople.append(st.number_input(
                                f"Anzahl an Personen im Raum", step = 1, key = f'people{num}', value=init_data['amount'][num-1], on_change = write_json, kwargs = {"json_data": json_data, "state": state, "num":num}))
                        st.write(num)
                        
                    with col_12:
                        peopleDescription.append(st.selectbox(label =  f'Beschreibung',
                                                            key=f'Beschreibung{num}',options=person_dict.keys(), index = init_data['type'][num])) 
                        
                        #with open(state,'w') as jsonkey:
                        #    json.dump(json_data, jsonkey)
                        
                    
                    #init_data['amount'][num] = st.session_state[f'people{num}']

                    #json_data['person_type' + str(num+1)]['amount'] = st.session_state[f'people{num}']
                    json_data['person_type' + str(num+1)]['type'] = peopleDescription[num]
                    with open(state,'w') as jsonkey:
                        json.dump(json_data, jsonkey)
                    #json_data['person_type' + str(num+1)]['amount'] = st.session_state[f'people{num}'] 
                    #json_data['person_type' + str(num+1)]['amount'] = numberOfPeople[num]
                    #json_data['person_type' + str(num+1)][ ]
                    
                    
            
            if st.button('Remove Personen', key='remove_button_persons'):
                if st.session_state['add_persons'] > 1 and len(peopleDescription) > 0:
                    st.session_state['add_persons'] -= 1
                    peopleDescription.pop()
                    numberOfPeople.pop()
                    #st.experimental_rerun()
                    json_data['number_people'] = st.session_state[f'add_persons']
                    with open(state,'w') as jsonkey:
                        json.dump(json_data, jsonkey)  
     

        else:
                #extract number of base area
                number1 = name[13]
                try:
                    number2 = name[14]
                    number = 10*int(number)+int(number2)
                except IndexError:
                    number = int(number1)


                if f'subAreas{name}' not in st.session_state:
                    st.session_state[f'subAreas{name}'] = init_data['number_subareas'][number]          #with this only one subarea is possible, but that one works just as intended
                con_1 = st.container()
                con_2 = st.container()

                with con_1:
                    col_1, col_2, col_3 = st.columns(3)

                    with col_1:
                        main_surfaces[name] = (st.number_input(
                            f"Fläche für {name}", value=init_data['area'][number-1], min_value=0))

                    with col_2:
                        category = st.selectbox(label='Bitte wählen Sie die Kategorie des Materials aus',
                                                key=f'{name}' ,options=material_dict.keys(), index=init_data['category'][number-1])
                    with col_3:
                        main_materials.append(st.selectbox(label =  f'Bitte wählen Sie das Material der {name} aus.',
                                                        options=material_dict[f'{category}'].keys(), index=init_data['material'][number-1]))

                    #save currenty wall area in json
                    #for i in range(int(areas)):
                    json_data['wall' + str(number)]['area'] = main_surfaces[name]
                    json_data['wall' + str(number)]['category'] = st.session_state[f'{name}']
                    json_data['wall' + str(number)]['material'] = main_materials[number-1]
                    with open(state,'w') as jsonkey:
                        json.dump(json_data, jsonkey)
                

                with con_2:
                    st.divider()
                    col_1, col_2, col_3 = st.columns(3)

                    #subAreas = init_data['number_subareas'][number]

                    if st.button('Add Subwandfläche', key = f'Button subArea{subAreas} {name}'):
                        st.session_state[f'subAreas{name}'] += 1
                    subAreas = st.session_state[f'subAreas{name}']

                    #if st.button('Remove Subwandfläche', key=f'remove Subfläche von {name}'):
                    #    if st.session_state[f'subAreas{name}'] > 0:
                    #        st.session_state[f'subAreas{name}'] -= 1
                    #        sub_materials[name].pop()
                    #        sub_surfaces[name].pop()

                    #write number of subareas in json file
                    json_data['wall' + str(number)]['number_subareas'] = subAreas  
                    

                    with open(state,'w') as jsonkey:
                        json.dump(json_data, jsonkey)     
#{"area": init_data['sub_area'][i], "category": init_data["sub_category"][i],  "sub_material": init_data['sub_material'][i]}
                
            #       '''
            #           Wand 1 -> surface[Wand 1] = [m²]
                        # sub_surfaces[Wand 1] =  [sub11 m², sub12 m², sub13m² ...]
                        # sub_surfaces[Wand 2] =  [sub21 m², sub22 m², sub23m² ...]
                        # sub_materials[wand 1] = [subMat]

                        # sub_alpha['125 Hz'][Wall 1] = [alpha_subwand1, alpha_subwand2 ...]
                        # sub_alpha['2k Hz'][Wall 1] = [alpha_subwand1, alpha_subwand2 ...]

                        # '''
                            
                    for num in range(0, subAreas):
                        #write corresponding data for subareas in json file 
                        #for i in range(subAreas):
                        json_data['wall' + str(number)]['subarea' + str(num+1)] = {}
                        json_data['wall' + str(number)]['subarea' + str(num+1)]['area'] = init_data['sub_area'][number][num+1]
                        cat = list(material_dict.keys())[init_data['sub_category'][number][num+1]]
                        json_data['wall' + str(number)]['subarea' + str(num+1)]['category'] = cat
                        json_data['wall' + str(number)]['subarea' + str(num+1)]['material'] = list(material_dict[f'{cat}'].keys())[init_data['sub_material'][number][num+1]]

                        with open(state,'w') as jsonkey:
                            json.dump(json_data, jsonkey)   

                        with col_1:
                            sub_surfaces[name].append(st.number_input(f"Fläche für Subwandfläche {num +1 }",
                                                                    value=init_data['sub_area'][number-1][num] , key = f'Fläche subArea{num} {name}',min_value=0))

                        with col_2:
                            category = st.selectbox(label='Bitte wählen Sie die Kategorie des Materials aus',
                                                     options=material_dict.keys(), key= f'cat_sub_{name}{num}', index = init_data['sub_category'][number-1][num])
                        with col_3:
                            sub_materials[name].append(st.selectbox(label =  f'Bitte wählen Sie das Material der Subfläche {num + 1} aus.'
                               ,options=material_dict[f'{category}'].keys(), key=f'Subfläche {num} von {name}', index = init_data['sub_material'][number-1][num]))
                            
                        #for i in range(subAreas):
                        #for every subarea, write area and material in json
                        #json_data['wall' + str(number)]['subarea' + str(num+1)] = {"area": sub_surfaces[name][num], "category": category[name][num], "material": sub_materials[name][num]}
                        json_data['wall' + str(number)]['subarea' + str(num+1)]['area'] = sub_surfaces[name][num]
                        json_data['wall' + str(number)]['subarea' + str(num+1)]['category'] = category
                        json_data['wall' + str(number)]['subarea' + str(num+1)]['material'] = sub_materials[name][num]
                        with open(state,'w') as jsonkey:
                            json.dump(json_data, jsonkey)     
                        #st.write(sub_surfaces)
                        #             
                    if st.button('Remove Subwandfläche', key=f'remove Subfläche von {name}') and len(sub_materials[name]) > 0:
                        if st.session_state[f'subAreas{name}'] > 0:
                            st.session_state[f'subAreas{name}'] -= 1
                            sub_materials[name].pop()
                            sub_surfaces[name].pop()
                            #st.experimental_rerun()
                            json_data['wall' + str(number)]['number_subareas'] = st.session_state[f'subAreas{name}']
                            with open(state,'w') as jsonkey:
                                json.dump(json_data, jsonkey)  
                                
#with st.container():
    #col_1, col_2 = st.columns(2)
    #with col_1:
        #with st.form(key = 'surface'):
            #input of wall area
            #surfaces = [st.number_input(f"Fläche für Wandfläche {i+1}", value=init_data['area'][i]) for i in range(int(areas))]
            #sub = st.form_submit_button('Submit')
            #save currenty wall area in json
            #for i in range(int(areas)):
            #    json_data['wall' + str(i+1)]['area'] = surfaces[i]
            #with open(state,'w') as jsonkey:
            #    json.dump(json_data, jsonkey)
    

    #Initialisierung des Dictionaries für die Absorptionsgrade
    alpha = basic_dict_2()

    #Befuellen des dicts mit den Absorptionsgeraden fuer die jeweiligen Oktavbaender und 
    #with col_2:
        #with st.form(key = 'material'):
            #selection of wall material
            #materials = [st.selectbox(label= f'Bitte wählen Sie das Material der Wand {i+1} aus.'
            #                          ,options=material_dict.keys(), index = init_data['material'][i])for i in range(int(areas))]
            #sub = st.form_submit_button('Submit')
            #save current wall material in json
            #for i in range(int(areas)):
            #    json_data['wall' + str(i+1)]['material'] = materials[i]
            #with open(state,'w') as jsonkey:
            #    json.dump(json_data, jsonkey)


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
                #save contents of file in session file
                with open(name + ".json", "r") as file:                 #needs an exception if file does not exist
                    with open(state, "w") as open_json:
                        open_json.write(file.read())
                #load_session(name, state)
                st.experimental_rerun()
                #with open(state) as jsonkey:
                #    json_data = json.load(jsonkey)
                #st.session_state.volume = json_data['volume']


#Befuellen des dicts mit den Absorptionsgeraden fuer die jeweiligen Oktavbaender und 
for ind, octaveBand in enumerate(alpha):
    for material in main_materials:
        try:
            alpha[octaveBand].append(material_dict_flattened[material][ind])
        except:
            alpha[octaveBand].append(None)

sub_alpha = sub_alpha_dict(main_walls)

for ind, octaveBand in enumerate(sub_alpha):
    for wall in sub_alpha[octaveBand]:
            for material in sub_materials[wall]:
                sub_alpha[octaveBand][wall].append(material_dict_flattened[material][ind])

#Erstellen des Objektes Raum der Klasse room
raum = room(volume=vol, surface=main_surfaces, sub_surface=sub_surfaces, alpha=alpha, 
            sub_alpha=sub_alpha, use=use, peopleDescription=peopleDescription, numberOfPeople=numberOfPeople)
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
