# constraints.py
from ortools.sat.python import cp_model


class ConstraintBuilder:

    def __init__(self, loader, calendar, variables):
        self.loader = loader
        self.calendar = calendar
        self.variables = variables
        self.model = variables.model

    # ==================================================
    # BUILD SEMUA CONSTRAINT
    # ==================================================

    def build(self):
        print("=" * 60)
        print("MEMASANG CONSTRAINT (SMART SCHEDULER V2)")
        print("=" * 60)

        self.constraint_guru()
        self.constraint_kelas()
        self.constraint_jp()

        print("=" * 60)
        print("SEMUA CONSTRAINT BERHASIL DIPASANG")
        print("=" * 60)

    # ==================================================
    # GURU
    # Guru tidak boleh mengajar lebih dari 1 kelas pada hari & jam yang sama
    # ==================================================

    def constraint_guru(self):
        print("Memasang Constraint Guru...")
        
        guru_list = self.loader.mengajar[
            self.loader.col_guru
        ].unique()
        
        total = 0

        for guru in guru_list:
            for slot in self.calendar.slot:
                hari = slot["hari"]
                jam = slot["jam"]
                vars_slot = []

                # Ambil subset data pengajaran milik guru yang bersangkutan
                data = self.loader.mengajar[
                    self.loader.mengajar[self.loader.col_guru] == guru
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
                        vars_slot.append(var)

                # Jika ada potensi konflik mengajar di slot yang sama
                if len(vars_slot) > 1:
                    self.model.Add(
                        sum(vars_slot) <= 1
                    )
                    total += 1

        print("Constraint Guru Terpasang:", total)

    # ==================================================
    # KELAS / ROMBEL
    # Satu kelas hanya boleh mengikuti maksimal 1 mapel pada hari & jam yang sama
    # ==================================================

    def constraint_kelas(self):
        print("Memasang Constraint Kelas...")
        
        kelas_list = self.loader.mengajar[
            self.loader.col_kelas
        ].unique()
        
        total = 0

        for kelas in kelas_list:
            for slot in self.calendar.slot:
                hari = slot["hari"]
                jam = slot["jam"]
                vars_slot = []

                # Ambil subset data pengajaran milik kelas yang bersangkutan
                data = self.loader.mengajar[
                    self.loader.mengajar[self.loader.col_kelas] == kelas
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
                        vars_slot.append(var)

                # Jika ada potensi bentrok mata pelajaran dalam kelas pada slot tersebut
                if len(vars_slot) > 1:
                    self.model.Add(
                        sum(vars_slot) <= 1
                    )
                    total += 1

        print("Constraint Kelas Terpasang:", total)

    # ==================================================
    # JAM PELAJARAN (JP)
    # Memastikan jumlah total slot mengajar sama dengan kuota JP
    # ==================================================

    def constraint_jp(self):
        print("Memasang Constraint Jam Pelajaran (JP)...")
        
        total = 0

        for _, row in self.loader.mengajar.iterrows():
            guru = row[self.loader.col_guru]
            kelas = row[self.loader.col_kelas]
            mapel = row[self.loader.col_mapel]
            jp = int(row[self.loader.col_jp])

            daftar = []

            for slot in self.calendar.slot:
                var = self.variables.get(
                    guru,
                    kelas,
                    mapel,
                    slot["hari"],
                    slot["jam"]
                )
                
                if var is not None:
                    daftar.append(var)

            if len(daftar) > 0:
                # Total slot yang terisi harus pas dengan target JP pada file data mengajar
                self.model.Add(
                    sum(daftar) == jp
                )
                total += 1

        print("Constraint JP Terpasang:", total)
