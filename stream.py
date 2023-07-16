import numpy as np 
import pickle
import streamlit as st
#import streamlit_tags as sttags
from room_calc import room
from utils import basic_dict , read_db, basic_dict_2, add_row, usecase, sub_alpha_dict, flatten_dict
import os
import json
from streamlit.runtime.scriptrunner.script_run_context import add_script_run_ctx
from session_utils import write_session_file, load_session_file, write_session_key, init_starting_values, sync_session, load_session, negate_checkbox, write_json#, subArea_subst
from pdf_protocol import pdfprotocol

#setup of  page data:
# sessionObj = open('session.obj', 'rb')
# st.session_state = pickle.load(sessionObj)
# sessionObj.close()

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
main_walls = []
default_area = 'default'

if 'main_walls' not in st.session_state:
    #'''creating List for main_walls in current session, so it can be updated by add button'''
    st.session_state.main_walls = [default_area]


#create a json file with session id as file name
state = add_script_run_ctx().streamlit_script_run_ctx.session_id +'.json'
state = './session/' + state  
write_session_file(state)

#load the last session into session json file
load_session_file(state)

#write current session id in session_key.json
session = add_script_run_ctx().streamlit_script_run_ctx.session_id
write_session_key(session)

#load data from current session
with open(state) as jsonkey:
    json_data = json.load(jsonkey)

load_session(state)
#read starting positions of input elements from last session... 
init_data = init_starting_values(json_data,material_dict,person_dict)

# #create a json file with session id as file name
# state = add_script_run_ctx().streamlit_script_run_ctx.session_id +'.json'
# write_session_file(state)

#load the last session into session json file
load_session_file(state)

#write current session id in session_key.json
session = add_script_run_ctx().streamlit_script_run_ctx.session_id
session = './session/' + session  
write_session_key(session)

#load data from current session
with open(state) as jsonkey:
    json_data = json.load(jsonkey)

load_session(state)
#read starting positions of input elements from last session... 
init_data = init_starting_values(json_data,material_dict,person_dict)

with st.container():
    st.title('Web-App für Nachhallzeitenanalyse')
    st.divider()
    st.header('Eingabeparameter')

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        #selection of usecase
        use = st.selectbox('Nutzungsart nach DIN 18041', options=usecase.keys(), index=init_data['usecase_index'],)
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
        #input of volume
        vol = st.number_input('Volumen in m³', min_value=min_lim,
                            max_value=max_lim,  key='volume', on_change = sync_session, kwargs ={"state": state})
        #save current volume in json
        json_data['volume'] = vol
        with open(state,'w') as jsonkey:
            json.dump(json_data, jsonkey)

        
    with col3:
        #input for name of next wall that is being added
        wall_name = st.text_input('Name der Wandfläche', value='Wand 1')

        #check if wall name exists already, if yes, tell user
        if st.button('Hinzufügen'):
            if wall_name in st.session_state.main_walls:
                st.write("Diese Grundfläche existiert bereits")
            else:
            #if not, create new wall
                if default_area in st.session_state.main_walls:
                    st.session_state.main_walls = [wall_name]
                else:
                    st.session_state.main_walls.append(wall_name)
        if st.button('Entfernen', help= 'Geben Sie den Namen der Grundfläche ein, die Sie entfernen möchten.'):
            if wall_name in st.session_state.main_walls and len(st.session_state.main_walls) > 1:
                ind = st.session_state.main_walls.index(wall_name)
                #Removing specific Mainwall
                st.session_state.main_walls.pop(ind)
                json_data.pop('wall' + str(ind+1))
        #save amount of walls in json file
        if 'Personen' in st.session_state.main_walls:
            json_data['number_walls'] = len(st.session_state.main_walls)-1
        else:
            json_data['number_walls'] = len(st.session_state.main_walls)
        with open(state,'w') as jsonkey:
            json.dump(json_data, jsonkey)
        

    with col4:
        st.empty()
        #setup json key
        json_data['persons'] = init_data['persons']
        #checkbox if persons are displayed or not
        if st.checkbox(label='Personen', key='personen', label_visibility='visible', on_change = negate_checkbox, kwargs = {"json_data": json_data, "state": state}):
            tabs_list = ['Personen']
            if 'Personen' not in st.session_state.main_walls:
                #'''check if Personen already exist, otherwise there are more personen tabs'''
                st.session_state.main_walls.insert(0, 'Personen')
        else:
            if 'Personen' in st.session_state.main_walls:
                # delete Personstab if it is deactivated
                st.session_state.main_walls.pop(0)

