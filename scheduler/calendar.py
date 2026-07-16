"""
====================================================
SMART SCHEDULER V2
CALENDAR ENGINE
====================================================
"""

class CalendarEngine:

    def __init__(self, loader):

        self.loader = loader

        self.slot = []

        self.slot_index = {}

    # ==================================================
    # MEMBUAT SLOT PEMBELAJARAN
    # ==================================================

    def build(self):

        print("=" * 60)
        print("MEMBANGUN SLOT PEMBELAJARAN")
        print("=" * 60)

        nomor = 1

        for _, row in self.loader.hari_jam.iterrows():

            hari = row[self.loader.col_hari]

            jam = int(row[self.loader.col_jam])

            jenis = str(
                row[self.loader.col_jenis]
            ).strip().lower()

            # hanya slot pembelajaran
            if jenis != "pembelajaran":
                continue

            self.slot.append({

                "id": nomor,

                "hari": hari,

                "jam": jam

            })

            self.slot_index[(hari, jam)] = nomor

            nomor += 1

        print("Jumlah Slot :", len(self.slot))

        print("=" * 60)

    # ==================================================
    # MENGAMBIL SLOT
    # ==================================================

    def get_slots(self):

        return self.slot

    # ==================================================
    # MENGAMBIL SLOT BERDASARKAN HARI
    # ==================================================

    def get_slots_by_day(self, hari):

        hasil = []

        for slot in self.slot:

            if slot["hari"] == hari:

                hasil.append(slot)

        return hasil

    # ==================================================
    # MENGAMBIL SLOT BERDASARKAN JAM
    # ==================================================

    def get_slots_by_hour(self, jam):

        hasil = []

        for slot in self.slot:

            if slot["jam"] == jam:

                hasil.append(slot)

        return hasil

    # ==================================================
    # CARI SLOT
    # ==================================================

    def find_slot(self, hari, jam):

        return self.slot_index.get(

            (hari, jam),

            None

        )

    # ==================================================
    # PREVIEW
    # ==================================================

    def preview(self, jumlah=20):

        print("=" * 60)
        print("PREVIEW SLOT")
        print("=" * 60)

        for row in self.slot[:jumlah]:

            print(row)

        print("=" * 60)

    # ==================================================
    # STATISTIK
    # ==================================================

    def statistics(self):

        print("=" * 60)
        print("STATISTIK SLOT")
        print("=" * 60)

        hari = {}

        for slot in self.slot:

            h = slot["hari"]

            hari[h] = hari.get(h, 0) + 1

        for h in hari:

            print(f"{h:10} : {hari[h]} slot")

        print("=" * 60)
