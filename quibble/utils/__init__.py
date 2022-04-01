"""Init for Quibble utils."""
from .functions import cprint, replace_inf
from .components import Objective, Constraint, DecisionVariable, ResultComponent
from .result import OptimizationResult
from .solver import Solver
from .problem import OptimizationProblem
