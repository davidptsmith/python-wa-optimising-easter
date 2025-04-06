from dataclasses import dataclass, field
from typing import Dict, List

from Optimiser.Child import Child
from Optimiser.Houses import House
from Optimiser.EggType import EggType

from ortools.linear_solver import pywraplp

@dataclass
class ModelParameters:
    golden_egg_name: str = "golden"
    health_min: int = 5
    happiness_min: int = 5
    egg_rate: int = 3
    fairness_threshold: int = 2

class Optimiser:
    def optimize_easter_enjoyment(
        houses: List[House],
        egg_types: Dict[str, EggType],
        total_supply: Dict[str, int],
        model_parameters: ModelParameters
    ) -> Dict[str, Dict[str, int]]:
        solver = pywraplp.Solver.CreateSolver('SCIP')
        if not solver:
            return {}

        all_children = [child for house in houses for child in house.children]
        egg_names = list(egg_types.keys())

        x = {}
        for child in all_children:
            for egg in egg_names:
                x[(child.name, egg)] = solver.IntVar(0, total_supply[egg], f'x_{child.name}_{egg}')

        for child in all_children:
            solver.Add(x[(child.name, model_parameters.golden_egg_name)] == 1)
            solver.Add(
                sum(x[(child.name, egg)] * egg_types[egg].health for egg in egg_names) >= model_parameters.health_min
            )
            solver.Add(
                sum(x[(child.name, egg)] * egg_types[egg].enjoyment for egg in egg_names) >= model_parameters.happiness_min
            )
            solver.Add(
                sum(x[(child.name, egg)] * egg_types[egg].size for egg in egg_names) <= child.basket_capacity
            )
            max_eggs = int(model_parameters.egg_rate * child.effective_time())
            solver.Add(
                sum(x[(child.name, egg)] for egg in egg_names) <= max_eggs
            )
            for egg in egg_names:
                if not child.preference.get(egg, False):
                    solver.Add(x[(child.name, egg)] == 0)

        for egg in egg_names:
            solver.Add(
                sum(x[(child.name, egg)] for child in all_children) <= total_supply[egg]
            )

        for house in houses:
            child_list = house.children
            for i in range(len(child_list)):
                for j in range(i + 1, len(child_list)):
                    ci = child_list[i]
                    cj = child_list[j]
                    diff = solver.IntVar(-solver.infinity(), solver.infinity(), f'diff_{ci.name}_{cj.name}')
                    solver.Add(diff == sum(x[(ci.name, e)] for e in egg_names) - sum(x[(cj.name, e)] for e in egg_names))
                    solver.Add(diff <= model_parameters.fairness_threshold)
                    solver.Add(diff >= -model_parameters.fairness_threshold)

        solver.Maximize(
            sum(x[(child.name, egg)] * egg_types[egg].enjoyment for child in all_children for egg in egg_names)
        )

        status = solver.Solve()
        if status != pywraplp.Solver.OPTIMAL:
            return "No Solution Found"

        result = {}
        for child in all_children:
            result[child.name] = {}
            for egg in egg_names:
                count = int(x[(child.name, egg)].solution_value())
                if count > 0:
                    result[child.name][egg] = count
        return result
    
    def optimize_easter_cost(
        houses: List[House],
        egg_types: Dict[str, EggType],
        total_supply: Dict[str, int],
        model_parameters: ModelParameters
    ) -> Dict[str, Dict[str, int]]:
        solver = pywraplp.Solver.CreateSolver('SCIP')
        if not solver:
            return {}

        all_children = [child for house in houses for child in house.children]
        egg_names = list(egg_types.keys())

        x = {}
        for child in all_children:
            for egg in egg_names:
                x[(child.name, egg)] = solver.IntVar(0, total_supply[egg], f'x_{child.name}_{egg}')

        for child in all_children:
            solver.Add(x[(child.name, model_parameters.golden_egg_name)] == 1)
            solver.Add(
                sum(x[(child.name, egg)] * egg_types[egg].health for egg in egg_names) >= model_parameters.health_min
            )
            solver.Add(
                sum(x[(child.name, egg)] * egg_types[egg].enjoyment for egg in egg_names) >= model_parameters.happiness_min
            )
            solver.Add(
                sum(x[(child.name, egg)] * egg_types[egg].size for egg in egg_names) <= child.basket_capacity
            )
            max_eggs = int(model_parameters.egg_rate * child.effective_time())
            solver.Add(
                sum(x[(child.name, egg)] for egg in egg_names) <= max_eggs
            )
            for egg in egg_names:
                if not child.preference.get(egg, False):
                    solver.Add(x[(child.name, egg)] == 0)

        for egg in egg_names:
            solver.Add(
                sum(x[(child.name, egg)] for child in all_children) <= total_supply[egg]
            )

        for house in houses:
            child_list = house.children
            for i in range(len(child_list)):
                for j in range(i + 1, len(child_list)):
                    ci = child_list[i]
                    cj = child_list[j]
                    diff = solver.IntVar(-solver.infinity(), solver.infinity(), f'diff_{ci.name}_{cj.name}')
                    solver.Add(diff == sum(x[(ci.name, e)] for e in egg_names) - sum(x[(cj.name, e)] for e in egg_names))
                    solver.Add(diff <= model_parameters.fairness_threshold)
                    solver.Add(diff >= -model_parameters.fairness_threshold)


        solver.Minimize(
            sum(x[(child.name, egg)] * egg_types[egg].cost for child in all_children for egg in egg_names)
        )

        status = solver.Solve()
        if status != pywraplp.Solver.OPTIMAL:
            return "No Solution Found"

        result = {}
        for child in all_children:
            result[child.name] = {}
            for egg in egg_names:
                count = int(x[(child.name, egg)].solution_value())
                if count > 0:
                    result[child.name][egg] = count
        return result
    
