"""
====================================================
SMART SCHEDULER V2
SOLVER ENGINE
====================================================
"""

import time
import pandas as pd
from ortools.sat.python import cp_model
from constraints import ConstraintBuilder


class ScheduleVariables:
    """
    Menyimpan dan mengelola semua variabel keputusan boolean (BoolVar) 
    untuk pencocokan antara Guru, Kelas, Mapel, Hari, dan Jam.
    """

    def __init__(self, model, loader, calendar):
        self.model = model
        self.vars = {}

        # Membangun variabel keputusan (0 atau 1) untuk setiap kombinasi pengajaran & slot kalender aktif
        for _, row in loader.mengajar.iterrows():
            guru = row[loader.col_guru]
            kelas = row[loader.col_kelas]
            mapel = row[loader.col_mapel]

            for slot in calendar.slot:
                hari = slot["hari"]
                jam = slot["jam"]

                key = (guru, kelas, mapel, hari, jam)
                # Membuat variabel boolean unik di dalam model OR-Tools
                self.vars[key] = model.NewBoolVar(
                    f"x_{guru.replace(' ', '_')}_{kelas.replace(' ', '_')}_{mapel.replace(' ', '_')}_{hari}_{jam}"
                )

    def get(self, guru, kelas, mapel, hari, jam):
        """Mengambil variabel keputusan berdasarkan spesifikasi parameter."""
        return self.vars.get((guru, kelas, mapel, hari, jam), None)


class SchedulerSolver:

    def __init__(self, loader, calendar):
        self.loader = loader
        self.calendar = calendar
        self.model = cp_model.CpModel()
        self.solver = cp_model.CpSolver()
        self.variables = None
        self.status = None
        self.runtime = 0.0

    # ==================================================
    # PROSES SOLVING JADWAL
    # ==================================================

    def solve(self, timeout_seconds=60.0):
        print("=" * 60)
        print("MEMULAI PROSES SOLVER")
        print("=" * 60)

        start_time = time.time()

        # 1. Bangun Variabel Keputusan
        print("Membangun Variabel Keputusan...")
        self.variables = ScheduleVariables(self.model, self.loader, self.calendar)

        # 2. Bangun & Pasang Semua Constraint menggunakan ConstraintBuilder
        builder = ConstraintBuilder(self.loader, self.calendar, self.variables)
        builder.build()

        # 3. Pengaturan Solver (Waktu Maksimal & Threading)
        self.solver.parameters.max_time_in_seconds = timeout_seconds
        self.solver.parameters.num_search_workers = 8  # Mempercepat proses pencarian (multithreading)

        # 4. Eksekusi Proses Optimalisasi
        print("Menghitung Kombinasi Optimal (CP-SAT)...")
        self.status = self.solver.Solve(self.model)
        self.runtime = time.time() - start_time

        print("=" * 60)
        print(f"Status Solver : {self.solver.StatusName(self.status)}")
        print(f"Waktu Proses  : {self.runtime:.2f} detik")
        print("=" * 60)

        # Mengembalikan status kelayakan penjadwalan
        return self.status == cp_model.OPTIMAL or self.status == cp_model.FEASIBLE

    # ==================================================
    # EKSTRAKSI HASIL JADWAL KE DATAFRAME
    # ==================================================

    def get_results(self):
        """
        Mengekstrak hasil keputusan solver yang bernilai 1 (aktif)
        menjadi list of dict / DataFrame yang siap digunakan oleh exporter.
        """
        if self.status not in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            print("Peringatan: Tidak ada jadwal layak (feasible) yang ditemukan.")
            return pd.DataFrame()

        hasil_jadwal = []

        for _, row in self.loader.mengajar.iterrows():
            guru = row[self.loader.col_guru]
            kelas = row[self.loader.col_kelas]
            mapel = row[self.loader.col_mapel]

            for slot in self.calendar.slot:
                hari = slot["hari"]
                jam = slot["jam"]

                var = self.variables.get(guru, kelas, mapel, hari, jam)

                # Jika variabel bernilai True (1), artinya slot tersebut berhasil dijadwalkan
                if var is not None and self.solver.Value(var) == 1:
                    hasil_jadwal.append({
                        "Hari": hari,
                        "Jam": jam,
                        "Kelas": kelas,
                        "Guru": guru,
                        "Mata Pelajaran": mapel
                    })

        # Urutkan berdasarkan Hari dan Jam agar rapi
        df_hasil = pd.DataFrame(hasil_jadwal)
        if not df_hasil.empty:
            df_hasil = df_hasil.sort_values(by=["Hari", "Jam"]).reset_index(drop=True)

        return df_hasil
