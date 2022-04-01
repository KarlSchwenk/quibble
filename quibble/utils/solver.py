from __future__ import annotations  # noqa T484

from random import random
from typing import Optional, List, Any

import numpy as np

from quibble import casadi as cd
from quibble.utils import replace_inf, cprint
from quibble.utils.problem import OptimizationProblem
from quibble.utils.result import OptimizationResult


class Solver:
    """Class for quibble solvers."""

    def __init__(self,
                 name: str,
                 problem: Optional[OptimizationProblem] = None) -> None:
        """Constructor method for Quibble Solver instances."""
        # some checks
        if name not in ['ipopt']:
            raise NotImplementedError(f"unknown solver name '{name}'")

        from quibble.utils.problem import OptimizationProblem
        if not isinstance(problem, OptimizationProblem):
            raise NotImplementedError(f"unknown problem class '{type(problem)}'")

        self._problem = problem
        self._name = name
        self._solver_instance = None
        self._solver_result: dict = {}

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def problem(self) -> OptimizationProblem:
        return self._problem

    @problem.setter
    def problem(self, value: OptimizationProblem) -> None:
        self._problem = value

    def _save_optimal_values(self) -> None:
        """Private method to save optimal values to OptimizationResult instance."""
        if self._problem.solved:
            self._problem.result = OptimizationResult()

            # constraints #########################################################################
            for count, constraint in enumerate(self._problem.constraints):
                constraint_result = constraint.to_result_component()
                #
                temp_function = cd.Function(constraint.name,
                                            list(map(lambda _: _.variable,
                                                     self._problem.decision_variables)),
                                            [constraint.variable])
                temp_result = float(
                    temp_function.call(
                        [self._solver_result['x'][_]
                         for _ in range(len(self._problem.decision_variables))])[0])

                constraint_result.optimal_value = temp_result
                del temp_function

                # constraint_result.optimal_value = float(self._solver_result['g'][count])

                activation_epsilon = 10 ** -5
                constraint_result.upper_bound_active = \
                    (abs(constraint.upper_bound - constraint_result.optimal_value) < activation_epsilon)
                constraint_result.lower_bound_active = \
                    (abs(constraint.lower_bound - constraint_result.optimal_value) < activation_epsilon)

                self._problem.result.constraints.append(constraint_result)

            # decision variables ##################################################################
            for count, dec_var in enumerate(self._problem.decision_variables):
                dec_var_result = dec_var.to_result_component()
                dec_var_result.optimal_value = float(self._solver_result['x'][count])
                self._problem.result.decision_variables.append(dec_var_result)

            # objectives ##########################################################################
            for objective in self._problem.objectives:
                objective_result = objective.to_result_component()
                temp_function = cd.Function(objective.name,
                                            list(map(lambda _: _.variable,
                                                     self._problem.decision_variables)),
                                            [objective.variable])
                temp_result = float(
                    temp_function.call(
                        [self._solver_result['x'][_] for _ in range(len(self._problem.decision_variables))])[0])
                objective_result.optimal_value = temp_result
                del temp_function
                self._problem.result.objectives.append(objective_result)

    def _check_constraints(self,
                           candidate: List[Any]) -> Optional[List[float]]:
        """Private method to check if possible solution satisfies constraints.

        Args:
            candidate: possible solution candidate

        Returns:
            None, if candidate dissatisfies constraints, list of constraints values else.
        """
        constraint_values = []
        for constraint in self._problem.constraints:
            temp_function = cd.Function(constraint.name,
                                        list(map(lambda _: _.variable,
                                                 self._problem.decision_variables)),
                                        [constraint.variable])
            constraint_value = float(temp_function.call(candidate)[0])

            if not constraint.lower_bound <= constraint_value <= constraint.upper_bound:
                return None
            constraint_values.append(constraint_value)

        return constraint_values

    def _ipopt_start(self,
                     trials: int = 1,
                     initial_guess: Optional[List[float]] = None) -> None:
        """Private method to start IPOPT Solver."""
        if self._problem is None:
            raise ValueError("Problem to solve not set yet!")

        self._solver_instance = cd.nlpsol('F',
                                          self._problem.solver_name,
                                          {'x': cd.vcat([_.variable for _ in self._problem.decision_variables]),
                                           'f': sum([_.variable for _ in self._problem.objectives]),
                                           'g': cd.vcat([_.variable for _ in self._problem.constraints])},
                                          self._problem.solver_options)

        if initial_guess is None:
            initial_guess = [
                float(
                    replace_inf(var.lower_bound) + random() *
                    (replace_inf(var.upper_bound) - replace_inf(var.lower_bound)))
                for var in self._problem.decision_variables]

        self._problem.solved = False

        cprint("Start solving...",
               'blue',
               end=False)

        successful_trials = []
        failed_trials = []

        for trial in range(trials):

            result = self._solver_instance(x0=cd.vcat(initial_guess),  # noqa: T484
                                           lbx=cd.vcat(self._problem.lower_bounds_decision_variables),
                                           ubx=cd.vcat(self._problem.upper_bounds_decision_variables),
                                           lbg=cd.vcat(self._problem.lower_bounds_constraints),
                                           ubg=cd.vcat(self._problem.upper_bounds_constraints))

            if not self._solver_instance.stats()['success']:  # noqa: T484
                # trial failed
                print(f"Could not solve problem on trial {trial + 1}.")
                if self._problem.verbose:
                    print(f"    Solver Status: {self._solver_instance.stats()['return_status']}")  # noqa: T484
                    print("    Use Lagrange multiplier for initial guess and try again...")
                next_guess = []
                failed_trials.append(result)
                for count, _ in enumerate(self._problem.decision_variables):
                    next_guess.append(float(result['lam_x'][count]))
                initial_guess = next_guess

            else:
                # trial successful
                print(f'Successfully solved problem on trial {trial + 1}.')
                if self._problem.verbose:
                    print(f"    Current objective value: {float(result['f'])}")
                    print(f"    Solver Status: {self._solver_instance.stats()['return_status']}")  # noqa: T484
                    if trial < trials - 1:
                        print("    Use current result and see if we can get better...")
                successful_trials.append(result)

                next_guess = []
                for count, _ in enumerate(self._problem.decision_variables):
                    next_guess.append(float(result['x'][count]))
                initial_guess = next_guess

        cprint("")

        if not successful_trials:
            cprint("Could not solve problem!", "r")
            self._problem.solved = False

        else:
            best_result_index = int(np.argmin(list(map(lambda x: float(x['f']), successful_trials))))
            self._solver_result = successful_trials[best_result_index]
            self._problem.solved = True

            # TODO: check also self._solver_instance.stats()['return_status']

            # success == True
            # EXIT: Optimal Solution Found. : Solve_Succeeded
            # EXIT: Solved to acceptable level. : Acceptable_Level

            # success == False
            # EXIT: Converged to a point of local infeasibility.
            # Problem may be infeasible. : Infeasible_Problem_Detected
            # EXIT: Maximum Number of Iterations Exceeded. : Maximum_Iterations_Exceeded
            # EXIT: Restoration Failed! : Restoration_Failed
            # EXIT: Invalid number in NLP function or derivative detected. : Invalid_Number_Detected
            # EXIT: Invalid option encountered. : Invalid_Option

        self._save_optimal_values()

    def start(self,
              trials: int = 1,
              initial_guess: Optional[List[float]] = None) -> None:
        """Public method to start solver.

        Args:
            trials: number of consecutive solving trials.
            initial_guess: optional list of assumed solution values.

        """
        if self._name == 'ipopt':
            self._ipopt_start(trials=trials,
                              initial_guess=initial_guess)
