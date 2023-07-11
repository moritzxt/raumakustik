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
        #if 'main_walls' in st.session_state:
            number_walls_init = json_data['number_walls']
            #number_walls_init = len(st.session_state.main_walls)
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

            #     for j in range(len(material_dict.keys())):
            #         if list(material_dict.keys())[j] == json_data['wall' + str(i+1)]['category']:
            #             category_init.append(j)

            #     for j in range(len(category_init)):
            #         for k in range(len(list(material_dict[f'{category_init_string[j]}'].keys()))): 
            #             if list(material_dict[f'{category_init_string[j]}'].keys())[k] == json_data['wall' + str(i+1)]['material']:   #what happens when key aint found? material_dict[f'{category}'].keys()
            #                 material_init.append(k)

            #     for j in range(number_subareas_init[i]):
            #         subarea_category_init_string[i].append(json_data['wall' + str(i+1)]['subarea' + str(j+1)]['category'])
            #         subarea_area_init[i].append(json_data['wall' + str(i+1)]['subarea' + str(j+1)]['area'])
            #         for n in range(len(material_dict.keys())):
            #             if list(material_dict.keys())[n] == json_data['wall' + str(i+1)]['subarea' + str(j+1)]['category']:
            #                 subarea_category_init[i].append(n)
            #         for l in range(len(subarea_category_init[i])):
            #             for k in range(len(list(material_dict[f'{subarea_category_init_string[i][l]}'].keys()))):
            #                 if list(material_dict[f'{subarea_category_init_string[i][l]}'].keys())[k] == json_data['wall' + str(i+1)]['subarea' + str(j+1)]['material']:
            #                     subarea_material_init[i].append(k)
        else:
            number_walls_init = 1
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
            category_init.append(0)
            category_init_string.append(list(material_dict)[0])
            material_init_string.append(list(material_dict)[0])
            material_init.append(0)
            number_subareas_init.append(0)
            subarea_area_init.append([])
            subarea_category_init.append([])
            subarea_material_init.append([])
            for j in range(100):
                subarea_area_init[i].append(1)
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
    #used to sync the session states to json file
    with open(state) as jsonkey:
        json_data = json.load(jsonkey)
    json_data['usecase'] = st.session_state['usecase']
    json_data['volume'] = st.session_state['volume']
    with open(state,'w') as jsonkey:
        json.dump(json_data, jsonkey)

def load_session(state):
    #st.session_state.main_walls = ['Wando', 'Wand 1', 'Wanda']
    #used to set necessary session states to starting values
    #read contents of session file
    with open(state) as jsonkey:
        json_data = json.load(jsonkey)
    #set session states to file content
    for keys in json_data:
        st.session_state[keys] = json_data[keys]
    for number in range(1,100):
        #if not st.session_state.main_walls[number-1] == 'Personen': 
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
                #    ind = st.session_state.main_walls.index(name)
                if len(st.session_state.main_walls) >= number:
                    st.session_state.main_walls[number-1] = name
                else:
                    st.session_state.main_walls.append(name)
            st.session_state[f'subAreas{name}'] = json_data['wall' + str(number)]['number_subareas']
    #    if f'person_type{number+1}' in json_data:
    #        st.session_state[f'people{number}'] = json_data['person_type' + str(number+1)]['amount']
    if 'persons' in json_data:
        st.session_state['personen'] = json_data['persons']
    if 'number_people' in json_data:
        st.session_state['add_persons'] = json_data['number_people']

def negate_checkbox(json_data, state):
    #used so that persons checkbox works properly
    json_data['persons'] = not json_data['persons']
    with open(state,'w') as jsonkey:
        json.dump(json_data, jsonkey)

def write_json(json_data,state,num):
    #used so that person inputs work properly with json
    json_data['person_type' + str(num+1)]['amount'] = st.session_state[f'people{num}']
    with open(state,'w') as jsonkey:
        json.dump(json_data, jsonkey)

# def subArea_subst(name):
#     st.session_state[f'subAreas{name}'] -= 1