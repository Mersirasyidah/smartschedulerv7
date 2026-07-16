# =====================================================
# scheduler.py
# Smart Scheduler V7
# AI Schedule Generator
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





    # =================================================
    # MEMBUAT SEMUA KEMUNGKINAN JADWAL
    # =================================================


    def create_index(self):


        nomor = 0


        for guru in self.data_guru:


            for kelas in self.data_kelas:


                for mapel in self.data_mapel:


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





    # =================================================
    # MEMBUAT VARIABLE AI
    # =================================================


    def create_variables(self):


        for item in self.index:



            nomor = item["id"]



            self.schedule_vars[nomor] = (

                self.model.NewBoolVar(

                    f"jadwal_{nomor}"

                )

            )





    # =================================================
    # GURU TIDAK BOLEH BENTROK
    # =================================================


    def constraint_guru_tidak_bentrok(self):


        for guru in self.data_guru:


            for hari in HARI:


                for jam in JAM:


                    daftar = []



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

                            sum(daftar) <= 1

                        )






    # =================================================
    # KELAS TIDAK BOLEH BENTROK
    # =================================================


    def constraint_kelas_tidak_bentrok(self):


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







    # =================================================
    # SESUAI BEBAN JAM MENGAJAR
    # =================================================


    def constraint_jumlah_jam(self):


        if self.data_jadwal is None:

            return



        for _,row in self.data_jadwal.iterrows():



            try:



                guru = row.iloc[0]

                kelas = row.iloc[1]

                mapel = row.iloc[2]

                jumlah = int(row.iloc[3])



            except:


                continue




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

                    == jumlah

                )







    # =================================================
    # ATURAN SEKOLAH
    # =================================================


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







    # =================================================
    # SEMUA CONSTRAINT
    # =================================================


    def build_constraints(self):


        self.constraint_guru_tidak_bentrok()


        self.constraint_kelas_tidak_bentrok()


        self.constraint_jumlah_jam()


        self.constraint_jumat()



        # PAKSA AI MEMILIH JADWAL

        self.model.Maximize(

            sum(

                self.schedule_vars.values()

            )

        )






    # =================================================
    # MENJALANKAN AI
    # =================================================


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





    # =================================================
    # MENGAMBIL HASIL
    # =================================================


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


                    "Hari": item["hari"],


                    "Jam": item["jam"],


                    "Kelas": item["kelas"],


                    "Mapel": item["mapel"],


                    "Guru": item["guru"]


                })



        return hasil






    # =================================================
    # DATAFRAME
    # =================================================


    def to_dataframe(self):


        hasil = self.get_result()



        if len(hasil)==0:


            return pd.DataFrame()



        df = pd.DataFrame(

            hasil

        )



        urutan = {


            "Senin":1,

            "Selasa":2,

            "Rabu":3,

            "Kamis":4,

            "Jumat":5,

            "Sabtu":6


        }



        df["urut"] = (

            df["Hari"]

            .map(urutan)

        )



        df = df.sort_values(

            [

                "urut",

                "Jam",

                "Kelas"

            ]

        )



        df = df.drop(

            columns=["urut"]

        )



        return df
