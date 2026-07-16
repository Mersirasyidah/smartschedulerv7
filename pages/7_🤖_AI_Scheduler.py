import streamlit as st
import pandas as pd

from database import load_database
from scheduler import Scheduler

# ==========================================================
# KONFIGURASI HALAMAN
# ==========================================================
st.set_page_config(
    page_title="AI Scheduler",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Scheduler V2")
st.caption("Smart Scheduler V2 - AI Timetable Generator")
st.divider()

# ==========================================================
# LOAD DATABASE
# ==========================================================
try:
    db = load_database()
except Exception as e:
    st.error("Database gagal dibaca.")
    st.exception(e)
    st.stop()

# ==========================================================
# MEMBACA TABEL
# ==========================================================
required_tables = [
    "Guru",
    "Guru_Mengajar",
    "Rombel",
    "Mapel",
    "Hari_Jam"
]

missing = [
    table
    for table in required_tables
    if table not in db
]

if missing:
    st.error(f"Tabel berikut belum tersedia: {', '.join(missing)}")
    st.stop()

guru = db["Guru"]
mengajar = db["Guru_Mengajar"]
rombel = db["Rombel"]
mapel = db["Mapel"]
hari_jam = db["Hari_Jam"]

# ==========================================================
# DASHBOARD STATISTIK
# ==========================================================
st.subheader("📊 Statistik Database")
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Guru", len(guru))
c2.metric("Mapel", len(mapel))
c3.metric("Rombel", len(rombel))
c4.metric("Mengajar", len(mengajar))
c5.metric("Hari/Jam", len(hari_jam))
st.divider()

# ==========================================================
# PREVIEW DATABASE
# ==========================================================
with st.expander("📂 Preview Database"):
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "Guru",
            "Guru Mengajar",
            "Rombel",
            "Mapel",
            "Hari_Jam"
        ]
    )
    with tab1:
        st.dataframe(guru, use_container_width=True)
    with tab2:
        st.dataframe(mengajar, use_container_width=True)
    with tab3:
        st.dataframe(rombel, use_container_width=True)
    with tab4:
        st.dataframe(mapel, use_container_width=True)
    with tab5:
        st.dataframe(hari_jam, use_container_width=True)

st.divider()

# ==========================================================
# SESSION STATE
# ==========================================================
if "jadwal" not in st.session_state:
    st.session_state.jadwal = pd.DataFrame()
if "scheduler" not in st.session_state:
    st.session_state.scheduler = None

# ==========================================================
# TOMBOL GENERATE
# ==========================================================
generate = st.button(
    "🚀 Generate Jadwal",
    use_container_width=True,
    type="primary"
)

# ==========================================================
# GENERATE SCHEDULER (ALUR EKSEKUSI V2 + FITUR AUTO-DEBUGGING)
# ==========================================================
if generate:
    st.divider()
    st.subheader("🤖 AI Scheduler Progress")
    progress = st.progress(0)
    status = st.empty()

    try:
        # 1. Inisialisasi Scheduler Engine
        status.info("Membuat Scheduler Engine...")
        scheduler = Scheduler(db)
        st.session_state.scheduler = scheduler
        progress.progress(15)

        # 2. Persiapan Data & Slot Pembelajaran
        status.info("Mempersiapkan slot pembelajaran & index database...")
        scheduler.prepare_engine()
        progress.progress(35)

        # --------------------------------------------------
        # 🔍 KOTAK ANALISIS KAPASITAS OTOMATIS (DEBUGGING)
        # --------------------------------------------------
        status.info("Menganalisis kapasitas data sekolah...")
        total_jp = int(scheduler.mengajar[scheduler.col_jp].sum())
        total_slot = len(scheduler.slot)
        total_kelas = len(scheduler.rombel)
        kapasitas_maks = total_kelas * total_slot
        
        st.info(f"""
        **📋 Hasil Audit Kapasitas Excel Anda:**
        *   Total JP yang diminta di Excel: **{total_jp} JP**
        *   Jumlah Rombel/Kelas: **{total_kelas} Kelas**
        *   Jumlah Slot Waktu Mengajar (per Minggu): **{total_slot} Slot**
        *   Kapasitas Maksimal Sekolah: **{kapasitas_maks} JP** (yaitu: {total_kelas} Kelas × {total_slot} Slot)
        """)
        
        # Evaluasi Kelayakan Matematis
        if total_jp > kapasitas_maks:
            st.error(
                f"🚨 **KESALAHAN DATA:** Total JP ({total_jp} JP) melebihi kapasitas maksimal sekolah ({kapasitas_maks} JP)! "
                f"Silakan kurangi atau pangkas minimal **{total_jp - kapasitas_maks} JP** pada file Excel Anda "
                f"di sheet `Guru_Mengajar` sebelum menjalankan ulang aplikasi ini."
            )
            progress.progress(100)
            status.error("Proses dihentikan karena keterbatasan kapasitas slot.")
            st.stop()
        else:
            st.success("✅ Kapasitas slot secara matematis mencukupi! Melanjutkan kompilasi AI...")
            progress.progress(50)

        # 3. Proses Solving (Variabel & Constraint ditangani di dalam .solve())
        status.info("Menjalankan AI Solver (Mengompilasi Constraint & Optimasi CP-SAT)...")
        sukses = scheduler.solve(timeout_seconds=60.0)
        progress.progress(90)

        # 4. Evaluasi Hasil
        if sukses:
            st.session_state.jadwal = scheduler.df_hasil
            progress.progress(100)
            status.success("AI berhasil membuat jadwal optimal!")
            st.success("🎉 Jadwal berhasil dibuat!")
        else:
            progress.progress(100)
            status.error("AI tidak menemukan solusi yang layak.")
            st.error(
                """
                **Penyebab yang mungkin terjadi:**
                *   **Beban Mengajar Guru Terlalu Tinggi:** Ada guru dengan jam mengajar mingguan yang melebihi jumlah hari kerja sekolah.
                *   **Aturan Bentrok:** Kombinasi ketersediaan guru sangat sempit (misal banyak guru meminta hari libur yang sama di MGMP).
                *   **Kapasitas Terlalu Mepet:** Meskipun secara matematis cukup, data JP yang terlalu mendekati limit slot maksimal membuat AI kesulitan menemukan celah jadwal yang bebas bentrok.
                """
            )
    except Exception as e:
        st.error("Terjadi error saat men-generate jadwal.")
        st.exception(e)

# ==========================================================
# OUTPUT JADWAL & EKSPOR FILE EXCEL
# ==========================================================
if not st.session_state.jadwal.empty:
    st.subheader("🗓️ Hasil Jadwal Generasi AI")
    st.dataframe(st.session_state.jadwal, use_container_width=True)

    # Mempersiapkan File Excel Multi-Sheet via Exporter V2
    try:
        excel_data = st.session_state.scheduler.export()
        if excel_data:
            st.download_button(
                label="📥 Unduh Jadwal Lengkap (Format Excel)",
                data=excel_data,
                file_name="Jadwal_Sekolah_AI_V2.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
    except Exception as e:
        st.warning("Gagal mempersiapkan file unduhan Excel.")
        st.exception(e)
