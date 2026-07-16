# ==========================================================
# scheduler.py
# SmartSchedulerV7
# Engine Scheduler
# ==========================================================


from ortools.sat.python import cp_model
import pandas as pd



# ==========================================================
# KONFIGURASI
# ==========================================================


HARI = [
    "Senin",
    "Selasa",
    "Rabu",
    "Kamis",
    "Jumat",
    "Sabtu"
]


JAM = [
    1,2,3,4,5,6,7,8
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


        self.data_guru = data_guru

        self.data_kelas = data_kelas

        self.data_mapel = data_mapel

        self.data_jadwal = data_jadwal



        self.model = cp_model.CpModel()

        self.solver = cp_model.CpSolver()



        self.index = []

        self.schedule_vars = {}



    # ======================================================
    # MEMBUAT KOMBINASI JADWAL
    # ======================================================


    def create_index(self):


        for guru in self.data_guru:


            for kelas in self.data_kelas:


                for mapel in self.data_mapel:


                    for hari in HARI:


                        for jam in JAM:


                            self.index.append({

                                "guru": guru,

                                "kelas": kelas,

                                "mapel": mapel,

                                "hari": hari,

                                "jam": jam

                            })



        return self.index




    # ======================================================
    # VARIABLE AI
    # ======================================================


    def create_variables(self):


        for i,item in enumerate(self.index):


            self.schedule_vars[i] = (

                self.model.NewBoolVar(

                    f"jadwal_{i}"

                )

            )




    # ======================================================
    # CONSTRAINT GURU
    # ======================================================


    def constraint_guru_tidak_bentrok(self):


        for guru in self.data_guru:


            for hari in HARI:


                for jam in JAM:


                    daftar = []


                    for i,item in enumerate(self.index):


                        if (

                            item["guru"] == guru

                            and

                            item["hari"] == hari

                            and

                            item["jam"] == jam

                        ):


                            daftar.append(

                                self.schedule_vars[i]

                            )



                    if daftar:


                        self.model.Add(

                            sum(daftar) <= 1

                        )





    # ======================================================
    # CONSTRAINT KELAS
    # ======================================================


    def constraint_kelas_tidak_bentrok(self):


        for kelas in self.data_kelas:


            for hari in HARI:


                for jam in JAM:


                    daftar=[]



                    for i,item in enumerate(self.index):


                        if (

                            item["kelas"] == kelas

                            and

                            item["hari"] == hari

                            and

                            item["jam"] == jam

                        ):


                            daftar.append(

                                self.schedule_vars[i]

                            )



                    if daftar:


                        self.model.Add(

                            sum(daftar) <= 1

                        )





    # ======================================================
    # CONSTRAINT JUMLAH JAM
    # ======================================================


    def constraint_jumlah_jam(self):


        if self.data_jadwal is None:

            return



        for _,row in self.data_jadwal.iterrows():


            guru = row.get(
                "guru",
                None
            )


            kelas = row.get(
                "kelas",
                None
            )


            mapel = row.get(
                "mapel",
                None
            )


            jam = row.get(
                "jam",
                None
            )



            if None in [
                guru,
                kelas,
                mapel,
                jam
            ]:

                continue



            daftar=[]



            for i,item in enumerate(self.index):


                if (

                    item["guru"] == guru

                    and

                    item["kelas"] == kelas

                    and

                    item["mapel"] == mapel

                ):


                    daftar.append(

                        self.schedule_vars[i]

                    )



            if daftar:


                self.model.Add(

                    sum(daftar)

                    == jam

                )




    # ======================================================
    # ATURAN JAM JUMAT
    # ======================================================


    def constraint_jumat(self):


        for i,item in enumerate(self.index):


            if (

                item["hari"]=="Jumat"

                and

                item["jam"]>6

            ):


                self.model.Add(

                    self.schedule_vars[i]

                    ==0

                )




    # ======================================================
    # BUILD SEMUA CONSTRAINT
    # ======================================================


    def build_constraints(self):


        print(
            "Memasang constraint..."
        )


        self.constraint_guru_tidak_bentrok()


        self.constraint_kelas_tidak_bentrok()


        self.constraint_jumlah_jam()


        self.constraint_jumat()


        print(
            "Constraint selesai"
        )

    # ======================================================
    # SOLVE : MENJALANKAN AI SEARCH
    # ======================================================


    def solve(self):

        """
        Menjalankan OR-Tools Solver
        untuk mencari jadwal terbaik
        """

        print(
            "AI Scheduler mulai mencari solusi..."
        )


        status = self.solver.Solve(
            self.model
        )


        if status in [
            cp_model.OPTIMAL,
            cp_model.FEASIBLE
        ]:


            print(
                "Solusi jadwal ditemukan"
            )


            return True


        else:


            print(
                "Tidak ditemukan solusi"
            )


            return False





    # ======================================================
    # MENGAMBIL HASIL SOLVER
    # ======================================================


    def get_result(self):


        """
        Mengambil variabel yang bernilai 1
        menjadi data jadwal
        """


        hasil = []



        for i,item in enumerate(self.index):


            nilai = self.solver.Value(

                self.schedule_vars[i]

            )


            if nilai == 1:


                hasil.append({

                    "Hari":
                        item["hari"],


                    "Jam":
                        item["jam"],


                    "Kelas":
                        item["kelas"],


                    "Mapel":
                        item["mapel"],


                    "Guru":
                        item["guru"]

                })



        return hasil





    # ======================================================
    # HASIL MENJADI DATAFRAME
    # ======================================================


    def to_dataframe(self):


        data = self.get_result()


        if len(data)==0:


            return pd.DataFrame()



        df = pd.DataFrame(
            data
        )


        # urutkan jadwal


        urutan_hari = {

            "Senin":1,
            "Selasa":2,
            "Rabu":3,
            "Kamis":4,
            "Jumat":5,
            "Sabtu":6

        }


        df["urut_hari"] = (

            df["Hari"]
            .map(urutan_hari)

        )


        df = df.sort_values(

            [
                "urut_hari",
                "Jam",
                "Kelas"

            ]

        )


        df = df.drop(

            columns=[
                "urut_hari"
            ]

        )


        return df
