import numpy as np 

import streamlit as st
#import streamlit_tags as sttags
from room_calc import room
from utils import basic_dict , read_db, basic_dict_2, add_row, usecase, sub_alpha_dict

st.set_page_config(page_title= 'Tool für Raumakustik', layout='wide',
                    initial_sidebar_state='collapsed')

# """Eingabe der Parameter"""


with st.container():
    st.title('WebApp for Roomacoustics')
    st.divider()
    st.header('Benötigt werden das Raumvolumen, die Anzahl'
        ' der Wände, deren Fläche, sowie das Material der Wandoberfläche')

col1, col2, col3 = st.columns(3)
with col1:
    use = st.selectbox('Usecase nach DIN 18041', options=usecase.keys())
    min_lim =  min(usecase[use])
    max_lim =  max(usecase[use])
with col2:
    vol = st.number_input('Volumen in m³', min_value=min_lim,
                        max_value=max_lim, value=min_lim)
with col3:
    areas = st.number_input('Anzahl der Wandflächen die Sie eingeben möchten'
                            ,min_value=1, step=1)
area =  np.linspace(0,int(areas),int(areas)+1)

main_surfaces = {} # Dict enthält den Flächeninhalte der Hauptfläche, korrespondierend zum Key (name der Hauptfläche)
main_materials = [] # Materialien 
main_walls = [f'Grundflaeche {i+1}' for i in range(areas)]
subAreas = 0
material_dict = read_db()
sub_surfaces = {}
sub_materials = {}
for key in main_walls:
    sub_surfaces[key] = []
    sub_materials[key] = []
    main_surfaces[key] = None
tabs = st.tabs(main_walls)

for tab, name in zip(tabs, main_walls):
    with tab:
        if f'subAreas{name}' not in st.session_state:
                st.session_state[f'subAreas{name}'] = 0
        con_1 = st.container()
        con_2 = st.container()
        with con_1:
            col_1, col_2 = st.columns(2)
            with col_1:
                #with st.form(key = f'MainSurface {name}'):
                main_surfaces[name] = (st.number_input(
                    f"Fläche für {name}", value=1))


                    #subAreas = st.number_input('Anzahl der Subwandflächen', min_value=0, step=1, value=0)
                    #sub = st.form_submit_button('Submit')
                #st.write(surfaces)

            with col_2:
                main_materials.append(st.selectbox(label =  f'Bitte wählen Sie das Material der {name} aus.'
                    ,options=material_dict.keys()))



        with con_2:
            col_1, col_2, col_3 = st.columns(3)

            if st.button('Add Subwandfläche', key = f'Button subArea{subAreas} {name}'):
                st.session_state[f'subAreas{name}'] += 1
            subAreas = st.session_state[f'subAreas{name}']

            if st.button('Remove', key=f'remove Subfläche von {name}'):
                if st.session_state[f'subAreas{name}'] > 0:
                    st.session_state[f'subAreas{name}'] -= 1
                    sub_materials[name].pop()
                    sub_surfaces[name].pop()
        
            '''
                Wand 1 -> surface[Wand 1] = [m²]
                sub_surfaces[Wand 1] =  [sub11 m², sub12 m², sub13m² ...]
                sub_surfaces[Wand 2] =  [sub21 m², sub22 m², sub23m² ...]
                sub_materials[wand 1] = [subMat]

                sub_alpha['125 Hz'][Wall 1] = [alpha_subwand1, alpha_subwand2 ...]
                sub_alpha['2k Hz'][Wall 1] = [alpha_subwand1, alpha_subwand2 ...]

                '''
                    
            for num in range(0, subAreas):
                with col_1:
                    
                    sub_surfaces[name].append(st.number_input(f"Fläche für Subwandfläche {num +1 }",
                                                            value=1, key = f'Fläche subArea{num} {name}'))

                with col_2:
                    sub_materials[name].append(st.selectbox(label =  f'Bitte wählen Sie das Material der Subfläche {num + 1} aus.'
                        ,options=material_dict.keys(), key=f'Subfläche {num} von {name}'))
                


alpha = basic_dict_2()

for ind, octaveBand in enumerate(alpha):
    for material in main_materials:
        alpha[octaveBand].append(material_dict[material][ind])

sub_alpha = sub_alpha_dict(main_walls)

for ind, octaveBand in enumerate(sub_alpha):
    for wall in sub_alpha[octaveBand]:
        for material in sub_materials[wall]:
            sub_alpha[octaveBand][wall].append(material_dict[material][ind])



#Erstellen des Objektes Raum der Klasse room
raum = room(volume=vol, surface=main_surfaces, sub_surface=sub_surfaces, alpha=alpha, sub_alpha=sub_alpha, use='Musik')
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
