"""Provides base class for optimization problems."""
from math import inf
from typing import List, Optional, Any

from quibble.casadi import SX
from quibble.utils import cprint, DecisionVariable, Objective, Constraint, OptimizationResult


class OptimizationProblem:
    """Base class for optimization problems."""

    def __init__(self,
                 solver_name: str,
                 verbose: bool = False) -> None:
        """Constructor for optimization problem instances.

        Args:
            verbose: print details in terminal if true
            solver_name: name of solver to call
        """
        self._decision_variables: List[DecisionVariable] = []
        self._objectives: List[Objective] = []
        self._constraints: List[Constraint] = []
        self._result: Optional[OptimizationResult] = None
        self._verbose: bool = verbose

        # Solving
        self._solved: bool = False
        self._solver_name: str = solver_name  # 'ipopt'
        self._solver_options: dict = {}
        self.reset_solver_options()

    ####################################################################################################################
    # region methods
    ####################################################################################################################

    @staticmethod
    def _check_bounds(name: str,
                      upper_bound: float,
                      lower_bound: float) -> None:
        """Private method to check validity of bounds of optimization component.

        Args:
            name: name of optimization component (for error message)
            upper_bound: upper bound to check
            lower_bound: lower bound to check

        Raises:
            ValueError if upper bound is less than lower bound
        """
        if upper_bound < lower_bound:
            raise ValueError(f"upper bound of {name} is below lower bound")

    @property
    def lower_bounds_constraints(self) -> List[float]:
        return list(map(lambda _: _.lower_bound, self._constraints))

    @property
    def upper_bounds_constraints(self) -> List[float]:
        return list(map(lambda _: _.upper_bound, self._constraints))

    @property
    def names_constraints(self) -> List[str]:
        return list(map(lambda _: _.name, self._constraints))

    @property
    def lower_bounds_decision_variables(self) -> List[float]:
        return list(map(lambda _: _.lower_bound, self._decision_variables))

    @property
    def upper_bounds_decision_variables(self) -> List[float]:
        return list(map(lambda _: _.upper_bound, self._decision_variables))

    def add_solver_options(self,
                           prefix: str = None,
                           **kwargs: Any) -> None:
        """Public Method to add solver option to optimization problem.

        Args:
            prefix: prefix to solver options concatenated with '.' (e.g. ipopt)
            **kwargs: key-value-pairs of solver options

        """
        if prefix is not None:
            prefix += '.'
        else:
            prefix = ''

        for key, value in kwargs.items():
            self._solver_options[prefix + key] = value

    def reset_solver_options(self,
                             delete_all: bool = False) -> None:
        """Public Method to reset solver option to hard coded defaults.

        Args:
            delete_all: if True, all options will be deleted, set default else
        """
        if delete_all:
            self._solver_options = {}
        else:
            if self._verbose:
                solver_output = 'no'
            else:
                solver_output = 'yes'

            if self._solver_name == 'ipopt':
                self._solver_options = {'print_time': self._verbose,
                                        'ipopt.suppress_all_output': solver_output,
                                        'ipopt.linear_solver': 'mumps',
                                        'ipopt.print_level': 4}

            else:
                self._solver_options = {'print_time': self._verbose}

    # Constraints ######################################################################################################
    def add_constraint(self,
                       equation: SX,
                       lower_bound: float = -inf,
                       upper_bound: float = inf,
                       name: Optional[str] = None,
                       group: Optional[str] = None) -> None:
        """Public method to add constraint to optimization problem.

        Args:
            equation: equation to evaluate
            name: constraint name for reference
            lower_bound: lower bound to maintain
            upper_bound: upper bound to maintain
            group: optional group for reference

        """
        self._check_bounds(name=equation,
                           lower_bound=lower_bound,
                           upper_bound=upper_bound)

        if name is None:
            name = f"Constraint_{len(self._constraints) + 1}"

        self._constraints.append(Constraint(equation=equation,
                                            lower_bound=lower_bound,
                                            upper_bound=upper_bound,
                                            name=name,
                                            group=group))

        if self._verbose:
            cprint(f"Added constraint {self._constraints[-1]} to problem.",
                   'blue')

    # Objectives #######################################################################################################
    def add_objective(self,
                      objective: SX,
                      name: Optional[str] = None,
                      group: Optional[str] = None) -> None:
        """Public method to add objective function to optimization problem.

        Args:
            objective: equation to evaluate
            name: objective name for reference
            group: optional group for reference

        """
        if name is None:
            name = f"Objective_{len(self._objectives) + 1}"

        self._objectives.append(Objective(equation=objective,
                                          name=name,
                                          group=group))
        if self._verbose:
            cprint(f"Added objective {self._objectives[-1]} to problem.",
                   'blue')

    # Decision Variables ###############################################################################################
    def add_decision_variable(self,
                              name: str,
                              lower_bound: float = -inf,
                              upper_bound: float = inf,
                              group: Optional[str] = None) -> SX:
        """Public method to add decision variable to optimization problem.

        Args:
            name: variable name for reference
            lower_bound: lower bound to maintain
            upper_bound: upper bound to maintain
            group: optional group for reference

        Returns:
            Casadi symbolic variable (SX() object)
        """
        self._check_bounds(name=name,
                           lower_bound=lower_bound,
                           upper_bound=upper_bound)

        temp = SX.sym(name)

        self._decision_variables.append(DecisionVariable(variable=temp,
                                                         lower_bound=lower_bound,
                                                         upper_bound=upper_bound,
                                                         name=name,
                                                         group=group))
        if self._verbose:
            cprint(f"Added decision variable {self._decision_variables[-1]} to problem.",
                   'blue')

        return temp

    ####################################################################################################################
    # endregion setter
    ####################################################################################################################

    ####################################################################################################################
    # region solving
    ####################################################################################################################
    def solve(self,
              solver_name: Optional[str] = None,
              initial_guess: Optional[List[float]] = None,
              trials: int = 1) -> Optional[OptimizationResult]:
        """Dummy method for solving.

        Args:
            solver_name: name of solver to use
            initial_guess: initial guess of solution as List[float]
            trials: number of trials to consecutively solve problem propagating solutions

        Returns:
             result dict if solved, None else
        """
        pass

    ####################################################################################################################
    # endregion methods
    ####################################################################################################################

    ####################################################################################################################
    # region getter and setter
    ####################################################################################################################
    @property
    def verbose(self) -> bool:
        return self._verbose

    @verbose.setter
    def verbose(self, value: bool) -> None:
        self._verbose = value

    # Constraints ######################################################################################################
    @property
    def constraints(self) -> List[Constraint]:
        return self._constraints

    # Objectives #######################################################################################################
    @property
    def objectives(self) -> List[Objective]:
        return self._objectives

    # Decision Variables ###############################################################################################
    @property
    def decision_variables(self) -> List[DecisionVariable]:
        return self._decision_variables

    # Results #########################################################################################################
    @property
    def result(self) -> OptimizationResult:
        if not self._solved:
            cprint("Problem not solved yet or no feasible solution found!",
                   'yellow')
        return self._result

    @result.setter
    def result(self, value: dict) -> None:
        self._result = value

    @property
    def solved(self) -> bool:
        return self._solved

    @solved.setter
    def solved(self, value: bool) -> None:
        self._solved = value

    # Solver ###########################################################################################################
    @property
    def solver_name(self) -> str:
        return self._solver_name

    @solver_name.setter
    def solver_name(self, name: str) -> None:
        self._solver_name = name
        self.reset_solver_options()

    @property
    def solver_options(self) -> dict:
        return self._solver_options

    @solver_options.setter
    def solver_options(self, option_dict: dict) -> None:
        self._solver_options = option_dict

    ####################################################################################################################
    # endregion getter and setter
    ####################################################################################################################
