from ortools.sat.python import cp_model
import pandas as pd



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





    # =====================================
    # MEMBUAT INDEX JADWAL
    # =====================================

    def create_index(self):


        no = 0


        for _, row in self.data_jadwal.iterrows():


            guru = row["Nama Guru"]

            mapel = row["Mapel"]

            kelas = row["Kelas"]



            for hari in HARI:


                for jam in JAM:


                    self.index.append({

                        "id":no,

                        "guru":guru,

                        "mapel":mapel,

                        "kelas":kelas,

                        "hari":hari,

                        "jam":jam

                    })


                    no += 1



        return self.index





    # =====================================
    # VARIABLE
    # =====================================

    def create_variables(self):


        for item in self.index:


            self.schedule_vars[item["id"]] = (

                self.model.NewBoolVar(

                    "jadwal_"+str(item["id"])

                )

            )







    # =====================================
    # GURU TIDAK BENTROK
    # =====================================


    def constraint_guru(self):


        for guru in self.data_guru:


            for hari in HARI:


                for jam in JAM:


                    daftar=[]


                    for item in self.index:


                        if (

                            item["guru"]==guru

                            and

                            item["hari"]==hari

                            and

                            item["jam"]==jam

                        ):


                            daftar.append(

                                self.schedule_vars[item["id"]]

                            )



                    if daftar:


                        self.model.Add(

                            sum(daftar)<=1

                        )








    # =====================================
    # KELAS TIDAK BENTROK
    # =====================================


    def constraint_kelas(self):


        for kelas in self.data_kelas:


            for hari in HARI:


                for jam in JAM:


                    daftar=[]


                    for item in self.index:


                        if (

                            item["kelas"]==kelas

                            and

                            item["hari"]==hari

                            and

                            item["jam"]==jam

                        ):


                            daftar.append(

                                self.schedule_vars[item["id"]]

                            )



                    if daftar:


                        self.model.Add(

                            sum(daftar)<=1

                        )








    # =====================================
    # SESUAI JP
    # =====================================


    def constraint_jp(self):


        for _,row in self.data_jadwal.iterrows():


            guru = row["Nama Guru"]

            mapel = row["Mapel"]

            kelas = row["Kelas"]

            jp = int(row["JP"])



            daftar=[]


            for item in self.index:


                if (

                    item["guru"]==guru

                    and

                    item["mapel"]==mapel

                    and

                    item["kelas"]==kelas

                ):


                    daftar.append(

                        self.schedule_vars[item["id"]]

                    )



            if daftar:


                self.model.Add(

                    sum(daftar)==jp

                )







    # =====================================
    # CONSTRAINT
    # =====================================

    def build_constraints(self):


        self.constraint_guru()


        self.constraint_kelas()


        self.constraint_jp()


        print(
            "Jumlah Index :",
            len(self.index)
        )


        print(
            "Jumlah Variable :",
            len(self.schedule_vars)
        )







    # =====================================
    # SOLVER
    # =====================================

    def solve(self):


        self.solver.parameters.max_time_in_seconds = 60



        status = self.solver.Solve(

            self.model

        )



        print(
            "STATUS SOLVER :",
            status
        )



        if status in [

            cp_model.FEASIBLE,

            cp_model.OPTIMAL

        ]:


            return True



        return False







    # =====================================
    # HASIL
    # =====================================


    def get_result(self):


        hasil=[]


        for item in self.index:


            nilai = self.solver.Value(

                self.schedule_vars[item["id"]]

            )


            if nilai==1:


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






    # =====================================
    # DATAFRAME
    # =====================================


    def to_dataframe(self):


        data = self.get_result()


        print(
            "Jumlah hasil :",
            len(data)
        )


        if not data:


            return pd.DataFrame()



        df=pd.DataFrame(data)


        return df
