import streamlit as st
import pandas as pd

from database import load_database
from scheduler import Scheduler


st.set_page_config(
    page_title="AI Scheduler",
    page_icon="🤖",
    layout="wide"
)


st.title("🤖 AI Scheduler")
st.caption("Smart Scheduler V7")



# ===============================
# LOAD DATABASE
# ===============================

try:

    db = load_database()

except Exception as e:

    st.error("Database gagal dibaca")
    st.exception(e)
    st.stop()



guru = db["Guru"]

mengajar = db["Guru_Mengajar"]

rombel = db["Rombel"]



# ===============================
# STATISTIK
# ===============================

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



# ===============================
# GENERATE
# ===============================


if st.button(
    "🚀 Generate Jadwal",
    use_container_width=True
):


    try:


        # ---------------------------
        # Ambil Guru
        # ---------------------------

        if "nama_guru" in guru.columns:

            data_guru = guru["nama_guru"].tolist()

        elif "nama" in guru.columns:

            data_guru = guru["nama"].tolist()

        else:

            data_guru = guru.iloc[:,1].tolist()



        # ---------------------------
        # Ambil Kelas
        # ---------------------------

        if "kelas" in rombel.columns:

            data_kelas = rombel["kelas"].tolist()

        elif "nama_kelas" in rombel.columns:

            data_kelas = rombel["nama_kelas"].tolist()

        else:

            data_kelas = rombel.iloc[:,1].tolist()



        # ---------------------------
        # Ambil Mapel
        # ---------------------------

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
            "Database berhasil dibaca"
        )



        # ===========================
        # ENGINE
        # ===========================


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
            "Index dibuat"
        )



        scheduler.create_variables()


        st.success(
            "Variable AI dibuat"
        )



        scheduler.build_constraints()


        st.success(
            "Constraint dibuat"
        )



        # ===========================
        # SOLVER
        # ===========================


        with st.spinner(
            "AI mencari jadwal..."
        ):


            hasil_solver = scheduler.solve()



        if hasil_solver:


            st.success(
                "Solver menemukan solusi"
            )



            hasil = scheduler.to_dataframe()



            st.write(
                "Jumlah Jadwal:",
                len(hasil)
            )



            if len(hasil)>0:


                # SIMPAN FILE

                hasil.to_csv(

                    "hasil_jadwal.csv",

                    index=False

                )



                # SIMPAN SESSION

                st.session_state["jadwal"] = hasil



                st.success(
                    "🎉 Jadwal berhasil dibuat dan disimpan"
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
                    """
                    Solver berhasil tetapi hasil jadwal kosong.

                    Periksa scheduler.py
                    """
                )



        else:


            st.error(
                "AI tidak menemukan jadwal"
            )



    except Exception as e:


        st.error(
            "Terjadi error"
        )

        st.exception(e)
