import math 
import numpy as np
import plotly.graph_objects as go
from utils import basic_dict, basic_dict_list, read_db

class room: 
    '''
    Class inheriting all characteristics of the room as well as calculation and plotting functionality.
    '''

    def __init__(self, volume, surface, sub_surface, alpha, sub_alpha, peopleDescription, numberOfPeople, use):
        """
        Constructor for room object.

        :param volume: Volume of the room in cubic meters
        :type volume: int
        
        :param surface: Dictionary with the names of the main surfaces as keys and their areas in square meters as values
        :type surface: dict of str: int
        
        :param sub_surface: Dictionary with the names of the main surfaces as keys and lists of their subsurface areas in square meters as values
        :type sub_surface: dict of str: list of int
        
        :param alpha: Dictionary with octave bands as keys and lists of absorption coefficients of main surfaces as values
        :type alpha: dict of str: list of float
        
        :param sub_alpha: Dictionary of Dictionarys. With octave bands as first keys, main surfaces as second keys and lists of absorption coefficients of sub surfaces as values
        :type sub_alpha: dict of str: dict of str: list of float
        
        :param peopleDescription: List of descriptions of people in the room based on DIN18041
        :type peopleDescription: list of str
        
        :param numberOfPeople: List of int for different kind of people in the room
        :type numberOfPeople: list of int
        
        :param use: Usecase for the room based on DIN18041
        :type use: str
        
        :return: Returns a room instance, which handles all calculations
        :rtype: class: room
        """
        self.input = {'Volume': volume, 'Surface': surface, 'Absorption coefficient': alpha}
        self.volume = volume
        self.surface = surface
        self.sub_surface = sub_surface
        self.alpha = alpha
        self.sub_alpha = sub_alpha
        self.peopleDescription = peopleDescription
        self.numberOfPeople = numberOfPeople
        self.use = use
        self.ErrorMessage = []

    def criticalDistance(self):
        """
        Returns the critical distance, at which energy densities of the direct and reflected soundfield are equal. 
        Makes use of an approximate formula based on statistical acoustics in a diffuse soundfield. 

        :return criticalDistance: Critical distance in meters
        :rtype criticalDistance: float
        """
        # '''
        # Function to calculate the critical distance, where the energy densities of the direct and reflected soundfield are equal. 
        # Calculation is made with an approximate formula based on statistical acoustics in a diffuse soundfield.
        # '''
        
        criticalDistance = np.sqrt(self.equivalentAbsorptionSurface() / 50)

        return criticalDistance
        
    def equivalentAbsorptionSurface_walls(self):
        '''
        Returns equivalent absorption surface for the walls by calculating the equivalent absorption surface for every wall and summing them. People and air are not taken into account.
        
        :return equivalentAbsorptionSurface_walls: equivalent absoprtion surface in square meters
        :rtype equivalentAbsorptionSurface_walls: float
        '''

        equivalentAbsorptionSurface_walls = basic_dict()

        wall_index = 0
        # Equivalent absorption surface for main walls 
        for octaveBands in self.alpha:
            alphaList = self.alpha[octaveBands]

            for walls in self.surface:
                equivalentAbsorptionSurface_walls[octaveBands] = equivalentAbsorptionSurface_walls[octaveBands] + (self.surface[walls] - sum(self.sub_surface[walls])) * alphaList[wall_index]
                wall_index = wall_index + 1
            wall_index = 0

        # Adding equivalent absorption surface for sub walls
        for octaveBands in self.sub_alpha.keys():
            sub_alphaDict = self.sub_alpha[octaveBands]
            for sub_walls in self.sub_surface.keys():
                sub_alphaList = sub_alphaDict[sub_walls]
                sub_surfaceList = self.sub_surface[sub_walls]
                    
                for sub_wall_index in range(len(sub_surfaceList)):
                    equivalentAbsorptionSurface_walls[octaveBands] = equivalentAbsorptionSurface_walls[octaveBands] + sub_surfaceList[sub_wall_index] * sub_alphaList[sub_wall_index]

        return equivalentAbsorptionSurface_walls
    
    
    def equivalentAbsorptionSurface_people(self):
        '''
        Returns equivalent absorption surface for the people in the room based on the number of people and their specification regarding age and position (e.g. standing, sitting).
        Data retrieved from Table A.1 in DIN 18041.
        
        :return equivalentAbsorptionSurface_people: equivalent absorption surface of the people in the room in square meters
        :rtype equivalentAbsorptionSurface_people: float 
        '''
        equivalentAbsorptionSurface_people = basic_dict()

        people_db = read_db('database/equivalentAbsorptionSurface_people_data.csv')
        
        for index in range(len(self.peopleDescription)):
            equivalentAbsorptionSurface_people_list =  people_db[self.peopleDescription[index]]

            for index_list, octaveBands in enumerate(equivalentAbsorptionSurface_people):
                equivalentAbsorptionSurface_people[octaveBands] += self.numberOfPeople[index] * equivalentAbsorptionSurface_people_list[index_list]
            
        return equivalentAbsorptionSurface_people
    
    def equivalentAbsorptionSurface_air(self):
        '''
        Returns equivalent absorption surface resulting from the dampening in air.
        
        :return equivalentAbsorptionSurface_air: equivalent absorption surface of the air in square meters
        :rtype equivalentAbsorptionSurface_air: float
        '''
        equivalentAbsorptionSurface_air = basic_dict()

        dampening = [0.1, 0.3, 0.6, 1, 1.9, 5.8]

        for index_list, octaveBands in enumerate(equivalentAbsorptionSurface_air):
            equivalentAbsorptionSurface_air[octaveBands] = 4 * dampening[index_list] * 10**(-3) * self.volume * .95

        return equivalentAbsorptionSurface_air
    
    def equivalentAbsorptionSurface(self):
        '''
        Returns sum of all equivalent absorption surfaces (walls, people, air).
        
        :return equivalentAbsorptionSurface: Sum of equivalent absorption surfaces in square meters
        :rtype equivalentAbsorptionSurface: float
        '''
        equivalentAbsorptionSurface = basic_dict_list()

        for octaveBands in equivalentAbsorptionSurface:
            equivalentAbsorptionSurface[octaveBands] = self.equivalentAbsorptionSurface_walls()[octaveBands] + self.equivalentAbsorptionSurface_people()[octaveBands] + self.equivalentAbsorptionSurface_air()[octaveBands]

        return equivalentAbsorptionSurface
   
   
    def reverberationTime(self):
        '''
        Returns the reverberation time calculated by the formula of Sabine.
        
        :return reverberationTimeSeconds: reverberation time in s
        :rtype reverberationTimeSeconds: float
        '''

        reverberationTimeSeconds = basic_dict()
        equivalentAbsorptionSurface = self.equivalentAbsorptionSurface()
        
        for octavebands in equivalentAbsorptionSurface:
            reverberationTimeSeconds[octavebands] = (self.volume / equivalentAbsorptionSurface[octavebands]) * 0.161

        return reverberationTimeSeconds
    
    def reverberationTime_ratio(self):
        '''
        Returns the ratio of calculated reverberation time to wanted reverberation time. Wanted reverberation time is based on the rooms use case and its volume.
        
        :return reverberationTime_ratio: Ratio calculated to wanted reverberation time
        :rtype reverberationTime_ratio: float

        :return self.ErrorMessage: Error message, when reverberation time is not inside the given boundaries
        :rtype self.ErrorMessage: List 
        '''

        reverberationTime_ratio = basic_dict()
        ReverberationTime_upperlimit = {'125 Hz':1.45 , '250 Hz':1.2 , '500 Hz':1.2 , '1 kHz':1.2, '2 kHz':1.2 , '4 kHz':1.2 }
        ReverberationTime_lowerlimit = {'125 Hz':0.65 , '250 Hz':0.8 , '500 Hz':0.8 , '1 kHz':0.8, '2 kHz':0.8 , '4 kHz':0.65 }

        # Calculation of the wanted reverberation time dependent on the use case given in DIN 18041 (and the volume in use case "Sport")
        if self.use == 'Musik':
            reverberationTime_wanted = 0.45 * math.log10(self.volume) + 0.07

        elif self.use == 'Sprache/Vortrag':
            reverberationTime_wanted = 0.37 * math.log10(self.volume) - 0.14

        elif self.use == 'Sprache/Vortrag inklusiv':    
            reverberationTime_wanted = 0.32 * math.log10(self.volume) - 0.17

        elif self.use == 'Unterricht/Kommunikation':
            reverberationTime_wanted = 0.32 * math.log10(self.volume) - 0.17

        elif self.use == 'Unterricht/Kommunikation inklusiv':
            reverberationTime_wanted = 0.26 * math.log10(self.volume) - 0.14

        elif self.use == 'Sport':
                if self.volume > 10000:        
                    reverberationTime_wanted = 2
                else:
                    reverberationTime_wanted = 0.75 * math.log10(self.volume) - 1

        # Calculation of the ratio of calculated reverberation time to wanted reverberation time from DIN 18041 
        for octaveBands in self.reverberationTime():
            reverberationTime_ratio[octaveBands] = self.reverberationTime()[octaveBands] / reverberationTime_wanted
            if reverberationTime_ratio[octaveBands] > ReverberationTime_upperlimit[octaveBands]:
                self.ErrorMessage.append(f'Nachhallzeit in Oktavband mit Mittenfrequenz {octaveBands} zu hoch')
            elif reverberationTime_ratio[octaveBands] < ReverberationTime_lowerlimit[octaveBands]:
                self.ErrorMessage.append(f'Nachhallzeit in Oktavband mit Mittenfrequenz {octaveBands} zu niedrig') 

        return reverberationTime_ratio, self.ErrorMessage
    
    def plot_reverberationTime(self):
        '''
        Creates a plot presenting the reverberation time in octave bands using plotly.
        
        :return: plot of reverberation time
        :rtype: plotly figure
        '''
        freq = np.array([125,250,500,1000,2000,4000])
        reverberationTimeSeconds = self.reverberationTime() 

        # Creation of figure
        fig = go.Figure()

        trace1 = go.Bar(x = freq, 
                        y = list(reverberationTimeSeconds.values()), 
                        name = 'Nachhallzeit', 
                        marker_color = 'rgba(28, 122, 255, 1)', 
                        showlegend= False, 
                        width=.2,
                        hovertemplate = 'Oktavband: %{x} Hz<br>Nachhallzeit: %{y:.2f} s<extra></extra>')
        
        fig.add_trace(trace1)

        fig.update_layout(xaxis_title = 'Frequenz [Hz]', 
                          yaxis_title = 'Nachhallzeit [s]', 
                          width = 1000, 
                          height = 600,
                          hoverlabel = dict(bgcolor = 'rgba(28, 122, 255, .4)'))
        
        fig.update_xaxes(type='category')

        return fig
    
    def plot_reverberationTime_ratio(self):
        '''
        Creates a plot presenting the calculated reverberation time in comparison to the wanted reverberation time, also showing the allowed deviations in octave bands using plotly.
        
        :return: plot comparing calculated and wanted reverberation time
        :rtype: plotly figure
        
        '''
        frequencies = [63,125,250,500,1000,2000,4000,8000]
        
        ReverberationTime_upperlimit = [1.7,1.45, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2]
        ReverberationTime_lowerlimit = [0.5,0.65, 0.8, 0.8, 0.8, 0.8, 0.65, 0.5]

        reverberationTime_ratio = list(self.reverberationTime_ratio()[0].values())
        reverberationTime_ratio.insert(0,0)
        reverberationTime_ratio.append(0)
        
        # Bars will be red, when conditions are not met
        color_condition_high = np.array(reverberationTime_ratio) < np.array(ReverberationTime_upperlimit) 
        color_condition_low = np.array(reverberationTime_ratio) > np.array(ReverberationTime_lowerlimit)
        color_condition = color_condition_high & color_condition_low
        
        # Legend color is red, when no octaveband meets the requirements
        if np.sum(color_condition) != 0:
            color_condition[0] = True 
        else:
             color_condition[0] = False

        bar_colors = ['rgba(28, 122, 255, 1)' if condition else 'rgba(207, 7, 7, 0.88)' for condition in color_condition]
        
        # Creation of figure
        fig = go.Figure()

        trace1 = go.Scatter(x = frequencies, 
                            y = ReverberationTime_lowerlimit, 
                            name = 'Fehlergrenzen', 
                            marker_color = 'green', 
                            mode = 'lines', 
                            legendgroup = 'boundaries',
                            hoverinfo = 'skip'
                            )
        
        trace2 = go.Scatter(x = frequencies, 
                            y = ReverberationTime_upperlimit, 
                            marker_color = 'green', 
                            fill = 'tonexty', 
                            fillcolor = 'rgba(26, 199, 93, 0.1)',
                            mode = 'lines',
                            legendgroup = 'boundaries',
                            showlegend = False,
                            hoverinfo = 'skip',
                            )
        
        trace3 = go.Bar(x = frequencies, 
                        y = reverberationTime_ratio, 
                        name = 'Nachhallzeitenvergleich',
                        width = .2,
                        marker_color = bar_colors,
                        hovertemplate = 'Oktavband: %{x} Hz<br>Nachhallzeitenvergleich: %{y:.2f} s<extra></extra>'
                        )
        
        fig.update_xaxes(type = 'category')       

        fig.update_layout(xaxis_title = 'Frequenz [Hz]',
                          yaxis_title = 'T / T_soll', 
                          width = 1000, 
                          height = 600, 
                          hoverlabel = dict(bgcolor = 'rgba(28, 122, 255, .4)')
                          )
        
        fig.add_trace(trace1)
        fig.add_trace(trace2)
        fig.add_trace(trace3)
        
        return fig