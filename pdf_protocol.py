from fpdf import FPDF
from fpdf.enums import XPos, YPos
import os
import plotly.io as pio

class pdfprotocol(FPDF):
    '''
    Class to retreive parameters out of .json session file and to create pdf protocol
    '''

    def __init__(self, filename, variables, plot_reverberationTime, plot_reverberationTimeRatio):
        '''
        Constructor for pdf object.

        :param volume: Volume of the room in cubic meters
        :type volume: int

        :param variables: Dictionary with json session parameters 
        :type variables: dict

        :param plot_reverberationTime: Plotly figure of the reverberation time
        :type plot_reverberationTime: plotly figure

        :param plot_reverberationTime_ratio: Plotly figure of the reverberation time ratio
                                             The ratio of calculated reverberation time to wanted reverberation time. 
                                             Wanted reverberation time is based on the rooms use case and its volume.
        :type plot_reverberationTime_ratio: Plotly figure

        :param font: Sets the font for the PDF file
        :type font: str       

        :return: Returns a pdfprotocol instance, which handles the PDF protocol 
        :rtype: class: pdfprotocol
        '''
        self.pdf = FPDF('P', 'mm', 'A4')
        self.filename = filename
        self.variables = variables 
        self.plot_reverberationTime = plot_reverberationTime
        self.plot_reverberationTimeRatio = plot_reverberationTimeRatio
        self.font = 'helvetica'

    def basic_variables(self):
        '''
        Returns the variables, that are not in another dictionary within the .json session file

        :rturn use: Usecase of the room
        :rtype use: str

        :rturn volume: Volume of the room
        :rtype volume: int

        :rturn number_walls: Number of main walls
        :rtype number_walls: int

        :rturn people: True, if there are people in the room
        :rtype people: boolean 

        :rturn number_people: Number of people will be returned, if there are people in the room
        :rtype number_people: int
        '''
        use = self.variables['usecase']
        volume = self.variables['volume']
        number_walls = self.variables['number_walls']
        people = self.variables['persons'] # True or False 7

        if people == True: 
            number_people = self.variables['number_people']
            return use, volume, number_walls, people, number_people
        else: 
            return use, volume, number_walls, people
    
    def wall_variables(self, index):
        '''
        Returns the variables for a specific main wall given by the index

        :param index: Index of the main wall for which the wall variables shall be retreived
        :type index: int

        :rturn name: Name of the main wall, as defined in the web-app
        :rtype name: str

        :rturn area: Area of the main wall 
        :rtype area: float

        :rturn category: Material category of the main wall
        :rtype category: str

        :rturn material: Material of the main wall
        :rtype material: str

        :rturn number_subareas: Number of the subareas that are on the given main wall
        :rtype number_subareas: float
        '''
        name = self.variables['wall' + f'{index + 1}']['name']
        area = self.variables['wall' + f'{index + 1}']['area']
        category = self.variables['wall' + f'{index + 1}']['category']
        material = self.variables['wall' + f'{index + 1}']['material']
        number_subareas = self.variables['wall' + f'{index + 1}']['number_subareas']

        return name, area, category, material, number_subareas

    def subwall_variables(self, index, subindex):
        '''
        Returns the variables for a specific subwall given by the index

        :param index: Index of the main wall on which the subwall lies
        :type index: int

        :param subindex: Index of the subwall for which the subwall variables shall be retreived
        :type subindex: int

        :rturn area: Area of the subwall
        :rtype area: float

        :rturn category: Category of the subwall
        :rtype category: str

        :rturn material: Material of the subwall
        :rtype material: str
        '''
        area = self.variables['wall' + f'{index + 1}']['subarea' + f'{subindex + 1}']['area']
        category = self.variables['wall' + f'{index + 1}']['subarea' + f'{subindex + 1}']['category']
        material = self.variables['wall' + f'{index + 1}']['subarea' + f'{subindex + 1}']['material']

        return area, category, material
    
    def people_variables(self, index):
        '''
        Returns the variables regarding people in the room for a given group

        :param index: Index of the group of people as set in the web-app
        :type index: int

        :rturn amount: Amount of people in the given group
        :rtype amount: int

        :rturn people_type: Description of people as given in Table A.1 in DIN 18041 
        :rtype people_type: str
        '''
        amount = self.variables['person_type' + f'{index + 1}']['amount']
        people_type = self.variables['person_type' + f'{index + 1}']['type']

        return amount, people_type
    
    def protocol(self):  
        '''
        Function that creates the PDF file out of the .json session variables
        '''      

        # Auto page break (margin: space from the bottom)
        self.pdf.set_auto_page_break(auto = True, margin = 15)

        # Add page
        self.pdf.add_page()
        
        # Title
        self.pdf.set_font(self.font, 'B', 16)
        self.pdf.set_fill_color(211, 211, 211)
        self.pdf.cell(0, 10 ,'Protokoll Nachhallzeitenanalyse', fill = True, new_x=XPos.LMARGIN, new_y=YPos.NEXT , align = 'C')
        self.pdf.ln(5)
    
        # Font and font size of text
        self.pdf.set_font(self.font, '', 9)
        
        # Usecase and volume
        self.pdf.cell(0, 5, f'Nutzungsart: {self.basic_variables()[0]}', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.pdf.cell(0, 5, f'Volumen: {self.basic_variables()[1]} m³', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.pdf.ln(3)
        
        # People
        if self.basic_variables()[3] == True:
            # Title
            self.pdf.set_font(self.font, 'B', 11)
            self.pdf.cell(0, 5, f'Personen', fill = True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.pdf.ln(1)
            self.pdf.set_font(self.font, '', 9)
            # People variables
            for index in range(self.basic_variables()[4]):

                # If there is more than one group of people write group 1, group 2... 
                if self.basic_variables()[4] != 1:
                    self.pdf.cell(0, 5, f'Personengruppe ' + f'{index + 1}:', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                    self.pdf.cell(5, 5, '')
                    self.pdf.cell(0, 5, f'Beschreibung: {self.people_variables(index)[1]}', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                    self.pdf.cell(5, 5, '')
                    self.pdf.cell(0, 5, f'Anzahl: {self.people_variables(index)[0]}', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                    self.pdf.ln(1)

                else:
                    self.pdf.cell(0, 5, f'Beschreibung: {self.people_variables(index)[1]}', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                    self.pdf.cell(0, 5, f'Anzahl: {self.people_variables(index)[0]}', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                    self.pdf.ln(1)

            self.pdf.ln(3)

        # Main walls
        for index in range(self.basic_variables()[2]):
            self.pdf.set_font(self.font, 'B', 11)
            self.pdf.cell(0, 5, f'{self.wall_variables(index)[0]}', fill = True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.pdf.ln(1)
            self.pdf.set_font(self.font, '', 9)
            

            self.pdf.cell(0, 5, f'Fläche: {self.wall_variables(index)[1]} m²', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.pdf.cell(0, 5, f'Kategorie: {self.wall_variables(index)[2]}', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.pdf.multi_cell(0, 5, f'Material: {self.wall_variables(index)[3]}', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.pdf.ln(1)
            # Subwalls
            for subindex in range(self.wall_variables(index)[4]):
                self.pdf.cell(0, 5, f'Subwand {subindex + 1}:', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

                self.pdf.cell(5, 5, '')
                self.pdf.cell(0, 5, f'Fläche: {self.subwall_variables(index, subindex)[0]} m²', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                self.pdf.cell(5, 5, '')
                self.pdf.cell(0, 5, f'Kategorie: {self.subwall_variables(index, subindex)[1]}', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                self.pdf.cell(5, 5, '')
                self.pdf.multi_cell(0, 5, f'Material: {self.subwall_variables(index, subindex)[2]}', 0,  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                self.pdf.ln(1)
            self.pdf.ln(2)

        # Write plots
        # Get working directory
        c_path =  os.getcwd()
        path_reverbereationTime = c_path + '/images/plot_reverberationTime.png'
        path_reverbereationTimeRatio = c_path + '/images/plot_reverberationTimeRatio.png'

        pio.write_image(self.plot_reverberationTime, path_reverbereationTime, format = 'png', engine='orca')
        pio.write_image(self.plot_reverberationTimeRatio, path_reverbereationTimeRatio, format = 'png', engine='orca')

        # Show plots
        self.pdf.add_page()
        self.pdf.ln(10)
        self.pdf.set_font(self.font, 'B', 14)
        self.pdf.cell(0, 5, 'Nachhallzeit', align = 'C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.pdf.image(path_reverbereationTime, w = 180)
        self.pdf.ln(10)
        self.pdf.cell(0, 5, 'Nachhallzeitenvergleich', align = 'C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.pdf.image(path_reverbereationTimeRatio, w = 180)

        # Output PDF file
        self.pdf.output('pdf_protocol.pdf')