import streamlit as st
import pandas as pd

from database import load_database
from scheduler import Scheduler


# =====================================
# KONFIGURASI
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



guru = db["Guru"]

mengajar = db["Guru_Mengajar"]

rombel = db["Rombel"]



# =====================================
# STATISTIK
# =====================================

c1,c2,c3 = st.columns(3)


c1.metric(
    "Guru",
    len(guru)
)


c2.metric(
    "Mengajar",
    len(mengajar)
)


c3.metric(
    "Rombel",
    len(rombel)
)


st.divider()



# =====================================
# GENERATE
# =====================================

if st.button(
    "🚀 Generate Jadwal",
    use_container_width=True
):


    try:


        st.info(
            "Membaca data sekolah..."
        )



        # =============================
        # DATA GURU
        # =============================

        if "nama_guru" in guru.columns:

            data_guru = guru["nama_guru"].tolist()

        elif "nama" in guru.columns:

            data_guru = guru["nama"].tolist()

        else:

            data_guru = guru.iloc[:,1].tolist()



        # =============================
        # DATA KELAS
        # =============================


        if "kelas" in rombel.columns:

            data_kelas = rombel["kelas"].tolist()

        elif "nama_kelas" in rombel.columns:

            data_kelas = rombel["nama_kelas"].tolist()

        else:

            data_kelas = rombel.iloc[:,1].tolist()



        # =============================
        # DATA MAPEL
        # =============================


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
                mengajar.iloc[:,1]
                .unique()
                .tolist()
            )



        st.success(
            "Data berhasil dibaca"
        )



        # =============================
        # BUAT ENGINE
        # =============================


        scheduler = Scheduler(

            data_guru,

            data_kelas,

            data_mapel,

            mengajar

        )


        st.success(
            "Scheduler Engine dibuat"
        )



        scheduler.create_index()


        st.success(
            "Index jadwal dibuat"
        )



        scheduler.create_variables()


        st.success(
            "Variable AI dibuat"
        )



        scheduler.build_constraints()


        st.success(
            "Constraint dipasang"
        )



        # =============================
        # SOLVER
        # =============================


        with st.spinner(
            "🤖 AI mencari jadwal..."
        ):


            solusi = scheduler.solve()



        if solusi:


            hasil = scheduler.to_dataframe()



            if hasil.empty:


                st.warning(
                    "AI selesai tetapi jadwal kosong"
                )


            else:


                # SIMPAN KE SESSION

                st.session_state["jadwal"] = hasil



                st.success(
                    "🎉 Jadwal berhasil dibuat"
                )



                st.subheader(
                    "📅 HASIL JADWAL"
                )



                st.dataframe(

                    hasil,

                    use_container_width=True,

                    hide_index=True

                )



        else:


            st.error(
                "AI tidak menemukan solusi"
            )



    except Exception as e:


        st.error(
            "Terjadi kesalahan"
        )

        st.exception(e)
