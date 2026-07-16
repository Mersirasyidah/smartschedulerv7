# ==========================================================
# scheduler.py
# SmartSchedulerV7
# Bagian 1 : Struktur Dasar dan Persiapan Model
# ==========================================================

from ortools.sat.python import cp_model
import pandas as pd
from collections import defaultdict


# ==========================================================
# KONFIGURASI WAKTU
# ==========================================================

HARI = [
    "Senin",
    "Selasa",
    "Rabu",
    "Kamis",
    "Jumat",
    "Sabtu"
]


# Jam pelajaran
JAM = [
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8
]


# ==========================================================
# CLASS SCHEDULER
# ==========================================================

class Scheduler:

    def __init__(
        self,
        data_guru,
        data_kelas,
        data_mapel,
        data_jadwal=None
    ):

        """
        Inisialisasi Scheduler

        Parameter:

        data_guru :
            Data guru

        data_kelas :
            Data kelas

        data_mapel :
            Data mata pelajaran

        data_jadwal :
            Beban jam pelajaran
        """


        self.data_guru = data_guru
        self.data_kelas = data_kelas
        self.data_mapel = data_mapel
        self.data_jadwal = data_jadwal


        # Model OR-Tools
        self.model = cp_model.CpModel()


        # Solver
        self.solver = cp_model.CpSolver()


        # Menyimpan variabel jadwal

        self.schedule_vars = {}


        # Hasil akhir

        self.result = []


        # Load data

        self.guru_list = []
        self.kelas_list = []
        self.mapel_list = []


        self.prepare_data()



    # ======================================================
    # PERSIAPAN DATA
    # ======================================================

    def prepare_data(self):

        """
        Mengubah dataframe menjadi list
        agar mudah digunakan solver
        """


        # Guru

        if isinstance(self.data_guru, pd.DataFrame):

            self.guru_list = (
                self.data_guru
                ["nama_guru"]
                .tolist()
            )

        else:

            self.guru_list = self.data_guru



        # Kelas

        if isinstance(self.data_kelas, pd.DataFrame):

            self.kelas_list = (
                self.data_kelas
                ["kelas"]
                .tolist()
            )

        else:

            self.kelas_list = self.data_kelas



        # Mata Pelajaran

        if isinstance(self.data_mapel, pd.DataFrame):

            self.mapel_list = (
                self.data_mapel
                ["mapel"]
                .tolist()
            )

        else:

            self.mapel_list = self.data_mapel



    # ======================================================
    # INFORMASI DATA
    # ======================================================

    def info(self):

        """
        Menampilkan informasi scheduler
        """


        print("==============================")
        print(" SMART SCHEDULER V7")
        print("==============================")

        print(
            "Jumlah Guru :",
            len(self.guru_list)
        )

        print(
            "Jumlah Kelas :",
            len(self.kelas_list)
        )

        print(
            "Jumlah Mapel :",
            len(self.mapel_list)
        )


        print("==============================")



    # ======================================================
    # MEMBUAT INDEX DATA
    # ======================================================


    def create_index(self):

        """
        Membuat index untuk solver

        Contoh:

        Guru A
        Kelas 7A
        IPA

        Senin jam 1

        """

        self.index = []


        for guru in self.guru_list:

            for kelas in self.kelas_list:

                for mapel in self.mapel_list:

                    for hari in HARI:

                        for jam in JAM:


                            item = {

                                "guru": guru,

                                "kelas": kelas,

                                "mapel": mapel,

                                "hari": hari,

                                "jam": jam

                            }


                            self.index.append(item)



        return self.index



    # ======================================================
    # MEMBUAT VARIABLE SOLVER
    # ======================================================


    def create_variables(self):

        """
        Membuat variabel boolean:

        1 = dipakai
        0 = tidak dipakai

        """


        for i, item in enumerate(self.index):


            var_name = (
                f"jadwal_{i}"
            )


            self.schedule_vars[i] = (
                self.model.NewBoolVar(var_name)
            )



    # ======================================================
    # CEK STATUS MODEL
    # ======================================================


    def model_status(self):

        return self.solver.StatusName()



# ==========================================================
# TEST SEDERHANA
# ==========================================================


if __name__ == "__main__":


    guru = [

        "Budi",
        "Siti",
        "Andi"

    ]


    kelas = [

        "7A",
        "7B",
        "8A"

    ]


    mapel = [

        "Matematika",
        "Informatika",
        "IPA"

    ]


    scheduler = Scheduler(

        guru,

        kelas,

        mapel

    )


    scheduler.info()


    scheduler.create_index()


    scheduler.create_variables()


    print(
        "Jumlah variabel:",
        len(
            scheduler.schedule_vars
        )
    )

