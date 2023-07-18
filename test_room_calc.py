import unittest
import room_calc
import utils
import math

# surface = {'wall1': 20, 'wall2': 20, 'wall3': 10, 'wall4': 10, 'wall5': 8, 'wall6': 8} # Abschaetzung eines normal grossen Raumes

# alpha = {'125 Hz': [0.2, 0.1 ,0.2, 0.1, 0.1, 0.1, 0.1], 
#         '250 Hz': [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1], 
#         '500 Hz': [0.02, 0.1, 0.2, 0.07, 0.1, 0.2, 0.1],
#         '1 kHz': [0.1, 0.1, 0.08, 0.1, 0.1, 0.1, 0.1], 
#         '2 kHz': [0.1, 0.04, 0.1, 0.2, 0.1, 0.1, 0.1], 
#         '4 kHz': [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
#         } 

# sub_surface = {'wall1':[5, 4], 'wall2':[6, 2], 'wall3': [5], 'wall4': [], 'wall5': [], 'wall6': [1, 2, 3]}

# sub_alpha = {'125 Hz': {'wall1':[0.15, 0.36], 'wall2':[0.16, 0.12], 'wall3': [0.13], 'wall4': [], 'wall5': [], 'wall6': [0.1, 0.2, 0.3]},
#             '250 Hz': {'wall1':[0.2, 0.1], 'wall2':[0.3, 0.1], 'wall3': [0.13], 'wall4': [], 'wall5': [], 'wall6': [0.1, 0.2, 0.3]}, 
#             '500 Hz': {'wall1':[0.2, 0.1], 'wall2':[0.2, 0.1], 'wall3': [0.13], 'wall4': [], 'wall5': [], 'wall6': [0.1, 0.2, 0.3]}, 
#             '1 kHz' : {'wall1':[0.2, 0.1], 'wall2':[0.2, 0.1], 'wall3': [0.13], 'wall4': [], 'wall5': [], 'wall6': [0.1, 0.2, 0.3]},
#             '2 kHz':  {'wall1':[0.2, 0.1], 'wall2':[0.2, 0.1], 'wall3': [0.13], 'wall4': [], 'wall5': [], 'wall6': [0.1, 0.2, 0.3]},
#             '4 kHz':  {'wall1':[0.2, 0.1], 'wall2':[0.2, 0.1], 'wall3': [0.13], 'wall4': [], 'wall5': [], 'wall6': [0.1, 0.2, 0.3]}  
#             }       

# use = 'Musik'

# default room_parameters
default_volume = 399    # valid for all usecases
default_surfaces = {'Grundflaeche 1': 378.5}
default_alphas = {'125 Hz': [0.2] , '250 Hz': [0.2] , '500 Hz': [0.2] , '1 kHz': [0.2], '2 kHz': [0.2] , '4 kHz': [0.2] }
default_subSurfaces = {'Grundflaeche 1': []}
default_subAlphas = {'125 Hz': {'Grundflaeche 1': []} , '250 Hz': {'Grundflaeche 1': []} , '500 Hz': {'Grundflaeche 1': []} , '1 kHz': {'Grundflaeche 1': []}, '2 kHz': {'Grundflaeche 1': []} , '4 kHz': {'Grundflaeche 1': []} }
default_peopleDescription = []
default_numberOfPeople = []
default_use = 'Musik'

# cuiboid a: 12   b: 9.5   c: 3.5 (in m)
defaultRoom = room_calc.room(
    volume = default_volume,   
    surface = default_surfaces,
    alpha = default_alphas,
    sub_surface = default_subSurfaces,
    sub_alpha = default_subAlphas,
    peopleDescription = default_peopleDescription,
    numberOfPeople = default_numberOfPeople,
    use = default_use
    )

# test on treating invalid input or not
test_inputValidation = False;


