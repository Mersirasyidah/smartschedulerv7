"""
====================================================
SMART SCHEDULER V2
VARIABLE BUILDER
====================================================
"""

from ortools.sat.python import cp_model


class VariableBuilder:

    def __init__(self, loader, calendar):

        self.loader = loader

        self.calendar = calendar

        self.model = cp_model.CpModel()

        self.x = {}

    # ==================================================
    # MEMBUAT VARIABLE
    # ==================================================

    def build(self):

        print("=" * 60)
        print("MEMBUAT VARIABLE AI")
        print("=" * 60)

        jumlah = 0

        for _, row in self.loader.mengajar.iterrows():

            guru = row[self.loader.col_guru]

            kelas = row[self.loader.col_kelas]

            mapel = row[self.loader.col_mapel]

            for slot in self.calendar.slot:

                key = (

                    guru,

                    kelas,

                    mapel,

                    slot["hari"],

                    slot["jam"]

                )

                self.x[key] = self.model.NewBoolVar(

                    f"x_{jumlah}"

                )

                jumlah += 1

        print("Jumlah Variable :", jumlah)

        print("=" * 60)

    # ==================================================
    # AMBIL VARIABLE
    # ==================================================

    def get(

        self,

        guru,

        kelas,

        mapel,

        hari,

        jam

    ):

        return self.x.get(

            (

                guru,

                kelas,

                mapel,

                hari,

                jam

            )

        )

    # ==================================================
    # SEMUA VARIABLE
    # ==================================================

    def all(self):

        return self.x

    # ==================================================
    # PREVIEW
    # ==================================================

    def preview(self, jumlah=20):

        print("=" * 60)
        print("PREVIEW VARIABLE")
        print("=" * 60)

        i = 0

        for k in self.x:

            print(k)

            i += 1

            if i >= jumlah:

                break

        print("=" * 60)

    # ==================================================
    # STATISTIK
    # ==================================================

    def statistics(self):

        print("=" * 60)
        print("STATISTIK VARIABLE")
        print("=" * 60)

        print("Total Variable :", len(self.x))

        print("=" * 60)
