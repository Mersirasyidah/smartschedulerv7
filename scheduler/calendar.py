class CalendarEngine:

    def __init__(self, loader):

        self.loader = loader

        self.slot = []


    def build(self):

        nomor = 0

        df = self.loader.hari_jam


        for _, row in df.iterrows():

            if row["Jenis"] != "Pembelajaran":
                continue

            self.slot.append({

                "id": nomor,

                "hari": row["Hari"],

                "jam": int(row["Jam"])

            })

            nomor += 1


        print("Slot Pembelajaran :", len(self.slot))
