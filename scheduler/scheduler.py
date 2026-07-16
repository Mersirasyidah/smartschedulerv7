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


    def prepare(self):

        self.loader.load_all()

        self.calendar = CalendarEngine(self.loader)

        self.calendar.build()


        self.variables = VariableBuilder(

            self.loader,

            self.calendar

        )

        self.variables.build()


        self.constraints = ConstraintBuilder(

            self.loader,

            self.calendar,

            self.variables

        )

        self.constraints.build()


        self.objective = ObjectiveBuilder(

            self.loader,

            self.variables

        )

        self.objective.build()


        self.solver = SolverEngine(

            self.variables.model

        )


    def solve(self):

        return self.solver.solve()


    def dataframe(self):

        self.exporter = Exporter(

            self.loader,

            self.calendar,

            self.variables,

            self.solver

        )

        return self.exporter.to_dataframe()
