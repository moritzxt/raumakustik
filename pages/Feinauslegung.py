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

    :return: area of the subwall, category of subwall, material of subwall
    :rtype area: float, str, str
    '''
    area = json_data[f'wall{index + 1}'][f'subarea{subindex + 1}']['area']
    category = json_data[f'wall{index + 1}'][f'subarea{subindex + 1}']['category']
    material = json_data[f'wall{index + 1}'][f'subarea{subindex + 1}']['material']

    return area, category, material


# Initializing the room_feinauslegung object from main page of web-app
try:
    fileObj = open('src/raum.obj', 'rb')
except:
    fileObj = open('../src/raum.obj', 'rb')
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



        # Setup of page data
    st.set_page_config(page_title='Feinauslegung', layout='wide')
    with st.container():
        st.header('Feinauslegung der Nachhallzeit')
        st.write('Variieren des Flächeninhalts einer Subfläche')
        st.divider()

    # Setup of page appearence 
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.form(key = f'wand'):
        # Selecting mainwall
            wall = st.selectbox('Wähle die zu bearbeitende Grundfläche aus',
                                options=main_walls)
            # Index for main wall for lists
            wall_ind =  main_walls.index(wall)
            st.form_submit_button('Übernehmen')
    try:
        with col2:
            tabs = st.tabs(sub_walls[wall])
            for tab, name in zip(tabs, sub_walls[wall]):
                with tab:

                    subwall_ind = sub_walls[wall].index(name)
                    max_area = float(room_feinauslegung.surface[wall] - sum(room_feinauslegung.sub_surface[wall]))
                    max_area = max_area + room_feinauslegung.sub_surface[wall][subwall_ind]
                    new_area = st.slider(label='Fläche der Subwandfläche', min_value=0., max_value=max_area, key={wall, name}, step=.1, format = '%.1f')
                    room_feinauslegung.sub_surface[wall][subwall_ind] = new_area
                    material =  subwall_variables(json_data, wall_ind, subwall_ind)[2]
                    st.write(f'Material: {material}')

        
        
        


    except:
        st.error("Die Ausgewählte Grundfläche besitzt keine Subfläche")

    tab1, tab2 = st.tabs(['Nachhallzeitenvergleich', 'Nachhallzeit'])

    fileObj = open('src/raum.obj', 'wb')
    pickle.dump(room_feinauslegung, fileObj)
    fileObj.close()


    with tab1:
        #plotting revernerationtime ratio

        fig2 = room_feinauslegung.plot_reverberationTime_ratio()
        st.plotly_chart(fig2)

    with tab2:
        # Plotting revernerationtime
        fig1 = room_feinauslegung.plot_reverberationTime()
        st.plotly_chart(fig1)


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
        for wall_ind, wall in enumerate(room_feinauslegung.sub_surface):
            for subwall_ind, subwall in enumerate(room_feinauslegung.sub_surface[wall]):
                json_data['wall' + str(wall_ind+1)]['subarea' + str(subwall_ind+1)]['area'] = subwall
        write_session_data_to_json(json_data, state)
        load_session(state)
except:
    st.error('Feinauslegung nicht möglich. Bitte zuerst Nachhallzeitenanalyse durchführen.')


