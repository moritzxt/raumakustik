import streamlit as st
import os
import json
from streamlit.runtime.scriptrunner.script_run_context import add_script_run_ctx
from utils import usecase

def write_session_file(state):
    if not os.path.isfile(state):
        #refactor all 2.WebApp.json to 2.WebApp variable
        with open(state, 'w') as init:
            json.dump({}, init)

def load_session_file(state):
    if os.path.isfile('session_key.json'):
        with open('session_key.json', 'r') as file:
            last_session_keyy = json.load(file)
            last_session_key = last_session_keyy['key']
            if os.path.isfile(last_session_key + '.json'):
                with open(last_session_key + '.json', 'r') as file:
                    last_session = json.load(file)
                    with open(state, 'w') as init:
                        json.dump(last_session, init)

def write_session_key(session):
    with open('session_key.json', 'w') as init:
        json.dump({'key': session}, init)

def init_starting_values(json_data,material_dict,person_dict):
    if not (json_data == {}):
        #for key, value in usecase:
        #    if json_data['usecase'] == 
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
        
        persons_init = json_data['persons']
        amount_init = []
        type_init = []
        type_init_string = []
        #fill amount and type data for existing people
        for i in range(persons_init):
            amount_init.append(json_data['person_type' + str(i+1)]['amount'])
            type_init_string.append(json_data['person_type' + str(i+1)]['type'])
            for j in range(len(list(person_dict))):
                if list(person_dict)[j] == json_data['person_type' + str(i+1)]['type']:   #what happens when key aint found?
                    material_init.append(j)
        #then set data to defaults for 100 next indices, to allow adding more walls - so limiting the number of walls to 100 would be smart
        for i in range(100):
            amount_init.append(1)
            type_init_string.append(list(person_dict)[0])
            type_init.append(0)
    #... if there isnt a last session, set starting positions to defaults
    else:
        usecase_init = 'Musik'
        usecase_index = 0
        volume_init = 30
        number_walls_init = 1
        area_init = []
        material_init = []
        material_init_string = []
        persons_init = False
        amount_init = []
        type_init = []
        type_init_string = []
        #material_init_string = {'Walls,hard surfaces average (brick walls, plaster, hard floors, etc.)'}
        for i in range(100):
            area_init.append(1)
            material_init_string.append(list(material_dict)[0])
            material_init.append(0)
            amount_init.append(1)
            type_init_string.append(list(person_dict)[0])
            type_init.append(0)


    init_data = dict()
    init_data['usecase'] = usecase_init
    init_data['usecase_index'] = usecase_index
    init_data['volume'] = volume_init
    init_data['number_walls'] = number_walls_init
    init_data['area'] = area_init
    init_data['material_string'] = material_init_string
    init_data['material'] = material_init
    init_data['persons'] = persons_init
    init_data['amount'] = amount_init
    init_data['type_string'] = type_init_string
    init_data['type'] = type_init

    return init_data