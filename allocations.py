#!python3

"""
Represents an allocation of objects to agents ---  the output of an item-allocation algorithm.

An immutable object; used mainly for display purposes.

Programmer: Erel Segal-Halevi
Since: 2021-04
"""

from typing import *


class Allocation:
    """
    Represents an allocation of objects to agents.
    An immutable object; used mainly for display purposes.

    >>> a = Allocation(agents=range(3), bundles=[[3,6],None,[2,5]], values=[9,0,7])
    >>> a
    0's bundle: {3,6},  value: 9.
    1's bundle: None,  value: 0.
    2's bundle: {2,5},  value: 7.
    <BLANKLINE>
    """

    agents:List[Any]
    bundles:List[List[Any]]
    values:List[float]

    num_of_agents:int

    def __init__(self, agents: List[Any], bundles: List[List[Any]], values:List[float]):
        """
        Initializes an allocation to the given agents, of the given bundles, with the given values.
        """
        num_of_agents = len(agents)
        if num_of_agents!=len(bundles) or num_of_agents!=len(values):
            raise ValueError("Numbers of agents, bundles and values must be identical, but they are not: {len(agents)}, {len(bundles)}, {len(values)}")
        self.num_of_agents = num_of_agents
        self.agents = agents
        self.bundles = bundles
        self.values = values

    def get_bundle(self, agent_index: int):
        return self.bundles[agent_index]

    def __getitem__(self, agent_index:int):
        return self.get_bundle(agent_index)

    def __repr__(self):
        result = ""
        for i_agent, agent in enumerate(self.agents):
            agent_bundle = self.bundles[i_agent]
            agent_value = self.values[i_agent]
            result += f"{agent}'s bundle: {stringify_bundle(agent_bundle)},  value: {agent_value}.\n"
        return result


def stringify_bundle(bundle: List[Any]):
    """
    Convert a bundle where each item is a character to a compact string representation.
    For testing purposes only.

    >>> stringify_bundle({'x','y'})
    '{x,y}'
    >>> stringify_bundle({'y','x'})
    '{x,y}'
    >>> stringify_bundle([2,1])
    '{1,2}'
    >>> stringify_bundle(None)
    'None'
    """
    if bundle is None:
        return "None"
    else:
        return "{" + ",".join(map(str,sorted(bundle))) + "}"
    # return ",".join(["".join(item) for item in bundle])



if __name__ == "__main__":
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
