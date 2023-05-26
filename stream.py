import streamlit as st
import streamlit_tags as sttags
from room_calc import Raum
from utils import basic_dict
import numpy as np 


st.title('My streamlit app for Roomacoustics')

st.text('First we need the general vertecies,\n the material of the walls and the volume of the the Room')
vol = st.number_input('Volume')

areas = st.number_input('Anzahl der Wandflächen die Sie eingeben möchten')
area =  np.linspace(0,int(areas),int(areas)+1)
with st.form(key = 'surface'):
    cols = st.columns(len(area))
    for i, col in enumerate(cols):
        surfaces = col.number_input(f"Enter number {i}")
        #surfaces = [st.number_input(f"Enter number {i}") for i in range(int(area))]
    sub = st.form_submit_button('Submitt')
st.write(surfaces)

alpha_d = basic_dict()

#st.write('alpha_d')

with st.form(key = f' alpha_d: '):
    for key in alpha_d:
            alpha_d[key] = sttags.st_tags(label = f'Enter values for alpha_d for {key}', key=key)
    submitted = st.form_submit_button('Submit')

#alpha_d =  st.experimental_data_editor(dict)

#alpha_d = [st.slider(f'Absorptionsgrad Wand {i}', min_value=0, max_value=1) for i in range(int(area))]
#st.write(alpha_d)

power = st.number_input('Leistung der Quelle')
dist = st.number_input('Abstand Quelle Empfänger')





room = Raum(volume=vol, surface=surfaces, alpha_d=alpha_d, power=power, distance=dist, use='Musik')

st.write(['Hallradius:' ,room.hallradius(),
        'Nachhallzeit:',room.nachhallzeit(), 'Sprachverständlichkeit:', room.sprachverstaendlichkeit()])





'''with st.beta_container():
    alpha_d = basic_dict()
    col1, col2 = st.beta_columns(2)
    with col1:
        k = st.text_input("Key")
    with col2:
        v = st.text_input("Value")
    button = st.button("Add")
    if button:
        if k and v:
            d[k] = v
    st.write(d)'''