class test_RoomConstructor(unittest.TestCase):
    
    def test_IsInstance(self):
        self.assertIsInstance(defaultRoom, room_calc.room)
    
    def test_MissingVolume(self):
        with self.assertRaises(TypeError):
                room_calc.room(surface=default_surfaces, alpha=default_alphas, use=default_use, sub_surface=default_subSurfaces, sub_alpha=default_subAlphas, peopleDescription = default_peopleDescription, numberOfPeople = default_numberOfPeople)
                
    def test_MissingSurface(self):
        with self.assertRaises(TypeError):
                room_calc.room(alpha=default_alphas, use=default_use, volume=default_volume, sub_surface=default_subSurfaces, sub_alpha=default_subAlphas, peopleDescription = default_peopleDescription, numberOfPeople = default_numberOfPeople)
                
    def test_MissingAlpha(self):
        with self.assertRaises(TypeError):
                room_calc.room(surface=default_surfaces, volume=default_volume, alpha=default_alphas, sub_surface=default_subSurfaces, sub_alpha=default_subAlphas, peopleDescription = default_peopleDescription, numberOfPeople = default_numberOfPeople)
                
    def test_MissingUse(self):
        with self.assertRaises(TypeError):
                room_calc.room(surface=default_surfaces, use=default_use, volume=default_volume, sub_surface=default_subSurfaces, sub_alpha=default_subAlphas, peopleDescription = default_peopleDescription, numberOfPeople = default_numberOfPeople)
                
    if (test_inputValidation):
                
        def test_InvalidSurface1(self):
            with self.assertRaises(Exception):
                    room_calc.room(surface={'Grundflaeche 1': 0.0}, alpha=default_alphas, use=default_use, volume=default_volume, sub_surface=default_subSurfaces, sub_alpha=default_subAlphas, peopleDescription = default_peopleDescription, numberOfPeople = default_numberOfPeople)
                    
        def test_InvalidSurface2(self):
            with self.assertRaises(Exception):
                    room_calc.room(surface=-1, alpha=default_alphas, use=default_use, volume=default_volume, sub_surface=default_subSurfaces, sub_alpha=default_subAlphas, peopleDescription = default_peopleDescription, numberOfPeople = default_numberOfPeople) 
        
        def test_InvalidAlpha1(self):
            with self.assertRaises(Exception):
                    room_calc.room(surface=default_surfaces, alpha=1.3, use=default_use, volume=default_volume, sub_surface=default_subSurfaces, sub_alpha=default_subAlphas, peopleDescription = default_peopleDescription, numberOfPeople = default_numberOfPeople)
                    
        def test_InvalidAlpha2(self):
            with self.assertRaises(Exception):
                    room_calc.room(surface=default_surfaces, alpha=-3, use=default_use, volume=default_volume, sub_surface=default_subSurfaces, sub_alpha=default_subAlphas, peopleDescription = default_peopleDescription, numberOfPeople = default_numberOfPeople)
        
        def test_InvalidVolumeMusik1(self):
            with self.assertRaises(Exception):
                room_calc.room(surface=default_surfaces, alpha=default_alphas, use=default_use, volume=29, sub_surface=default_subSurfaces, sub_alpha=default_subAlphas, peopleDescription = default_peopleDescription, numberOfPeople = default_numberOfPeople)
                
        def test_InvalidVolumeMusik2(self):
            with self.assertRaises(Exception):
                room_calc.room(surface=default_surfaces, alpha=default_alphas, use=default_use, volume=1001, sub_surface=default_subSurfaces, sub_alpha=default_subAlphas, peopleDescription = default_peopleDescription, numberOfPeople = default_numberOfPeople)
                
        def test_InvalidVolumeSpracheVortrag1(self):
            with self.assertRaises(Exception):
                room_calc.room(surface=default_surfaces, alpha=default_alphas, use='Sprache/Vortrag', volume=49, sub_surface=default_subSurfaces, sub_alpha=default_subAlphas, peopleDescription = default_peopleDescription, numberOfPeople = default_numberOfPeople)
                
        def test_InvalidVolumeSpracheVortrag2(self):
            with self.assertRaises(Exception):
                room_calc.room(surface=default_surfaces, alpha=default_alphas, use='Sprache/Vortrag', volume=5001, sub_surface=default_subSurfaces, sub_alpha=default_subAlphas, peopleDescription = default_peopleDescription, numberOfPeople = default_numberOfPeople)    
                    
        def test_InvalidVolumeUnterrichtKommunikation1(self):
            with self.assertRaises(Exception):
                room_calc.room(surface=default_surfaces, alpha=default_alphas, use='Unterricht/Kommunikation', volume=29, sub_surface=default_subSurfaces, sub_alpha=default_subAlphas, peopleDescription = default_peopleDescription, numberOfPeople = default_numberOfPeople)
                
        def test_InvalidVolumeUnterrichtKommunikation2(self):
            with self.assertRaises(Exception):
                room_calc.room(surface=default_surfaces, alpha=default_alphas, use='Unterricht/Kommunikation', volume=5001, sub_surface=default_subSurfaces, sub_alpha=default_subAlphas, peopleDescription = default_peopleDescription, numberOfPeople = default_numberOfPeople)
                
        def test_InvalidVolumeUnterrichtKommunikationInklusiv1(self):
            with self.assertRaises(Exception):
                room_calc.room(surface=default_surfaces, alpha=default_alphas, use='Unterricht/Kommunikation inklusiv', volume=29, sub_surface=default_subSurfaces, sub_alpha=default_subAlphas, peopleDescription = default_peopleDescription, numberOfPeople = default_numberOfPeople)
        
        def test_InvalidVolumeUnterrichtKommunikationInklusiv2(self):
            with self.assertRaises(Exception):
                room_calc.room(surface=default_surfaces, alpha=default_alphas, use='Unterricht/Kommunikation inklusiv', volume=501, sub_surface=default_subSurfaces, sub_alpha=default_subAlphas, peopleDescription = default_peopleDescription, numberOfPeople = default_numberOfPeople)
              
        def test_InvalidVolumeSport1(self):
            with self.assertRaises(Exception):
                room_calc.room(surface=default_surfaces, alpha=default_alphas, use='Sport', volume=199, sub_surface=default_subSurfaces, sub_alpha=default_subAlphas, peopleDescription = default_peopleDescription, numberOfPeople = default_numberOfPeople)
                
        def test_InvalidVolumeSport2(self):
            with self.assertRaises(Exception):
                room_calc.room(surface=default_surfaces, alpha=default_alphas, use='Sport', volume=10001, sub_surface=default_subSurfaces, sub_alpha=default_subAlphas, peopleDescription = default_peopleDescription, numberOfPeople = default_numberOfPeople)
                
        def test_InvalidUse(self):
            with self.assertRaises(Exception):
                room_calc.room(surface=default_surfaces, alpha=default_alphas, use='invalid', volume=default_volume, sub_surface=default_subSurfaces, sub_alpha=default_subAlphas, peopleDescription = default_peopleDescription, numberOfPeople = default_numberOfPeople)
                
