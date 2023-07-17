import streamlit as st
import json
import pickle
from streamlit.runtime.scriptrunner.script_run_context import add_script_run_ctx
from session_utils import *

def subwall_variables(json_data, index, subindex):
    '''
    Returns the variables for a specific subwall given by the index

    :param json_data: Session file
    :type json_data: dict

    :param index: Index of the main wall on which the subwall lies
    :type index: int

    :param subindex: Index of the subwall for which the subwall variables shall be retreived
    :type subindex: int

    :rturn area: Area of the subwall
    :rtype area: float

    :rturn category: Category of the subwall
    :rtype category: str

    :rturn material: Material of the subwall
    :rtype material: str
    '''
    area = json_data[f'wall{index + 1}'][f'subarea{subindex + 1}']['area']
    category = json_data[f'wall{index + 1}'][f'subarea{subindex + 1}']['category']
    material = json_data[f'wall{index + 1}'][f'subarea{subindex + 1}']['material']

    return area, category, material

def slider_for_surface(room_feinauslegung,wall,sub_wall_ind,sub_material, key = 1):
    '''
    Returns the area, which the slider is set to 

    :param room_feinauslegung: Object of class room 
    :type room_feinauslegung: class: room 

    :param wall: Name of the main wall as set in web-app
    :type wall: str

    :param sub_wall: Name of subwall as set in web-app
    :type sub_wall: str

    :param sub_wall_ind: Index of subwall for the slider 
    :type sub_wall_ind: int

    :param sub_material: Material of the subwall, which area shall be changed with the slider
    :type sub_material: str

    :param key: Widgte key, 1 by default
    :type key: int 

    :return room_feinauslegung.sub_surface[wall][sub_wall_ind]: Area of subwall, given by the slider
    :rtype room_feinauslegung.sub_surface[wall][sub_wall_ind]: int
    '''
    max_area = float(room_feinauslegung.surface[wall] - sum(room_feinauslegung.sub_surface[wall]))
    room_feinauslegung.sub_surface[wall][sub_wall_ind] = st.slider(
        label='Fläche der Subwandfläche', min_value=0., max_value=max_area, key=f'SubAreaSlider{sub_wall_ind}{key}', step=1)
    st.write(sub_material)

    return room_feinauslegung.sub_surface[wall][sub_wall_ind]

# Initializing the room_feinauslegung object from main page of web-app
fileObj = open('raum.obj', 'rb')
room_feinauslegung = pickle.load(fileObj)
fileObj.close()

# Initializing session state 
state = add_script_run_ctx().streamlit_script_run_ctx.session_id +'.json'
state = './session/' + state  
load_session_file(state)

# Write current session id in session_key.json
session = add_script_run_ctx().streamlit_script_run_ctx.session_id
write_session_key(session)

# Load data from current session
with open(state) as jsonkey:
    json_data = json.load(jsonkey)
    jsonkey.close()

# Get list without 'Personen'
main_walls = [element for element in st.session_state['main_walls'] if element != 'Personen']
sub_walls = []
for name in main_walls:
    sub_walls.append(st.session_state[f'subAreas{name}'])

# Setup of page data
st.set_page_config(page_title='Feinauslegung', layout='wide')
with st.container():
    st.title('Feinauslegung der Nachhallzeit')
    st.text('Variieren des Flächeninhalts einer Subfläche')
    st.divider()

# Setup of page appearence 
col1, col2, col3 = st.columns(3)
with col1:
    wall = st.selectbox('Wähle die zu bearbeitende Grundfläche aus',
                        options=main_walls)
    wall_ind =  main_walls.index(wall)

with col2:
    sub_surface_count = len(room_feinauslegung.sub_surface[wall])
    sub_wall = st.selectbox(
        'Wähle die Subfläche aus', options=sub_walls)
    sub_wall_ind = sub_walls.index(sub_wall)
    sub_material = subwall_variables(json_data, wall_ind, sub_wall_ind)[2]

with col1:
    area = slider_for_surface(room_feinauslegung,wall,sub_wall_ind, sub_material, key=sub_wall_ind)

tab1, tab2 = st.tabs(['Nachhallzeit', 'Nachhallzeitenvergleich'])


with tab1:


    fig1 = room_feinauslegung.plot_reverberationTime()
    st.plotly_chart(fig1)

with tab2:

    fig2 = room_feinauslegung.plot_reverberationTime_ratio()
    st.plotly_chart(fig2)



state = add_script_run_ctx().streamlit_script_run_ctx.session_id +'.json'
state = './session/' + state  
load_session_file(state)

# Write current session id in session_key.json
session = add_script_run_ctx().streamlit_script_run_ctx.session_id
write_session_key(session)

# Load data from current session
with open(state) as jsonkey:
    json_data = json.load(jsonkey)
    jsonkey.close()

if st.button('Übernehmen', help = 'Übernehme die Änderung und fahre auf der Hauptseite fort'):
    json_data['wall' + str(wall_ind+1)]['subarea' + str(sub_wall_ind+1)]['area'] = area
    write_session_data_to_json(json_data, state)
    load_session(state)
