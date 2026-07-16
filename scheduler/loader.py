class DataLoader:

    def __init__(self, database):

        self.database = database


    def load_all(self):

        self.guru = self.database["Guru"]

        self.mapel = self.database["Mapel"]

        self.rombel = self.database["Rombel"]

        self.mengajar = self.database["Guru_Mengajar"]

        self.hari_jam = self.database["Hari_Jam"]


        print("Guru :", len(self.guru))

        print("Mapel :", len(self.mapel))

        print("Rombel :", len(self.rombel))

        print("Mengajar :", len(self.mengajar))

        print("HariJam :", len(self.hari_jam))
