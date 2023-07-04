import streamlit as st
import csv


def basic_dict():
    dictionary = {'125 Hz': 0, '250 Hz': 0,
                  '500 Hz': 0, '1 kHz': 0, '2 kHz': 0, '4 kHz': 0}
    return dictionary


def basic_dict_2():
    dictionary = {'125 Hz': [], '250 Hz': [], '500 Hz': [],
                  '1 kHz': [], '2 kHz': [], '4 kHz': []}
    return dictionary


def sub_alpha_dict(key_list_surfaces):
    sub_alpha = basic_dict()
    for octaveBands in sub_alpha:
        sub_alpha[octaveBands] = {}
        for surface_key in key_list_surfaces:
            sub_alpha[octaveBands][surface_key] = []

    return sub_alpha


def read_db(filename):
    '''Function to read the csv database. Creating a dict in a dict first key is the category of thy material, second key is the material, values are the absorptioncoefficient'''

    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        header = next(reader)
        dict_db2 = {}
        dict_cat_mat = {}

        for row in reader:
            key = row[0]

            try:
                values = row[1:]
                dict_cat_mat[key] = [float(v) for v in values]

            except:
                #dict_db2 = {}
                #dict_db = {}
                category = row[1]
                values = row[2:]
                if category not in dict_cat_mat:
                    dict_cat_mat.update({category: dict()})
                dict_cat_mat[category].update({key: [float(v) for v in values]})
        file.close()
    return dict_cat_mat


def add_row(list):
    """Funktion um Daten der Datenbank hinzuzufügen"""
    with open('Datenbank_DIN18041.csv', mode='a', newline='\n', encoding='utf-8') as file:
        writer_object = csv.writer(file, delimiter=';')
        writer_object.writerow(list)
        file.close()

def flatten_dict(dict):
    '''Function to flatten two level dict to a one level dict. 
        Category key will be lost'''
    
    flattened_dict = {}
    for key in dict:
        for key_2 in dict[key]:
            flattened_dict[key_2] = dict[key][key_2]
    return flattened_dict


# Sport: 30000 m^2, as it is the biggest room volume applicable with DIN 18041 (see page 5)
usecase = {'Musik': [30, 1000], 'Sprache/Vortrag': [50, 5000], 'Sprache/Vortrag inklusiv': [30, 5000],
           'Unterricht/Kommunikation': [30, 1000],'Unterricht/Kommunikation inklusiv': [30, 500], 'Sport': [200, 30000]} 
