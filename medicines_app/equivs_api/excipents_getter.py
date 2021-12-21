from models.database_setup import MedicineDatabase

class ExcipentsGetter:

    def get_excipents(self, medicine_id):
        with MedicineDatabase('models/medicine.db') as db:
            excipents = db.get_medicinal_product_excipents(medicine_id).fetchall()
            return self.__get_excipents(excipents)

    def __get_excipents(self, excipents):
        excipents_list = []
        for excipent in excipents:
            excipents_list.append(excipent[0])
        return sorted(excipents_list)
