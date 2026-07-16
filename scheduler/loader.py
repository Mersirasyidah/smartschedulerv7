"""
====================================================
SMART SCHEDULER V2
LOADER
====================================================
"""

import pandas as pd


class DataLoader:

    def __init__(self, database):

        self.db = database

        self.guru = None
        self.mapel = None
        self.rombel = None
        self.mengajar = None
        self.hari_jam = None
        self.ruangan = None
        self.mgmp = None

    # ==================================================
    # LOAD DATABASE
    # ==================================================

    def load_all(self):

        print("=" * 60)
        print("MEMBACA DATABASE SEKOLAH")
        print("=" * 60)

        self.guru = self.db["Guru"].copy()

        self.mapel = self.db["Mapel"].copy()

        self.rombel = self.db["Rombel"].copy()

        self.mengajar = self.db["Guru_Mengajar"].copy()

        self.hari_jam = self.db["Hari_Jam"].copy()

        if "Ruangan" in self.db:

            self.ruangan = self.db["Ruangan"].copy()

        else:

            self.ruangan = pd.DataFrame()

        if "MGMP" in self.db:

            self.mgmp = self.db["MGMP"].copy()

        else:

            self.mgmp = pd.DataFrame()

        print("Guru           :", len(self.guru))
        print("Mapel          :", len(self.mapel))
        print("Rombel         :", len(self.rombel))
        print("Mengajar       :", len(self.mengajar))
        print("Hari_Jam       :", len(self.hari_jam))
        print("Ruangan        :", len(self.ruangan))
        print("MGMP           :", len(self.mgmp))

        print("=" * 60)

        self.detect_columns()

    # ==================================================
    # DETEKSI KOLOM
    # ==================================================

    def detect(self, dataframe, kandidat):

        for kolom in kandidat:

            if kolom in dataframe.columns:

                return kolom

        return None

    def detect_columns(self):

        # -----------------------------
        # Guru Mengajar
        # -----------------------------

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

        # -----------------------------
        # Hari Jam
        # -----------------------------

        self.col_hari = self.detect(

            self.hari_jam,

            [

                "Hari",

                "hari"

            ]

        )

        self.col_jam = self.detect(

            self.hari_jam,

            [

                "Jam",

                "jam"

            ]

        )

        self.col_jenis = self.detect(

            self.hari_jam,

            [

                "Jenis",

                "jenis"

            ]

        )

        print("Deteksi Kolom")

        print("-" * 40)

        print("Guru       :", self.col_guru)

        print("Mapel      :", self.col_mapel)

        print("Kelas      :", self.col_kelas)

        print("JP         :", self.col_jp)

        print("Pembagian  :", self.col_pembagian)

        print("Hari       :", self.col_hari)

        print("Jam        :", self.col_jam)

        print("Jenis      :", self.col_jenis)

        print("=" * 60)

    # ==================================================
    # VALIDASI
    # ==================================================

    def validate(self):

        wajib = [

            self.col_guru,

            self.col_mapel,

            self.col_kelas,

            self.col_jp,

            self.col_hari,

            self.col_jam,

            self.col_jenis

        ]

        if None in wajib:

            raise Exception(

                "Masih ada kolom database yang tidak dikenali."

            )

        print("Validasi database berhasil.")