subAreas = 0

numPeople = init_data['number_people'] # Anzahl der Personengruppen im Raum 

for key in st.session_state.main_walls:
     if not key == 'Personen':
        #making sure, that Person is no key for the lists    
        sub_surfaces[key] = []
        sub_materials[key] = []
        main_surfaces[key] = 0

tabs = st.tabs(st.session_state.main_walls)


# Tabs für die jeweiligen Flächen und die 
# Personen

for tab, name in zip(tabs, st.session_state.main_walls):

    with tab:
        if name == 'Personen':
            col_11, col_12 = st.columns(2)

            #setup number of person types for first runthrough
            if 'add_persons' not in st.session_state:
                st.session_state['add_persons'] = numPeople
            #button to add more person types
            if st.button('Personengruppe hinzufügen', key ='button_add_persons'):
                st.session_state['add_persons'] += 1

            #if person type has been removed on last runthrough, display one less
            if 'remove_button_persons' in st.session_state:
                if st.session_state.remove_button_persons == True:
                    numPeople = st.session_state.add_persons-1
                else:
                    numPeople = st.session_state['add_persons']
            #put number of person types into json
            json_data['number_people'] = numPeople
            for i in range(numPeople):
                if 'person_type' + str(i+1) not in json_data:
                    json_data['person_type' + str(i+1)] = {}
            with open(state,'w') as jsonkey:
                json.dump(json_data, jsonkey)

            for num in range(0, numPeople):
                    #input of amount of persons per person type
                    with col_11:
                        numberOfPeople.append(st.number_input(
                                f"Anzahl der Personen", step = 1, key = f'people{num}', value=init_data['amount'][num], on_change = write_json, kwargs = {"json_data": json_data, "state": state, "num":num}))
                        
                    #put amount of people of type in json file
                    json_data['person_type' + str(num+1)]['amount'] = numberOfPeople[num]
                    #input of the type description of person 
                    with col_12:
                        peopleDescription.append(st.selectbox(label =  f'Beschreibung',
                                                            key=f'Beschreibung{num}',options=person_dict.keys(), index = init_data['type'][num])) 
                        
                    #put type description into json file
                    json_data['person_type' + str(num+1)]['type'] = peopleDescription[num]
                    with open(state,'w') as jsonkey:
                        json.dump(json_data, jsonkey)

                    
            #removal button for person types
            if st.button('Personengruppe entfernen', key='remove_button_persons'):
                if st.session_state['add_persons'] > 1 and len(peopleDescription) > 0:
                    st.session_state['add_persons'] -= 1
                    peopleDescription.pop()
                    numberOfPeople.pop()
                    json_data.pop('person_type' + str(st.session_state.add_persons+1))
                    #sync amount of person types with json file
                    json_data['number_people'] = st.session_state[f'add_persons']
                    with open(state,'w') as jsonkey:
                        json.dump(json_data, jsonkey)  
     

        else:
                #extract number of base area (differently if persons is ticked or not)
                if 'Personen' in st.session_state.main_walls:
                    number = st.session_state.main_walls.index(name)-1
                else:
                    number = st.session_state.main_walls.index(name)

                if 'wall'+str(number+1) not in json_data:
                    json_data['wall' + str(number+1)] = {}
                #put name of wall into json file
                json_data['wall' + str(number+1)]['name'] = name
                with open(state,'w') as jsonkey:
                    json.dump(json_data, jsonkey)


                if f'subAreas{name}' not in st.session_state:
                    st.session_state[f'subAreas{name}'] = init_data['number_subareas'][number]
                con_1 = st.container()
                con_2 = st.container()

                with con_1:
                    col_1, col_2, col_3 = st.columns(3)
                    #area for every subarea
                    with col_1:
                        main_surfaces[name] = (st.number_input(
                            f"Fläche für {name}", value=init_data['area'][number], min_value=0))
                    #category for each subarea
                    with col_2:
                        category = st.selectbox(label='Materialkategorie',
                                                key=f'{name}' ,options=material_dict.keys(), index=init_data['category'][number])
                    #material for every subarea
                    with col_3:
                        main_materials.append(st.selectbox(label =  f'Material von {name}',
                                                        options=material_dict[f'{category}'].keys(), index=init_data['material'][number]))

                    #save currenty wall area, category and type in json
                    json_data['wall' + str(number+1)]['area'] = main_surfaces[name]
                    json_data['wall' + str(number+1)]['category'] = st.session_state[f'{name}']
                    json_data['wall' + str(number+1)]['material'] = main_materials[number]
                    with open(state,'w') as jsonkey:
                        json.dump(json_data, jsonkey)
                

                with con_2:
                    st.divider()
                    col_1, col_2, col_3 = st.columns(3)

                    #get initial data for number of subareas
                    subAreas = init_data['number_subareas'][number]
                    #button for adding subareas
                    if st.button('Subfläche hinzufügen', key = f'Button subArea{subAreas} {name}'):
                        st.session_state[f'subAreas{name}'] += 1
                    #check if "remove subfläche"-button has been hit last runthrough, in that case, display one less subarea
                    if f'remove Subfläche von {name}' in st.session_state:
                        if st.session_state[f'remove Subfläche von {name}'] == True:
                            subAreas = st.session_state[f'subAreas{name}'] -1
                        else:
                            subAreas = st.session_state[f'subAreas{name}']
                    #write number of subareas in json file
                    json_data['wall' + str(number+1)]['number_subareas'] = subAreas  
                    with open(state,'w') as jsonkey:
                        json.dump(json_data, jsonkey)     
                            
                    for num in range(0, subAreas):
                        #write corresponding data for subareas into json file 
                        json_data['wall' + str(number+1)]['subarea' + str(num+1)] = {}
                        json_data['wall' + str(number+1)]['subarea' + str(num+1)]['area'] = init_data['sub_area'][number][num+1]
                        cat = list(material_dict.keys())[init_data['sub_category'][number][num+1]]
                        json_data['wall' + str(number+1)]['subarea' + str(num+1)]['category'] = cat
                        json_data['wall' + str(number+1)]['subarea' + str(num+1)]['material'] = list(material_dict[f'{cat}'].keys())[init_data['sub_material'][number][num+1]]

                        with open(state,'w') as jsonkey:
                            json.dump(json_data, jsonkey)   
                        #input for area for each subarea
                        with col_1:
                            sub_surfaces[name].append(st.number_input(f"Fläche für Subfläche {num +1 }",
                                                                    value=init_data['sub_area'][number][num] , key = f'Fläche subArea{num} {name}',min_value=0, max_value=int((main_surfaces[name] - sum(sub_surfaces[name])))))
                        #input for category for each subarea
                        with col_2:
                            category = st.selectbox(label='Bitte wählen Sie die Kategorie des Materials aus',
                                                     options=material_dict.keys(), key= f'cat_sub_{name}{num}', index = init_data['sub_category'][number][num])
                        #input for material for each subarea
                        with col_3:
                            sub_materials[name].append(st.selectbox(label =  f'Bitte wählen Sie das Material der Subfläche {num + 1} aus.'
                               ,options=material_dict[f'{category}'].keys(), key=f'Subfläche {num} von {name}', index = init_data['sub_material'][number][num]))

                        #for every subarea, write area, category and material in json
                        json_data['wall' + str(number+1)]['subarea' + str(num+1)]['area'] = sub_surfaces[name][num]
                        json_data['wall' + str(number+1)]['subarea' + str(num+1)]['category'] = category
                        json_data['wall' + str(number+1)]['subarea' + str(num+1)]['material'] = sub_materials[name][num]
                        with open(state,'w') as jsonkey:
                            json.dump(json_data, jsonkey)     

                    #removal button for subareas           
                    if st.button('Subfläche entfernen', key=f'remove Subfläche von {name}') and len(sub_materials[name]) > 0:
                        if st.session_state[f'subAreas{name}'] > 0:
                            st.session_state[f'subAreas{name}'] -= 1
                            sub_materials[name].pop()
                            sub_surfaces[name].pop()
                            json_data['wall' + str(number+1)].pop('subarea' + str(subAreas+1))
                    #sync number of subareas with json file
                    json_data['wall' + str(number+1)]['number_subareas'] = st.session_state[f'subAreas{name}']
                    with open(state,'w') as jsonkey:
                        json.dump(json_data, jsonkey)  
    

    #Initialisierung des Dictionaries für die Absorptionsgrade
    alpha = basic_dict_2()

