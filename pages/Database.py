import streamlit as st
import pandas as pd
from utils import read_db

dict_alpha = read_db()

dataframe =  pd.read_csv('Datenbank_Absorptionsgrade.csv',sep = ';')

st.dataframe(dataframe)