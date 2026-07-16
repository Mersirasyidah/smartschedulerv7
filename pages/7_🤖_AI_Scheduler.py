import streamlit as st
import pandas as pd

from database import load_database
from scheduler import Scheduler


# =====================================
# KONFIGURASI HALAMAN
# =====================================

st.set_page_config(
    page_title="AI Scheduler",
    page_icon="🤖",
    layout="wide"
)


st.title("🤖 AI Scheduler")
st.caption("Smart Scheduler V7")


# =====================================
# LOAD DATABASE
# =====================================

try:

    db = load_database()


except Exception as e:

    st.error("Database gagal dibaca")

    st.exception(e)

    st.stop()



# =====================================
# AMBIL TABEL DATABASE
# =====================================

try:

    guru = db["Guru"]

    mengajar = db["Guru_Mengajar"]

    rombel = db["Rombel"]


except Exception as e:

    st.error(
        "Tabel database belum lengkap"
    )

    st.exception(e)

    st.stop()



# =====================================
# STATISTIK
# =====================================

col1, col2, col3 = st.columns(3)


col1.metric(
    "Jumlah Guru",
    len(guru)
)


col2.metric(
    "Data Mengajar",
    len(mengajar)
)


col3.metric(
    "Jumlah Rombel",
    len(rombel)
)


st.divider()



# =====================================
# GENERATE JADWAL
# =====================================

if st.button(
    "🚀 Generate Jadwal",
    use_container_width=True
):


    st.info(
        "Menyiapkan AI Scheduler..."
    )


    # =================================
    # TAMPILKAN DATABASE
    # =================================

    with st.expander(
        "🔎 Lihat Data Database"
    ):


        st.subheader(
            "Data Guru"
        )

        st.dataframe(
            guru
        )


        st.subheader(
            "Data Guru Mengajar"
        )

        st.dataframe(
            mengajar
        )


        st.subheader(
            "Data Rombel"
        )

        st.dataframe(
            rombel
        )



    # =================================
    # AMBIL DATA GURU
    # =================================

    try:


        if "nama_guru" in guru.columns:

            data_guru = guru[
                "nama_guru"
            ].tolist()


        elif "nama" in guru.columns:

            data_guru = guru[
                "nama"
            ].tolist()


        elif "guru" in guru.columns:

            data_guru = guru[
                "guru"
            ].tolist()


        else:

            data_guru = guru.iloc[:,1].tolist()



        # ==============================
        # KELAS
        # ==============================


        if "kelas" in rombel.columns:

            data_kelas = rombel[
                "kelas"
            ].tolist()


        elif "nama_kelas" in rombel.columns:

            data_kelas = rombel[
                "nama_kelas"
            ].tolist()


        else:

            data_kelas = rombel.iloc[:,1].tolist()



        # ==============================
        # MAPEL
        # ==============================


        if "mapel" in mengajar.columns:

            data_mapel = mengajar[
                "mapel"
            ].unique().tolist()


        elif "mata_pelajaran" in mengajar.columns:

            data_mapel = mengajar[
                "mata_pelajaran"
            ].unique().tolist()


        else:

            data_mapel = mengajar.iloc[:,1].unique().tolist()



    except Exception as e:


        st.error(
            "Gagal membaca data sekolah"
        )

        st.exception(e)

        st.stop()



    st.success(
        "Database berhasil dibaca"
    )



    # =================================
    # DATA BEBAN MENGAJAR
    # =================================

    data_jadwal = mengajar.copy()



    # =================================
    # BUAT ENGINE
    # =================================

    try:


        scheduler = Scheduler(

            data_guru,

            data_kelas,

            data_mapel,

            data_jadwal

        )


        st.success(
            "Scheduler Engine berhasil dibuat"
        )


    except Exception as e:


        st.error(
            "Gagal membuat Scheduler"
        )

        st.exception(e)

        st.stop()



    # =================================
    # INDEX
    # =================================

    scheduler.create_index()


    st.success(
        "Index jadwal berhasil dibuat"
    )



    # =================================
    # VARIABLE
    # =================================


    scheduler.create_variables()


    st.success(
        "Variable AI berhasil dibuat"
    )



    # =================================
    # CONSTRAINT
    # =================================


    scheduler.build_constraints()


    st.success(
        "Constraint berhasil dipasang"
    )



    st.divider()



    # =================================
    # SOLVER
    # =================================


    with st.spinner(

        "🤖 AI sedang mencari jadwal..."

    ):


        solusi = scheduler.solve()



    if solusi:


        st.success(
            "🎉 Jadwal berhasil dibuat"
        )


        hasil = scheduler.to_dataframe()



        # SIMPAN HASIL

        if not hasil.empty:


            hasil.to_csv(

                "hasil_jadwal.csv",

                index=False

            )



        # =================================
        # TAMPILKAN HASIL
        # =================================


        st.subheader(
            "📅 HASIL JADWAL"
        )


        if not hasil.empty:


            st.dataframe(

                hasil,

                use_container_width=True,

                hide_index=True

            )


            st.divider()



            # =================================
            # FILTER KELAS
            # =================================


            st.subheader(
                "🏫 Jadwal Per Kelas"
            )


            kelas_pilih = st.selectbox(

                "Pilih Kelas",

                hasil["Kelas"].unique()

            )


            hasil_kelas = hasil[

                hasil["Kelas"] == kelas_pilih

            ]


            st.dataframe(

                hasil_kelas,

                use_container_width=True,

                hide_index=True

            )



            st.divider()



            # =================================
            # FILTER GURU
            # =================================


            st.subheader(
                "👨‍🏫 Jadwal Per Guru"
            )


            guru_pilih = st.selectbox(

                "Pilih Guru",

                hasil["Guru"].unique()

            )


            hasil_guru = hasil[

                hasil["Guru"] == guru_pilih

            ]


            st.dataframe(

                hasil_guru,

                use_container_width=True,

                hide_index=True

            )



        else:


            st.warning(
                "Solver berhasil tetapi jadwal kosong"
            )



    else:


        st.error(
            """
            AI tidak menemukan solusi.

            Periksa:
            - Beban jam mengajar
            - Jumlah ruang
            - Bentrok guru
            - Bentrok kelas
            """
        )
