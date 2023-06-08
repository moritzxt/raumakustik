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
        file.close()
    return dict_db2

def add_row(list):
    with open('Datenbank_Absorptionsgrade.csv', mode='a', newline='\n') as file:
        writer_object = csv.writer(file, delimiter=';')
        writer_object.writerow(list)
        file.close()
        
# 30000 m^2, as it is the biggest room volume applicable with DIN 18041 (see page 5)
usecase = {'Musik': [30, 1000], 'Sprache/Vortrag': [50, 5000], 'Sprache/Vortrag inklusiv': [30, 5000],
           'Unterricht/Kommunikation': [30, 1000], 'Sport': [200, 30000]} 