with st.container():
    col_1, col_2 = st.columns(2)
    with col_1:
        #create a save as button that unlocks a text input space
        if "save_as_name" not in st.session_state:
            st.session_state["save_as_name"] = ""

        if "save_as" not in st.session_state:
            st.session_state["save_as"] = False

        if st.button("Speichern"):
            st.session_state["save_as"] = not st.session_state["save_as"]

        key_file_name_save = " "

        if st.session_state["save_as"]:
            #space to input file name
            save_as_file_name = st.text_input("Dateiname", key=key_file_name_save)
            st.session_state["save_as_name"] = st.session_state[key_file_name_save]
            #saves the json file as the input file name
            if st.button("Speichern"):
                name = st.session_state[key_file_name_save]
                st.write(save_as_file_name + "Session wurde gespeichert" )               #should prolly only display if save was successful, should disappear after a while
                with open(name + ".json", "w") as file:
                    with open(state, "r") as open_json:
                        file.write(open_json.read())

    with col_2:
        #create an open file button that unlocks a text input space
        if "open_file_name" not in st.session_state:
            st.session_state["open_file_name"] = ""

        if "open_file" not in st.session_state:
            st.session_state["open_file"] = False

        if st.button("Datei öffnen"):
            st.session_state["open_file"] = not st.session_state["open_file"]

        key_file_name_open = ""
        if st.session_state["open_file"]:
            #space to input file name
            save_as_file_name = st.text_input("file name (if file doesn't load properly, try refreshing the page)", key=key_file_name_open)
            st.session_state["open_file_name"] = st.session_state[key_file_name_open]
            #put the contents of the opened file in current session json and relaod page
            if st.button("open"):
                name = st.session_state[key_file_name_open]
                #save contents of file in session file
                with open(name + ".json", "r") as file:                 #needs an exception if file does not exist
                    with open(state, "w") as open_json:
                        open_json.write(file.read())
                st.experimental_rerun()


