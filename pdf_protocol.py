from fpdf import FPDF
from fpdf.enums import XPos, YPos
import json
import plotly.io as pio

class pdfprotocol(FPDF):

    def __init__(self, filename, plot_reverberationTime, plot_reverberationTimeRatio):
        # create object
        self.pdf = FPDF('P', 'mm', 'A4')
        self.filename = filename
        self.plot_reverberationTime = plot_reverberationTime
        self.plot_reverberationTimeRatio = plot_reverberationTimeRatio
        self.font = 'arial'

    def load_variables(self):
        json_file = open(self.filename)
        variables = json.load(json_file)
        json_file.close()

        return variables
    
    def header(self):
        self.pdf.set_font(self.font, 'B', 16)
        self.pdf.set_fill_color(211, 211, 211)
        self.pdf.cell(0, 10 ,'Raumakustik Protokoll', fill = True, new_x=XPos.LMARGIN, new_y=YPos.NEXT , align = 'C')
        self.pdf.ln(5)
        
    def footer(self):
        self.pdf.set_y(-15)
        self.pdf.set_font(self.font, 'I', 9)
        self.pdf.cell(0,10, f'Seite {self.pdf.page_no()}/{{nb}}', align = 'R')
        
    def basic_variables(self):
        use = self.load_variables()['usecase']
        volume = self.load_variables()['volume']
        number_walls = self.load_variables()['number_walls']
        persons = self.load_variables()['persons'] # True or False 7

        if persons == True: 
            number_people = self.load_variables()['number_people']
            return use, volume, number_walls, persons, number_people
        else: 
            return use, volume, number_walls, persons
    
    def wall_variables(self, index):
        '''
        Function to read variables of walls
        '''
        name = self.load_variables()['wall' + f'{index + 1}']['name']
        area = self.load_variables()['wall' + f'{index + 1}']['area']
        category = self.load_variables()['wall' + f'{index + 1}']['category']
        material = self.load_variables()['wall' + f'{index + 1}']['material']
        number_subareas = self.load_variables()['wall' + f'{index + 1}']['number_subareas']

        return name, area, category, material, number_subareas

    def subwall_variables(self, index, subindex):
        '''
        Function to read variables of subwalls
        '''
        area = self.load_variables()['wall' + f'{index + 1}']['subarea' + f'{subindex + 1}']['area']
        category = self.load_variables()['wall' + f'{index + 1}']['subarea' + f'{subindex + 1}']['category']
        material = self.load_variables()['wall' + f'{index + 1}']['subarea' + f'{subindex + 1}']['material']

        return area, category, material
    
    def people_variables(self, index):
        amount = self.load_variables()['person_type' + f'{index + 1}']['amount']
        type = self.load_variables()['person_type' + f'{index + 1}']['type']

        return amount, type
    
    def protocol(self):        
        # get total page number
        self.pdf.alias_nb_pages()
        # auto page break (margin: space from the bottom)
        self.pdf.set_auto_page_break(auto = True, margin = 15)
        # add page
        self.pdf.add_page()

        # pdf.set_text_color(220, 50 50) # rot
        
        # header
        self.header()
    
        # font of text
        self.pdf.set_font(self.font, '', 9)
        
        # usecase and volume
        # (width, height, 'text', ln = True/False -> cursor moves to the next line, border = True/False)
        self.pdf.cell(0, 5, f'Nutzungsart: {self.basic_variables()[0]}', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.pdf.cell(0, 5, f'Volumen: {self.basic_variables()[1]} m³', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.pdf.ln(3)
        
        # people
        if self.basic_variables()[3] == True:
            # header
            self.pdf.set_font(self.font, 'B', 11)
            self.pdf.cell(0, 5, f'Personen:', fill = True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.pdf.ln(1)
            self.pdf.set_font(self.font, '', 9)
            # people variables
            for index in range(self.basic_variables()[4]):
                # if there is more than one group of people write group 1, group 2... 
                if self.basic_variables()[4] != 1:
                    self.pdf.cell(0, 5, f'Personengruppe ' + f'{index + 1}:', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

                self.pdf.cell(0, 5, f'Beschreibung: {self.people_variables(index)[1]}', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                self.pdf.cell(0, 5, f'Anzahl: {self.people_variables(index)[0]}', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                self.pdf.ln(1)

            self.pdf.ln(3)
        # main walls
        for index in range(self.basic_variables()[2]):
            self.pdf.set_font(self.font, 'B', 11)
            self.pdf.cell(0, 5, f'{self.wall_variables(index)[0]}', fill = True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.pdf.ln(1)
            self.pdf.set_font(self.font, '', 9)
            

            self.pdf.cell(0, 5, f'Fläche: {self.wall_variables(index)[1]} m²', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.pdf.cell(0, 5, f'Kategorie: {self.wall_variables(index)[2]}', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.pdf.multi_cell(0, 5, f'Material: {self.wall_variables(index)[3]}', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.pdf.ln(1)
            # sub walls
            for subindex in range(self.wall_variables(index)[4]):
                # if self.wall_variables(index)[4] > 1:
                self.pdf.cell(0, 5, f'Subwand {subindex + 1}:', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

                self.pdf.cell(5, 5, '')
                self.pdf.cell(0, 5, f'Fläche: {self.subwall_variables(index, subindex)[0]} m²', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                self.pdf.cell(5, 5, '')
                self.pdf.cell(0, 5, f'Kategorie: {self.subwall_variables(index, subindex)[1]}', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                self.pdf.cell(5, 5, '')
                self.pdf.multi_cell(0, 5, f'Material: {self.subwall_variables(index, subindex)[2]}', 0,  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                self.pdf.ln(1)
            self.pdf.ln(2)

        # write plots
        pio.write_image(self.plot_reverberationTime, 'plot_reverberationTime', format = 'png')
        pio.write_image(self.plot_reverberationTimeRatio, 'plot_reverberationTimeRatio', format = 'png')

        # show plots
        self.pdf.add_page()
        self.pdf.ln(10)
        self.pdf.set_font(self.font, 'B', 14)
        self.pdf.cell(0, 5, 'Nachhallzeit', align = 'C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.pdf.image('plot_reverberationTime', w = 180)
        self.pdf.ln(10)
        self.pdf.cell(0, 5, 'Nachhallzeitenvergleich', align = 'C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.pdf.image('plot_reverberationTimeRatio', w = 180)

        # footer
        # self.footer()

        # output PDF file
        self.pdf.output('pdf_test.pdf')