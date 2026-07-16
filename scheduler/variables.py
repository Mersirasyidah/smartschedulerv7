from ortools.sat.python import cp_model


class VariableBuilder:

    """
    Membangun seluruh variabel OR-Tools

    1 variabel =

    Guru
    +
    Kelas
    +
    Mapel
    +
    Slot HariJam

    Nilai:

    1 = mengajar

    0 = tidak mengajar
    """

    def __init__(

        self,

        loader,

        calendar

    ):

        self.loader = loader

        self.calendar = calendar

        self.model = cp_model.CpModel()

        self.variables = {}

        self.index = []



    # =====================================================
    # MEMBANGUN VARIABEL
    # =====================================================

    def build(self):

        nomor = 0

        mengajar = self.loader.mengajar

        slot = self.calendar.slot

        for _, row in mengajar.iterrows():

            guru = row["Nama Guru"]

            mapel = row["Mapel"]

            kelas = row["Kelas"]

            jp = int(row["JP"])

            pembagian = row["Pembagian"]

            guru_id = row["ID Guru"]

            for s in slot:

                key = (

                    guru,

                    kelas,

                    mapel,

                    s["hari"],

                    s["jam"]

                )

                var = self.model.NewBoolVar(

                    f"J_{nomor}"

                )

                self.variables[key] = var

                self.index.append({

                    "id": nomor,

                    "guru": guru,

                    "guru_id": guru_id,

                    "kelas": kelas,

                    "mapel": mapel,

                    "jp": jp,

                    "pembagian": pembagian,

                    "hari": s["hari"],

                    "jam": s["jam"],

                    "variable": var

                })

                nomor += 1

        print("=" * 60)
        print("VARIABLE BUILDER")
        print("=" * 60)
        print("Jumlah Variabel :", len(self.index))
        print("=" * 60)



    # =====================================================
    # MENGAMBIL SEMUA VARIABEL
    # =====================================================

    def all(self):

        return self.index



    # =====================================================
    # FILTER GURU
    # =====================================================

    def by_guru(

        self,

        guru

    ):

        return [

            x

            for x in self.index

            if x["guru"] == guru

        ]



    # =====================================================
    # FILTER KELAS
    # =====================================================

    def by_kelas(

        self,

        kelas

    ):

        return [

            x

            for x in self.index

            if x["kelas"] == kelas

        ]



    # =====================================================
    # FILTER MAPEL
    # =====================================================

    def by_mapel(

        self,

        mapel

    ):

        return [

            x

            for x in self.index

            if x["mapel"] == mapel

        ]



    # =====================================================
    # FILTER SLOT
    # =====================================================

    def by_slot(

        self,

        hari,

        jam

    ):

        return [

            x

            for x in self.index

            if

            x["hari"] == hari

            and

            x["jam"] == jam

        ]



    # =====================================================
    # FILTER GURU + SLOT
    # =====================================================

    def guru_slot(

        self,

        guru,

        hari,

        jam

    ):

        return [

            x

            for x in self.index

            if

            x["guru"] == guru

            and

            x["hari"] == hari

            and

            x["jam"] == jam

        ]



    # =====================================================
    # FILTER KELAS + SLOT
    # =====================================================

    def kelas_slot(

        self,

        kelas,

        hari,

        jam

    ):

        return [

            x

            for x in self.index

            if

            x["kelas"] == kelas

            and

            x["hari"] == hari

            and

            x["jam"] == jam

        ]



    # =====================================================
    # FILTER MAPEL
    # =====================================================

    def guru_mapel(

        self,

        guru,

        kelas,

        mapel

    ):

        return [

            x

            for x in self.index

            if

            x["guru"] == guru

            and

            x["kelas"] == kelas

            and

            x["mapel"] == mapel

        ]
