import math 
import numpy as np
import plotly.graph_objects as go
from utils import basic_dict, read_db

class room: 
    '''Class inheriting all functions for calculations and making plots.'''

    def __init__(self, volume, surface, sub_surface, alpha, sub_alpha, use):
        '''Function to initialize the class "room"'''
        self.input = {'Volume': volume, 'Surface': surface, 'Absorption coefficient': alpha}
        self.volume = volume
        self.surface = surface
        self.sub_surface = sub_surface
        self.alpha = alpha
        self.sub_alpha = sub_alpha
        self.use = use
        self.ErrorMessage = []

    def criticalDistance(self):
        '''
        Function to calculate the critical distance, where the energy densities of the direct and reflected soundfield are equal. 
        Calculation is made with an approximate formula based on statistical acoustics in a diffuse soundfield.
        '''
        
        criticalDistance = np.sqrt(self.equivalentAbsorptionSurface() / 50)

        return criticalDistance
        
    def equivalentAbsorptionSurface(self):
        '''Function to calculate the equivalent absorption surface.'''

        equivalentAbsorptionSurface = basic_dict()

        wall_index = 0
        # equivalent absorption surface for main walls 
        for octaveBands in self.alpha:
            alphaList = self.alpha[octaveBands]

            for walls in self.surface:
                equivalentAbsorptionSurface[octaveBands] = equivalentAbsorptionSurface[octaveBands] + (self.surface[walls] - sum(self.sub_surface[walls])) * alphaList[wall_index]
                wall_index = wall_index + 1
            wall_index = 0

        # adding equivalent absorption surface for sub walls
        for octaveBands in self.sub_alpha.keys():
            sub_alphaDict = self.sub_alpha[octaveBands]
            for sub_walls in self.sub_surface.keys():
                sub_alphaList = sub_alphaDict[sub_walls]
                sub_surfaceList = self.sub_surface[sub_walls]
                    
                for sub_wall_index in range(len(sub_surfaceList)):
                    equivalentAbsorptionSurface[octaveBands] = equivalentAbsorptionSurface[octaveBands] + sub_surfaceList[sub_wall_index] * sub_alphaList[sub_wall_index]

        return equivalentAbsorptionSurface
    
    
    def equivalentAbsorptionSurface_people(self, peopleDescription, numberOfPeople):
        '''
        Function to add equivalent absorption surface based on the number of people in the room and their specification regarding age and position (e.g. standing, sitting).
        Data retrieved from Table A.1 in DIN 18041
        '''
        equivalentAbsorptionSurface_total = basic_dict()
        equivalentAbsorptionSurface_walls = self.equivalentAbsorptionSurface()

        equivalentAbsorptionSurface_people = read_db('equivalentAbsorptionSurface_people_data.csv')

        equivalentAbsorptionSurface_people_list =  equivalentAbsorptionSurface_people[peopleDescription]

        index = 0

        for octaveBands in equivalentAbsorptionSurface_walls:
            
            equivalentAbsorptionSurface_total[octaveBands] = equivalentAbsorptionSurface_walls[octaveBands] + numberOfPeople * equivalentAbsorptionSurface_people_list[index]
            index += 1
            print(index)

        return equivalentAbsorptionSurface_total

    def reverberationTime(self):
        '''Function to calculate the reverberation time.'''

        reverberationTimeSeconds = basic_dict()
        equivalentSurface = self.equivalentAbsorptionSurface()
        for octavebands in equivalentSurface:
            reverberationTimeSeconds[octavebands] = (self.volume / equivalentSurface[octavebands]) * 0.161

        return reverberationTimeSeconds
    
    def reverberationTime_ratio(self):
        '''Function to calculate the ratio of given reverberation time to wanted reverberation time. Wanted reverberation time is based on the rooms use case and its volume.'''

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
        '''Function, which returns a plot of the reverberation time in octave bands.'''

        freq = np.array([125,250,500,1000,2000,4000])
        reverberationTimeSeconds = self.reverberationTime()

        fig = go.Figure()

        trace1 = go.Bar(x = freq, y = list(reverberationTimeSeconds.values()), marker_color = 'blue')
        fig.add_trace(trace1)

        fig.update_layout(xaxis_title = 'Frequenz [Hz]', yaxis_title = 'Nachhallzeit [s]', width = 1000, height = 600)
        fig.update_xaxes(type='category')
        fig.update_traces(width=.2)

        return fig
    
    def plot_reverberationTime_ratio(self):
        '''Function, which returns a plot of the calculated reverberation time in comparison to the wanted reverberation time and the allowed deviations in octave bands.'''
        
        freq = [125,250,500,1000,2000,4000]
        
        ReverberationTime_upperlimit = [1.45, 1.2, 1.2, 1.2, 1.2, 1.2]
        ReverberationTime_lowerlimit = [0.65, 0.8, 0.8, 0.8, 0.8, 0.65]

        reverberationTime_ratio = list(self.reverberationTime_ratio()[0].values())

        fig = go.Figure()
        trace1 = go.Scatter(x = freq, y = ReverberationTime_lowerlimit, marker_color = 'green', mode='lines')
        trace2 = go.Scatter(x = freq, y = ReverberationTime_upperlimit, marker_color = 'green', fill = 'tonexty', fillcolor='rgba(26, 199, 93, 0.1)', mode='lines')
        trace3 = go.Bar(x = freq, y = reverberationTime_ratio, marker_color = 'blue')
        
        fig.update_xaxes(type='category')          
        fig.update_layout(xaxis_title = 'Frequenz [Hz]', yaxis_title = 'T / T_soll', width = 1000, height = 600)
        
        fig.add_trace(trace3)
        fig.update_traces(width=.2)
        fig.add_trace(trace1)
        fig.add_trace(trace2)
       
        return fig


