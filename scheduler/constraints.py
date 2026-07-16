"""
====================================================
SMART SCHEDULER V2
CONSTRAINT BUILDER
====================================================
"""

from ortools.sat.python import cp_model


class ConstraintBuilder:

    def __init__(

        self,

        loader,

        calendar,

        variables

    ):

        self.loader = loader

        self.calendar = calendar

        self.variables = variables

        self.model = variables.model


    # ==================================================
    # BUILD SEMUA CONSTRAINT
    # ==================================================

    def build(self):

        print("=" * 60)
        print("MEMASANG CONSTRAINT")
        print("=" * 60)

        self.constraint_guru()

        print("=" * 60)


    # ==================================================
    # GURU TIDAK BOLEH BENTROK
    # ==================================================

    def constraint_guru(self):

        print("Constraint Guru ...")

        total = 0

        daftar_guru = self.loader.mengajar[
            self.loader.col_guru
        ].unique()

        for guru in daftar_guru:

            for slot in self.calendar.slot:

                hari = slot["hari"]

                jam = slot["jam"]

                daftar_variable = []

                data = self.loader.mengajar[
                    self.loader.mengajar[
                        self.loader.col_guru
                    ] == guru
                ]

                for _, row in data.iterrows():

                    kelas = row[self.loader.col_kelas]

                    mapel = row[self.loader.col_mapel]

                    var = self.variables.get(

                        guru,

                        kelas,

                        mapel,

                        hari,

                        jam

                    )

                    if var is not None:

                        daftar_variable.append(var)

                if len(daftar_variable) > 1:

                    self.model.Add(

                        sum(daftar_variable) <= 1

                    )

                    total += 1

        print("Constraint Guru :", total)
