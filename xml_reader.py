from urllib import request
from bs4 import BeautifulSoup


class MedicineProduct:

    units = [' mg/ml', ' g/l', ' g/50 ml', ' g/100 ml',
             ' mg (nie mniej niż 150 mln żywych prątków BCG)/ml',
             'mg (nie mniej niż 300 mln żywych prątków BCG) / ml',
             ' mg/g (co odpowiada 435,6 mg amoksycyliny)', ' mg/g',
             ' mg Fe 2+', 'mg', '/ml', 'mcg'
    ]

    def __init__(self, product, pack):
        self.id = product.get('id')
        self.name = product.get('nazwaProduktu')
        self.dose = self.get_doses(product)
        self.ean = pack.get('kodEAN')

    def get_active_ingr(self, product):
        active_ingr = []
        for ingr in product.find_all('substancjaCzynna'):
            active_ingr.append(ingr)
        return active_ingr

    def divide_dose_and_unit(self, dose):
        dose_list = []
        for i in dose:
            for unit in self.units:
                if not i.find(unit) == -1:
                    splitted_dose = i.split(unit)
                    splitted_dose[0] = splitted_dose[0].strip()
                    splitted_dose[1] = unit
                    dose_list.append(splitted_dose)
                    break
        return dose_list

    def get_doses(self, product):
        try:
            doses = product.get('moc').split(' + ')
            dose = self.divide_dose_and_unit(doses)
        except:
            dose = product.get('moc')
        return dose



url = 'https://rejestrymedyczne.ezdrowie.gov.pl/api/rpl/medicinal-products/public-pl-report/get-old-xml/incremental'
response = request.urlopen(url)
contents = response.read()
soup = BeautifulSoup(contents, 'xml')
medicines = soup.find_all('produktLeczniczy')
medicines_list = []
for medicine in medicines:
    for pack in medicine.find_all('opakowanie'):
        m = MedicineProduct(medicine, pack)
        medicines_list.append(m)