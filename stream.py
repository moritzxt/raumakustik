import streamlit as st
from room_calc import Raum

st.title('My streamlit app for Roomacoustics')

st.text('First we need the general vertecies,\n the material of the walls and the volume of the the Room')
vol = st.number_input('Volume')

area = st.number_input('Anzahl der Wandflächen die Sie eingeben möchten')
surfaces = [st.number_input(f"Enter number {i}") for i in range(int(area))]
st.write(surfaces)

alpha_d = [st.slider(f'Absorptionsgrad Wand {i}', min_value=0, max_value=1) for i in range(int(area))]
st.write(alpha_d)

power = st.number_input('Leistung der Quelle')
dist = st.number_input('Abstand Quelle Empfänger')





room = Raum(volume=vol, surface=surfaces, alpha_d=alpha_d, power=power, distance=dist)

st.write(['Hallradius:' ,room.hallradius(),
        'Nachhallzeit:',room.nachhallzeit(), 'Sprachverständlichkeit:', room.sprachverstaendlichkeit()])


