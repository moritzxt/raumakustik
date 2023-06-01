import math 
import numpy as np
import plotly.graph_objects as go
from utils import basic_dict

class room: 

    def __init__(self, volume, surface, alpha, use):
        self.input = {'Volume': volume, 'Surface': surface, 'Absorption coefficient': alpha}
        self.volume = volume
        self.surface = surface
        self.alpha = alpha
        self.use = use
        
    def equivalent_absorption_surface(self):
        # surface als list mit m^2 der einzelnen Waende
        # alpha_d als dictionary mit Oktavbandfrequenzen als key und Liste der diffusen Absorptionsgrade pro Wand als value   
        
        # basic_dict() muss noch umgeschrieben werden {'125 Hz':0 , '250 Hz':0 , '500 Hz':0 , '1 kHz':0, '2 kHz':0 , '4 kHz':0 }
        A = basic_dict()

        for walls in range(len(self.surface)):
            for octavebands in A:
                alphaValuesList = self.alpha[octavebands]
                A[octavebands] = A[octavebands] + self.surface[walls] * alphaValuesList[walls]
 
        return A
   
    def nachhallzeit(self):
        reverberationTimeSeconds = basic_dict()
        equivalentSurface = self.equivalent_absorption_surface()
        for octavebands in equivalentSurface:
            reverberationTimeSeconds[octavebands] = (self.volume / equivalentSurface[octavebands]) * 0.161
        return reverberationTimeSeconds
    
    # def level_diffuse(self):
    #     L_R = basic_dict()
    #     equivalentSurface = self.equivalent_absorption_surface()
    #     for octavebands in self.alpha_d:
    #         L_R[octavebands] = 10 * math.log10(power / 10**(-12)) - 10 * math.log10(equivalentSurface[octavebands]) + 6
    #     return L_R
    
    # def level_direct(self):
    #     L_D = 10 * math.log10(self.power / 10**(-12)) - 10 * math.log10(4 * np.pi * self.distance**2)
    #     return L_D

    def hallradius(self):
        # distance = 10**(-10)
        # L_R = self.level_diffuse()
        # L_D = self.level_direct()

        # L_Rm = 0 # Initalisierung fuer Mittelwert des reflektierten Schalldruckpegels ueber alle Oktavbaender
        # # Mittelwertbildung des reflektierten Schalldruckpegels
        # for i in L_R:
        #     L_Rm = L_Rm + L_R[i] 
        # L_Rm = L_Rm / len(L_R)
        # # Sobald Mittelwert des reflektierten Schalldruckpegels
        # # groesser als direkter Schalldruckpegel ist wird Hallradius ausgegeben
        # while L_Rm < L_D:
        #     self.distance = self.distance + 0.01
        #     L_D = self.level_direct()            
        # return self.distance 
        hallradius = np.sqrt(self.equivalent_absorption_surface() / 50)

        return hallradius
    
    def sprachverstaendlichkeit(self):
        T_Vergleich = basic_dict()
        T_upperlimit = {'125 Hz':1.45 , '250 Hz':1.2 , '500 Hz':1.2 , '1 kHz':1.2, '2 kHz':1.2 , '4 kHz':1.2 }
        T_lowerlimit = {'125 Hz':0.65 , '250 Hz':0.8 , '500 Hz':0.8 , '1 kHz':0.8, '2 kHz':0.8 , '4 kHz':0.65 }

        # Pruefung welchen use (welche Nutzungsart nach DIN 18041) vorliegt und Berechnung der Soll-Nachhallzeit abhaengig vom Raumvolumen
        if self.use == 'Musik':
            # Pruefung, ob das Volumen nach DIN 18041 fuer Nutzungsart zugelassen ist
            # Falls es nicht passend ist wird T_Vergleich 0 gesetzt, damit im Folgenden auch die Funktion plot_nachhallzeit beendet werden kann ohne, dass es zu Fehlern kommt
            # Ansonsten wird einfach die T_soll ausgerechnet 
            while True:
                if self.volume < 30:
                    print(f'Volumen ist mit {self.volume} m^3 zu klein für die Berechnung nach DIN 18041 mit der Nutzungsart "Musik"')
                    # T_Vergleich = {'125 Hz':0 , '250 Hz':0 , '500 Hz':0 , '1 kHz':0, '2 kHz':0 , '4 kHz':0 }
                    return T_Vergleich
                elif self.volume > 1000:        
                    print(f'Volumen ist mit {self.volume} m^3 zu groß für die Berechnung nach DIN 18041 mit der Nutzungsart "Musik"')
                    # T_Vergleich = {'125 Hz':0 , '250 Hz':0 , '500 Hz':0 , '1 kHz':0, '2 kHz':0 , '4 kHz':0 }
                    return T_Vergleich
                else:    
                    T_soll = 0.45 * math.log10(self.volume) + 0.07
                    break
                

        elif self.use == 'Sprache/Vortrag':
            while True:
                if self.volume < 50:
                    print(f'Volumen ist mit {self.volume} m^3 zu klein für die Berechnung nach DIN 18041 mit der Nutzungsart "Sprache/Vortrag"')
                    # T_Vergleich = {'125 Hz':0 , '250 Hz':0 , '500 Hz':0 , '1 kHz':0, '2 kHz':0 , '4 kHz':0 }
                    return T_Vergleich
                elif self.volume > 5000:        
                    print(f'Volumen ist mit {self.volume} m^3 zu groß für die Berechnung nach DIN 18041 mit der Nutzungsart "Sprache/Vortrag"')
                    # T_Vergleich = {'125 Hz':0 , '250 Hz':0 , '500 Hz':0 , '1 kHz':0, '2 kHz':0 , '4 kHz':0 }
                    return T_Vergleich
                else:    
                    T_soll = 0.37 * math.log10(self.volume) - 0.14
                    break

        elif self.use == 'Sprache/Vortrag inklusiv':
            while True:
                if self.volume < 30:
                    print(f'Volumen ist mit {self.volume} m^3 zu klein für die Berechnung nach DIN 18041 mit der Nutzungsart "Sprache/Vortrag inklusiv"')
                    # T_Vergleich = {'125 Hz':0 , '250 Hz':0 , '500 Hz':0 , '1 kHz':0, '2 kHz':0 , '4 kHz':0 }
                    return T_Vergleich
                elif self.volume > 5000:        
                    print(f'Volumen ist mit {self.volume} m^3 zu groß für die Berechnung nach DIN 18041 mit der Nutzungsart "Sprache/Vortrag inklusiv"')
                    # T_Vergleich = {'125 Hz':0 , '250 Hz':0 , '500 Hz':0 , '1 kHz':0, '2 kHz':0 , '4 kHz':0 }
                    return T_Vergleich
                else:    
                    T_soll = 0.32 * math.log10(self.volume) - 0.17
                    break

        elif self.use == 'Unterricht/Kommunikation':
            while True:
                if self.volume < 30:
                    print(f'Volumen ist mit {self.volume} m^3 zu klein für die Berechnung nach DIN 18041 mit der Nutzungsart "Unterricht/Kommunikation"')
                    # T_Vergleich = {'125 Hz':0 , '250 Hz':0 , '500 Hz':0 , '1 kHz':0, '2 kHz':0 , '4 kHz':0 }
                    return T_Vergleich
                elif self.volume > 1000:        
                    print(f'Volumen ist mit {self.volume} m^3 zu groß für die Berechnung nach DIN 18041 mit der Nutzungsart "Unterricht/Kommunikation"')
                    # T_Vergleich = {'125 Hz':0 , '250 Hz':0 , '500 Hz':0 , '1 kHz':0, '2 kHz':0 , '4 kHz':0 }
                    return T_Vergleich
                else:
                    T_soll = 0.32 * math.log10(self.volume) - 0.17

        elif self.use == 'Unterricht/Kommunikation inklusiv':
            while True:
                if self.volume < 30:
                    print(f'Volumen ist mit {self.volume} m^3 zu klein für die Berechnung nach DIN 18041 mit der Nutzungsart "Unterricht/Kommunikation inklusiv"')
                    # T_Vergleich = {'125 Hz':0 , '250 Hz':0 , '500 Hz':0 , '1 kHz':0, '2 kHz':0 , '4 kHz':0 }
                    return T_Vergleich
                elif self.volume > 500:        
                    print(f'Volumen ist mit {self.volume} m^3 zu groß für die Berechnung nach DIN 18041 mit der Nutzungsart "Unterricht/Kommunikation inklusiv"')
                    # T_Vergleich = {'125 Hz':0 , '250 Hz':0 , '500 Hz':0 , '1 kHz':0, '2 kHz':0 , '4 kHz':0 }
                    return T_Vergleich
                else:
                    T_soll = 0.26 * math.log10(self.volume) - 0.14

        elif self.use == 'Sport':
            while True:
                if self.volume < 200:
                    print(f'Volumen ist mit {self.volume} m^3 zu klein für die Berechnung nach DIN 18041 mit der Nutzungsart "Sport"')
                    # T_Vergleich = {'125 Hz':0 , '250 Hz':0 , '500 Hz':0 , '1 kHz':0, '2 kHz':0 , '4 kHz':0 }
                    return T_Vergleich
                elif self.volume > 10000:        
                    T_soll = 2
                    break
                else:
                    T_soll = 0.75 * math.log10(self.volume) - 1
                    break

        # Berechnung des Quotienten RT/RT_soll und Pruefung, ob berechnete Nachhallzeit in den Fehlerschranken nach Abbildung 2 in DIN 18041 liegt
        for octavbands in self.nachhallzeit():
            T_Vergleich[octavbands] = self.nachhallzeit()[octavbands] / T_soll
            if T_Vergleich[octavbands] > T_upperlimit[octavbands]:
                print(f'Nachhallzeit in Oktavband mit Mittenfrequenz {octavbands} zu hoch')
            elif T_Vergleich[octavbands] < T_lowerlimit[octavbands]:
                print(f'Nachhallzeit in Oktavband mit Mittenfrequenz {octavbands} zu niedrig')      
        return T_Vergleich
    
    def plotly_nachhallzeit(self):
        freq = np.array([125,250,500,1000,2000,4000])
        reverberationTimeSeconds = self.nachhallzeit()

        fig = go.Figure()

        trace1 = go.Bar(x = freq, y = list(reverberationTimeSeconds.values()), marker_color = 'blue')
        fig.add_trace(trace1)

        fig.update_layout(xaxis_title = 'Frequenz [Hz]', yaxis_title = 'Nachhallzeit [s]', width = 1000, height = 600)
        fig.update_xaxes(type='category')
        fig.update_traces(width=.2)

        fig.show()
        return fig
    
    def plotly_nachhallzeit_vergleich(self):

        T_Vergleich = np.array(list(self.sprachverstaendlichkeit().values()))
        if np.average(T_Vergleich) == 0:
            return 
        
        freq = [125,250,500,1000,2000,4000]
        
        T_upperlimit = np.array([1.45, 1.2, 1.2, 1.2, 1.2, 1.2])
        T_lowerlimit = np.array([0.65, 0.8, 0.8, 0.8, 0.8, 0.65])

        fig = go.Figure()
        trace1 = go.Scatter(x = freq, y = T_lowerlimit, marker_color = 'green', mode='lines')
        trace2 = go.Scatter(x = freq, y = T_upperlimit, marker_color = 'green', fill = 'tonexty', fillcolor='rgba(26, 199, 93, 0.1)', mode='lines')
        trace3 = go.Bar(x = freq, y = T_Vergleich, marker_color = 'blue')
        
        fig.update_xaxes(type='category')          
        fig.update_layout(xaxis_title = 'Frequenz [Hz]', yaxis_title = 'T / T_soll', width = 1000, height = 600)
        
        fig.add_trace(trace3)
        fig.update_traces(width=.2)
        fig.add_trace(trace1)
        fig.add_trace(trace2)
       
        return fig


