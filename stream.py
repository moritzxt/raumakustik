import numpy as np 

import streamlit as st
#import streamlit_tags as sttags
from room_calc import room
from utils import basic_dict , read_db, basic_dict_2, add_row, usecase, sub_alpha_dict, flatten_dict

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
#_walls = []
#if len(main_walls) == 0:
if 'main_walls' not in st.session_state:
    st.session_state.main_walls = ['Grundfläche 1']

#session_state = st.session_state.get(main_walls = main_walls)
#    print('True')

with st.container():
    st.title('WebApp for Roomacoustics')
    st.divider()
    st.header('Benötigt werden das Raumvolumen, die Anzahl'
        ' der Wände, deren Fläche, sowie das Material der Wandoberfläche')

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        use = st.selectbox('Usecase nach DIN 18041', options=usecase.keys())
        min_lim =  min(usecase[use])
        max_lim =  max(usecase[use])
    with col2:
        vol = st.number_input('Volumen in m³', min_value=min_lim,
                            max_value=max_lim, value=min_lim)
    with col3:
        #areas = st.number_input('Anzahl der Wandflächen die Sie eingeben möchten'
        #                        ,min_value=1, step=1)
        wall_name = st.text_input('Name der Wandfläche', value='Wand 1')
        
        if st.button('Add'):
            st.session_state.main_walls.append(wall_name)


    with col4:
        st.empty()
        if st.checkbox(label='Personen', value= False, key='personen', label_visibility='visible'):
            tabs_list = ['Personen']

    
#area =  np.linspace(0,int(areas),int(areas)+1)



#main_walls = [f'Grundflaeche {i+1}' for i in range(areas)]
subAreas = 0

numPeople = 1 # Anzahl der Personengruppen im Raum 
st.session_state.main_walls.extend(tabs_list)

for key in st.session_state.main_walls:
    print(key)
    sub_surfaces[key] = []
    sub_materials[key] = []
    main_surfaces[key] = None

tabs = st.tabs(st.session_state.main_walls)


# Tabs für die jeweiligen Flächen und die 
# Personen

for tab, name in zip(tabs, st.session_state.main_walls):
    with tab:
        print(name)
        if name == 'Personen':
            col_11, col_12 = st.columns(2)

            if 'add_persons' not in st.session_state:
                st.session_state['add_persons'] = numPeople

            if st.button('Add Personen', key ='button_add_persons'):
                st.session_state['add_persons'] += 1

            numPeople = st.session_state['add_persons']

            for num in range(0, numPeople):
                
                    with col_11:
                        numberOfPeople.append(st.number_input(
                                f"Anzahl an Personen im Raum", value=1, key = f'people{num}'))
                    with col_12:
                        peopleDescription.append(st.selectbox(label =  f'Beschreibung',
                                                            key=f'Beschreibung{num}',options=person_dict.keys()))  


            
            
            if st.button('Remove Personen', key='remove_button_persons'):
                if st.session_state['add_persons'] > 1 and len(peopleDescription) > 0:
                    st.session_state['add_persons'] -= 1
                    peopleDescription.pop()
                    numberOfPeople.pop()
                    st.experimental_rerun()
     

        else:
            
                if f'subAreas{name}' not in st.session_state:
                        st.session_state[f'subAreas{name}'] = 0
                con_1 = st.container()
                con_2 = st.container()

                with con_1:
                    col_1, col_2, col_3 = st.columns(3)

                    with col_1:
                        main_surfaces[name] = (st.number_input(
                            f"Fläche für {name}", value=1, min_value=0))

                    with col_2:
                        category = st.selectbox(label='Bitte wählen Sie die Kategorie des Materials aus',
                                                key=f'{name}' ,options=material_dict.keys())
                    with col_3:
                        main_materials.append(st.selectbox(label =  f'Bitte wählen Sie das Material der {name} aus.',
                                                        options=material_dict[f'{category}'].keys()))

                

                with con_2:
                    st.divider()
                    col_1, col_2, col_3 = st.columns(3)

                    if st.button('Add Subwandfläche', key = f'Button subArea{subAreas} {name}'):
                        st.session_state[f'subAreas{name}'] += 1
                    subAreas = st.session_state[f'subAreas{name}']



                
            #       '''
            #           Wand 1 -> surface[Wand 1] = [m²]
                        # sub_surfaces[Wand 1] =  [sub11 m², sub12 m², sub13m² ...]
                        # sub_surfaces[Wand 2] =  [sub21 m², sub22 m², sub23m² ...]
                        # sub_materials[wand 1] = [subMat]

                        # sub_alpha['125 Hz'][Wall 1] = [alpha_subwand1, alpha_subwand2 ...]
                        # sub_alpha['2k Hz'][Wall 1] = [alpha_subwand1, alpha_subwand2 ...]

                        # '''
                            
                    for num in range(0, subAreas):
                        with col_1:
                            sub_surfaces[name].append(st.number_input(f"Fläche für Subwandfläche {num +1 }",
                                                                    value=1, key = f'Fläche subArea{num} {name}',min_value=0))

                        with col_2:
                            category = st.selectbox(label='Bitte wählen Sie die Kategorie des Materials aus',
                                                     options=material_dict.keys(), key= f'cat_sub_{name}{num}')
                        with col_3:
                            sub_materials[name].append(st.selectbox(label =  f'Bitte wählen Sie das Material der Subfläche {num + 1} aus.'
                                ,options=material_dict[f'{category}'].keys(), key=f'Subfläche {num} von {name}'))
                            
                    if st.button('Remove Subwandfläche', key=f'remove Subfläche von {name}') and len(sub_materials[name]) > 0:
                        if st.session_state[f'subAreas{name}'] > 0:
                            st.session_state[f'subAreas{name}'] -= 1
                            sub_materials[name].pop()
                            sub_surfaces[name].pop()
                            st.experimental_rerun()
                        
        

#Initialisierung des Dictionaries für die Absorptionsgrade
alpha = basic_dict_2()

#Befuellen des dicts mit den Absorptionsgeraden fuer die jeweiligen Oktavbaender und 
for ind, octaveBand in enumerate(alpha):
    for material in main_materials:
        try:
            alpha[octaveBand].append(material_dict_flattened[material][ind])
        except:
            alpha[octaveBand].append(None)

sub_alpha = sub_alpha_dict(st.session_state.main_walls)

for ind, octaveBand in enumerate(sub_alpha):
    for wall in sub_alpha[octaveBand]:
            for material in sub_materials[wall]:
                sub_alpha[octaveBand][wall].append(material_dict_flattened[material][ind])



#Erstellen des Objektes Raum der Klasse room
raum = room(volume=vol, surface=main_surfaces, sub_surface=sub_surfaces, alpha=alpha, 
            sub_alpha=sub_alpha, use=use, peopleDescription=peopleDescription, numberOfPeople=numberOfPeople)
#Plots erstellen

st.divider()
st.subheader('Ergebnisse')
st.divider()
tab1, tab2 = st.tabs(['Nachhallzeit', 'Vergleich der Nachhallzeit'])

with tab1:
    fig1 = raum.plot_reverberationTime()
    st.plotly_chart(fig1)

with tab2:
    fig2 = raum.plot_reverberationTime_ratio()

    st.plotly_chart(fig2)
