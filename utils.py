import streamlit as st
import csv
import base64

def basic_dict():
    """
    Returns a dictionary with the octavebands from 125 Hz to 4 kHz as keys. Values are initialized with zero.
    
    :return: Dictionary with the octavebands from 125 Hz to 4 kHz as keys. Values are initialized with zero.
    :rtype: dict of str: float
    """
    dictionary = {'125 Hz': 0, '250 Hz': 0,
                  '500 Hz': 0, '1 kHz': 0, '2 kHz': 0, '4 kHz': 0}
    return dictionary


def basic_dict_list():
    """
    Returns a dictionary with the octavebands from 125 Hz to 4 kHz as keys. Values are initialized with empty lists.
    
    :return: Dictionary with the octavebands from 125 Hz to 4 kHz as keys. Values are initialized with empty lists.
    :rtype: dict of str: list
    """
    dictionary = {'125 Hz': [], '250 Hz': [], '500 Hz': [],
                  '1 kHz': [], '2 kHz': [], '4 kHz': []}
    return dictionary


def sub_alpha_dict(key_list_surfaces):
    """
    Returns a dictionary with the octavebands from 125 Hz to 4 kHz as first keys and names of the main surfaces as second keys. Values are initialized with empty lists.
    
    :param key_list_surfaces: list of the names of the main surfaces
    :type key_list_surfaces: list of str
    
    :return: Dictionary with the octavebands from 125 Hz to 4 kHz as first keys and names of the main surfaces as second keys. Values are initialized with empty lists.
    :rtype: dict of str: dict of str: list
    """
    sub_alpha = basic_dict()
    for octaveBands in sub_alpha:
        sub_alpha[octaveBands] = {}
        for surface_key in key_list_surfaces:
            sub_alpha[octaveBands][surface_key] = []

    return sub_alpha


def read_db(filename):
    '''
    Reads the csv database and returns a Dictionary. The first key is the category of the material, second key is the material, values are the absorption coefficients.
    
    
    :param filename: filepath of csv file
    :type filename: str
    
    :return: Dictionary of Dictionary. The first key is the category of the material, second key is the material, values are absorption coefficients
    :rtype: dict of str: dict of str: float
    '''

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
    """
    Adds an entry (new material) to the database. Takes in a list in which every item represents one column in the csv file e.g. ["material", "category", 0.1, 0.2, 0.3, 0.4, 0.5, 0.6].
    
    :param list: List of data representing the new material
    :type list: list
    """
    with open('Datenbank_DIN18041.csv', mode='a', newline='\n', encoding='utf-8') as file:
        writer_object = csv.writer(file, delimiter=';')
        writer_object.writerow(list)
        file.close()

def flatten_dict(dict):
    '''
    Flattens two level dict to a one level dict. Category key will be lost.
    
    :param dict: Dictionary to be flattened
    :type dict: dict of str: dict of str: float
    
    :return: Flattened dictionary. Category key is lost.
    :rtype: dict of str: float
    '''
    
    flattened_dict = {}
    for key in dict:
        for key_2 in dict[key]:
            flattened_dict[key_2] = dict[key][key_2]
    return flattened_dict

def displayPDF(filepath):
    '''
    Displays pdf file.
    
    :param filepath: filepath of pdf file to display
    :type filepath: str
    '''
    # Opening file from file path
    with open(filepath, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    # Embedding PDF in HTML
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'

    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)

# Sport: 30000 m^2, as it is the biggest room volume applicable with DIN 18041 (see page 5)
usecase = {'Musik': [30, 1000], 'Sprache/Vortrag': [50, 5000], 'Sprache/Vortrag inklusiv': [30, 5000],
           'Unterricht/Kommunikation': [30, 1000],'Unterricht/Kommunikation inklusiv': [30, 500], 'Sport': [200, 30000]} 
