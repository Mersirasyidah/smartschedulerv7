import streamlit as st
from database import load_database

st.title("📅 Hari MGMP Guru")

db = load_database()

guru = db["Guru"]

st.dataframe(
    guru[
        [
            "ID Guru",
            "Nama Guru",
            "Hari MGMP",
            "Prioritas"
        ]
    ],
    use_container_width=True,
    hide_index=True
)
