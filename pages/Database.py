import streamlit as st
import pandas as pd
from utils import read_db, add_row
# from streamlit_js_eval import streamlit_js_eval 

dict_alpha = read_db('Datenbank_DIN18041.csv')
dataframe =  pd.read_csv('Datenbank_DIN18041.csv',sep = ';')
st.set_page_config(page_title= 'Database', layout='wide')
st.title('Materialdatenbank')
st.divider()
st.dataframe(dataframe, use_container_width= True)

material_dict = read_db('Datenbank_Absorptionsgrade.csv')


def valuesAreValid(values):
    # check size of material_dict matches requirements (6)
    if not (len(values) == 6):
        return False
    # check if values are reasonable
    for v in values:
        if (v < 0 or v > 1):
            return False
    return True


# '''Updaten der Datenbank mit Benutzerdefinierten Werten \n 
# Bitte Werte mit Komma voneinander trennen und einen Punkt \n
#  als Dezimaltrennzeichen verwenden'''

with st.container():
    st.caption('Updaten der Datenbank mit Benutzerdefinierten Werten. '
            'Bitte Werte mit Komma von einander trennen und einen Punkt '
            'als Dezimaltrennzeichen verwenden.'
            'Neuer Eintrag wird erst angezeitgt,'
            ' nachdem die Seite einmale neu geladen wurde.')
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        key_add = st.text_input("Key")
    with col2:
        value_add = st.text_input("Value")
    button = st.button("Add")
    if button:
        if key_add and value_add:
            try:
                values =[float(v) for v in str.split(value_add, sep = ',')]
                if (valuesAreValid(values)):
                    material_dict[key_add] = values
                    list_add = [key_add]
                    list_add.append('user')
                    for v in material_dict[key_add]:
                        list_add.append(v)
                    add_row(list_add)
                    # RELOAD
                    # automatischer reload --> kommt mit neuen requirements und ungetestet
                    #streamlit_js_eval(js_expressions="parent.window.location.reload()")
                    # reruns the script -> st.error get displayed gain
                    # st.experimental_rerun
                else:
                    st.error('Das Material konnte der Datenbank nicht hinzugefügt werden.'
                             'Bitte Werte für die sechs Oktavbänder von 125Hz bis 4kHZ eingeben ' 
                             'und diese mit Komma von einander trennen sowie einen Punkt '
                             'als Dezimaltrennzeichen verwenden. '
                             'Bsp.: 0.1, 0.3, 0.1, 0.02, 0.5, 0.3')
            except:
                st.error('Das Material konnte der Datenbank nicht hinzugefügt werden.'
                         'Bitte Werte für die sechs Oktavbänder von 125Hz bis 4kHZ eingeben ' 
                         'und diese mit Komma von einander trennen sowie einen Punkt '
                         'als Dezimaltrennzeichen verwenden. '
                         'Bsp.: 0.1, 0.3, 0.1, 0.02, 0.5, 0.3')
            
            



