import math 
import numpy as np

class Raum: 
    def __init__(self, volume, surface, alpha_d, power = 1e-7, distance = 1):
        self.input = {'Volume': volume, 'Surface': surface, 'Absorption coefficient': alpha_d,
                       'Source pwoer': power, 'Distance source <-> receiver': distance}
        self.volume = volume
        self.surface = surface
        self.alpha_d = alpha_d
        self.power = power
        self.distance = distance
        
    
    def eq_a(self):
        # surface als list mit m^2 der einzelnen Waende
        # alpha_d als dictionary mit Oktavbandfrequenzen als key und Liste der diffusen Absorptionsgrade pro Wand als value   
        A = {'125 Hz':0 , '250 Hz':0 , '500 Hz':0 , '1 kHz':0, '2 kHz':0 , '4 kHz':0 }

        for j in range(len(self.surface)):
            for i in A:
                X = self.alpha_d[i]
                A[i] = A[i] + self.surface[j] * X[j]
 
        return A
   
    def nachhallzeit(self):
        RT = {'125 Hz':0 , '250 Hz':0 , '500 Hz':0 , '1 kHz':0, '2 kHz':0 , '4 kHz':0 }
        A = self.eq_a()
        for i in A:
            RT[i] = (self.volume / A[i]) * 0.161
        return RT
    
    def level_diffuse(self):
        L_R = {'125 Hz':0 , '250 Hz':0 , '500 Hz':0 , '1 kHz':0, '2 kHz':0 , '4 kHz':0 }
        A = self.eq_a()
        for i in self.alpha_d:
            L_R[i] = 10 * math.log10(power / 10**(-12)) - 10 * math.log10(A[i]) + 6
        return L_R
    
    def level_direct(self):
        L_D = 7#10 * math.log10(self.power / 10**(-12)) - 10 * math.log10(4 * np.pi * self.distance**2)
        return L_D

    def hallradius(self):
        distance = 10**(-10)
        L_R = self.level_diffuse()
        L_D = self.level_direct()

        L_Rm = 0 # Initalisierung fuer Mittelwert des reflektierten Schalldruckpegels ueber alle Oktavbaender
        # Mittelwertbildung des reflektierten Schalldruckpegels
        for i in L_R:
            L_Rm = L_Rm + L_R[i] 
        L_Rm = L_Rm / len(L_R)
        # Sobald Mittelwert des reflektierten Schalldruckpegels
        # groesser als direkter Schalldruckpegel ist wird Hallradius ausgegeben
        while L_Rm < L_D:
            self.distance = self.distance + 0.01
            L_D = self.level_direct()            
        return self.distance
    
    def sprachverstaendlichkeit(self):
        L_R = self.level_diffuse()
        L_Rm = 0
        for i in L_R:
            L_Rm = L_Rm + L_R[i] 
        L_Rm = L_Rm / len(L_R)

        SV = self.level_direct() - L_Rm
        return SV