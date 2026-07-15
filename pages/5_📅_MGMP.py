import streamlit as st
from database import load_database

st.title("📅 Hari MGMP Guru")

db = load_database()

if "Guru" in db:

    guru = db["Guru"]

    st.dataframe(
        guru[
            [
                "Nama Guru",
                "Nama Mapel",
                "Hari MGMP"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )
