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
# AMBIL DATA DATABASE
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
# TOMBOL GENERATE
# =====================================

if st.button(
    "🚀 Generate Jadwal",
    use_container_width=True
):


    st.info(
        "Menyiapkan AI Scheduler..."
    )


    # =================================
    # CEK STRUKTUR DATABASE
    # =================================

    with st.expander(
        "🔎 Lihat Struktur Database"
    ):

        st.write(
            "Tabel Guru"
        )

        st.dataframe(
            guru
        )


        st.write(
            "Tabel Guru_Mengajar"
        )

        st.dataframe(
            mengajar
        )


        st.write(
            "Tabel Rombel"
        )

        st.dataframe(
            rombel
        )



    # =================================
    # AMBIL DATA GURU
    # =================================

    try:


        if "nama_guru" in guru.columns:

            data_guru = (
                guru["nama_guru"]
                .tolist()
            )


        elif "nama" in guru.columns:

            data_guru = (
                guru["nama"]
                .tolist()
            )


        elif "guru" in guru.columns:

            data_guru = (
                guru["guru"]
                .tolist()
            )


        else:

            data_guru = (
                guru
                .iloc[:,1]
                .tolist()
            )



        # ==============================
        # DATA KELAS
        # ==============================


        if "kelas" in rombel.columns:

            data_kelas = (
                rombel["kelas"]
                .tolist()
            )


        elif "nama_kelas" in rombel.columns:

            data_kelas = (
                rombel["nama_kelas"]
                .tolist()
            )


        else:

            data_kelas = (
                rombel
                .iloc[:,1]
                .tolist()
            )



        # ==============================
        # DATA MAPEL
        # ==============================


        if "mapel" in mengajar.columns:


            data_mapel = (
                mengajar["mapel"]
                .unique()
                .tolist()
            )


        elif "mata_pelajaran" in mengajar.columns:


            data_mapel = (
                mengajar["mata_pelajaran"]
                .unique()
                .tolist()
            )


        else:


            data_mapel = (
                mengajar
                .iloc[:,1]
                .unique()
                .tolist()
            )



    except Exception as e:


        st.error(
            "Gagal membaca data database"
        )


        st.exception(e)

        st.stop()



    # =================================
    # TAMPILKAN HASIL BACA DATABASE
    # =================================


    st.success(
        "Database berhasil dibaca"
    )


    col1,col2,col3 = st.columns(3)


    col1.write(
        "Guru"
    )

    col1.write(
        data_guru
    )


    col2.write(
        "Kelas"
    )

    col2.write(
        data_kelas
    )


    col3.write(
        "Mapel"
    )

    col3.write(
        data_mapel
    )



    # =================================
    # DATA BEBAN MENGAJAR
    # =================================


    data_jadwal = mengajar.copy()



    # =================================
    # MEMBUAT ENGINE
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
            "Gagal membuat Scheduler Engine"
        )

        st.exception(e)

        st.stop()



    # =================================
    # MEMBUAT INDEX
    # =================================


    try:


        scheduler.create_index()


        st.success(
            "Index jadwal berhasil dibuat"
        )


    except Exception as e:


        st.error(
            "Gagal membuat index"
        )

        st.exception(e)

        st.stop()



    # =================================
    # VARIABLE AI
    # =================================


    try:


        scheduler.create_variables()


        st.success(
            "Variable AI berhasil dibuat"
        )


    except Exception as e:


        st.error(
            "Gagal membuat variable AI"
        )

        st.exception(e)

        st.stop()



    # =================================
    # CONSTRAINT
    # =================================


    if hasattr(
        scheduler,
        "build_constraints"
    ):


        try:


            scheduler.build_constraints()


            st.success(
                "Constraint berhasil dipasang"
            )


        except Exception as e:


            st.warning(
                "Constraint belum dapat dijalankan"
            )

            st.exception(e)



    else:


        st.warning(
            """
            scheduler.py belum memiliki
            fungsi build_constraints()
            """)


    st.divider()


    # =================================
    # JALANKAN AI SOLVER
    # =================================


    try:


        with st.spinner(
            "🤖 AI sedang mencari jadwal terbaik..."
        ):


            solusi = scheduler.solve()



        if solusi:


            st.success(
                "🎉 Jadwal berhasil dibuat"
            )


            hasil = scheduler.to_dataframe()



            st.subheader(
                "📅 Hasil Jadwal"
            )



            if not hasil.empty:


                st.dataframe(

                    hasil,

                    use_container_width=True

                )


            else:


                st.warning(
                    "Solver berhasil tetapi data jadwal kosong"
                )



        else:


            st.error(
                """
                AI tidak menemukan jadwal.

                Kemungkinan:
                - Beban jam terlalu banyak
                - Guru bentrok
                - Kelas tidak cukup
                - Constraint terlalu ketat
                """
            )



    except Exception as e:


        st.error(
            "Terjadi error saat menjalankan AI Solver"
        )


        st.exception(e)
