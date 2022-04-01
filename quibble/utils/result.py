"""Provides class for optimization results."""
from typing import Optional, List, Union
from quibble.utils import Constraint, Objective, DecisionVariable


class OptimizationResult:
    """Class to store results."""

    def __init__(self) -> None:
        """Constructor for optimization result class."""
        # from quibble.utils import Constraint, Objective, DecisionVariable
        self._constraints: List[Constraint] = []
        self._objectives: List[Objective] = []
        self._decision_variables: List[DecisionVariable] = []

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return str({
            'objective_sum': self.optimal_objective_sum(),
            'optimal_values': {
                'objectives': self.optimal_objective_values(as_dict=True),
                'decision_variables': self.optimal_decision_variables(as_dict=True),
                'constraints': self.optimal_constraint_values(as_dict=True)
            },

            'active_set': {
                'constraints': {
                    'lower_bounds': self.active_lower_bounds_constraints(as_dict=True),
                    'upper_bounds': self.active_upper_bounds_constraints(as_dict=True)
                },
                'decision_variables': {
                    'lower_bounds': self.active_lower_bounds_decision_variables(as_dict=True),
                    'upper_bounds': self.active_upper_bounds_decision_variables(as_dict=True)
                }
            }
        })

    #####################################################################
    # region methods
    #####################################################################
    @staticmethod
    def _extract_optimal_values(as_dict: bool,
                                group: Optional[str],
                                category: list) -> Union[List[float], dict]:
        """Internal method to extract optimal values from solution.

        Args:
            as_dict: if True: return a dict, variable names as keys, return list else
            group: select variables of specified group only
            category: optimization component to extract optimal values from

        Returns:
            List or dictionary of optimal values

        """
        if group is None:
            out_list = list(map(lambda obj: obj.optimal_value, category))
            out_dict = {}

            for count, obj in enumerate(category):
                out_dict[obj.name] = out_list[count]
        else:

            out_list = list(map(lambda obj: obj.optimal_value,
                                filter(lambda obj: obj.group == group,
                                       category)))
            out_dict = {}

            for count, obj in enumerate(filter(lambda obj: obj.group == group, category)):
                out_dict[obj.name] = obj.optimal_value

        if as_dict:
            return out_dict
        return out_list

    @staticmethod
    def _extract_active_upper_bound(as_dict: bool,
                                    group: Optional[str],
                                    category: list) -> Union[List[bool], dict]:
        """Internal method to extract active upper bounds from solution.

        Args:
            as_dict: if True: return a dict, variable names as keys, return list else
            group: select variables of specified group only
            category: optimization component to extract active upper bound values from

        Returns:
            List or dictionary of active upper bounds

        """
        if group is None:
            out_list = list(map(lambda obj: obj.optimal_value, category))
            out_dict = {}

            for count, obj in enumerate(category):
                out_dict[obj.name] = out_list[count]
        else:

            out_list = list(map(lambda obj: obj.optimal_value,
                                filter(lambda obj: obj.group == group,
                                       category)))
            out_dict = {}

            for count, obj in enumerate(filter(lambda obj: obj.group == group, category)):
                out_dict[obj.name] = obj.optimal_value

        if as_dict:
            return out_dict
        return out_list

    @staticmethod
    def _extract_active_lower_bound(as_dict: bool,
                                    group: Optional[str],
                                    category: list) -> Union[List[bool], dict]:
        """Internal method to extract active lower bounds from solution.

        Args:
            as_dict: if True: return a dict, variable names as keys, return list else
            group: select variables of specified group only
            category: optimization component to extract active lower bound values from

        Returns:
            List or dictionary of active lower bounds

        """
        if group is None:
            out_list = list(map(lambda obj: obj.optimal_value, category))
            out_dict = {}

            for count, obj in enumerate(category):
                out_dict[obj.name] = out_list[count]
        else:

            out_list = list(map(lambda obj: obj.optimal_value,
                                filter(lambda obj: obj.group == group,
                                       category)))
            out_dict = {}

            for count, obj in enumerate(filter(lambda obj: obj.group == group, category)):
                out_dict[obj.name] = obj.optimal_value

        if as_dict:
            return out_dict
        return out_list

    def optimal_decision_variables(self,
                                   as_dict: bool = False,
                                   group: Optional[str] = None) -> Union[List[float], dict]:
        """Public method to access optimal decision variables from solution.

        Args:
            as_dict: if True: return a dict, variable names as keys, return list else
            group: select variables of specified group only

        Returns:
            List or dictionary of optimal decision variables if problem was solved

        """
        return self._extract_optimal_values(as_dict=as_dict,
                                            group=group,
                                            category=self._decision_variables)

    def optimal_constraint_values(self,
                                  as_dict: bool = False,
                                  group: Optional[str] = None) -> Union[List[float], dict]:
        """Public method to access optimal constraint values from solution.

        Args:
            as_dict: if True: return a dict, variable names as keys, return list else
            group: select variables of specified group only

        Returns:
            List or dictionary of optimal constraint values if problem was solved

        """
        return self._extract_optimal_values(as_dict=as_dict,
                                            group=group,
                                            category=self._constraints)

    def optimal_objective_values(self,
                                 as_dict: bool = False,
                                 group: Optional[str] = None) -> Union[List[float], dict]:
        """Public method to access optimal objective value from solution.

        Args:
            as_dict: if True: return a dict, variable names as keys, return list else
            group: select variables of specified group only

        Returns:
            List or dictionary of optimal objective values if problem was solved

        """
        return self._extract_optimal_values(as_dict=as_dict,
                                            group=group,
                                            category=self._objectives)

    def optimal_objective_sum(self,
                              group: Optional[str] = None) -> float:
        """Public method to access sum of optimal objective values from solution.

        Args:
            group: select variables of specified group only

        Returns:
            Sum of optimal objective values if problem was solved

        """
        return sum(self._extract_optimal_values(as_dict=False,
                                                group=group,
                                                category=self._objectives))

    def active_lower_bounds_constraints(self,
                                        as_dict: bool = False,
                                        group: Optional[str] = None) -> Union[List[bool], dict]:
        """Public method to access active lower bounds of constraints from solution.

        Args:
            as_dict: if True: return a dict, variable names as keys, return list else
            group: select variables of specified group only

        Returns:
            List or dictionary of active lower bounds of constraints if problem was solved.

        """
        return self._extract_active_lower_bound(as_dict=as_dict,
                                                group=group,
                                                category=self._constraints)

    def active_upper_bounds_constraints(self,
                                        as_dict: bool = False,
                                        group: Optional[str] = None) -> Union[List[bool], dict]:
        """Public method to access active lower upper of constraints from solution.

        Args:
            as_dict: if True: return a dict, variable names as keys, return list else
            group: select variables of specified group only

        Returns:
            List or dictionary of active upper bounds of constraints if problem was solved.

        """
        return self._extract_active_upper_bound(as_dict=as_dict,
                                                group=group,
                                                category=self._constraints)

    def active_lower_bounds_decision_variables(self,
                                               as_dict: bool = False,
                                               group: Optional[str] = None) -> Union[List[bool], dict]:
        """Public method to access active lower bounds of decision variables from solution.

        Args:
            as_dict: if True: return a dict, variable names as keys, return list else
            group: select variables of specified group only

        Returns:
            List or dictionary of active lower bounds of decision variables if problem was solved.

        """
        return self._extract_active_lower_bound(as_dict=as_dict,
                                                group=group,
                                                category=self._decision_variables)

    def active_upper_bounds_decision_variables(self, as_dict: bool = False,
                                               group: Optional[str] = None) -> Union[List[bool], dict]:
        """Public method to access active upper bounds of decision variables from solution.

        Args:
            as_dict: if True: return a dict, variable names as keys, return list else
            group: select variables of specified group only

        Returns:
            List or dictionary of active upper bounds of decision variables if problem was solved.

        """
        return self._extract_active_upper_bound(as_dict=as_dict,
                                                group=group,
                                                category=self._decision_variables)

    #####################################################################
    # endregion methods
    #####################################################################

    #####################################################################
    # region getter setter
    #####################################################################
    @property
    def constraints(self) -> List[Constraint]:
        return self._constraints

    @constraints.setter
    def constraints(self, value: List[Constraint]) -> None:
        self._constraints = value

    @property
    def objectives(self) -> List[Objective]:
        return self._objectives

    @objectives.setter
    def objectives(self, value: List[Objective]) -> None:
        self._objectives = value

    @property
    def decision_variables(self) -> List[DecisionVariable]:
        return self._decision_variables

    @decision_variables.setter
    def decision_variables(self, value: List[DecisionVariable]) -> None:
        self._decision_variables = value
    #####################################################################
    # endregion getter setter
    #####################################################################
