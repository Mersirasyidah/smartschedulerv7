import streamlit as st

from database import load_database
from scheduler.scheduler import Scheduler

st.title("🧪 Test Scheduler V2")

if st.button("Jalankan Scheduler V2"):

    db = load_database()

    engine = Scheduler(db)

    engine.prepare()

    status = engine.solve()

    st.write("Status Solver:", status)

    if status:
        df = engine.dataframe()
        st.dataframe(df)
    else:
        st.error("Tidak ada solusi.")
