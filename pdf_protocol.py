from fpdf import FPDF
from fpdf.enums import XPos, YPos
# from stream import fig1, fig2
import json

# altering class 
class pdfprotocol(FPDF):

    def __init__(self, filename):
        # create object
        self.pdf = FPDF('P', 'mm', 'A4')
        self.filename = filename

    def load_variables(self):
        json_file = open(self.filename)
        variables = json.load(json_file)
        json_file.close()

        return variables
    
    def header(self):
        self.pdf.set_font('helvetica', '', 16)
        self.cell(0, 10 ,'Raumakustik Protokoll', new_x=XPos.LMARGIN, new_y=YPos.NEXT , align = 'C')
        self.ln(10)
        

    def footer(self):
        self.set_y(-15)
        self.pdf.set_font('helvetica', '', 9)
        self.cell(0,10, f'Seite {self.page_no()}/{{nb}}', align = 'R')
        

    def wall_variables(index):
        '''
        Function to read variables of walls
        '''
        name = self.load_variables()['wall' + f'{index + 1}']['name']
        area = self.load_variables()['wall' + f'{index + 1}']['area']
        category = self.load_variables()['wall' + f'{index + 1}']['category']
        material = self.load_variables()['wall' + f'{index + 1}']['material']
        number_subareas = self.load_variables()['wall' + f'{index + 1}']['number_subareas']

        return name, area, category, material, number_subareas

    def subwall_variables(index):
        '''
        Function to read variables of subwalls
        '''
        area = self.load_variables()['wall' + f'{index + 1}']['subarea' + f'{index + 1}']['area']
        category = self.load_variables()['wall' + f'{index + 1}']['subarea' + f'{index + 1}']['category']
        material = self.load_variables()['wall' + f'{index + 1}']['subarea' + f'{index + 1}']['material']

        return area, category, material

    def protocol(self):
        # reading variables out of json file    

        # assigning general variables
        use = self.load_variables()['usecase']
        volume = self.load_variables()['volume']
        number_walls = self.load_variables()['number_walls']
        persons = self.load_variables()['persons'] # True or False 


        # get total page number
        self.pdf.alias_nb_pages()

        # auto page break (margin: space from the bottom)
        self.pdf.set_auto_page_break(auto = True, margin = 15)

        # add page
        self.pdf.add_page()

        # font
        self.pdf.set_font('helvetica', '', 9)
        # pdf.set_text_color(220, 50 50) # rot

        # printing of parameters
        # (width, height, 'text', ln = True/False -> cursor moves to the next line, border = True/False)
        self.pdf.cell(0, 5, f'use: {use}', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.pdf.cell(0, 5, f'volume: {volume}', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        for index in range(number_walls):
            self.pdf.cell(0, 5, f'name: {self.wall_variables(index)[0]}', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.pdf.cell(0, 5, f'area: {self.wall_variables(index)[1]}', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.pdf.cell(0, 5, f'category: {self.wall_variables(index)[2]}', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.pdf.cell(0, 5, f'Material: {self.wall_variables(index)[3]}', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            for subindex in range(self.wall_variables(index)[4]):
                self.pdf.cell(5, 5, '')
                self.pdf.cell(0, 5, f'sub area: {self.subwall_variables(subindex)[0]}', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                self.pdf.cell(0, 5, f'sub category: {self.subwall_variables(subindex)[1]}', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                self.pdf.cell(0, 5, f'sub material: {self.subwall_variables(subindex)[2]}', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.pdf.cell(0, 5, '', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # load and plot figure

        self.pdf.output('pdf_test.pdf')



