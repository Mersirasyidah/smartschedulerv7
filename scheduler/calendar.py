"""
====================================================
SMART SCHEDULER V2
CALENDAR ENGINE
====================================================
"""

from collections import defaultdict


class CalendarEngine:

    def __init__(self, loader):

        self.loader = loader

        self.slot = []

        self.slot_index = {}

        self.day_slots = defaultdict(list)

        self.total_slot = 0

    # ==================================================
    # MEMBANGUN SLOT PEMBELAJARAN
    # ==================================================

    def build(self):

        print("=" * 60)
        print("MEMBANGUN CALENDAR")
        print("=" * 60)

        nomor = 1

        self.slot = []
        self.slot_index = {}
        self.day_slots = defaultdict(list)

        for _, row in self.loader.hari_jam.iterrows():

            hari = row[self.loader.col_hari]

            jam = int(row[self.loader.col_jam])

            jenis = str(
                row[self.loader.col_jenis]
            ).strip().lower()

            # hanya slot pembelajaran
            if jenis != "pembelajaran":
                continue

            item = {

                "id": nomor,

                "hari": hari,

                "jam": jam

            }

            self.slot.append(item)

            self.slot_index[(hari, jam)] = item

            self.day_slots[hari].append(item)

            nomor += 1

        # urutkan setiap hari
        for hari in self.day_slots:

            self.day_slots[hari] = sorted(

                self.day_slots[hari],

                key=lambda x: x["jam"]

            )

        self.total_slot = len(self.slot)

        print("Total Slot :", self.total_slot)

        print("=" * 60)

    # ==================================================
    # SEMUA SLOT
    # ==================================================

    def get_slots(self):

        return self.slot

    # ==================================================
    # SLOT PER HARI
    # ==================================================

    def get_slots_by_day(self, hari):

        return self.day_slots.get(hari, [])

    # ==================================================
    # SLOT BERDASARKAN HARI DAN JAM
    # ==================================================

    def get_slot(self, hari, jam):

        return self.slot_index.get(

            (hari, jam),

            None

        )

    # ==================================================
    # SLOT BERIKUTNYA
    # ==================================================

    def next_slot(self, hari, jam):

        data = self.day_slots.get(hari, [])

        for i in range(len(data) - 1):

            if data[i]["jam"] == jam:

                return data[i + 1]

        return None

    # ==================================================
    # SLOT SEBELUMNYA
    # ==================================================

    def previous_slot(self, hari, jam):

        data = self.day_slots.get(hari, [])

        for i in range(1, len(data)):

            if data[i]["jam"] == jam:

                return data[i - 1]

        return None

    # ==================================================
    # SLOT BERURUTAN
    # ==================================================

    def consecutive_slots(

        self,

        hari,

        jam,

        panjang

    ):

        hasil = []

        data = self.day_slots.get(hari, [])

        posisi = None

        for i, slot in enumerate(data):

            if slot["jam"] == jam:

                posisi = i

                break

        if posisi is None:

            return hasil

        akhir = posisi + panjang

        if akhir > len(data):

            return hasil

        hasil = data[posisi:akhir]

        if len(hasil) != panjang:

            return []

        # memastikan jam benar-benar berurutan
        for i in range(len(hasil) - 1):

            if hasil[i + 1]["jam"] != hasil[i]["jam"] + 1:

                return []

        return hasil

    # ==================================================
    # DAFTAR HARI
    # ==================================================

    def days(self):

        return list(self.day_slots.keys())

    # ==================================================
    # JUMLAH SLOT HARI
    # ==================================================

    def total_slot_day(self, hari):

        return len(

            self.day_slots.get(hari, [])

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
        print("STATISTIK CALENDAR")
        print("=" * 60)

        print("Total Slot :", self.total_slot)

        for hari in self.day_slots:

            print(

                f"{hari:10} : "

                f"{len(self.day_slots[hari])} slot"

            )

        print("=" * 60)
