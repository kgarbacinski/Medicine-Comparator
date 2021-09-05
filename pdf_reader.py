import requests
import pdfplumber
from io import BytesIO

class PDFReader:
    def __init__(self, url):
        self.url = url

    def read_pdf(self):

        rq = requests.get(self.url)
        try:
            pdf = pdfplumber.open(BytesIO(rq.content))
        except:
            print('Coś nie tak')


        final = ''

        for page in range(len(pdf.pages)):
            data = pdf.pages[page].extract_text()
            if data != None:
                final = final + '\n' + data

        return final


    def get_additives(self):
        start = self.read_pdf().find('Wykaz substancji pomocniczych')
        start_length = len('Wykaz substancji pomocniczych')
        end = self.read_pdf().find('Niezgodności farmaceutyczne')

        end_of_string = len(self.read_pdf()) - end
        new_list = []


        additives_text = self.read_pdf()[start+start_length:len(self.read_pdf())-end_of_string-5]
        if ';' in additives_text:
            my_list = additives_text.split(';')
            for i in my_list:
                i = i.strip()
                i = i.replace('\n', '')
                if i != '':
                    new_list.append(i)
        else:
            for i in additives_text.splitlines():
                i = i.strip()
                if i != '':
                    new_list.append(i)
        return new_list