class test_equivalentAbsorptionSurface(unittest.TestCase):
    

    def test_Output1Wall(self):
        
        # set parameters
        alpha = {'125 Hz': [0.2] , '250 Hz': [0.2] , '500 Hz': [0.2] , '1 kHz': [0.2], '2 kHz': [0.2] , '4 kHz': [0.2] }
        surface = {'Grundflaeche 1': 378.5}
        volume = 399
        sub_surfaces = {'Grundflaeche 1': []}
        sub_alphas = {'125 Hz': {'Grundflaeche 1': []} , '250 Hz': {'Grundflaeche 1': []} , '500 Hz': {'Grundflaeche 1': []} , '1 kHz': {'Grundflaeche 1': []}, '2 kHz': {'Grundflaeche 1': []} , '4 kHz': {'Grundflaeche 1': []} }
        
        # set expected output
        expectedEAS = {'125 Hz': 75.7 , '250 Hz': 75.7 , '500 Hz': 75.7 , '1 kHz': 75.7, '2 kHz': 75.7 , '4 kHz': 75.7 }
        expectedEAS_air = {'125 Hz': 0.15162, '250 Hz': 0.45486, '500 Hz':  0.90972, '1 kHz': 1.5162, '2 kHz': 2.88078, '4 kHz': 8.79396}
        for octave in expectedEAS:
            expectedEAS[octave] += expectedEAS_air[octave]
        
        # create room
        room = room_calc.room(alpha=alpha, surface=surface, volume=volume, use=default_use, sub_surface = sub_surfaces, sub_alpha=sub_alphas, peopleDescription = default_peopleDescription, numberOfPeople = default_numberOfPeople)
        
        # calculate eqA
        calculatedEAS = room.equivalentAbsorptionSurface()
        
        # assertEqual length of dicts
        self.assertEqual(len(expectedEAS), len(calculatedEAS))
        # assert almostEqual for value of every key
        for octave in expectedEAS:
            self.assertAlmostEqual(expectedEAS[octave], calculatedEAS[octave])
            
    def test_Output2Walls(self):
        # set parameters
        alpha = {'125 Hz': [0.023, 0.2] , '250 Hz': [0.176, 0.6] , '500 Hz': [0.2, 0.4] , '1 kHz': [0.1, 0.35], '2 kHz': [0.1, 0.32] , '4 kHz': [0.2, 0.2] }
        surface = {'Grundflaeche 1': 200, 'Grundflaeche 2': 178.5}
        volume = 399
        sub_surfaces = {'Grundflaeche 1': [], 'Grundflaeche 2': []}
        sub_alphas = {'125 Hz': {'Grundflaeche 1': [], 'Grundflaeche 2': []} , '250 Hz': {'Grundflaeche 1': [], 'Grundflaeche 2': []} , '500 Hz': {'Grundflaeche 1': [], 'Grundflaeche 2': []} , '1 kHz': {'Grundflaeche 1': [], 'Grundflaeche 2': []}, '2 kHz': {'Grundflaeche 1': [], 'Grundflaeche 2': []} , '4 kHz': {'Grundflaeche 1': [], 'Grundflaeche 2': []} }
        
        # set expected output
        expectedEAS = {'125 Hz': 40.3 , '250 Hz': 142.3 , '500 Hz': 111.4 , '1 kHz': 82.475, '2 kHz':  77.12, '4 kHz': 75.7 }
        expectedEAS_air = {'125 Hz': 0.15162, '250 Hz': 0.45486, '500 Hz':  0.90972, '1 kHz': 1.5162, '2 kHz': 2.88078, '4 kHz': 8.79396}
        for octave in expectedEAS:
            expectedEAS[octave] += expectedEAS_air[octave]
            
        # create room
        room = room_calc.room(alpha=alpha, surface=surface, volume=volume, use=default_use, sub_surface = sub_surfaces, sub_alpha=sub_alphas, peopleDescription = default_peopleDescription, numberOfPeople = default_numberOfPeople)
        # calculate eqA
        calculatedEAS = room.equivalentAbsorptionSurface()
        
        # assertEqual length of dicts
        self.assertEqual(len(expectedEAS), len(calculatedEAS))
        # assert almostEqual for value of every key
        for octave in expectedEAS:
            self.assertAlmostEqual(expectedEAS[octave], calculatedEAS[octave])
            

