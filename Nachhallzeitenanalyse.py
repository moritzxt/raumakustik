
import pickle
import streamlit as st
#import streamlit_tags as sttags
from room_calc import room
from utils import read_db, basic_dict_list, usecase, sub_alpha_dict, flatten_dict
import os
import glob
import json
from streamlit.runtime.scriptrunner.script_run_context import add_script_run_ctx
from session_utils import *
from pdf_protocol import pdfprotocol
from datetime import datetime
import zipfile

# Retreive date for file export
today = datetime.today().strftime('%Y%m%d')

# Setup of page data:
st.set_page_config(page_title= 'Tool für Raumakustik', layout='wide',
                    initial_sidebar_state='collapsed')



# Initializing parameters
tabs_list = []
main_surfaces = {} 
main_materials = [] 
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
    # Creating list for main_walls in current session, so it can be updated by add button
    st.session_state.main_walls = [default_area]

# Create a json file with session id as file name
state = add_script_run_ctx().streamlit_script_run_ctx.session_id +'.json'
state = './session/' + state  
write_session_file(state)

# Load the last session into session json file
load_session_file(state)

# Write current session id in session_key.json
session = add_script_run_ctx().streamlit_script_run_ctx.session_id
write_session_key(session)

# Load data from current session
with open(state) as jsonkey:
    json_data = json.load(jsonkey)
    jsonkey.close()

load_session(state)
#read starting positions of input elements from last session... 
#init_data = init_starting_values(json_data,material_dict,person_dict)

# #create a json file with session id as file name
# state = add_script_run_ctx().streamlit_script_run_ctx.session_id +'.json'
# write_session_file(state)

# Load the last session into session json file
load_session_file(state)

# Write current session id in session_key.json
session = add_script_run_ctx().streamlit_script_run_ctx.session_id
write_session_key(session)

# Load data from current session
with open(state) as jsonkey:
    json_data = json.load(jsonkey)
    jsonkey.close()

load_session(state)
# Read starting positions of input elements from last session... 
init_data = init_starting_values(json_data,material_dict,person_dict)

with st.container():
    st.title('Web-app für Nachhallzeitenanalyse')
    st.divider()
    old_session = None
    old_session = st.file_uploader('Session-Datei hochladen', help = 'Lade eine ".json" Datei von einer bestehenden Session hoch.', )
    if old_session != None:
        upload_session_file(old_session, state)
        init_data = init_starting_values(json_data,material_dict,person_dict)
        if st.button('Session aktualisieren'):
            st.experimental_rerun()
    st.divider()

        #st.experimental_rerun()


    st.divider()
    st.header('Eingabeparameter')
    
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        # Selection of usecase
        use = st.selectbox('Nutzungsart nach DIN 18041', options=usecase.keys(), index=init_data['usecase_index'],)
        # On change save current usecase into json
        json_data['usecase'] = use
        with open(state,'w') as jsonkey:
            json.dump(json_data, jsonkey)
            jsonkey.close()

        # Set boundaries of volume for usecase
        min_lim =  min(usecase[use])
        max_lim =  max(usecase[use])

        if 'volume' not in st.session_state:
            st.session_state['volume'] = init_data['volume']
        # Check if initial values are in limits and replace them if they aren't
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
        # Input of volume
        vol = st.number_input('Volumen in m³', min_value=min_lim,
                            max_value=max_lim,  key='volume', on_change = sync_session, kwargs ={"state": state})
        # Save current volume in json
        json_data['volume'] = vol
        with open(state,'w') as jsonkey:
            json.dump(json_data, jsonkey)
            jsonkey.close()

        
    with col3:
        # Input for name of next wall that is being added
        wall_name = st.text_input('Name der Wandfläche', value='Wand 1')

        # Check if wall name exists already, if yes, tell user
        if st.button('Hinzufügen'):
            if wall_name in st.session_state.main_walls:
                st.write("Diese Grundfläche existiert bereits")
            else:
            # If not, create new wall
                if default_area in st.session_state.main_walls:
                    st.session_state.main_walls = [wall_name]
                else:
                    st.session_state.main_walls.append(wall_name)
        if st.button('Entfernen', help= 'Geben Sie den Namen der Grundfläche ein, die Sie entfernen möchten.'):
            if wall_name in st.session_state.main_walls and len(st.session_state.main_walls) > 1:
                ind = st.session_state.main_walls.index(wall_name)
                # Removing specific Mainwall
                st.session_state.main_walls.pop(ind)
                json_data.pop('wall' + str(ind+1))
        # Save amount of walls in json file
        if 'Personen' in st.session_state.main_walls:
            json_data['number_walls'] = len(st.session_state.main_walls)-1
        else:
            json_data['number_walls'] = len(st.session_state.main_walls)
        with open(state,'w') as jsonkey:
            json.dump(json_data, jsonkey)
            jsonkey.close()
        

    with col4:
        st.empty()
        # Setup json key
        json_data['persons'] = init_data['persons']
        # Checkbox if persons are displayed or not
        if st.checkbox(label='Personen', key='personen', label_visibility='visible', on_change = negate_checkbox, kwargs = {"json_data": json_data, "state": state}):
            tabs_list = ['Personen']
            if 'Personen' not in st.session_state.main_walls:
                # Check if Personen already exist, otherwise there are more personen tabs
                st.session_state.main_walls.insert(0, 'Personen')
        else:
            if 'Personen' in st.session_state.main_walls:
                # Delete Personstab if it is deactivated
                st.session_state.main_walls.pop(0)

