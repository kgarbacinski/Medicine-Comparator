from medicines_app.api_loader.medicinal_products_base_loader import MedicinalProductsBaseLoader
from medicines_app.api_loader.medicinal_product_builder import MedicinalProductBuilder
from medicines_app.scrapping.medicine_info_scrapper import pdf_scrapper
from medicines_app.models.database_setup import MedicineDatabase
import requests


class DatabaseUpdater:
    def __init__(self):
        self.db_path = '../models/medicine.db'
        self.medicinal_products = self.__get_products()

    def __get_products(self):
        return MedicinalProductsBaseLoader().get_medicinal_products()

    def update_medicinal_products_base(self):
        for product in self.medicinal_products:
            if product['characteristicFileName']:
                product = MedicinalProductBuilder(product)

                self.add_medicine(product)
                self.add_active_substances(product)
                self.update_ean_codes(product)

    def add_medicine(self, product):
        with MedicineDatabase(self.db_path) as db:
            medicines_id = db.get_medicine_by_id(product.id)
            if not medicines_id:
                db.add_medicine_to_table(product.id,
                                         product.name,
                                         product.pharmaceutical_form,
                                         product.content_length)

    def add_active_substances(self, product):
        for substance in product.active_substances_data:
            with MedicineDatabase(self.db_path) as db:
                if not db.get_active_substance_id_by_name(substance):
                    db.add_active_substance_to_table(substance)
                active_substance_id = db.get_active_substance_id_by_name(substance)
                if not db.get_medicines_active_substances_id(product.id, active_substance_id):
                    db.add_to_table_medicines_active_substances(product.id, active_substance_id)
                    medicines_active_substances_id = db.get_medicines_active_substances_id(product.id,
                                                                                           active_substance_id)
                    db.add_to_table_medicines_active_substances_details(medicines_active_substances_id,
                                                                        product.active_substances_data[substance][
                                                                            'power'],
                                                                        product.active_substances_data[substance][
                                                                            'unit'])

    def update_ean_codes(self, product):
        with MedicineDatabase(self.db_path) as db:
            db.delete_ean_codes_from_table(product.id)
        for ean_code in product.ean:
            with MedicineDatabase(self.db_path) as db:
                db.add_ean_to_table(ean_code, product.id)

    def update_excipents_base(self):
        with MedicineDatabase(self.db_path) as db:
            medicinal_products = db.get_all_medicines()
        for product in medicinal_products:
            if product[3] != self.content_length_getter(product[0]):
                self.delete_medicine_excipents(product[0])
                self.add_excipents(product[0])

    def delete_medicine_excipents(self, product_id):
        with MedicineDatabase(self.db_path) as db:
            db.delete_medicine_excipents_from_table(product_id)

    def add_excipents(self, product_id):
        with MedicineDatabase(self.db_path) as db:
            url = f'https://rejestrymedyczne.ezdrowie.gov.pl/api/rpl/medicinal-products/{product_id}/characteristic'
            try:
                excipents = pdf_scrapper(url)
            except:
                excipents = ['Błąd pobierania danych']
                print(f'pdfminer.pdfparser.PDFSyntaxError: No /Root object! | medicine_id: {product_id}')
            self.update_excipents(excipents, product_id)
            db.set_content_length(product_id, self.content_length_getter(product_id))

    def update_excipents(self, excipents, medicine_id):
        for excipent in excipents:
            with MedicineDatabase(self.db_path) as db:
                if not db.get_excipent_id_by_name(excipent):
                    db.add_excipent_to_table(excipent)
                excipent_id = db.get_excipent_id_by_name(excipent)
                db.add_medicine_excipents_to_table(medicine_id, excipent_id)

    def content_length_getter(self, product_id):
        url = f'https://rejestrymedyczne.ezdrowie.gov.pl/api/rpl/medicinal-products/{product_id}/characteristic'
        file = requests.get(url=url)
        return int(file.headers['Content-Length'])


medicinal_product_updater = DatabaseUpdater()
# medicinal_product_updater.update_medicinal_products_base()
medicinal_product_updater.update_excipents_base()
