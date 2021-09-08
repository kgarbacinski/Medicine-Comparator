import pdfplumber
import io
import requests


class Scraper:

    def get_page(self, url):
        request = requests.get(url)
        file = io.BytesIO(request.content)
        return file

    def get_whole_data(self, file):
        pdf = pdfplumber.open(file)
        for page in range(len(pdf.pages)):
            pdf_to_text = ''
            data = pdf.pages[page].extract_text()
            pdf_to_text = pdf_to_text + '\n' + data
            return pdf_to_text

    def get_list_of_excipents(self, pdf_to_text):
        text_without_footer = pdf_to_text.replace('10     DE/H/0960/001-003/IA/077', '')
        start = text_without_footer.index('Wykaz substancji pomocniczych')
        start_length = len('Wykaz substancji pomocniczych')
        end = text_without_footer.index('Niezgodności farmaceutyczne')
        text_to_delete = len(text_without_footer) - end
        excipents = text_without_footer[start + start_length:len(text_without_footer) - text_to_delete - 5].splitlines()
        sorted_excipents = [x for x in excipents if not x.isdigit()]
        final_list_of_excipents = [excipent for excipent in sorted_excipents if excipent.strip() != '']
        return final_list_of_excipents

def main(url):
    scraper = Scraper()
    file = scraper.get_page(url) # 'http://leki.urpl.gov.pl/files/Amlopin5mg10mgtabl_dwiedawki.pdf'
    pdf_to_text = scraper.get_whole_data(file)
    scraper.get_list_of_excipents(pdf_to_text)

