"""Provides NonLinearProgramming class."""
from pprint import pprint
from typing import List, Optional

from quibble.utils import cprint, OptimizationProblem, OptimizationResult, Solver


class NonLinearProgramming(OptimizationProblem):
    """NonLinearProgramming class."""

    def __init__(self,
                 solver_name: str = 'ipopt',
                 verbose: bool = False) -> None:
        """Constructor for NonLinearProgramming instances.

        Args:
            verbose: print details in terminal if true
            solver_name: name of solver to call, default to 'ipopt'
        """
        super().__init__(solver_name, verbose)

    def solve(self,
              solver_name: Optional[str] = None,
              initial_guess: Optional[List[float]] = None,
              trials: int = 1) -> Optional[OptimizationResult]:
        """Method for solving NonLinearProgramming instances.

        Args:
            solver_name: name of solver to use
            initial_guess: initial guess of solution
            trials: number of trials to consecutively solve problem propagating solutions

        Returns:
             result dict if solved, None else
        """
        if solver_name is not None:
            self._solver_name = solver_name

        if self._verbose:
            cprint(f"Using {self._solver_name} solver, options: {self._solver_options}",
                   'blue')

        solver = Solver(name=self._solver_name,
                        problem=self)

        solver.start(trials=trials,
                     initial_guess=initial_guess)

        if self._solved:
            cprint("", "green", end=False)
            print(f"{80 * '#'}\n")
            print("Solve succeeded.")
            if self._verbose:
                print("Results:\n")
                pprint(self._result)
            print(f"\n{80 * '#'}")
            cprint("")

        else:

            cprint("", "red", end=False)
            print(f"{80 * '#'}\n")
            print("Problem seems infeasible!")
            print(f"\n{80 * '#'}")
            cprint("")

        return self._result
