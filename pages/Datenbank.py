import streamlit as st
import pandas as pd
from utils import read_db, add_row

def valuesAreValid(values):
    '''
    Checks, if the absorption coefficients are given as required and are reasonable, when user adds material.

    :param values: Absorption coefficients that are given by the user
    :type values: List of floats

    :return: True, if the values meet the requirements, else otherwise
    :rtype: boolean
    '''
    # Check, if size of material_dict matches requirements (6)
    if not (len(values) == 6):
        return False
    # Check, if values are reasonable
    for v in values:
        if (v < 0 or v > 1):
            return False
    return True

# Read database and initialize dataframe
material_dict = read_db('database/Datenbank_DIN18041.csv')
dataframe =  pd.read_csv('database/Datenbank_DIN18041.csv',sep = ';')

# Page setup
st.set_page_config(page_title= 'Datenbank', layout='wide')
st.header('Datenbank')
st.divider()
st.dataframe(dataframe, use_container_width= True)

with st.container():
    st.divider()
    st.write('Updaten der Datenbank mit Benutzerdefinierten Werten.')
    st.caption('Bitte Werte mit einem Komma von einander trennen und einen Punkt '
            'als Dezimaltrennzeichen verwenden.')
    col1, col2, col3 = st.columns(3)

    # Generating input fields
    with col1:
        key_add = st.text_input("Material")

    with col2:
        category = st.selectbox(label= 'Kategorie', options=material_dict.keys())

    with col3:
        value_add = st.text_input("Absorptionsgrade")

    # Button for adding material
    button = st.button("Eintrag hinzufügen")
    if button:
        if key_add and value_add:
            try:
                values =[float(v) for v in str.split(value_add, sep = ',')]
                # Checking, if values are valid
                if (valuesAreValid(values)):
                    material_dict[key_add] = values
                    list_add = [key_add]
                    list_add.append(category)
                    for v in material_dict[key_add]:
                        list_add.append(v)
                    add_row(list_add)
                    # RELOAD required for displaying 
                # Error message, if values dont meet the requirements
                else:
                    st.error('Das Material konnte der Datenbank nicht hinzugefügt werden.'
                             ' Bitte Werte für die sechs Oktavbänder von 125Hz bis 4kHZ eingeben ' 
                             'und diese mit Komma von einander trennen sowie einen Punkt '
                             'als Dezimaltrennzeichen verwenden. '
                             'Bsp.: 0.1, 0.3, 0.1, 0.02, 0.5, 0.3')
            # Error message, if values dont meet the requirements
            except:
                st.error('Das Material konnte der Datenbank nicht hinzugefügt werden.'
                         ' Bitte Werte für die sechs Oktavbänder von 125Hz bis 4kHZ eingeben ' 
                         'und diese mit Komma von einander trennen sowie einen Punkt '
                         'als Dezimaltrennzeichen verwenden. '
                         'Bsp.: 0.1, 0.3, 0.1, 0.02, 0.5, 0.3')
            st.experimental_rerun()            
            



