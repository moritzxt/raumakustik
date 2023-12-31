import streamlit as st
import os
import json
from streamlit.runtime.scriptrunner.script_run_context import add_script_run_ctx
from utils import usecase

def get_current_session_key():
    '''
    Gets current session_key to update current session

    :return: The session_key
    :rtype: str

    '''
    if os.path.isfile('session_key.json'):
        with open('session_key.json', 'r') as file:
            dict_file = json.load(file)
            session_key = dict_file['key']
            file.close()
    return session_key

def upload_file(file):
    '''
    Writes uploaded json file from upload button to current session state

    :param file: User uploaded json file 
    :type file: json 
    '''
    session_key = get_current_session_key()
    with open(f'session/{session_key}.json','w') as session:                 #needs an exception if file does not exist
        json_dict = json.load(file)
        json.dump(json_dict, session)
        session.close()
        st.experimental_rerun()




def write_session_file(state):
    """
    Dumps session state into json file.
    
    :param state: name of json file of current session (name of current session + '.json')
    :type state: str
    """
    if not os.path.isfile(state):
        #refactor all 2.WebApp.json to 2.WebApp variable
        with open(state, 'w') as init:
            json.dump({}, init)
            init.close()

def load_session_file(state):
    """
    Loads session state from json file.
    
    :param state: name of json file of current session (name of current session + '.json')
    :type state: str
    """
    if os.path.isfile('session_key.json'):
        with open('session_key.json', 'r') as file:
            last_session_keyy = json.load(file)
            last_session_key = last_session_keyy['key']
            file.close()
            if os.path.isfile(last_session_key + '.json'):
                with open(last_session_key + '.json', 'r') as file:
                    last_session = json.load(file)
                    file.close()
                    with open(state, 'w') as init:
                        json.dump(last_session, init)
                        init.close()


def write_session_key(session):
    """
    Dumps session key as json file.

    :param session: name of current session
    :type session: str
    """
    with open('session_key.json', 'w') as init:
        json.dump({'key': session}, init)
        init.close()

