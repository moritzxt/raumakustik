import streamlit as st
import copy
import json
from utils import usecase
#from session_utils import load_session, add_script_run_ctx, write_json, write_session_file, load_session_file, write_session_key
from Nachhallzeitenanalyse import sub_materials
import pickle
from streamlit.runtime.scriptrunner.script_run_context import add_script_run_ctx
from session_utils import write_session_file, load_session_file, write_session_key, sync_session, write_json, write_session_data_to_json, load_session
fileObj = open('raum.obj', 'rb')
raum_fine = pickle.load(fileObj)
fileObj.close()

state = add_script_run_ctx().streamlit_script_run_ctx.session_id +'.json'
state = './session/' + state  
load_session_file(state)

#write current session id in session_key.json
session = add_script_run_ctx().streamlit_script_run_ctx.session_id
write_session_key(session)

#load data from current session
with open(state) as jsonkey:
    json_data = json.load(jsonkey)
    jsonkey.close()


main_walls = [element for element in st.session_state['main_walls'] if element != 'Personen']
sub_walls = []
for name in main_walls:
    sub_walls.append(st.session_state[f'subAreas{name}'])

def subwall_variables(json_data, index, subindex):
    '''
    Function to read variables of subwalls
    '''
    area = json_data[f'wall{index + 1}'][f'subarea{subindex + 1}']['area']
    category = json_data[f'wall{index + 1}'][f'subarea{subindex + 1}']['category']
    material = json_data[f'wall{index + 1}'][f'subarea{subindex + 1}']['material']

    return area, category, material

def slider_for_surface(raum_fine,wall,sub_wall_ind,sub_material, key = 1):

        max_area = int(raum_fine.surface[wall] - sum(raum_fine.sub_surface[wall]))
        raum_fine.sub_surface[wall][sub_wall_ind] = st.slider(
            label='Fläche der Subwandfläche', min_value=0, max_value=max_area, key=f'SubAreaSlider{sub_wall_ind}{key}', step=1)
        st.write(sub_material)
        return raum_fine.sub_surface[wall][sub_wall_ind]

st.set_page_config(page_title='Feinauslegung', layout='wide')
with st.container():
    st.title('Tool für die Feinauslegung einer Wandfläche Raums')
    st.text('Variieren der Fläche einer Subfläche')
    st.divider()

col1, col2, col3 = st.columns(3)
with col1:
    wall = st.selectbox('Wähle die zu bearbeitende Hauptfläche aus',
                        options=main_walls)
    wall_ind =  main_walls.index(wall)



with col2:
    sub_surface_count = len(raum_fine.sub_surface[wall])
    sub_wall = st.selectbox(
        'Wähle die Subfläche aus', options=sub_walls)
    sub_wall_ind = sub_walls.index(sub_wall)
    sub_material = subwall_variables(json_data, wall_ind, sub_wall_ind)[2]

with col1:
    area = slider_for_surface(raum_fine,wall,sub_wall_ind, sub_material, key=sub_wall_ind)


tab1, tab2 = st.tabs(['Nachhallzeit', 'Vergleich der Nachhallzeit'])

with tab1:
    fig1 = raum_fine.plot_reverberationTime()
    st.plotly_chart(fig1)

with tab2:
    fig2 = raum_fine.plot_reverberationTime_ratio()
    st.plotly_chart(fig2)



state = add_script_run_ctx().streamlit_script_run_ctx.session_id +'.json'
state = './session/' + state  
load_session_file(state)

#write current session id in session_key.json
session = add_script_run_ctx().streamlit_script_run_ctx.session_id
write_session_key(session)

#load data from current session
with open(state) as jsonkey:
    json_data = json.load(jsonkey)
    jsonkey.close()

#area = self.load_variables()['wall' + f'{index + 1}']['subarea' + f'{subindex + 1}']['area']
if st.button('Übernehmen', help = 'Übernehme die Änderung und fahre auf der Hauptseite fort'):
    json_data['wall' + str(wall_ind+1)]['subarea' + str(sub_wall_ind+1)]['area'] = area
    write_session_data_to_json(json_data, state)
    #load_session_file(state)
    load_session(state)