class test_equivalentAbsorptionSurface_people(unittest.TestCase):
    
    if (test_inputValidation):
        
        def test_InvalidPeopleDescription(self):
            with self.assertRaises(Exception):
                   room = defaultRoom.copy
                   room.peopleDescription = 'invalid'
                   room.equivalentAbsorptionSurface()
        
        def test_InvalidNumPeople1(self):
            with self.assertRaises(Exception):
                room = defaultRoom.copy
                room.numberOfPeople = -1
                room.equivalentAbsorptionSurface_people()
        
        def test_InvalidNumPeople2(self):
            with self.assertRaises(Exception):
                room = defaultRoom.copy
                room.numberOfPeople = [2.3]
                room.equivalentAbsorptionSurface_people()
        
        def test_InvalidNumPeople3(self):
            with self.assertRaises(Exception):
                room = defaultRoom.copy
                room.numberOfPeople = 'invalid'
                room.equivalentAbsorptionSurface_people()
    
    def test_1PersonSitzendLeichtpolster(self):

        expectedEAS = {'125 Hz': 0.1 , '250 Hz': 0.15 , '500 Hz': 0.2 , '1 kHz': 0.25 , '2 kHz': 0.25 , '4 kHz': 0.25 }
        
        # calculate equivalentAbsorptinSurface_people
        numberOfPeople = [1]
        peopleDescription = ['Person sitzend auf Leichtpolsterbestuhlung']
        room = room_calc.room(alpha=default_alphas, surface=default_surfaces, 
                              volume=default_volume, use=default_use, 
                              sub_surface = default_subSurfaces, sub_alpha=default_subAlphas, 
                              peopleDescription = peopleDescription, numberOfPeople = numberOfPeople)

        calculatedEAS = room.equivalentAbsorptionSurface_people()
        
        # assertEqual length of dicts
        self.assertEqual(len(expectedEAS), len(calculatedEAS))
        # assert almostEqual for value of every key
        for octave in expectedEAS:
            self.assertAlmostEqual(expectedEAS[octave], calculatedEAS[octave])
            
    def test_12SchülerSekundarstufe(self):
        peopleDescription = ['Schüler Sekundarstufe, sitzend an Tischen']
        numberOfPeople = [12]
        expectedEAS = {'125 Hz': 1.2 , '250 Hz': 1.8 , '500 Hz': 4.2 , '1 kHz': 6.0 , '2 kHz': 6.0 , '4 kHz': 6.6 }

        # calculate equivalentAbsorptinSurface_people
        room = room_calc.room(alpha=default_alphas, 
                              surface=default_surfaces, 
                              volume=default_volume, 
                              use=default_use, 
                              sub_surface = default_subSurfaces, 
                              sub_alpha=default_subAlphas, 
                              peopleDescription = peopleDescription, 
                              numberOfPeople = numberOfPeople)
        calculatedEAS = room.equivalentAbsorptionSurface_people()
        
        # assertEqual length of dicts
        self.assertEqual(len(expectedEAS), len(calculatedEAS))
        # assert almostEqual for value of every key
        for octave in expectedEAS:
            self.assertAlmostEqual(expectedEAS[octave], calculatedEAS[octave])