subAreas = 0

numPeople = init_data['number_people']

for key in st.session_state.main_walls:
     if not key == 'Personen':
        # Making sure, that Person is no key for the lists    
        sub_surfaces[key] = []
        sub_materials[key] = []
        main_surfaces[key] = 0

tabs = st.tabs(st.session_state.main_walls)


# Tabs for main walls and people in the room 

for tab, name in zip(tabs, st.session_state.main_walls):

    with tab:
        if name == 'Personen':
            col_11, col_12 = st.columns(2)

            # Setup number of person types for first runthrough
            if 'add_persons' not in st.session_state:
                st.session_state['add_persons'] = numPeople
            # Button to add more person types
            if st.button('Personengruppe hinzufügen', key ='button_add_persons'):
                st.session_state['add_persons'] += 1

            # If person type has been removed on last runthrough, display one less
            if 'remove_button_persons' in st.session_state:
                if st.session_state.remove_button_persons == True:
                    numPeople = st.session_state.add_persons-1
                else:
                    numPeople = st.session_state['add_persons']
            # Put number of person types into json
            json_data['number_people'] = numPeople
            for i in range(numPeople):
                if 'person_type' + str(i+1) not in json_data:
                    json_data['person_type' + str(i+1)] = {}
            with open(state,'w') as jsonkey:
                json.dump(json_data, jsonkey)
                jsonkey.close()

            for num in range(0, numPeople):
                    #Input of amount of persons per person type
                    with col_11:
                        numberOfPeople.append(st.number_input(
                                f"Anzahl der Personen", step = 1, key = f'people{num}', value=init_data['amount'][num], on_change = write_json, kwargs = {"json_data": json_data, "state": state, "num":num}))
                        
                    # Put amount of people of type in json file
                    json_data['person_type' + str(num+1)]['amount'] = numberOfPeople[num]
                    #input of the type description of person 
                    with col_12:
                        peopleDescription.append(st.selectbox(label =  f'Beschreibung',
                                                            key=f'Beschreibung{num}',options=person_dict.keys(), index = init_data['type'][num])) 
                        
                    # Put type description into json file
                    json_data['person_type' + str(num+1)]['type'] = peopleDescription[num]
                    with open(state,'w') as jsonkey:
                        json.dump(json_data, jsonkey)
                        jsonkey.close()

                    
            # Removal button for person types
            if st.button('Personengruppe entfernen', key='remove_button_persons'):
                if st.session_state['add_persons'] > 1 and len(peopleDescription) > 0:
                    st.session_state['add_persons'] -= 1
                    peopleDescription.pop()
                    numberOfPeople.pop()
                    json_data.pop('person_type' + str(st.session_state.add_persons+1)) #funktioniert das?
                    # Sync amount of person types with json file
                    json_data['number_people'] = st.session_state[f'add_persons']
                    with open(state,'w') as jsonkey:
                        json.dump(json_data, jsonkey)  
                        jsonkey.close()
     

        else:
                # Extract number of base area (differently if persons is ticked or not)
                if 'Personen' in st.session_state.main_walls:
                    number = st.session_state.main_walls.index(name)-1
                else:
                    number = st.session_state.main_walls.index(name)

                if 'wall'+str(number+1) not in json_data:
                    json_data['wall' + str(number+1)] = {}
                # Put name of wall into json file
                json_data['wall' + str(number+1)]['name'] = name
                with open(state,'w') as jsonkey:
                    json.dump(json_data, jsonkey)
                    jsonkey.close()


                if f'subAreas{name}' not in st.session_state:
                    st.session_state[f'subAreas{name}'] = init_data['number_subareas'][number]
                con_1 = st.container()
                con_2 = st.container()

                with con_1:
                    col_1, col_2, col_3 = st.columns(3)
                    # Area for every subarea
                    with col_1:
                        main_surfaces[name] = (st.number_input(
                            f"Fläche für {name}", value=init_data['area'][number], min_value=0))
                    # Category for each subarea
                    with col_2:
                        category = st.selectbox(label='Materialkategorie',
                                                key=f'{name}' ,options=material_dict.keys(), index=init_data['category'][number])
                    # Material for every subarea
                    with col_3:
                        main_materials.append(st.selectbox(label =  f'Material von {name}',
                                                        options=material_dict[f'{category}'].keys(), index=init_data['material'][number]))

                    # Save currenty wall area, category and type in json
                    json_data['wall' + str(number+1)]['area'] = main_surfaces[name]
                    json_data['wall' + str(number+1)]['category'] = st.session_state[f'{name}']
                    json_data['wall' + str(number+1)]['material'] = main_materials[number]
                    with open(state,'w') as jsonkey:
                        json.dump(json_data, jsonkey)
                        jsonkey.close()
                

                with con_2:
                    st.divider()
                    col_1, col_2, col_3 = st.columns(3)

                    # Get initial data for number of subareas
                    subAreas = init_data['number_subareas'][number]
                    # Button for adding subareas
                    if st.button('Subfläche hinzufügen', key = f'Button subArea{subAreas} {name}'):
                        st.session_state[f'subAreas{name}'] += 1
                    # Check if "remove subfläche"-button has been hit last runthrough, in that case, display one less subarea
                    if f'remove Subfläche von {name}' in st.session_state:
                        if st.session_state[f'remove Subfläche von {name}'] == True:
                            subAreas = st.session_state[f'subAreas{name}'] -1
                        else:
                            subAreas = st.session_state[f'subAreas{name}']
                    # Write number of subareas in json file
                    json_data['wall' + str(number+1)]['number_subareas'] = subAreas  
                    with open(state,'w') as jsonkey:
                        json.dump(json_data, jsonkey)     
                        jsonkey.close()
                            
                    for num in range(0, subAreas):
                        # Write corresponding data for subareas into json file 
                        json_data['wall' + str(number+1)]['subarea' + str(num+1)] = {}
                        json_data['wall' + str(number+1)]['subarea' + str(num+1)]['area'] = init_data['sub_area'][number][num+1]
                        cat = list(material_dict.keys())[init_data['sub_category'][number][num+1]]
                        json_data['wall' + str(number+1)]['subarea' + str(num+1)]['category'] = cat
                        json_data['wall' + str(number+1)]['subarea' + str(num+1)]['material'] = list(material_dict[f'{cat}'].keys())[init_data['sub_material'][number][num+1]]

                        with open(state,'w') as jsonkey:
                            json.dump(json_data, jsonkey)   
                            jsonkey.close()
                        # Input for area for each subarea
                        with col_1:
                            sub_surfaces[name].append(st.number_input(f"Fläche für Subfläche {num +1 }",
                                                                    value=init_data['sub_area'][number][num] , key = f'Fläche subArea{num} {name}',min_value=0, max_value=int((main_surfaces[name] - sum(sub_surfaces[name])))))
                        # Input for category for each subarea
                        with col_2:
                            category = st.selectbox(label='Bitte wählen Sie die Kategorie des Materials aus',
                                                     options=material_dict.keys(), key= f'cat_sub_{name}{num}', index = init_data['sub_category'][number][num])
                        # Input for material for each subarea
                        with col_3:
                            sub_materials[name].append(st.selectbox(label =  f'Bitte wählen Sie das Material der Subfläche {num + 1} aus.'
                               ,options=material_dict[f'{category}'].keys(), key=f'Subfläche {num} von {name}', index = init_data['sub_material'][number][num]))

                        # For every subarea, write area, category and material in json
                        json_data['wall' + str(number+1)]['subarea' + str(num+1)]['area'] = sub_surfaces[name][num]
                        json_data['wall' + str(number+1)]['subarea' + str(num+1)]['category'] = category
                        json_data['wall' + str(number+1)]['subarea' + str(num+1)]['material'] = sub_materials[name][num]
                        with open(state,'w') as jsonkey:
                            json.dump(json_data, jsonkey)    
                            jsonkey.close() 

                    # Removal button for subareas           
                    if st.button('Subfläche entfernen', key=f'remove Subfläche von {name}') and len(sub_materials[name]) > 0:
                        if st.session_state[f'subAreas{name}'] > 0:
                            st.session_state[f'subAreas{name}'] -= 1
                            sub_materials[name].pop()
                            sub_surfaces[name].pop()
                            json_data['wall' + str(number+1)].pop('subarea' + str(subAreas+1))
                    # Sync number of subareas with json file
                    json_data['wall' + str(number+1)]['number_subareas'] = st.session_state[f'subAreas{name}']
                    with open(state,'w') as jsonkey:
                        json.dump(json_data, jsonkey)  
                        jsonkey.close()
    

    # Initializing the absorption coefficient dictionary
    alpha = basic_dict_list()


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

