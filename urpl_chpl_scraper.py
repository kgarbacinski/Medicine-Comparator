from bs4 import BeautifulSoup
from urllib import request
import pdf_reader

class UrplChPLScraper:
    def __init__(self, url):
        self.response = request.urlopen(url)
        self.content = self.response.read()
        self.soup = BeautifulSoup(self.content, 'lxml')
        self.records = self.soup.find_all('tr')[1:]


class UrplChPLMedicinalProduct:
    def __init__(self, record):
        self.record = record
        self.record_tds = record.find_all('td')
        self.gtin_code = self.set_gtin_code()
        self.chpl_link = self.get_link()

    def get_link(self) -> str:
        return 'http://leki.urpl.gov.pl' + self.record_tds[5].find('img').get('onclick')[13:-2]

    def set_gtin_code(self) -> str:
        r = self.record.find_all('td')
        return r[4].text

    def get_ean_code(self) -> str:
        if len(self.gtin_code) == 14:
            return self.gtin_code[1:]
        return self.gtin_code



scraper = UrplChPLScraper('http://leki.urpl.gov.pl/index.php?id=%27%%27')

for record in scraper.records[20:30]:
    m = UrplChPLMedicinalProduct(record)
    r = pdf_reader.PDFReader(m.get_link())
    print(r.get_additives())