# ==========================================================
# BAGIAN 2
# CONSTRAINT AI SCHEDULER
# ==========================================================


    # ======================================================
    # CONSTRAINT GURU
    # ======================================================

    def constraint_guru_tidak_bentrok(self):

        """
        Satu guru hanya boleh mengajar
        satu kelas dalam satu waktu

        Contoh salah:

        Senin Jam 1

        Budi -> 7A Matematika
        Budi -> 8A IPA

        Tidak boleh
        """


        for guru in self.guru_list:


            for hari in HARI:


                for jam in JAM:


                    guru_slot = []


                    for i, item in enumerate(self.index):


                        if (
                            item["guru"] == guru
                            and
                            item["hari"] == hari
                            and
                            item["jam"] == jam
                        ):

                            guru_slot.append(
                                self.schedule_vars[i]
                            )



                    if guru_slot:


                        self.model.Add(
                            sum(guru_slot) <= 1
                        )





    # ======================================================
    # CONSTRAINT KELAS
    # ======================================================


    def constraint_kelas_tidak_bentrok(self):

        """
        Satu kelas tidak boleh
        mendapatkan dua mapel
        pada waktu yang sama

        """


        for kelas in self.kelas_list:


            for hari in HARI:


                for jam in JAM:


                    kelas_slot = []


                    for i,item in enumerate(self.index):


                        if (

                            item["kelas"] == kelas

                            and

                            item["hari"] == hari

                            and

                            item["jam"] == jam

                        ):


                            kelas_slot.append(

                                self.schedule_vars[i]

                            )



                    if kelas_slot:


                        self.model.Add(

                            sum(kelas_slot) <= 1

                        )





    # ======================================================
    # CONSTRAINT BEBAN JAM MAPEL
    # ======================================================


    def constraint_jumlah_jam(self):

        """
        Mengatur jumlah jam pelajaran

        Contoh:

        Matematika kelas 7A
        = 5 JP

        """



        if self.data_jadwal is None:

            return



        for _, row in self.data_jadwal.iterrows():


            guru = row["guru"]

            kelas = row["kelas"]

            mapel = row["mapel"]

            kebutuhan = row["jam"]



            daftar_variabel = []



            for i,item in enumerate(self.index):


                if (

                    item["guru"] == guru

                    and

                    item["kelas"] == kelas

                    and

                    item["mapel"] == mapel

                ):


                    daftar_variabel.append(

                        self.schedule_vars[i]

                    )



            if daftar_variabel:


                self.model.Add(

                    sum(daftar_variabel)

                    == kebutuhan

                )





    # ======================================================
    # CONSTRAINT HARI MGMP
    # ======================================================


    def constraint_mgmp_guru(self, data_mgmp):

        """
        Guru tidak dijadwalkan
        pada hari MGMP


        Contoh:

        Budi MGMP Rabu

        Maka:
        Rabu semua jam kosong

        """


        for guru, hari_larangan in data_mgmp.items():


            for i,item in enumerate(self.index):


                if (

                    item["guru"] == guru

                    and

                    item["hari"] == hari_larangan

                ):


                    self.model.Add(

                        self.schedule_vars[i] == 0

                    )





    # ======================================================
    # CONSTRAINT JAM KHUSUS
    # ======================================================


    def constraint_jam_jumat(self):

        """
        Aturan hari Jumat

        Misal:

        Jumat hanya sampai jam 6

        """


        for i,item in enumerate(self.index):


            if (

                item["hari"] == "Jumat"

                and

                item["jam"] > 6

            ):


                self.model.Add(

                    self.schedule_vars[i] == 0

                )





    # ======================================================
    # MEMASANG SEMUA CONSTRAINT
    # ======================================================


    def build_constraints(
            self,
            data_mgmp=None
        ):


        print(
            "Memasang constraint..."
        )


        # guru tidak bentrok

        self.constraint_guru_tidak_bentrok()



        # kelas tidak bentrok

        self.constraint_kelas_tidak_bentrok()



        # jumlah jam

        self.constraint_jumlah_jam()



        # MGMP

        if data_mgmp:

            self.constraint_mgmp_guru(
                data_mgmp
            )



        # Jumat

        self.constraint_jam_jumat()



        print(
            "Constraint selesai"
        )