#Befuellen des dicts mit den Absorptionsgeraden fuer die jeweiligen Oktavbaender und 
for ind, octaveBand in enumerate(alpha):
    for material in main_materials:
        try:
            alpha[octaveBand].append(material_dict_flattened[material][ind])
        except:
            alpha[octaveBand].append(None)
            print('Appended None')
walls = [i for i in st.session_state.main_walls if 'Personen' not in i]

sub_alpha = sub_alpha_dict(walls)

for ind, octaveBand in enumerate(sub_alpha):
    for wall in sub_alpha[octaveBand]:
            for material in sub_materials[wall]:
                sub_alpha[octaveBand][wall].append(material_dict_flattened[material][ind])

#Erstellen des Objektes Raum der Klasse room
raum = room(volume=vol, surface=main_surfaces, sub_surface=sub_surfaces, alpha=alpha, 
            sub_alpha=sub_alpha, use=use, peopleDescription=peopleDescription, numberOfPeople=numberOfPeople)
#Plots erstellen
fileObj = open('raum.obj', 'wb')
pickle.dump(raum, fileObj)
fileObj.close()

st.divider()
st.subheader('Ergebnisse')
st.divider()
tab1, tab2 = st.tabs(['Nachhallzeit', 'Nachhallzeitenvergleich'])

with tab1:
    
    fig_reverberationTime = raum.plot_reverberationTime()
    st.plotly_chart(fig_reverberationTime)

with tab2:
    fig_reverberationTime_ratio = raum.plot_reverberationTime_ratio()
    st.plotly_chart(fig_reverberationTime_ratio)

#Exporting the results as PDF with pdfprotocol class and download the pdf
st.divider()
st.subheader('Exportieren der Ergebnisse als PDF')

#creating the pdf
#reading the variables out of the json file 
json_file = open(state)
variables = json.load(json_file)
json_file.close()

pdf1 = pdfprotocol(state, variables, fig_reverberationTime ,fig_reverberationTime_ratio)
if st.button('Erstellen der PDF'):
    st.write('PDF wird erstellt, sobald der Download verfügbar ist erscheint eine "Download PDF" Schaltfläche.')
    pdf1.protocol()
    with open("pdf_test.pdf", "rb") as pdf_file:
        PDFbyte = pdf_file.read()
    st.download_button('Download PDF', PDFbyte, 'Raumakustikprotokoll.pdf')


