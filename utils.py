import streamlit as st
import csv

def basic_dict():
    dictionary = {'125 Hz':0 , '250 Hz':0 , '500 Hz':0 , '1 kHz':0, '2 kHz':0 , '4 kHz':0 }
    return dictionary
def basic_dict_2():
    dictionary = {'125 Hz':[] , '250 Hz':[] , '500 Hz':[] , '1 kHz':[], '2 kHz':[] , '4 kHz':[] }
    return dictionary

def read_db():
    with open('Datenbank_Absorptionsgrade.csv', 'r', ) as file:
        reader = csv.reader(file, delimiter=';')
        header = next(reader)
        dict_db2 = {}
        for row in reader:
            key = row[0]
            values = row[1:]
            dict_db2[key] = [float(v) for v in values]
    return dict_db2