def init_starting_values(json_data,material_dict,person_dict):
    """
    Returns init data. If no values are set for the specific key, the corresponding value is set to its default.

    :param json_data: copy of contents of json file of current session as variable, for use in code and modifying of file data 
    :type json data: dict of str: int or float or str or dict of str: int or float or str 
        
    :param material_dict: dictionary with all the absorption materials as keys and their respective absorption coefficients over octave bands
    :type material_dict: dict of str: list of float
        
    :param person_dict: dictionary with all the person types from DIN as keys and their respective absorption coefficients over octave bands 
    :type person_dict: list of float

    :return: init data
    :rtype: dict of str: int or float or str or dict of str: int or float or str 

    """
    #initialize usecase init data. if it doesnt exist yet, set to default
    if 'usecase' in json_data:
        usecase_init = json_data['usecase']
        if usecase_init == 'Musik':
            usecase_index = 0
        elif usecase_init == 'Sprache/Vortrag':
            usecase_index = 1
        elif usecase_init == 'Sprache/Vortrag inklusiv':
            usecase_index = 2
        elif usecase_init == 'Unterricht/Kommunikation':
            usecase_index = 3
        elif usecase_init == 'Unterricht/Kommunikation inklusiv':
            usecase_index = 4
        elif usecase_init == 'Sport':
            usecase_index = 5
    else:
        usecase_init = 'Musik'
        usecase_index = 0
    #initialize volume init data. if it doesnt exist yet, set to default
    if 'volume' in json_data:
        volume_init = json_data['volume']
    else:
        volume_init = usecase[usecase_init]
        volume_init = volume_init[0]
    #initialize walls init data. if it doesnt exist yet, set to default
    if 'number_walls' in json_data:
        number_walls_init = json_data['number_walls']
        name_init = []
        area_init = []
        category_init = []
        category_init_string = []
        material_init = []
        material_init_string = []
        number_subareas_init = []
        subarea_area_init = []
        subarea_category_init = []
        subarea_category_init_string = []
        subarea_material_init = []
        subarea_material_init_string = []
        for wall_name in st.session_state.main_walls:
            ind = st.session_state.main_walls.index(wall_name)
            name_init.append(st.session_state.main_walls[ind])
    
        #fill area and material data for existing walls
        for i in range(number_walls_init):
            subarea_area_init.append([])
            subarea_category_init.append([])
            subarea_category_init_string.append([])
            subarea_material_init.append([])
            subarea_material_init_string.append([])
            
            area_init.append(json_data['wall' + str(i+1)]['area'])
            category_init_string.append(json_data['wall' + str(i+1)]['category'])
            material_init_string.append(json_data['wall' + str(i+1)]['material'])
            number_subareas_init.append(json_data['wall' + str(i+1)]['number_subareas'])

            for j in range(len(material_dict.keys())):
                if list(material_dict.keys())[j] == json_data['wall' + str(i+1)]['category']:
                    category_init.append(j)

            for j in range(len(category_init)):
                for k in range(len(list(material_dict[f'{category_init_string[j]}'].keys()))): 
                    if list(material_dict[f'{category_init_string[j]}'].keys())[k] == json_data['wall' + str(i+1)]['material']:   #what happens when key aint found? material_dict[f'{category}'].keys()
                        material_init.append(k)

            for j in range(number_subareas_init[i]):
                subarea_category_init_string[i].append(json_data['wall' + str(i+1)]['subarea' + str(j+1)]['category'])
                subarea_area_init[i].append(json_data['wall' + str(i+1)]['subarea' + str(j+1)]['area'])
                for n in range(len(material_dict.keys())):
                    if list(material_dict.keys())[n] == json_data['wall' + str(i+1)]['subarea' + str(j+1)]['category']:
                        subarea_category_init[i].append(n)
                for l in range(len(subarea_category_init[i])):
                    for k in range(len(list(material_dict[f'{subarea_category_init_string[i][l]}'].keys()))):
                        if list(material_dict[f'{subarea_category_init_string[i][l]}'].keys())[k] == json_data['wall' + str(i+1)]['subarea' + str(j+1)]['material']:
                            subarea_material_init[i].append(k)
    else:
        number_walls_init = 1
        name_init = []
        area_init = []
        category_init = []
        category_init_string = []
        material_init = []
        material_init_string = []
        number_subareas_init = []
        subarea_area_init = []
        subarea_category_init = []
        subarea_category_init_string = []
        subarea_material_init = []
        subarea_material_init_string = []
            
    #then set data to defaults for 100 next indices, to allow adding more walls - so limiting the number of walls to 100 would be smart
    for i in range(100):
        area_init.append(1)
        name_init = "Wand "+str(i+1)
        category_init.append(0)
        category_init_string.append(list(material_dict)[0])
        material_init_string.append(list(material_dict)[0])
        material_init.append(0)
        number_subareas_init.append(0)
        subarea_area_init.append([])
        subarea_category_init.append([])
        subarea_material_init.append([])
        for j in range(100):
            subarea_area_init[i].append(0)
            subarea_category_init[i].append(0)
            subarea_material_init[i].append(0)

    #initialize person init data. if it doesnt exist yet, set to defaults
    if 'persons' in json_data:
        persons_init = json_data['persons']
    else:
        persons_init = False
    #initialize number of person types init data. if it doesnt exist yet, set to defaults
    if 'number_people' in json_data:
        number_people_init = json_data['number_people']
    else:
        number_people_init = 0
    
    amount_init = []
    type_init = []
    type_init_string = []
    #fill amount and type data for existing people
    for i in range(number_people_init):
        amount_init.append(json_data['person_type' + str(i+1)]['amount'])
        type_init_string.append(json_data['person_type' + str(i+1)]['type'])
        for j in range(len(list(person_dict))):
            if list(person_dict)[j] == json_data['person_type' + str(i+1)]['type']:   #what happens when key aint found?
                type_init.append(j)
    #then set data to defaults for 100 next indices, to allow adding more people types - so limiting the number of people types to 100 would be smart
    for i in range(100):
        amount_init.append(1)
        type_init_string.append(list(person_dict)[0])
        type_init.append(0)

    #put all the init data into dictionary and return
    init_data = dict()
    init_data['usecase'] = usecase_init
    init_data['usecase_index'] = usecase_index
    init_data['volume'] = volume_init
    init_data['number_walls'] = number_walls_init
    init_data['name'] = name_init
    init_data['area'] = area_init
    init_data['category'] = category_init
    init_data['category_string'] = category_init_string
    init_data['material_string'] = material_init_string
    init_data['material'] = material_init
    init_data['persons'] = persons_init
    init_data['number_people'] = number_people_init
    init_data['amount'] = amount_init
    init_data['type_string'] = type_init_string
    init_data['type'] = type_init
    init_data['number_subareas'] = number_subareas_init
    init_data['sub_area'] = subarea_area_init
    init_data['sub_category'] = subarea_category_init
    init_data['sub_material'] = subarea_material_init

    return init_data

