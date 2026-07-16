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

        self.constraint_kelas()

        print("=" * 60)
        print("SEMUA CONSTRAINT BERHASIL DIPASANG")
        print("=" * 60)

    # ==================================================
    # CONSTRAINT GURU
    # Guru tidak boleh mengajar 2 kelas pada jam yang sama
    # ==================================================

    def constraint_guru(self):

        print("Memasang Constraint Guru...")

        total = 0

        daftar_guru = self.loader.mengajar[
            self.loader.col_guru
        ].unique()

        for guru in daftar_guru:

            for slot in self.calendar.slot:

                hari = slot["hari"]
                jam = slot["jam"]

                variable = []

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

                        variable.append(var)

                if len(variable) > 1:

                    self.model.Add(

                        sum(variable) <= 1

                    )

                    total += 1

        print("Constraint Guru :", total)

    # ==================================================
    # CONSTRAINT KELAS
    # Satu kelas hanya boleh memiliki
    # satu mapel pada satu jam
    # ==================================================

    def constraint_kelas(self):

        print("Memasang Constraint Kelas...")

        total = 0

        daftar_kelas = self.loader.mengajar[
            self.loader.col_kelas
        ].unique()

        for kelas in daftar_kelas:

            for slot in self.calendar.slot:

                hari = slot["hari"]
                jam = slot["jam"]

                variable = []

                data = self.loader.mengajar[
                    self.loader.mengajar[
                        self.loader.col_kelas
                    ] == kelas
                ]

                for _, row in data.iterrows():

                    guru = row[self.loader.col_guru]

                    mapel = row[self.loader.col_mapel]

                    var = self.variables.get(

                        guru,

                        kelas,

                        mapel,

                        hari,

                        jam

                    )

                    if var is not None:

                        variable.append(var)

                if len(variable) > 1:

                    self.model.Add(

                        sum(variable) <= 1

                    )

                    total += 1

        print("Constraint Kelas :", total)
