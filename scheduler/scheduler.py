from .loader import DataLoader
from .calendar import CalendarEngine
from .variables import VariableBuilder
from .constraints import ConstraintBuilder
from .objective import ObjectiveBuilder
from .solver import SolverEngine
from .exporter import Exporter


class Scheduler:

    def __init__(self, database):

        self.database = database

        self.loader = DataLoader(database)

        self.calendar = None

        self.variables = None

        self.constraints = None

        self.objective = None

        self.solver = None

        self.exporter = None

    # ==================================================
    # PERSIAPAN ENGINE
    # ==================================================
    def prepare(self):

        print("=" * 60)
        print("MEMBACA DATABASE")
        print("=" * 60)

        # Load seluruh data
        self.loader.load_all()

        print("✓ Database berhasil dibaca")

        # Bangun kalender
        self.calendar = CalendarEngine(self.loader)
        self.calendar.build()

        print("✓ Calendar Engine selesai")

        # Bangun variabel OR-Tools
        self.variables = VariableBuilder(
            self.loader,
            self.calendar
        )
        self.variables.build()

        print("✓ Variable Builder selesai")

        # Constraint
        self.constraints = ConstraintBuilder(
            self.loader,
            self.calendar,
            self.variables
        )
        self.constraints.build()

        print("✓ Constraint selesai")

        # Objective
        self.objective = ObjectiveBuilder(
            self.loader,
            self.variables
        )
        self.objective.build()

        print("✓ Objective selesai")

        # Solver
        self.solver = SolverEngine(
            self.variables.model
        )

        print("✓ Solver siap")
        print("=" * 60)

    # ==================================================
    # MENJALANKAN SOLVER
    # ==================================================
    def solve(self):

        return self.solver.solve()

    # ==================================================
    # HASIL DATAFRAME
    # ==================================================
    def dataframe(self):

        self.exporter = Exporter(
            self.loader,
            self.calendar,
            self.variables,
            self.solver
        )

        return self.exporter.to_dataframe()
