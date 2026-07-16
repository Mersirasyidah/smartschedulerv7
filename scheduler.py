"""
=============================================================
SMART SCHEDULER V2
Version 2.0
=============================================================

AI Timetable Generator
Menggunakan Google OR-Tools CP-SAT

=============================================================
"""

import pandas as pd
import numpy as np
from collections import defaultdict

try:
    from ortools.sat.python import cp_model
    ORTOOLS = True
except ImportError:
    ORTOOLS = False

# Import modul internal scheduler V2
from solver import SchedulerSolver
from exporter import ScheduleExporter


class Scheduler:
    """
    =========================================================
    SMART SCHEDULER ENGINE V2
    =========================================================
    Orkestrator utama untuk pembacaan data, inisialisasi
    variabel, kompilasi constraint, pemecahan masalah (solving),
    hingga pengeksporan jadwal ke format Excel.
    """

    # =====================================================
    # INIT
    # =====================================================

    def __init__(self, database):
        self.db = database
        self.model = cp_model.CpModel() if ORTOOLS else None
        self.variables = {}
        self.index = []
        self.slot = []
        self.df_hasil = pd.DataFrame()
        
        self.load_database()

    # =====================================================
    # LOAD DATABASE
    # =====================================================

    def load_database(self):
        print("="*60)
        print("MEMBACA DATABASE")
        print("="*60)

        self.guru = self.db["Guru"].copy()
        self.mapel = self.db["Mapel"].copy()
        self.rombel = self.db["Rombel"].copy()
        self.mengajar = self.db["Guru_Mengajar"].copy()
        self.hari_jam = self.db["Hari_Jam"].copy()

        print("Guru           :", len(self.guru))
        print("Mapel          :", len(self.mapel))
        print("Rombel         :", len(self.rombel))
        print("Mengajar       :", len(self.mengajar))
        print("Hari_Jam       :", len(self.hari_jam))
        print("="*60)

        self.detect_column()

    # =====================================================
    # DETEKSI KOLOM OTOMATIS
    # =====================================================

    def detect(self, df, kandidat):
        for k in kandidat:
            if k in df.columns:
                return k
        return None

    def detect_column(self):
        self.col_guru = self.detect(
            self.mengajar,
            ["Nama Guru", "nama_guru", "Guru", "guru"]
        )
        self.col_mapel = self.detect(
            self.mengajar,
            ["Mapel", "mapel"]
        )
        self.col_kelas = self.detect(
            self.mengajar,
            ["Kelas", "kelas"]
        )
        self.col_jp = self.detect(
            self.mengajar,
            ["JP", "jp"]
        )
        self.col_pembagian = self.detect(
            self.mengajar,
            ["Pembagian", "pembagian"]
        )
        self.col_hari = self.detect(
            self.hari_jam,
            ["Hari"]
        )
        self.col_jam = self.detect(
            self.hari_jam,
            ["Jam"]
        )
        self.col_jenis = self.detect(
            self.hari_jam,
            ["Jenis"]
        )

        print("Kolom Guru      :", self.col_guru)
        print("Kolom Mapel     :", self.col_mapel)
        print("Kolom Kelas     :", self.col_kelas)
        print("Kolom JP        :", self.col_jp)
        print("Kolom Pembagian :", self.col_pembagian)
        print("="*60)

    # =====================================================
    # MEMBUAT SLOT PEMBELAJARAN
    # =====================================================

    def create_slot(self):
        print("MEMBUAT SLOT")
        self.slot = []
        nomor = 1

        for _, row in self.hari_jam.iterrows():
            if str(row[self.col_jenis]).lower() != "pembelajaran":
                continue

            self.slot.append({
                "id": nomor,
                "hari": row[self.col_hari],
                "jam": int(row[self.col_jam])
            })
            nomor += 1

        print("Jumlah Slot :", len(self.slot))

    # =====================================================
    # METODE UTK INTEGRASI EKSTERNAL
    # =====================================================

    def get_slots(self):
        """Getter slot untuk diakses oleh Exporter."""
        return self.slot

    def days(self):
        """Mendapatkan daftar hari unik yang aktif mengajar."""
        return list(self.hari_jam[self.col_hari].unique())

    # =====================================================
    # PERSIAPAN ENGINE JADWAL
    # =====================================================

    def prepare(self):
        self.create_slot()
        print("Scheduler siap.")

    def create_index(self):
        print("=" * 60)
        print("MEMBUAT INDEX JADWAL")
        print("=" * 60)

        self.index = []
        nomor = 1

        for _, row in self.mengajar.iterrows():
            guru = row[self.col_guru]
            mapel = row[self.col_mapel]
            kelas = row[self.col_kelas]
            jp = int(row[self.col_jp])
            pembagian = str(row[self.col_pembagian]) if self.col_pembagian is not None else ""

            for slot in self.slot:
                self.index.append({
                    "id": nomor,
                    "guru": guru,
                    "kelas": kelas,
                    "mapel": mapel,
                    "jp": jp,
                    "pembagian": pembagian,
                    "hari": slot["hari"],
                    "jam": slot["jam"]
                })
                nomor += 1

        print("Jumlah Index :", len(self.index))
        print("=" * 60)

    def prepare_engine(self):
        self.prepare()
        self.create_index()
        print("Engine siap digunakan.")

    # =====================================================
    # SOLVING & EXPORT INTEGRATION
    # =====================================================

    def solve(self, timeout_seconds=60.0):
        """
        Menjalankan SchedulerSolver yang mengintegrasikan CP-SAT 
        dan ConstraintBuilder.
        """
        if not ORTOOLS:
            print("Kesalahan: Google OR-Tools tidak terinstall.")
            return False

        # Inisialisasi dan jalankan solver wrapper
        solver_engine = SchedulerSolver(loader=self, calendar=self)
        success = solver_engine.solve(timeout_seconds=timeout_seconds)

        if success:
            self.df_hasil = solver_engine.get_results()
            print(f"Penjadwalan Sukses! Berhasil menyusun {len(self.df_hasil)} entri jadwal.")
        else:
            print("Penjadwalan Gagal: Solver tidak dapat menemukan solusi yang layak.")
            self.df_hasil = pd.DataFrame()

        return success

    def export(self):
        """
        Melakukan ekspor hasil optimasi jadwal menjadi bytes Excel 
        menggunakan ScheduleExporter.
        """
        if self.df_hasil.empty:
            print("Peringatan: Data jadwal kosong. Harap jalankan `.solve()` terlebih dahulu.")
            return None

        # Kirim "self" ke exporter karena self bertindak sebagai loader sekaligus calendar
        exporter = ScheduleExporter(df_results=self.df_hasil, calendar=self)
        return exporter.to_excel_bytes()
