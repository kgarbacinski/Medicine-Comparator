import sqlite3


class MedicineDatabase:
    def __init__(self, path):
        self.con = sqlite3.connect(path)

    def create_medicine_table(self):
        medicine_table = '''CREATE TABLE IF NOT EXISTS Medicines(
                            MedicineID INTEGER PRIMARY KEY,
                            Name TEXT NOT NULL,
                            Form TEXT NOT NULL,
                            ContentLenght INTEGER NOT NULL
                            ); '''
        self.con.execute(medicine_table)

    def create_excipents_table(self):
        excipents_table = '''CREATE TABLE IF NOT EXISTS Excipents (
                            ExcipentsID INTEGER PRIMARY KEY,
                            Name TEXT NOT NULL,
                            MedicineID INTEGER NOT NULL,
                            FOREIGN KEY (MedicineID) REFERENCES Medicines (MedicineID)
                            ); '''
        self.con.execute(excipents_table)

    def create_active_substances_table(self):
        active_substances_table = '''CREATE TABLE IF NOT EXISTS ActiveSubstances(
                                    ActiveSubstanceID INTEGER PRIMARY KEY,
                                    Name TEXT NOT NULL,
                                    Concentration INTEGER NOT NULL,
                                    Unit type TEXT NOT NULL,
                                    MedicineID INTEGER NOT NULL,
                                    FOREIGN KEY (MedicineID) REFERENCES Medicines (MedicineID)
                                    ); '''
        self.con.execute(active_substances_table)

    def create_ean_table(self):
        ean_table = '''CREATE TABLE IF NOT EXISTS EanTable(
                    EanID INTEGER PRIMARY KEY,
                    EanNumber INTEGER NOT NULL,
                    MedicineID INTEGER NOT NULL,
                    FOREIGN KEY(MedicineID) REFERENCES Medicines (MedicineID)
                    ); '''
        self.con.execute(ean_table)

    def add_medicine_to_table(self, name, form):
        medicine = "INSERT INTO Medicines(name, form) VALUES (?, ?)"
        self.con.execute(medicine, (name, form))

    def add_active_substance_to_table(self, name, concentration, unit):
        active_substace = "INSERT INTO ActiveSubstances(Name, Concentration, Unit type) VALUES (?, ?, ?)"
        self.con.execute(active_substace, (name, concentration, unit))

    def add_excipents_to_table(self, name):
        excipent = "INSERT INTO Excipents (Name) VALUES (?)"
        self.con.execute(excipent, (name))

    def add_ean_to_table(self, ean_number):
        ean = "INSERT INTO EanTable (EanNumber) VALUES (?)"
        self.con.execute(ean, (ean_number))

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
