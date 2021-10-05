import sqlite3


class MedicineDatabase:
    def __init__(self, path):
        self.con = sqlite3.connect(path)

    def create_medicine_table(self):
        medicine_table = '''CREATE TABLE IF NOT EXISTS Medicines(
                            MedicineID INTEGER PRIMARY KEY,
                            Name TEXT NOT NULL,
                            PowerDescryption TEXT,
                            Form TEXT NOT NULL,
                            ContentLength INTEGER NOT NULL
                            ); '''
        self.con.execute(medicine_table)

    def create_excipents_table(self):
        excipents_table = '''CREATE TABLE IF NOT EXISTS Excipents (
                            ExcipentID INTEGER PRIMARY KEY,
                            Name TEXT NOT NULL
                            ); '''
        self.con.execute(excipents_table)

    def create_medicines_excipents_table(self):
        medicine_excipents_table = '''CREATE TABLE IF NOT EXISTS MedicinesExcipents (
                            ID INTEGER PRIMARY KEY,
                            MedicineID INTEGER NOT NULL,
                            ExcipentID INTEGER NOT NULL,
                            FOREIGN KEY (MedicineID) REFERENCES Medicines (MedicineID)
                            FOREIGN KEY (ExcipentID) REFERENCES Medicines (ExcipentID)
                            ); '''
        self.con.execute(medicine_excipents_table)

    def create_active_substances_table(self):
        active_substances_table = '''CREATE TABLE IF NOT EXISTS ActiveSubstances(
                                    ActiveSubstanceID INTEGER PRIMARY KEY,
                                    Name TEXT NOT NULL
                                    ); '''
        self.con.execute(active_substances_table)

    def create_medicines_active_substances_table(self):
        medicine_active_substances_table = '''CREATE TABLE IF NOT EXISTS MedicinesActiveSubstances (
                            ID INTEGER PRIMARY KEY,
                            MedicineID INTEGER NOT NULL,
                            ActiveSubstanceID INTEGER NOT NULL,
                            FOREIGN KEY (MedicineID) REFERENCES Medicines (MedicineID)
                            FOREIGN KEY (ActiveSubstanceID) REFERENCES MedicinesActiveSubstances (ActiveSubstanceID)
                            ); '''
        self.con.execute(medicine_active_substances_table)

    def create_medicines_active_substances_values_table(self):
        medicine_active_substances_values_table = '''CREATE TABLE IF NOT EXISTS MedicinesActiveSubstancesValues (
                                                ID INTEGER PRIMARY KEY,
                                                Concentration TEXT NOT NULL,
                                                Unit TEXT NOT NULL,
                                                FOREIGN KEY(ID) REFERENCES MedicinesActiveSubstances (ID)
                                                ); '''
        self.con.execute(medicine_active_substances_values_table)

    def create_ean_table(self):
        ean_table = '''CREATE TABLE IF NOT EXISTS EanTable(
                    EanID INTEGER PRIMARY KEY,
                    EanNumber INTEGER NOT NULL,
                    MedicineID INTEGER NOT NULL,
                    FOREIGN KEY(MedicineID) REFERENCES Medicines (MedicineID)
                    ); '''
        self.con.execute(ean_table)

    def add_medicine_to_table(self, medicine_id, name, power_descr, form, content_length):
        medicine = "INSERT INTO Medicines(medicineId, name, PowerDescryption, form, ContentLength) VALUES (?, ?, ?, ?, ?)"
        self.con.execute(medicine, (medicine_id, name, power_descr, form, content_length))

    def add_active_substance_to_table(self, name):
        query_substance = "INSERT INTO ActiveSubstances(Name) VALUES (?)"
        self.con.execute(query_substance, [name])

    def add_to_table_medicines_active_substances(self, medicine_id, active_substance_id):
        query = "INSERT INTO MedicinesActiveSubstances " \
                "(MedicineID, ActiveSubstanceId) VALUES (?, ?)"
        self.con.execute(query, (medicine_id, str(active_substance_id[0])))

    def add_to_table_medicines_active_substances_values(self, medicines_active_substances_id, concentration, unit):
        query = "INSERT INTO MedicinesActiveSubstancesValues " \
                "(Id, Concentration, Unit) VALUES (?, ?, ?)"
        self.con.execute(query, (str(medicines_active_substances_id[0]), str(concentration), unit))

    def add_medicine_excipents_to_table(self, medicine_id, excipent_id):
        query = "INSERT INTO MedicinesExcipents (MedicineID, ExcipentId) VALUES (?, ?)"
        self.con.execute(query, (medicine_id, excipent_id[0]))

    def add_excipent_to_table(self, name):
        excipent = "INSERT INTO Excipents (Name) VALUES (?)"
        self.con.execute(excipent, [name])

    def add_ean_to_table(self, ean_number, medicine_id):
        ean = "INSERT INTO EanTable (EanNumber, MedicineID) VALUES (?, ?)"
        self.con.execute(ean, (ean_number, medicine_id))

    def get_active_substance_id_by_name(self, name):
        query = "SELECT ActiveSubstanceId FROM ActiveSubstances WHERE Name = (?)"
        return self.con.execute(query, [name]).fetchone()

    def get_excipent_id_by_name(self, name):
        query = "SELECT ExcipentId FROM Excipents WHERE Name = (?)"
        return self.con.execute(query, [name]).fetchone()

    def get_all_medicines(self):
        query = "SELECT * FROM Medicines"
        cursor = self.con.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        return records

    def get_all_medicines_ids(self):
        query = "SELECT MedicineID FROM Medicines"
        return self.con.execute(query).fetchall()

    def get_medicine_by_id(self, medicine_id):
        query_medicine_id = "SELECT * FROM Medicines WHERE MedicineID = (?)"
        return self.con.execute(query_medicine_id, [medicine_id]).fetchone()

    def get_medicines_active_substances_id(self, medicine_id, active_substance_id):
        query = "SELECT ID FROM MedicinesActiveSubstances WHERE MedicineID = (?) AND ActiveSubstanceId = (?)"
        return self.con.execute(query, (medicine_id, str(active_substance_id[0]))).fetchone()

    def set_content_length(self, medicine_id, content_length):
        query = "UPDATE Medicines SET ContentLength = (?) WHERE MedicineID = (?)"
        self.con.execute(query, (content_length, medicine_id))

    def delete_medicine_excipents_from_table(self, medicine_id):
        query = "DELETE FROM MedicinesExcipents WHERE MedicineID = (?)"
        self.con.execute(query, [str(medicine_id)])

    def delete_ean_codes_from_table(self, medicine_id):
        query = "DELETE FROM EanTable WHERE MedicineID = (?)"
        self.con.execute(query, [str(medicine_id)])

    def __enter__(self):
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        if isinstance(exc_value, Exception):
            self.con.rollback()
        else:
            self.con.commit()

        self.con.close()


with MedicineDatabase('models/medicine.db') as db:
    db.create_medicine_table()
    db.create_active_substances_table()
    db.create_excipents_table()
    db.create_ean_table()
    db.create_medicines_active_substances_table()
    db.create_medicines_active_substances_values_table()
    db.create_medicines_excipents_table()