class equivalentAbsorptionSurface_air(unittest.TestCase):
    
    def testOutputDefaultAir(self):
     expectedEAS = {'125 Hz': 0.15162, '250 Hz': 0.45486, '500 Hz':  0.90972, '1 kHz': 1.5162, '2 kHz': 2.88078, '4 kHz': 8.79396}
     
     room = defaultRoom
     calculatedEAS = room.equivalentAbsorptionSurface_air()
     
     self.assertEqual(len(expectedEAS), len(calculatedEAS))
     for octave in expectedEAS:
         self.assertAlmostEqual(expectedEAS[octave], calculatedEAS[octave])

class test_reverberation_Time(unittest.TestCase):
    
    
    def test_Output1Wall(self):
                   
        # set parameters
        alpha = {'125 Hz': [0.2] , '250 Hz': [0.2] , '500 Hz': [0.2] , '1 kHz': [0.2], '2 kHz': [0.2] , '4 kHz': [0.2] }
        surface = {'Grundflaeche 1': 378.5}
        volume = 399
        sub_surfaces = {'Grundflaeche 1': []}
        sub_alphas = {'125 Hz': {'Grundflaeche 1': []} , '250 Hz': {'Grundflaeche 1': []} , '500 Hz': {'Grundflaeche 1': []} , '1 kHz': {'Grundflaeche 1': []}, '2 kHz': {'Grundflaeche 1': []} , '4 kHz': {'Grundflaeche 1': []} }
        
        # get expected output
        # expectedEAS = {'125 Hz': 75.7 , '250 Hz': 75.7 , '500 Hz': 75.7 , '1 kHz': 75.7, '2 kHz': 75.7 , '4 kHz': 75.7 }
        # expectedEAS_air = {'125 Hz': 0.15162, '250 Hz': 0.45486, '500 Hz':  0.90972, '1 kHz': 1.5162, '2 kHz': 2.88078, '4 kHz': 8.79396} 
        # for octave in expectedEAS:
        #     expectedEAS[octave] += expectedEAS_air[octave]
        # expectRevTime = utils.basic_dict()
        # for octave in expectRevTime:
        #     expectRevTime[octave] = (volume / expectedEAS[octave]) * 0.161
        
        # set expected output
        expectRevTime = {'125 Hz': 0.8469034675857945, '250 Hz': 0.8435311942008691, '500 Hz': 0.8385228401826819, '1 kHz': 0.83193682154781, '2 kHz': 0.8174899765566084, '4 kHz': 0.7602791962881135}
        
        # create room
        room = room_calc.room(alpha=alpha, surface=surface, volume=volume, use=default_use, sub_surface = sub_surfaces, sub_alpha=sub_alphas, peopleDescription = default_peopleDescription, numberOfPeople = default_numberOfPeople)
        # calculate revTime
        calcRevTime = room.reverberationTime()
        
        # assertEqual length of dicts
        self.assertEqual(len(expectRevTime), len(calcRevTime))
        # assert almostEqual for value of every key
        for octave in expectRevTime:
            self.assertAlmostEqual(expectRevTime[octave], calcRevTime[octave])
            
    def test_Output2Walls(self):
        
        # set parameters
        alpha = {'125 Hz': [0.023, 0.2] , '250 Hz': [0.176, 0.6] , '500 Hz': [0.2, 0.4] , '1 kHz': [0.1, 0.35], '2 kHz': [0.1, 0.32] , '4 kHz': [0.2, 0.2] }
        surface = {'Grundflaeche 1': 200, 'Grundflaeche 2': 178.5}
        volume = 399
        sub_surfaces = {'Grundflaeche 1': [], 'Grundflaeche 2': []}
        sub_alphas = {'125 Hz': {'Grundflaeche 1': [], 'Grundflaeche 2': []} , '250 Hz': {'Grundflaeche 1': [], 'Grundflaeche 2': []} , '500 Hz': {'Grundflaeche 1': [], 'Grundflaeche 2': []} , '1 kHz': {'Grundflaeche 1': [], 'Grundflaeche 2': []}, '2 kHz': {'Grundflaeche 1': [], 'Grundflaeche 2': []} , '4 kHz': {'Grundflaeche 1': [], 'Grundflaeche 2': []} }
        
        # # get expected output
        # expectedEAS = {'125 Hz': 40.3 , '250 Hz': 142.3 , '500 Hz': 111.4 , '1 kHz': 82.475, '2 kHz':  77.12, '4 kHz': 75.7 }
        # expectedEAS_air = {'125 Hz': 0.15162, '250 Hz': 0.45486, '500 Hz':  0.90972, '1 kHz': 1.5162, '2 kHz': 2.88078, '4 kHz': 8.79396}
        # for octave in expectedEAS:
        #     expectedEAS[octave] += expectedEAS_air[octave]
        # expectRevTime = utils.basic_dict()
        # for octave in expectRevTime:
        #     expectRevTime[octave] = (volume / expectedEAS[octave]) * 0.161

        # set expected output
        expectRevTime = {'125 Hz': 1.5880451759410377, '250 Hz': 0.44999518755438517, '500 Hz': 0.5719807688951588, '1 kHz': 0.7648301250607207, '2 kHz': 0.8029796709482083, '4 kHz': 0.7602791962881135}
        
        # create room
        room = room_calc.room(alpha=alpha, surface=surface, volume=volume, use=default_use, sub_surface = sub_surfaces, sub_alpha=sub_alphas, peopleDescription = default_peopleDescription, numberOfPeople = default_numberOfPeople )
        # calculate revTime
        calcRevTime = room.reverberationTime()
        
        # assertEqual length of dicts
        self.assertEqual(len(expectRevTime), len(calcRevTime))
        # assert almostEqual for value of every key
        for octave in expectRevTime:
            self.assertAlmostEqual(expectRevTime[octave], calcRevTime[octave])
        
