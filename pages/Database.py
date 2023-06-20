import streamlit as st
import pandas as pd
from utils import read_db, add_row

dict_alpha = read_db()
dataframe =  pd.read_csv('Datenbank_DIN18041.csv',sep = ';')
st.set_page_config(page_title= 'Database', layout='wide')
st.title('Materialdatenbank')
st.divider()
st.dataframe(dataframe, use_container_width= True)

material_dict = read_db()

# '''Updaten der Datenbank mit Benutzerdefinierten Werten \n 
# Bitte Werte mit Komma voneinander trennen und einen Punkt \n
#  als Dezimaltrennzeichen verwenden'''

with st.container():
    st.caption('Updaten der Datenbank mit Benutzerdefinierten Werten. '
            'Bitte Werte mit Komma von einander trennen und einen Punkt '
            'als Dezimaltrennzeichen verwenden')
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        key_add = st.text_input("Key")
    with col2:
        value_add = st.text_input("Value")
    button = st.button("Add")
    if button:
        if key_add and value_add:
            material_dict[key_add] = [float(v) for v in str.split(value_add, sep = ',')]
            list_add = [key_add]
            for v in material_dict[key_add]:
                list_add.append(v)
            add_row(list_add)
            


