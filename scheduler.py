from ortools.sat.python import cp_model
import pandas as pd



HARI = [
    "Senin",
    "Selasa",
    "Rabu",
    "Kamis",
    "Jumat"
]


JAM = [
    1,2,3,4,5,6
]



class Scheduler:


    def __init__(
        self,
        data_guru,
        data_kelas,
        data_mapel,
        data_jadwal
    ):


        self.data_jadwal=data_jadwal

        self.model=cp_model.CpModel()

        self.solver=cp_model.CpSolver()

        self.index=[]

        self.vars={}




    def create_index(self):


        no=0


        for _,r in self.data_jadwal.iterrows():


            for h in HARI:

                for j in JAM:


                    self.index.append({

                        "id":no,

                        "guru":r["Nama Guru"],

                        "kelas":r["Kelas"],

                        "mapel":r["Mapel"],

                        "hari":h,

                        "jam":j

                    })


                    no+=1




    def create_variables(self):


        for x in self.index:


            self.vars[x["id"]]=(

                self.model.NewBoolVar(

                    f"x{x['id']}"

                )

            )





    def build_constraints(self):


        for _,r in self.data_jadwal.iterrows():


            daftar=[]


            for x in self.index:


                if (

                    x["guru"]==r["Nama Guru"]

                    and

                    x["kelas"]==r["Kelas"]

                    and

                    x["mapel"]==r["Mapel"]

                ):


                    daftar.append(

                        self.vars[x["id"]]

                    )


            self.model.Add(

                sum(daftar)

                == int(r["JP"])

            )



        # guru tidak bentrok


        for x in self.index:


            daftar=[]


            for y in self.index:


                if (

                    x["guru"]==y["guru"]

                    and

                    x["hari"]==y["hari"]

                    and

                    x["jam"]==y["jam"]

                ):


                    daftar.append(

                        self.vars[y["id"]]

                    )


            self.model.Add(

                sum(daftar)<=1

            )





    def solve(self):


        status=self.solver.Solve(

            self.model

        )


        print(
            "STATUS",
            status
        )


        return status in [

            cp_model.FEASIBLE,

            cp_model.OPTIMAL

        ]




    def to_dataframe(self):


        hasil=[]


        for x in self.index:


            if self.solver.Value(

                self.vars[x["id"]]

            )==1:


                hasil.append({

                    "Hari":x["hari"],

                    "Jam":x["jam"],

                    "Kelas":x["kelas"],

                    "Mapel":x["mapel"],

                    "Guru":x["guru"]

                })


        return pd.DataFrame(hasil)
