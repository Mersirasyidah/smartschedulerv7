from database import load_database
from scheduler.scheduler import Scheduler

print("Membaca database...")

db = load_database()

print("Database OK")

engine = Scheduler(db)

engine.prepare()

print("Engine siap")

hasil = engine.solve()

print("Status Solver :", hasil)

if hasil:

    df = engine.dataframe()

    print(df.head())

else:

    print("Tidak ada solusi.")
