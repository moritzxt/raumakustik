import numpy as np 

import streamlit as st
#import streamlit_tags as sttags
from room_calc import room
from utils import basic_dict , read_db, basic_dict_2, add_row


st.title('My streamlit app for Roomacoustics')

st.text('Benötigt werden das Raumvolumen, die Anzahl der Wände sowie deren Fläche \nund Absorptionsgrad (im Moment noch der über alle Bänder gemittelte)')
vol = st.number_input('Volume')

areas = st.number_input('Anzahl der Wandflächen die Sie eingeben möchten', step=1)
area =  np.linspace(0,int(areas),int(areas)+1)
with st.form(key = 'surface'):
    #cols = st.columns(len(area))
    #for i, col in enumerate(cols):
        #surfaces = [col.number_input(f"Enter number {i}") for k in range(int(areas))]
    surfaces = [st.number_input(f"Fläche für Wandfläche {i+1}") for i in range(int(areas))]
    sub = st.form_submit_button('Submitt')
st.write(surfaces)

alpha_d = basic_dict_2()

material_dict = read_db()

with st.form(key = 'material'):
    #cols = st.columns(len(area))
    #for i, col in enumerate(cols):
        #surfaces = [col.number_input(f"Enter number {i}") for k in range(int(areas))]
    materials = [st.selectbox(label= f'Bitte wählen Sie das Material der Wand {i} aus.',options=material_dict.keys())for i in range(int(areas))]
    sub = st.form_submit_button('Submit')




#st.write('alpha_d')
for wand, key in enumerate(materials):
    liste = material_dict[key]
    for freq in alpha_d:
        alpha_d[freq].append(float(liste[wand]))


# Updaten der Datenbank über ein dict

# with st.form(key = f' alpha_d: '):
#     for key in alpha_d:
#             alpha_d[key] = sttags.st_tags(label = f'Enter values for alpha_d for {key}', key=key)
#     submitted = st.form_submit_button('Submit')
# st.write(alpha_d)

# for key, value in alpha_d.items():
#     alpha_d[key] = [float(v) for v in value]

st.write(alpha_d)


#alpha_d =  st.experimental_data_editor(dict)

#alpha_d = [st.slider(f'Absorptionsgrad Wand {i}', min_value=0, max_value=1) for i in range(int(area))]
#st.write(alpha_d)

power = st.number_input('Leistung der Quelle')
dist = st.number_input('Abstand Quelle Empfänger')





raum = room(volume=vol, surface=surfaces, alpha=alpha_d, use='Musik')

st.write([
        'Nachhallzeit:',raum.nachhallzeit(), 'Sprachverständlichkeit:', raum.sprachverstaendlichkeit()])



#'Hallradius:' ,room.hallradius(),

fig = raum.plotly_nachhallzeit()
st.plotly_chart(fig)

# '''with st.beta_container():
#     alpha_d = basic_dict()
#     col1, col2 = st.beta_columns(2)
#     with col1:
#         k = st.text_input("Key")
#     with col2:
#         v = st.text_input("Value")
#     button = st.button("Add")
#     if button:
#         if k and v:
#             d[k] = v
#     st.write(d)'''