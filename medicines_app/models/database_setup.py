import sqlite3
from pathlib import Path
import os


class MedicineDatabase:
    def __init__(self, path):
        # self.path = self.get_path(path)
        self.con = sqlite3.connect(path)

    def get_path(self, path):
        if os.path.exists(path):
            print(path)
            return path
        print(path.replace('/', '\\'))
        return path.replace('/', '\\')

    def chk_conn(self, conn):
        try:
            conn.cursor()
            return True
        except Exception as ex:
            return False

    # "(Path(path).absolute().as_uri())"
    def create_medicine_table(self):
        medicine_table = '''CREATE TABLE IF NOT EXISTS Medicines(
                            MedicineID INTEGER PRIMARY KEY,
                            Name TEXT NOT NULL,
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

    def create_medicines_active_substances_details_table(self):
        medicine_active_substances_details_table = '''CREATE TABLE IF NOT EXISTS MedicinesActiveSubstancesDetails (
                                                ID INTEGER PRIMARY KEY,
                                                Concentration TEXT NOT NULL,
                                                Unit TEXT NOT NULL,
                                                FOREIGN KEY(ID) REFERENCES MedicinesActiveSubstances (ID)
                                                ); '''
        self.con.execute(medicine_active_substances_details_table)

    def create_ean_table(self):
        ean_table = '''CREATE TABLE IF NOT EXISTS EanTable(
                    EanID INTEGER PRIMARY KEY,
                    EanNumber INTEGER NOT NULL,
                    MedicineID INTEGER NOT NULL,
                    FOREIGN KEY(MedicineID) REFERENCES Medicines (MedicineID)
                    ); '''
        self.con.execute(ean_table)

    def create_tmp_table(self):
        tmp_table = '''CREATE TABLE IF NOT EXISTS tmp(
                    MedicineID INTEGER,
                    Name TEXT,
                    Description TEXT,
                    Form TEXT,
                    ActiveSubstanceID INTEGER,
                    Concentration TEXT,
                    Unit TEXT
                    );'''
        self.con.execute(tmp_table)

    def add_medicine_to_table(self, medicine_id, name, form, content_length):
        medicine = "INSERT INTO Medicines(medicineId, name, form, ContentLength) VALUES (?, ?, ?, ?)"
        self.con.execute(medicine, (medicine_id, name, form, content_length))

    def add_active_substance_to_table(self, name):
        query_substance = "INSERT INTO ActiveSubstances(Name) VALUES (?)"
        self.con.execute(query_substance, [name])

    def add_to_table_medicines_active_substances(self, medicine_id, active_substance_id):
        query = "INSERT INTO MedicinesActiveSubstances " \
                "(MedicineID, ActiveSubstanceId) VALUES (?, ?)"
        self.con.execute(query, (medicine_id, str(active_substance_id[0])))

    def add_to_table_medicines_active_substances_details(self, medicines_active_substances_id, concentration, unit):
        query = "INSERT INTO MedicinesActiveSubstancesDetails " \
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
        query_medicine_id = "SELECT * FROM Medicines WHERE MedicineID = ? "
        return self.con.execute(query_medicine_id, [medicine_id]).fetchone()

    def get_medicine_id_by_name(self, name: str):
        query = 'SELECT Medicines.MedicineID FROM Medicines WHERE Medicines.Name = (?) '
        return self.con.execute(query, [name]).fetchone()

    def get_medicine_id_by_ean(self, ean:int):
        query = f'SELECT EanTable.MedicineID FROM EanTable WHERE EanTable.EanNumber = (?)'
        return self.con.execute(query, [ean]).fetchone()

    def get_medicines_active_substances_id(self, medicine_id, active_substance_id):
        query = "SELECT ID FROM MedicinesActiveSubstances WHERE MedicineID = (?) AND ActiveSubstanceId = (?)"
        return self.con.execute(query, (medicine_id, str(active_substance_id[0]))).fetchone()

    def get_active_substances_details(self, medicine_id):
        query = """SELECT ActiveSubstances.Name, MedicinesActiveSubstancesDetails.Concentration, MedicinesActiveSubstancesDetails.Unit
                    FROM ActiveSubstances, MedicinesActiveSubstances, MedicinesActiveSubstancesDetails, Medicines
                    WHERE Medicines.MedicineID = MedicinesActiveSubstances.MedicineID
                    AND MedicinesActiveSubstances.ActiveSubstanceID = ActiveSubstances.ActiveSubstanceID
                    AND MedicinesActiveSubstances.ID = MedicinesActiveSubstancesDetails.ID
                    AND Medicines.MedicineID = (?)"""
        return self.con.execute(query, [str(medicine_id)])

    def get_medicines_by_name_like(self, part_name):
        query = f'SELECT Medicines.Name FROM Medicines WHERE Medicines.Name LIKE "{part_name}%" ORDER BY Medicines.Name'
        return self.con.execute(query).fetchall()

    def get_medicine_equivalents(self):
        query = f"""
                SELECT
                TAB1.MedicineID 
                ,MED.Name 
                ,MED.Form 
                ,MAS.ActiveSubstanceID 
                ,EAN.EanNumber 
                ,DET.Concentration 
                ,DET.Unit 
                ,ACT.Name 
                FROM 
                    (
                    SELECT MedicineID FROM 	
                        (
                        SELECT X.*, U.cnt 
                        FROM MedicinesActiveSubstances X, MedicinesActiveSubstancesDetails Z
                        LEFT JOIN (		SELECT Y.MedicineID, Count(Y.ActiveSubstanceID) cnt	
                        FROM MedicinesActiveSubstances Y GROUP BY Y.medicineID		) U 
                        ON U.MedicineID = X.MedicineID
                        WHERE X.ID = Z.ID 
                        AND X.ActiveSubstanceID in (SELECT tmp.ActiveSubstanceID FROM tmp)
                        AND Z.Concentration in 
                            (SELECT tmp.Concentration
                             FROM tmp 
                             WHERE Z.ID = X.ID AND X.ActiveSubstanceID = tmp.ActiveSubstanceID)
                        AND Z.Unit in 
                        (SELECT tmp.Unit FROM tmp WHERE Z.ID = X.ID AND X.ActiveSubstanceID = tmp.ActiveSubstanceID)
                        ) MEDID 
                    WHERE cnt = (SELECT count(1) FROM tmp)
                    GROUP BY MEDID.MedicineID HAVING count(cnt)= (SELECT count(1) FROM tmp)
                    ) TAB1
                LEFT JOIN Medicines MED on MED.MedicineID = TAB1.MedicineID 
                LEFT JOIN MedicinesActiveSubstances MAS on MAS.MedicineID = TAB1.MedicineID 
                LEFT JOIN EanTable EAN on EAN.MedicineID = TAB1.MedicineID 
                LEFT JOIN MedicinesActiveSubstancesDetails DET on DET.ID = MAS.ID 
                LEFT JOIN ActiveSubstances ACT on ACT.ActiveSubstanceID = MAS.ActiveSubstanceID
                WHERE TAB1.MedicineID <> (SELECT tmp.MedicineID FROM tmp)
                GROUP BY TAB1.MedicineID
                ORDER BY MED.Name
                """
        return self.con.execute(query).fetchall()

    def get_medicinal_product_excipents(self, medicine_id):
        query = f"""
                SELECT Excipents.Name
                FROM Medicines, Excipents, MedicinesExcipents
                WHERE Medicines.MedicineID = MedicinesExcipents.MedicineID
                AND MedicinesExcipents.ExcipentID = Excipents.ExcipentID
                AND Medicines.MedicineID = {medicine_id}
                """
        return self.con.execute(query)

    def set_content_length(self, medicine_id, content_length):
        query = "UPDATE Medicines SET ContentLength = (?) WHERE MedicineID = (?)"
        self.con.execute(query, (content_length, medicine_id))

    def delete_medicine_excipents_from_table(self, medicine_id):
        query = "DELETE FROM MedicinesExcipents WHERE MedicineID = (?)"
        self.con.execute(query, [str(medicine_id)])

    def delete_ean_codes_from_table(self, medicine_id):
        query = "DELETE FROM EanTable WHERE MedicineID = (?)"
        self.con.execute(query, [str(medicine_id)])

    def delete_from_tmp(self):
        query = 'DELETE FROM tmp;'
        self.con.execute(query)

    def insert_into_tmp(self, medicine_id):
        query = f'''INSERT INTO tmp 
                SELECT MED.MedicineID, MED.Name, MED.Form, 
                    MAS.ActiveSubstanceID, DET.Concentration, DET.Unit
                FROM MedicinesActiveSubstances MAS, MedicinesActiveSubstancesDetails DET
                INNER JOIN Medicines MED on MAS.MedicineID = MED.MedicineID
                INNER JOIN MedicinesActiveSubstances on MAS.ID = DET.ID
                WHERE MED.MedicineID = (?)
                GROUP BY MAS.ActiveSubstanceID'''
        self.con.execute(query, [str(medicine_id)])

    def __enter__(self):
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        if isinstance(exc_value, Exception):
            self.con.rollback()
        else:
            self.con.commit()

        self.con.close()


with MedicineDatabase('medicine.db') as db:
    db.create_medicine_table()
    db.create_active_substances_table()
    db.create_excipents_table()
    db.create_ean_table()
    db.create_medicines_active_substances_table()
    db.create_medicines_active_substances_details_table()
    db.create_medicines_excipents_table()
    db.create_tmp_table()

# with MedicineDatabase('../models/medicine.db') as db:
#     db.create_medicine_table()
#     db.create_active_substances_table()
#     db.create_excipents_table()
#     db.create_ean_table()
#     db.create_medicines_active_substances_table()
#     db.create_medicines_active_substances_details_table()
#     db.create_medicines_excipents_table()
#     db.create_tmp_table()
