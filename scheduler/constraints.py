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

"""
====================================================
SMART SCHEDULER V2
CONSTRAINT BUILDER
====================================================
"""

from ortools.sat.python import cp_model


class ConstraintBuilder:

    def __init__(self, loader, calendar, variables):

        self.loader = loader
        self.calendar = calendar
        self.variables = variables
        self.model = variables.model

    # ==================================================
    # BUILD
    # ==================================================

    def build(self):

        print("=" * 60)
        print("MEMASANG CONSTRAINT")
        print("=" * 60)

        self.constraint_guru()

        self.constraint_kelas()

        self.constraint_jp()

        print("=" * 60)
        print("SEMUA CONSTRAINT TERPASANG")
        print("=" * 60)

    # ==================================================
    # GURU
    # ==================================================

    def constraint_guru(self):

        print("Constraint Guru")

        guru_list = self.loader.mengajar[
            self.loader.col_guru
        ].unique()

        total = 0

        for guru in guru_list:

            for slot in self.calendar.slot:

                hari = slot["hari"]
                jam = slot["jam"]

                vars_slot = []

                data = self.loader.mengajar[
                    self.loader.mengajar[
                        self.loader.col_guru
                    ] == guru
                ]

                for _, row in data.iterrows():

                    var = self.variables.get(

                        guru,

                        row[self.loader.col_kelas],

                        row[self.loader.col_mapel],

                        hari,

                        jam

                    )

                    if var:

                        vars_slot.append(var)

                if len(vars_slot) > 1:

                    self.model.Add(

                        sum(vars_slot) <= 1

                    )

                    total += 1

        print("Constraint Guru :", total)

    # ==================================================
    # KELAS
    # ==================================================

    def constraint_kelas(self):

        print("Constraint Kelas")

        kelas_list = self.loader.mengajar[
            self.loader.col_kelas
        ].unique()

        total = 0

        for kelas in kelas_list:

            for slot in self.calendar.slot:

                hari = slot["hari"]
                jam = slot["jam"]

                vars_slot = []

                data = self.loader.mengajar[
                    self.loader.mengajar[
                        self.loader.col_kelas
                    ] == kelas
                ]

                for _, row in data.iterrows():

                    var = self.variables.get(

                        row[self.loader.col_guru],

                        kelas,

                        row[self.loader.col_mapel],

                        hari,

                        jam

                    )

                    if var:

                        vars_slot.append(var)

                if len(vars_slot) > 1:

                    self.model.Add(

                        sum(vars_slot) <= 1

                    )

                    total += 1

        print("Constraint Kelas :", total)

    # ==================================================
    # JP
    # ==================================================

    def constraint_jp(self):

        print("Constraint JP")

        total = 0

        for _, row in self.loader.mengajar.iterrows():

            guru = row[self.loader.col_guru]

            kelas = row[self.loader.col_kelas]

            mapel = row[self.loader.col_mapel]

            jp = int(

                row[self.loader.col_jp]

            )

            daftar = []

            for slot in self.calendar.slot:

                var = self.variables.get(

                    guru,

                    kelas,

                    mapel,

                    slot["hari"],

                    slot["jam"]

                )

                if var:

                    daftar.append(var)

            if len(daftar) > 0:

                self.model.Add(

                    sum(daftar) == jp

                )

                total += 1

        print("Constraint JP :", total)


