from ortools.sat.python import cp_model


class ConstraintBuilder:

    def __init__(

        self,

        loader,

        calendar,

        variables

    ):

        self.loader = loader

        self.calendar = calendar

        self.variables = variables

        self.model = variables.model


    # ======================================================
    # MEMANGGIL SEMUA CONSTRAINT
    # ======================================================

    def build(self):

        print("=" * 60)
        print("MEMBANGUN CONSTRAINT")
        print("=" * 60)

        self.constraint_guru()

        self.constraint_kelas()

        self.constraint_mgmp()

        print("=" * 60)
        print("Constraint selesai")
        print("=" * 60)



    # ======================================================
    # GURU TIDAK BOLEH BENTROK
    # ======================================================

    def constraint_guru(self):

        print("Constraint Guru ...")


        guru_list = self.loader.guru["Nama Guru"].tolist()


        for guru in guru_list:


            for slot in self.calendar.slot:


                daftar = []


                hari = slot["hari"]

                jam = slot["jam"]


                for item in self.variables.guru_slot(

                    guru,

                    hari,

                    jam

                ):


                    daftar.append(

                        item["variable"]

                    )


                if len(daftar) > 1:

                    self.model.Add(

                        sum(daftar)

                        <= 1

                    )


        print("OK")



    # ======================================================
    # KELAS TIDAK BOLEH BENTROK
    # ======================================================

    def constraint_kelas(self):

        print("Constraint Kelas ...")


        kelas_list = self.loader.rombel["Kelas"].tolist()


        for kelas in kelas_list:


            for slot in self.calendar.slot:


                daftar = []


                hari = slot["hari"]

                jam = slot["jam"]


                for item in self.variables.kelas_slot(

                    kelas,

                    hari,

                    jam

                ):


                    daftar.append(

                        item["variable"]

                    )


                if len(daftar) > 1:

                    self.model.Add(

                        sum(daftar)

                        <= 1

                    )


        print("OK")



    # ======================================================
    # MGMP
    # ======================================================

    def constraint_mgmp(self):

        print("Constraint MGMP ...")


        guru_df = self.loader.guru


        for _, row in guru_df.iterrows():


            guru = row["Nama Guru"]


            hari_mgmp = row["Hari MGMP"]


            if str(hari_mgmp).strip() == "":

                continue


            if str(hari_mgmp).lower() == "nan":

                continue


            for item in self.variables.by_guru(

                guru

            ):


                if (

                    item["hari"]

                    ==

                    hari_mgmp

                ):


                    if item["jam"] > 4:


                        self.model.Add(

                            item["variable"]

                            == 0

                        )


        print("OK")
