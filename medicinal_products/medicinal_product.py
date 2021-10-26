from medicinal_products.excipents_getter import ExcipentsGetter
from models.database_setup import MedicineDatabase

class MedicinalProduct:
    def __init__(self, medicine_id):
        with MedicineDatabase('models/medicine.db') as db:
            db_data = db.get_medicine_by_id(medicine_id)
        self.id = db_data[0]
        self.name = db_data[1]
        self.description = db_data[2]
        self.form = db_data[3]

    def get_excipents(self):
        return self.__get_validated_excipents()

    def __get_validated_excipents(self):
        excipents_getter = ExcipentsGetter()
        if excipents_getter.get_excipents(self.id):
            return excipents_getter.get_excipents(self.id)
        return ['Przykro nam! Dla tego leku nie mamy jeszcze składników dodatkowych!']

    def get_equivalents(self) -> list:
        with MedicineDatabase('models/medicine.db') as db:
            db.delete_from_tmp()
            db.insert_into_tmp(self.id)
            equivsalents = db.get_medicine_equivalents().fetchall()
            return self.__get_equivalents(equivalents=equivsalents)

    def __get_equivalents(self, equivalents: list) -> list:
        _eqiuvs = []
        for equivalent in equivalents:
            _eqiuvs.append(MedicinalProduct(equivalent[0]))
        return _eqiuvs
