"""Provides classes for optimization components."""
from __future__ import annotations  # noqa T484

from math import inf
from typing import Optional

from quibble import casadi as cd


class OptimizationComponent:
    """Base class for optimization components."""

    def __init__(self,
                 variable: cd.SX,
                 lower_bound: float = -inf,
                 upper_bound: float = inf,
                 name: Optional[str] = None,
                 group: Optional[str] = None) -> None:
        """Constructor method for optimization components.

        Args:
            variable: Casadi type symbolic variable
            lower_bound: lower bound of component
            upper_bound: upper bound of component
            name: name for reference
            group: group for reference
        """
        self._name = name
        self._variable = variable
        self._lower_bound = lower_bound
        self._upper_bound = upper_bound
        self._group = group

    def __str__(self) -> str:
        return f"{self._name}: {self._lower_bound} <= {self._variable} <= {self._upper_bound}"

    def to_result_component(self) -> ResultComponent:
        """Public method to create result component from optimization component.

        Returns: result component equivalent

        """
        return ResultComponent(name=self._name,
                               group=self._group)

    @property
    def lower_bound(self) -> float:
        return self._lower_bound

    @property
    def upper_bound(self) -> float:
        return self._upper_bound

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def variable(self) -> cd.SX:
        return self._variable

    @property
    def group(self) -> Optional[str]:
        return self._group


class DecisionVariable(OptimizationComponent):
    """Inherited component for decision variables."""

    def __init__(self,
                 variable: cd.SX,
                 lower_bound: float = -inf,
                 upper_bound: float = inf,
                 name: Optional[str] = None,
                 group: Optional[str] = None,
                 is_discrete: bool = False) -> None:
        """Constructor method for decision variables.

        Args:
            variable: decision variable
            lower_bound: lower bound of decision variable
            upper_bound: upper bound of decision variable
            name: name of decision variable for reference
            group: group name of decision variable for reference
            is_discrete: flag indicating integer variable if True
        """
        super().__init__(variable, lower_bound, upper_bound, name, group)

        self._is_discrete = is_discrete

    @property
    def is_discrete(self) -> bool:
        return self._is_discrete

    @is_discrete.setter
    def is_discrete(self, value: bool) -> None:
        self._is_discrete = value


class Constraint(OptimizationComponent):
    """Inherited component for constraints."""
    def __init__(self,
                 equation: cd.SX,
                 lower_bound: float = -inf,
                 upper_bound: float = inf,
                 name: Optional[str] = None,
                 group: Optional[str] = None) -> None:
        """Constructor method for constraints.

        Args:
            equation: center of constraint equation
            lower_bound: lower bound of constraint
            upper_bound: upper bound of constraint
            name: name of constraint for reference
            group: group name of constraint for reference
        """
        super().__init__(equation,
                         lower_bound,
                         upper_bound,
                         name,
                         group)


class Objective(OptimizationComponent):
    """Inherited component for optimization objective."""
    def __init__(self,
                 equation: cd.SX,
                 name: Optional[str] = None,
                 group: Optional[str] = None) -> None:
        """Constructor method for optimization objective.

        Args:
            equation: equation of optimization objective
            name: name of optimization objective for reference
            group: group name of optimization objective for reference
        """
        super().__init__(variable=equation,
                         name=name,
                         group=group)

    def __str__(self) -> str:
        return f"{self._name}: {self._variable}"


class ResultComponent:
    """Component to store single optimization results."""

    def __init__(self,
                 name: Optional[str],
                 group: Optional[str] = None) -> None:
        """Constructor for result components.

        Args:
            name: component name
            group: optional group of component
        """
        self._name = name
        self._group = group
        self._optimal_value: Optional[float] = None
        self._lower_bound_active: bool = False
        self._upper_bound_active: bool = False

    #####################################################################
    # region getter setter
    #####################################################################
    @property
    def name(self) -> Optional[str]:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def group(self) -> Optional[str]:
        return self._group

    @group.setter
    def group(self, value: str) -> None:
        self._group = value

    @property
    def optimal_value(self) -> Optional[float]:
        return self._optimal_value

    @optimal_value.setter
    def optimal_value(self, value: float) -> None:
        self._optimal_value = value

    @property
    def lower_bound_active(self) -> bool:
        return self._lower_bound_active

    @lower_bound_active.setter
    def lower_bound_active(self, value: bool) -> None:
        self._lower_bound_active = value

    @property
    def upper_bound_active(self) -> bool:
        return self._upper_bound_active

    @upper_bound_active.setter
    def upper_bound_active(self, value: bool) -> None:
        self._upper_bound_active = value

    #####################################################################
    # endregion getter setter
    #####################################################################
