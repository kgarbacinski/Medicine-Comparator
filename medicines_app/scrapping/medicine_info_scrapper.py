import pdfplumber
import io
import requests
import re


class PDFReader:

    def get_page(self, url):
        request = requests.get(url, verify=False)
        file = io.BytesIO(request.content)
        return file

    def get_whole_data(self, file):
        pdf = pdfplumber.open(file)

        pdf_to_text = ''
        if pdf.pages[0].extract_text() != None:
            for page in range(len(pdf.pages)):
                data = pdf.pages[page].extract_text()
                pdf_to_text += '\n' + data
            return pdf_to_text
        return '6.1. Wykaz substancji pomocniczych' \
               'Błąd odczytu danych z pliku PDF' \
               '6.2.  Niezgodności farmaceutyczne'

    def get_set_of_excipents(self, pdf_to_text):
        start_end_len = self.set_start_end_paragraph(pdf_to_text)
        excipents_text = pdf_to_text[start_end_len[0] + start_end_len[2]:
                    len(pdf_to_text) - (len(pdf_to_text) - start_end_len[1]) - 4]

        excipents_text_lines = self.extract_excipents_lines(excipents_text)
        return set(self.clean_excipents_list(excipents_text_lines))

    def clean_excipents_list(self, excipents_text_lines):
        final_list_of_excipents = []
        for i in excipents_text_lines:
            i = i.strip().lower()
            try:
                i = i.replace(re.search('^-\s*', i).group(), '')
            except:
                pass
            try:
                i = i.replace(re.search('\.$', i).group(), '')
            except:
                pass

            if len(i) > 2:
                final_list_of_excipents.append(i)
        return final_list_of_excipents

    def extract_excipents_lines(self, excipents_text):
        if ';' in excipents_text:
            return self.make_excipents_line_by_line(excipents_text, ';').splitlines()
        elif ',' in excipents_text:
            return self.make_excipents_line_by_line(excipents_text, ',').splitlines()
        else:
            return excipents_text.splitlines()

    def make_excipents_line_by_line(self, excipents_text, split_mark):
        if excipents_text.count(split_mark) > 1:
            excipents_text = excipents_text.replace('\n', '')
            excipents_text = excipents_text.replace(split_mark, '\n')
            return excipents_text.strip().lower()
        return excipents_text.strip().lower()

    def set_start_end_paragraph(self, pdf_to_text):
        start = pdf_to_text.index(re.search('6.(.)+wykaz(.)+pomocniczych', pdf_to_text, re.IGNORECASE).group())
        start_length = len(re.search('6.(.)+wykaz(.)+pomocniczych', pdf_to_text, re.IGNORECASE).group())
        end = pdf_to_text.index(re.search('6.(.)+niezgodności(.)+(farmaceutyczne)*', pdf_to_text, re.IGNORECASE).group())
        return [start, end, start_length]

def pdf_scrapper(url):
    scraper = PDFReader()
    file = scraper.get_page(url)
    pdf_to_text = scraper.get_whole_data(file)
    return scraper.get_set_of_excipents(pdf_to_text)

