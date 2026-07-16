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
except:
    ORTOOLS = False


class Scheduler:

    """
    =========================================================
    SMART SCHEDULER ENGINE V2
    =========================================================
    """

    # =====================================================
    # INIT
    # =====================================================

    def __init__(self, database):

        self.db = database

        self.model = cp_model.CpModel() if ORTOOLS else None

        self.variables = {}

        self.index = []

        self.solution = []

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

        print("Guru           :",len(self.guru))
        print("Mapel          :",len(self.mapel))
        print("Rombel         :",len(self.rombel))
        print("Mengajar       :",len(self.mengajar))
        print("Hari_Jam       :",len(self.hari_jam))

        print("="*60)


        self.detect_column()


    # =====================================================
    # DETEKSI KOLOM
    # =====================================================

    def detect(self, df, kandidat):

        for k in kandidat:

            if k in df.columns:
                return k

        return None


    def detect_column(self):

        self.col_guru = self.detect(

            self.mengajar,

            [

                "Nama Guru",

                "nama_guru",

                "Guru",

                "guru"

            ]

        )

        self.col_mapel = self.detect(

            self.mengajar,

            [

                "Mapel",

                "mapel"

            ]

        )

        self.col_kelas = self.detect(

            self.mengajar,

            [

                "Kelas",

                "kelas"

            ]

        )

        self.col_jp = self.detect(

            self.mengajar,

            [

                "JP",

                "jp"

            ]

        )

        self.col_pembagian = self.detect(

            self.mengajar,

            [

                "Pembagian",

                "pembagian"

            ]

        )

        self.col_hari = self.detect(

            self.hari_jam,

            [

                "Hari"

            ]

        )

        self.col_jam = self.detect(

            self.hari_jam,

            [

                "Jam"

            ]

        )

        self.col_jenis = self.detect(

            self.hari_jam,

            [

                "Jenis"

            ]

        )

        print("Kolom Guru      :",self.col_guru)
        print("Kolom Mapel     :",self.col_mapel)
        print("Kolom Kelas     :",self.col_kelas)
        print("Kolom JP        :",self.col_jp)
        print("Kolom Pembagian :",self.col_pembagian)

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

                "id":nomor,

                "hari":row[self.col_hari],

                "jam":int(row[self.col_jam])

            })

            nomor += 1

        print("Jumlah Slot :",len(self.slot))


    # =====================================================
    # PERSIAPAN
    # =====================================================

    def prepare(self):

        self.create_slot()

        print("Scheduler siap.")

      # =====================================================
    # MEMBUAT INDEX JADWAL
    # =====================================================

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

            pembagian = ""

            if self.col_pembagian is not None:
                pembagian = str(row[self.col_pembagian])

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


    # =====================================================
    # MEMBUAT VARIABLE AI
    # =====================================================

    def create_variables(self):

        print("=" * 60)
        print("MEMBUAT VARIABLE AI")
        print("=" * 60)

        if not ORTOOLS:

            print("OR-Tools belum tersedia")

            return

        self.variables = {}

        total = 0

        for item in self.index:

            key = (

                item["guru"],

                item["kelas"],

                item["mapel"],

                item["hari"],

                item["jam"]

            )

            self.variables[key] = self.model.NewBoolVar(

                f"x_{total}"

            )

            total += 1

        print("Jumlah Variable :", total)

        print("=" * 60)


    # =====================================================
    # MELIHAT SAMPLE INDEX
    # =====================================================

    def preview_index(self, jumlah=10):

        print("=" * 60)
        print("PREVIEW INDEX")
        print("=" * 60)

        for row in self.index[:jumlah]:

            print(row)

        print("=" * 60)


    # =====================================================
    # STATISTIK
    # =====================================================

    def statistics(self):

        print("=" * 60)
        print("STATISTIK")
        print("=" * 60)

        print("Guru            :", len(self.guru))
        print("Mapel           :", len(self.mapel))
        print("Rombel          :", len(self.rombel))
        print("Mengajar        :", len(self.mengajar))
        print("Slot            :", len(self.slot))
        print("Index           :", len(self.index))
        print("Variable        :", len(self.variables))

        print("=" * 60)


    # =====================================================
    # PERSIAPAN ENGINE
    # =====================================================

    def prepare_engine(self):

        self.prepare()

        self.create_index()

        self.create_variables()

        self.statistics()

        print("Engine siap digunakan.")

  
