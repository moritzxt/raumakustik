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

main_walls = [element for element in st.session_state['main_walls'] if element != 'Personen']

def slider_for_surface(raum_fine,wall,sub_materials, key = 1):
        main_walls = [element for element in st.session_state['main_walls'] if element != 'Personen']

        max_area = int(raum_fine.surface[wall] -
                sum(raum_fine.sub_surface[wall]))
        raum_fine.sub_surface[wall][sub_wall_ind] = st.slider(
            label='Fläche der Subwandfläche', min_value=0, max_value=max_area, key=f'SubAreaSlider{sub_wall_ind}{key}', step=1)
        sub_wall_material = sub_materials[f'{wall}'][sub_wall_ind]
        st.write(sub_wall_material)
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
    sub_wall_list = [f'Subfläche {i+1}' for i in range(sub_surface_count)]
    sub_wall = st.selectbox(
        'Wähle die Subfläche aus', options=sub_wall_list)
    sub_wall_ind = sub_wall_list.index(sub_wall)

# with col3:
#     max_area = float(raum_fine.surface[wall] -
#                      sum(raum_fine.sub_surface[wall]))
#     raum_fine.sub_surface[wall][sub_wall_ind] = st.slider(
#         label='Fläche der Subwandfläche', min_value=.0, max_value=max_area, key=f'SubAreaSlider{sub_wall_ind}', step=0.1)
#     sub_wall_material = sub_materials[wall][sub_wall_ind]
#     st.write(sub_wall_material)

tab1, tab2 = st.tabs(['Nachhallzeit', 'Vergleich der Nachhallzeit'])

with tab1:
    col_1, col_2 = st.columns(2)

    with col_2:
        area = slider_for_surface(raum_fine,wall, sub_materials, key=sub_wall_ind,)
    with col_1:
        fig1 = raum_fine.plot_reverberationTime()
        st.plotly_chart(fig1)

with tab2:

    col_1, col_2 = st.columns(2)

    with col_2:
        area = slider_for_surface(raum_fine, wall, sub_materials, key = f'{sub_wall_ind + 1}')
    with col_1:
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