def sync_session(state):
    """
    Synchronizes session state and json file.
    
    :param state: name of json file of current session (name of current session + ".json")
    :type state: str
    """
    #used to sync the session states to json file
    with open(state) as jsonkey:
        json_data = json.load(jsonkey)
        jsonkey.close()
    json_data['usecase'] = st.session_state['usecase']
    json_data['volume'] = st.session_state['volume']
    with open(state,'w') as jsonkey:
        json.dump(json_data, jsonkey)
        jsonkey.close()

def load_session(state):
    """
    Sets necessary session states to starting values and reads contents of session file.
 
    :param state: name of json file of current session (name of current session + ".json")
    :type state: str
    """
    #used to set necessary session states to starting values
    #read contents of session file
    with open(state) as jsonkey:
        json_data = json.load(jsonkey)
        jsonkey.close()
    #set session states to file content
    for keys in json_data:
        st.session_state[keys] = json_data[keys]
    for number in range(1,100):
        if f'wall{number}' in json_data:
            name = json_data['wall'+str(number)]['name']
            #if there is a 'personen' tab, put it in tabs beginning from the second...
            if 'Personen' in st.session_state.main_walls:
                if len(st.session_state.main_walls) > number:
                    st.session_state.main_walls[number] = name
                else:
                    st.session_state.main_walls.append(name)
            #else put it in tabs beginning from the first
            else:
                if len(st.session_state.main_walls) >= number:
                    st.session_state.main_walls[number-1] = name
                else:
                    st.session_state.main_walls.append(name)
            st.session_state[f'subAreas{name}'] = json_data['wall' + str(number)]['number_subareas']
    if 'persons' in json_data:
        st.session_state['personen'] = json_data['persons']
    if 'number_people' in json_data:
        st.session_state['add_persons'] = json_data['number_people']

def negate_checkbox(json_data, state):
    """
    Negates current state of json_data['persons']. Used on change of persons checkbox to update state. 
    
    :param json_data: copy of contents of json file of current session as variable, for use in code and modifying of file data 
    :type json data: dict of str: int or float or str or dict of str: int or float or str 
        
    :param state: name of json file of current session (name of current session + ".json")
    :type state: str
    """
    #used so that persons checkbox works properly
    json_data['persons'] = not json_data['persons']
    with open(state,'w') as jsonkey:
        json.dump(json_data, jsonkey)
        jsonkey.close()

def write_json(json_data,state,num):
    """
    Formats user_input number of persons, writes it into json_data and dumps json_data as json file.
    
    :param json_data: copy of contents of json file of current session as variable, for use in code and modifying of file data 
    :type json data: dict of str: int or float or str or dict of str: int or float or str 
        
    :param state: name of json file of current session (name of current session + ".json")
    :type state: str
        
    :param num: number of persons in the room 
    :type num: int
        
    """
    #used so that person inputs work properly with json
    json_data['person_type' + str(num+1)]['amount'] = st.session_state[f'people{num}']
    with open(state,'w') as jsonkey:
        json.dump(json_data, jsonkey)
        jsonkey.close()

def write_session_data_to_json(json_data,state):
    """
    Dumps session data to json file.
    
    :param json_data: copy of contents of json file of current session as variable, for use in code and modifying of file data 
    :type json data: dict of str: int or float or str or dict of str: int or float or str 
        
    :param state: name of json file of current session (name of current session + ".json")
    :type state: str

    """
    #used so that person inputs work properly with json
    with open(state,'w') as jsonkey:
        json.dump(json_data, jsonkey)
        jsonkey.close()