# Erstellen des Objektes Raum der Klasse room
raum = room(volume=vol, surface=main_surfaces, sub_surface=sub_surfaces, alpha=alpha, 
            sub_alpha=sub_alpha, use=use, peopleDescription=peopleDescription, numberOfPeople=numberOfPeople)
# Plots erstellen
fileObj = open('raum.obj', 'wb')
pickle.dump(raum, fileObj)
fileObj.close()

st.divider()
st.subheader('Ergebnisse')
# st.divider()
tab1, tab2 = st.tabs(['Nachhallzeit', 'Nachhallzeitenvergleich'])

with tab1:
    
    fig_reverberationTime = raum.plot_reverberationTime()
    st.plotly_chart(fig_reverberationTime)

with tab2:
    fig_reverberationTime_ratio = raum.plot_reverberationTime_ratio()
    st.plotly_chart(fig_reverberationTime_ratio)

# Exporting the results as PDF with pdfprotocol class and download the pdf
st.divider()
st.subheader('Exportieren der Ergebnisse als PDF')

# Creating the pdf
# Reading the variables out of the json file 
json_file = open(state)
variables = json.load(json_file)
json_file.close()

pdf1 = pdfprotocol(state, variables, fig_reverberationTime ,fig_reverberationTime_ratio)

if st.button('Erstellen der PDF und der Session-Datei'):
    st.caption('Dateien werden erstellt...')
    pdf1.protocol()

    with open("pdf_test.pdf", "rb") as pdf_file:
        PDFbyte = pdf_file.read()
        pdf_file.close()

    with open(state, 'rb') as json_dict:
        session_json = json_dict.read()
        json_dict.close()

    # Save PDF byte content to a file
    with open("pdf_test.pdf", "wb") as pdf_file:
        pdf_file.write(PDFbyte)

    # Save session file
    with open(state, 'wb') as json_file:
        json_file.write(session_json)

    # Create a zip file
    with zipfile.ZipFile("files.zip", "w") as zip_file:
        # Add the PDF to the zip file
        zip_file.write("pdf_protocol.pdf", f"Protokoll_Nachhallzeitanalyse_{today}.pdf")
        # Add the session file to the zip file
        zip_file.write(state, f"Session_Datei_{today}.json")

    # Read the contents of the zip file
    with open("files.zip", "rb") as zip_file:
        zip_content = zip_file.read()

    # Provide the zip file as a download button
    st.download_button('Download', zip_content, f'Ergebnisse_Nachhallzeitenanalyse_{today}.zip')

if st.button('Neue Session starten'):
    json_file_list = glob.glob('./session/*.json')
    json_data = {}
    st.cache_data.clear()
    for file in json_file_list:
        os.remove(file)
    init_data = init_starting_values(json_data,material_dict,person_dict)
