import requests
import json


class MedicinalProductsBaseLoader:
    def __init__(self):
        self.total_pages = json.loads(requests.get(url=self.get_url()).text)['totalPages']

    def get_url(self, page=0):
        return f'https://rejestrymedyczne.ezdrowie.gov.pl/api/rpl/medicinal-products/search/public?' \
               f'page={page}&' \
               f'specimenTypeEnum=L&' \
               f'isAdvancedSearch=false&' \
               f'size=1000'

    def get_medicinal_products(self):
        all_medicinal_products = []
        for i in range(self.total_pages):
            page_content = json.loads(requests.get(self.get_url(i)).text)['content']
            all_medicinal_products.extend(page_content)
        return all_medicinal_products
