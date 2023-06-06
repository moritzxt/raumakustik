import math 
import numpy as np
import plotly.graph_objects as go
from utils import basic_dict

class room: 
    '''Class inheriting all functions for calculations and making plots.'''
    def __init__(self, volume, surface, alpha, use):
        '''Function to initialize the class "room"'''
        self.input = {'Volume': volume, 'Surface': surface, 'Absorption coefficient': alpha}
        self.volume = volume
        self.surface = surface
        self.alpha = alpha
        self.use = use
        
    def equivalent_absorption_surface(self):
        '''Function to calculate the equivalent absorption surface.'''
        # surface als list mit m^2 der einzelnen Waende
        # alpha_d als dictionary mit Oktavbandfrequenzen als key und Liste der diffusen Absorptionsgrade pro Wand als value   
        
        # basic_dict() muss noch umgeschrieben werden {'125 Hz':0 , '250 Hz':0 , '500 Hz':0 , '1 kHz':0, '2 kHz':0 , '4 kHz':0 }
        A = basic_dict()

        for walls in range(len(self.surface)):
            for octavebands in A:
                alphaValuesList = self.alpha[octavebands]
                A[octavebands] = A[octavebands] + self.surface[walls] * alphaValuesList[walls]
 
        return A
   
    def reverberationTime(self):
        '''Function to calculate the reverberation time.'''
        reverberationTimeSeconds = basic_dict()
        equivalentSurface = self.equivalent_absorption_surface()
        for octavebands in equivalentSurface:
            reverberationTimeSeconds[octavebands] = (self.volume / equivalentSurface[octavebands]) * 0.161
        return reverberationTimeSeconds

    def hallradius(self):
        '''Function to calculate the distance, where direct and reflected sound are equal.'''
        hallradius = np.sqrt(self.equivalent_absorption_surface() / 50)

        return hallradius
    
    def reverberationTime_ratio(self):
        '''Function to calculate the ratio of given reverberation time to wanted reverberation time. Wanted reverberation time is based on the rooms use case and its volume.'''
        reverberationTime_ratio = basic_dict()
        T_upperlimit = {'125 Hz':1.45 , '250 Hz':1.2 , '500 Hz':1.2 , '1 kHz':1.2, '2 kHz':1.2 , '4 kHz':1.2 }
        T_lowerlimit = {'125 Hz':0.65 , '250 Hz':0.8 , '500 Hz':0.8 , '1 kHz':0.8, '2 kHz':0.8 , '4 kHz':0.65 }

        # Pruefung welchen use (welche Nutzungsart nach DIN 18041) vorliegt und Berechnung der Soll-Nachhallzeit abhaengig vom Raumvolumen
        if self.use == 'Musik':
            T_soll = 0.45 * math.log10(self.volume) + 0.07

        elif self.use == 'Sprache/Vortrag':
            T_soll = 0.37 * math.log10(self.volume) - 0.14

        elif self.use == 'Sprache/Vortrag inklusiv':    
            T_soll = 0.32 * math.log10(self.volume) - 0.17

        elif self.use == 'Unterricht/Kommunikation':
            T_soll = 0.32 * math.log10(self.volume) - 0.17

        elif self.use == 'Unterricht/Kommunikation inklusiv':
            T_soll = 0.26 * math.log10(self.volume) - 0.14

        elif self.use == 'Sport':
                if self.volume > 10000:        
                    T_soll = 2
                else:
                    T_soll = 0.75 * math.log10(self.volume) - 1

        # Berechnung des Quotienten RT/RT_soll und Pruefung, ob berechnete Nachhallzeit in den Fehlerschranken nach Abbildung 2 in DIN 18041 liegt
        for octavbands in self.reverberationTime():
            reverberationTime_ratio[octavbands] = self.reverberationTime()[octavbands] / T_soll
            if reverberationTime_ratio[octavbands] > T_upperlimit[octavbands]:
                print(f'Nachhallzeit in Oktavband mit Mittenfrequenz {octavbands} zu hoch')
            elif reverberationTime_ratio[octavbands] < T_lowerlimit[octavbands]:
                print(f'Nachhallzeit in Oktavband mit Mittenfrequenz {octavbands} zu niedrig')      
        return reverberationTime_ratio
    
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
        
        T_upperlimit = [1.45, 1.2, 1.2, 1.2, 1.2, 1.2]
        T_lowerlimit = [0.65, 0.8, 0.8, 0.8, 0.8, 0.65]

        reverberationTime_ratio = list(self.sprachverstaendlichkeit().values())

        fig = go.Figure()
        trace1 = go.Scatter(x = freq, y = T_lowerlimit, marker_color = 'green', mode='lines')
        trace2 = go.Scatter(x = freq, y = T_upperlimit, marker_color = 'green', fill = 'tonexty', fillcolor='rgba(26, 199, 93, 0.1)', mode='lines')
        trace3 = go.Bar(x = freq, y = reverberationTime_ratio, marker_color = 'blue')
        
        fig.update_xaxes(type='category')          
        fig.update_layout(xaxis_title = 'Frequenz [Hz]', yaxis_title = 'T / T_soll', width = 1000, height = 600)
        
        fig.add_trace(trace3)
        fig.update_traces(width=.2)
        fig.add_trace(trace1)
        fig.add_trace(trace2)
       
        return fig


