# =====================================================
# scheduler.py
# Smart Scheduler V7
# Sesuai Database Guru_Mengajar
# =====================================================


from ortools.sat.python import cp_model
import pandas as pd



# ==============================
# KONFIGURASI
# ==============================

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



# =====================================================
# CLASS SCHEDULER
# =====================================================


class Scheduler:



    def __init__(

        self,

        data_guru,

        data_kelas,

        data_mapel,

        data_jadwal


    ):


        self.data_guru = data_guru

        self.data_kelas = data_kelas

        self.data_mapel = data_mapel

        self.data_jadwal = data_jadwal



        self.model = cp_model.CpModel()


        self.solver = cp_model.CpSolver()



        self.index = []


        self.schedule_vars = {}





    # ==================================================
    # MEMBUAT KANDIDAT JADWAL
    # ==================================================


    def create_index(self):


        nomor = 0


        for guru in self.data_guru:


            data_guru = self.data_jadwal[

                self.data_jadwal["Nama Guru"]

                == guru

            ]



            for _, row in data_guru.iterrows():


                kelas = row["Kelas"]

                mapel = row["Mapel"]



                for hari in HARI:


                    for jam in JAM:



                        self.index.append({


                            "id": nomor,


                            "guru": guru,


                            "kelas": kelas,


                            "mapel": mapel,


                            "hari": hari,


                            "jam": jam


                        })


                        nomor += 1



        return self.index






    # ==================================================
    # VARIABLE AI
    # ==================================================


    def create_variables(self):


        for item in self.index:


            self.schedule_vars[

                item["id"]

            ] = self.model.NewBoolVar(


                f"jadwal_{item['id']}"

            )







    # ==================================================
    # GURU TIDAK BENTROK
    # ==================================================


    def constraint_guru(self):


        for guru in self.data_guru:


            for hari in HARI:


                for jam in JAM:


                    daftar=[]



                    for item in self.index:


                        if (

                            item["guru"] == guru

                            and

                            item["hari"] == hari

                            and

                            item["jam"] == jam

                        ):


                            daftar.append(

                                self.schedule_vars[
                                    item["id"]
                                ]

                            )



                    if daftar:


                        self.model.Add(

                            sum(daftar)<=1

                        )







    # ==================================================
    # KELAS TIDAK BENTROK
    # ==================================================


    def constraint_kelas(self):


        for kelas in self.data_kelas:


            for hari in HARI:


                for jam in JAM:


                    daftar=[]



                    for item in self.index:


                        if (

                            item["kelas"] == kelas

                            and

                            item["hari"] == hari

                            and

                            item["jam"] == jam

                        ):


                            daftar.append(

                                self.schedule_vars[
                                    item["id"]
                                ]

                            )



                    if daftar:


                        self.model.Add(

                            sum(daftar)<=1

                        )







    # ==================================================
    # SESUAI JUMLAH JP
    # ==================================================


    def constraint_jp(self):


        for _, row in self.data_jadwal.iterrows():


            guru = row["Nama Guru"]


            kelas = row["Kelas"]


            mapel = row["Mapel"]


            jp = int(row["JP"])




            daftar=[]



            for item in self.index:


                if (

                    item["guru"] == guru

                    and

                    item["kelas"] == kelas

                    and

                    item["mapel"] == mapel

                ):


                    daftar.append(

                        self.schedule_vars[
                            item["id"]
                        ]

                    )



            if daftar:


                self.model.Add(

                    sum(daftar)

                    == jp

                )







    # ==================================================
    # CONSTRAINT JUMAT
    # ==================================================


    def constraint_jumat(self):


        for item in self.index:


            if (

                item["hari"]=="Jumat"

                and

                item["jam"]>6

            ):


                self.model.Add(

                    self.schedule_vars[
                        item["id"]
                    ]

                    ==0

                )






    # ==================================================
    # PASANG SEMUA ATURAN
    # ==================================================


    def build_constraints(self):


        self.constraint_guru()


        self.constraint_kelas()


        self.constraint_jp()


        self.constraint_jumat()



        # agar AI memilih jadwal

        self.model.Maximize(

            sum(

                self.schedule_vars.values()

            )

        )







    # ==================================================
    # JALANKAN AI
    # ==================================================


    def solve(self):


        status = self.solver.Solve(

            self.model

        )


        if status in [

            cp_model.OPTIMAL,

            cp_model.FEASIBLE

        ]:


            return True



        return False






    # ==================================================
    # AMBIL HASIL
    # ==================================================


    def get_result(self):


        hasil=[]



        for item in self.index:


            nilai = self.solver.Value(

                self.schedule_vars[

                    item["id"]

                ]

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







    # ==================================================
    # HASIL DATAFRAME
    # ==================================================


    def to_dataframe(self):


        data = self.get_result()



        if len(data)==0:


            return pd.DataFrame()



        df = pd.DataFrame(data)



        urutan = {


            "Senin":1,

            "Selasa":2,

            "Rabu":3,

            "Kamis":4,

            "Jumat":5,

            "Sabtu":6

        }



        df["urutan"] = (

            df["Hari"]

            .map(urutan)

        )



        df = df.sort_values(

            [

                "urutan",

                "Jam",

                "Kelas"

            ]

        )



        df.drop(

            columns=["urutan"],

            inplace=True

        )



        return df
