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


# Initializing the room_feinauslegung object from main page of web-app
fileObj = open('src/raum.obj', 'rb')
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
try:
    with open(state) as jsonkey:
        json_data = json.load(jsonkey)
        jsonkey.close()
        
    # Get list without 'Personen'
    main_walls = [element for element in st.session_state['main_walls'] if element != 'Personen']
    sub_walls = {}
    for name in main_walls:
        n_sub_walls = st.session_state[f'subAreas{name}']

        sub_walls[name] = [f'Subfläche {element + 1}' for element in range(0, n_sub_walls)]

    # get walls that have subwalls
    walls_with_subwalls = []
    for key in sub_walls:
        if (len(sub_walls[key]) > 0):
            walls_with_subwalls.append(key)
    # if no wall with subwalls do something
    if (len(walls_with_subwalls) < 1):
        st.error("Feinauslegung nicht möglich, da keine Subflächen definiert sind.")
    else:
        # Setup of page data
        st.set_page_config(page_title='Feinauslegung', layout='wide')
        with st.container():
            st.header('Feinauslegung der Nachhallzeit')
            st.text('Variieren des Flächeninhalts einer Subfläche')
            st.divider()
        
        # Setup of page appearence 
        col1, col2, col3 = st.columns(3)
        with col1:
            # Selecting mainwall
            wall = st.selectbox('Wähle die zu bearbeitende Grundfläche aus',
                                options=walls_with_subwalls)
            # Index for main wall for lists
            wall_ind =  main_walls.index(wall)
        
        with col2:
            tabs = st.tabs(sub_walls[wall])
            for tab, name in zip(tabs, sub_walls[wall]):
                with tab:

                    sub_wall_ind = sub_walls[wall].index(name)
                    max_area = float(room_feinauslegung.surface[wall] - sum(room_feinauslegung.sub_surface[wall]))
                    max_area = max_area + room_feinauslegung.sub_surface[wall][sub_wall_ind]
                    new_area = st.slider(label='Fläche der Subwandfläche', min_value=0., max_value=max_area, key={name}, step=.1, format = '%.1f')
                    room_feinauslegung.sub_surface[wall][sub_wall_ind] = new_area

            
            
            
        if (len(walls_with_subwalls) > 0):
            with col1:
                area = slider_for_surface(room_feinauslegung,wall,sub_wall_ind, sub_material, key=sub_wall_ind)
        else:
            print("keine subfläche vorhanden")
        
        tab1, tab2 = st.tabs(['Nachhallzeit', 'Nachhallzeitenvergleich'])
        
        
        with tab1:
            # Plotting revernerationtime
            fig1 = room_feinauslegung.plot_reverberationTime()
            st.plotly_chart(fig1)
        
        with tab2:
            #plotting revernerationtime ratio
        
            fig2 = room_feinauslegung.plot_reverberationTime_ratio()
            st.plotly_chart(fig2)
        
        # Session Path for adding values to current session
        
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
            # Overwrite button to save data in current sessoion_state so it can be used in the main page
            json_data['wall' + str(wall_ind+1)]['subarea' + str(sub_wall_ind+1)]['area'] = area
            write_session_data_to_json(json_data, state)
            load_session(state)
except:
    st.error('Feinauslegung nicht möglich. Bitte zuerst Nachhallzeitenanalyse durchführen.')


