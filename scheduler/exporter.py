"""
====================================================
SMART SCHEDULER V2
EXPORTER ENGINE
====================================================
"""

import io
import pandas as pd


class ScheduleExporter:

    def __init__(self, df_results, calendar):
        """
        Parameters:
        - df_results: DataFrame hasil dari solver.get_results()
        - calendar: Instance dari CalendarEngine
        """
        self.df = df_results
        self.calendar = calendar

    # ==================================================
    # 1. MEMBUAT GRID JADWAL UTAMA
    # ==================================================

    def build_main_grid(self):
        """
        Mengubah jadwal flat menjadi representasi tabel Grid Jadwal berdasarkan:
        Baris = Jam Pelajaran, Kolom = Hari.
        Setiap sel berisi informasi kelas, mapel, dan guru yang aktif.
        """
        if self.df.empty:
            return pd.DataFrame()

        hari_list = self.calendar.days()
        slots = self.calendar.get_slots()
        max_jam = max([s["jam"] for s in slots]) if slots else 10

        # Inisialisasi struktur grid kosong
        grid_data = {hari: ["" for _ in range(max_jam)] for hari in hari_list}

        # Isi grid berdasarkan hasil dari solver
        for _, row in self.df.iterrows():
            hari = row["Hari"]
            jam = int(row["Jam"])
            info = f"{row['Kelas']}\n{row['Mata Pelajaran']}\n({row['Guru']})"

            # Indeks list python dimulai dari 0 (jam pelajaran - 1)
            if jam <= max_jam:
                # Jika ada lebih dari satu kegiatan mengajar di jam yang sama (untuk kelas berbeda)
                if grid_data[hari][jam - 1] != "":
                    grid_data[hari][jam - 1] += f"\n\n{info}"
                else:
                    grid_data[hari][jam - 1] = info

        df_grid = pd.DataFrame(grid_data)
        df_grid.insert(0, "Jam Ke", [i + 1 for i in range(max_jam)])
        return df_grid

    # ==================================================
    # 2. MEMBUAT JADWAL SPESIFIK PER KELAS (ROMBEL)
    # ==================================================

    def build_grid_per_kelas(self, target_kelas):
        """Menghasilkan grid jadwal mingguan khusus untuk satu kelas tertentu."""
        df_filtered = self.df[self.df["Kelas"] == target_kelas]
        hari_list = self.calendar.days()
        slots = self.calendar.get_slots()
        max_jam = max([s["jam"] for s in slots]) if slots else 10

        grid_data = {hari: ["" for _ in range(max_jam)] for hari in hari_list}

        for _, row in df_filtered.iterrows():
            hari = row["Hari"]
            jam = int(row["Jam"])
            grid_data[hari][jam - 1] = f"{row['Mata Pelajaran']}\n({row['Guru']})"

        df_grid = pd.DataFrame(grid_data)
        df_grid.insert(0, "Jam Ke", [i + 1 for i in range(max_jam)])
        return df_grid

    # ==================================================
    # 3. MEMBUAT JADWAL SPESIFIK PER GURU
    # ==================================================

    def build_grid_per_guru(self, target_guru):
        """Menghasilkan grid jadwal mingguan khusus untuk satu guru tertentu."""
        df_filtered = self.df[self.df["Guru"] == target_guru]
        hari_list = self.calendar.days()
        slots = self.calendar.get_slots()
        max_jam = max([s["jam"] for s in slots]) if slots else 10

        grid_data = {hari: ["" for _ in range(max_jam)] for hari in hari_list}

        for _, row in df_filtered.iterrows():
            hari = row["Hari"]
            jam = int(row["Jam"])
            grid_data[hari][jam - 1] = f"{row['Kelas']}\n{row['Mata Pelajaran']}"

        df_grid = pd.DataFrame(grid_data)
        df_grid.insert(0, "Jam Ke", [i + 1 for i in range(max_jam)])
        return df_grid

    # ==================================================
    # 4. EXPORT KE EXCEL SEBAGAI MULTI-SHEETS BYTES
    # ==================================================

    def to_excel_bytes(self):
        """
        Mengompilasi seluruh visualisasi tabel jadwal ke dalam satu file Excel (.xlsx)
        dengan tab/sheet terpisah agar rapi saat dicetak atau dibagikan.
        """
        output = io.BytesIO()

        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            # 1. Simpan Data Flat Hasil Solver
            self.df.to_excel(writer, sheet_name="Data_Jadwal_Flat", index=False)

            # 2. Simpan Grid Utama Master Jadwal
            df_main = self.build_main_grid()
            if not df_main.empty:
                df_main.to_excel(writer, sheet_name="Master_Jadwal_Grid", index=False)

            # 3. Simpan Jadwal Per Kelas di Tab Terpisah
            all_kelas = self.df["Kelas"].unique()
            for kelas in sorted(all_kelas):
                df_k = self.build_grid_per_kelas(kelas)
                sheet_name = f"Kelas_{kelas.replace(' ', '_')}"[:31]  # Limit penamaan sheet excel maks 31 karakter
                df_k.to_excel(writer, sheet_name=sheet_name, index=False)

            # 4. Simpan Jadwal Per Guru di Tab Terpisah
            all_guru = self.df["Guru"].unique()
            for guru in sorted(all_guru):
                df_g = self.build_grid_per_guru(guru)
                sheet_name = f"Guru_{guru.replace(' ', '_')}"[:31]
                df_g.to_excel(writer, sheet_name=sheet_name, index=False)

        return output.getvalue()