class test_reverberationTime_ratio(unittest.TestCase):
    
    def test_OutputMusik1Wall(self):
        
        # set parameters
        alpha = {'125 Hz': [0.2] , '250 Hz': [0.2] , '500 Hz': [0.2] , '1 kHz': [0.2], '2 kHz': [0.2] , '4 kHz': [0.2] }
        surface = {'Grundflaeche 1': 378.5}
        volume = 399
        use = 'Musik'        
        sub_surfaces = {'Grundflaeche 1': []}
        sub_alphas = {'125 Hz': {'Grundflaeche 1': []} , '250 Hz': {'Grundflaeche 1': []} , '500 Hz': {'Grundflaeche 1': []} , '1 kHz': {'Grundflaeche 1': []}, '2 kHz': {'Grundflaeche 1': []} , '4 kHz': {'Grundflaeche 1': []} }
        
        # # get expected output
        # expectEAS = {'125 Hz': 75.7 , '250 Hz': 75.7 , '500 Hz': 75.7 , '1 kHz': 75.7, '2 kHz': 75.7 , '4 kHz': 75.7 }
        # expectRevTime = {'125 Hz': 0.8469034675857945, '250 Hz': 0.8435311942008691, '500 Hz': 0.8385228401826819, '1 kHz': 0.83193682154781, '2 kHz': 0.8174899765566084, '4 kHz': 0.7602791962881135}
        # expectRevTimeWanted = 0.45 * math.log10(399) + 0.07
        # expectRevTimeRatio = utils.basic_dict()
        # for octave in expectRevTime:
        #     expectRevTimeRatio[octave] = expectRevTime[octave] / expectRevTimeWanted

        # set expected output
        expectRevTimeRatio = {'125 Hz': 0.6827456124742817, '250 Hz': 0.6800269970172156, '500 Hz': 0.6759894273737912, '1 kHz': 0.6706799966077905, '2 kHz': 0.6590334271824035, '4 kHz': 0.6129119851178295}
        
        # create room
        room = room_calc.room(alpha=alpha, surface=surface, volume=volume, use=use, sub_surface = sub_surfaces, sub_alpha=sub_alphas, peopleDescription = default_peopleDescription, numberOfPeople = default_numberOfPeople)
        # calculate revTime_ratio
        calcRevTimeRatio, errors = room.reverberationTime_ratio()
        
        # assertEqual length of dicts
        self.assertEqual(len(expectRevTimeRatio), len(calcRevTimeRatio))
        # assert almostEqual for value of every key
        for octave in expectRevTimeRatio:
            self.assertAlmostEqual(expectRevTimeRatio[octave], calcRevTimeRatio[octave])
        
        
    def test_OutputSpracheVortrag2Walls(self):
        
        # set parameters
        alpha = {'125 Hz': [0.023, 0.2] , '250 Hz': [0.176, 0.6] , '500 Hz': [0.2, 0.4] , '1 kHz': [0.1, 0.35], '2 kHz': [0.1, 0.32] , '4 kHz': [0.2, 0.2] }
        surface = {'Grundflaeche 1': 200, 'Grundflaeche 2': 178.5}
        volume = 399
        use = 'Sprache/Vortrag'
        sub_surfaces = {'Grundflaeche 1': [], 'Grundflaeche 2': []}
        sub_alphas = {'125 Hz': {'Grundflaeche 1': [], 'Grundflaeche 2': []} , '250 Hz': {'Grundflaeche 1': [], 'Grundflaeche 2': []} , '500 Hz': {'Grundflaeche 1': [], 'Grundflaeche 2': []} , '1 kHz': {'Grundflaeche 1': [], 'Grundflaeche 2': []}, '2 kHz': {'Grundflaeche 1': [], 'Grundflaeche 2': []} , '4 kHz': {'Grundflaeche 1': [], 'Grundflaeche 2': []} }
        
        # get expected output
        expectRevTime = {'125 Hz': 1.5880451759410377, '250 Hz': 0.44999518755438517, '500 Hz': 0.5719807688951588, '1 kHz': 0.7648301250607207, '2 kHz': 0.8029796709482083, '4 kHz': 0.7602791962881135}
        expectRevTimeWanted = 0.37 * math.log10(volume) - 0.14
        expectRevTimeRatio = utils.basic_dict()
        for octave in expectRevTime:
            expectRevTimeRatio[octave] = expectRevTime[octave] / expectRevTimeWanted
        
        # set expected output
        expectRevTimeRatio = {'125 Hz': 1.9310827753807258, '250 Hz': 0.5471997704193502, '500 Hz': 0.6955357614483098, '1 kHz': 0.9300429880540637, '2 kHz': 0.9764333125032841, '4 kHz': 0.9245090018061229}
        
        # create room
        room = room_calc.room(alpha=alpha, surface=surface, volume=volume, use=use, sub_surface = sub_surfaces, sub_alpha=sub_alphas, peopleDescription = default_peopleDescription, numberOfPeople = default_numberOfPeople)
        # calculate revTimeRatio
        calcRevTimeRatio, errors = room.reverberationTime_ratio()

        # assertEqual length of dicts
        self.assertEqual(len(expectRevTimeRatio), len(calcRevTimeRatio))
        # assert almostEqual for value of every key
        for octave in expectRevTimeRatio:
            self.assertAlmostEqual(expectRevTimeRatio[octave], calcRevTimeRatio[octave])
    
  
    def test_ErrorOnRevTimeToHighLow(self):
        # set parameters
        volume = 399
        surface = {'Grundflaeche 1': 200, 'Grundflaeche 2': 178.5}
        alpha = {'125 Hz': [0.023, 0.2] , '250 Hz': [0.176, 0.6] , '500 Hz': [0.2, 0.4] , '1 kHz': [0.1, 0.35], '2 kHz': [0.1, 0.32] , '4 kHz': [0.2, 0.2] }
        sub_surfaces = {'Grundflaeche 1': [], 'Grundflaeche 2': []}
        sub_alphas = {'125 Hz': {'Grundflaeche 1': [], 'Grundflaeche 2': []} , '250 Hz': {'Grundflaeche 1': [], 'Grundflaeche 2': []} , '500 Hz': {'Grundflaeche 1': [], 'Grundflaeche 2': []} , '1 kHz': {'Grundflaeche 1': [], 'Grundflaeche 2': []}, '2 kHz': {'Grundflaeche 1': [], 'Grundflaeche 2': []} , '4 kHz': {'Grundflaeche 1': [], 'Grundflaeche 2': []} }
        use = 'Sprache/Vortrag'
        
        # expectRevTimeRatio = {'125 Hz': 1.9383480550433365, '250 Hz': 0.5489488869869746, '500 Hz': 0.70121567879934, '1 kHz': 0.9471406683024733, '2 kHz': 1.0129075028299594, '4 kHz': 1.03190788135068}
        
        # create room
        room = room_calc.room(alpha=alpha, surface=surface, volume=volume, use=use, sub_surface = sub_surfaces, sub_alpha=sub_alphas, peopleDescription = default_peopleDescription, numberOfPeople = default_numberOfPeople)
        # calculate revTimeRatio
        calcRevTimeRatio, calcErrors = room.reverberationTime_ratio()
        
        expectErrors = ['Nachhallzeit in Oktavband mit Mittenfrequenz 125 Hz zu hoch', 'Nachhallzeit in Oktavband mit Mittenfrequenz 250 Hz zu niedrig', 'Nachhallzeit in Oktavband mit Mittenfrequenz 500 Hz zu niedrig']
        
        
        self.assertEqual(expectErrors, calcErrors)
        
        

if __name__ == "__main__":
    unittest.main()
        
        
        
        