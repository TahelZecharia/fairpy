#!python3
"""
    A min-sharing max-product allocation algorithm.

    Programmer: Eliyahu Sattat
    Since:  2020
"""

import cvxpy

from fairpy.valuations import ValuationMatrix
from fairpy.divisible.allocations import AllocationMatrix
from fairpy.divisible.max_product import max_product_allocation

from fairpy.divisible.min_sharing_impl.ConsumptionGraph import ConsumptionGraph
from fairpy.divisible.min_sharing_impl.FairThresholdAllocationProblem import FairThresholdAllocationProblem


from cvxpy.constraints.constraint import Constraint

import logging
logger = logging.getLogger(__name__)


class FairMaxProductAllocationProblem(FairThresholdAllocationProblem):
    """
    Finds a Nash-optimal (aka max-product) allocation with minimum sharing.

    >>> v = [[1, 2, 3,4], [4, 5, 6,5], [7, 8, 9,6]]
    >>> fpap =FairMaxProductAllocationProblem(v)
    >>> g1 = [[0.0, 0.0, 0.0, 1], [1, 1, 1, 1], [0.0, 0.0, 0.0, 1]]
    >>> g = ConsumptionGraph(g1)
    >>> print(fpap.find_allocation_for_graph(g))
    None
    >>> g1 = [[0.0, 0.0, 0.0, 1], [1, 1, 1, 1], [1, 0.0, 0.0, 1]]
    >>> g = ConsumptionGraph(g1)
    >>> print(fpap.find_allocation_for_graph(g))
    None
    >>> g1 = [[0.0, 0.0, 0.0, 1], [0.0, 1, 1, 1], [1, 0.0, 0.0, 1]]
    >>> g = ConsumptionGraph(g1)
    >>> print(fpap.find_allocation_for_graph(g))
    None
    >>> g1 = [[0.0, 0.0, 0.0, 1], [0.0, 1, 1, 1], [1, 1, 0.0, 1]]
    >>> g = ConsumptionGraph(g1)
    >>> print(fpap.find_allocation_for_graph(g).round(2))
    [[0.   0.   0.   0.99]
     [0.   0.34 1.   0.  ]
     [1.   0.66 0.   0.  ]]
    >>> g1 = [[0.0, 0.0, 0.0, 1], [0.0, 0.0, 1, 1], [1, 1, 0.0, 1]]
    >>> g = ConsumptionGraph(g1)
    >>> print(fpap.find_allocation_for_graph(g))
    None
    >>> g1 = [[0.0, 0.0, 0.0, 1], [0.0, 0.0, 1, 1], [1, 1, 1, 1]]
    >>> g = ConsumptionGraph(g1)
    >>> print(fpap.find_allocation_for_graph(g))
    None
    >>> g1 = [[0.0, 0.0, 0.0, 1], [0.0, 1, 1, 1], [1, 0.0, 0.0, 0.0]]
    >>> g = ConsumptionGraph(g1)
    >>> print(fpap.find_allocation_for_graph(g))
    None
    >>> g1 = [[0.0, 0.0, 0.0, 1], [0.0, 1, 1, 1], [1, 1, 0.0, 0.0]]
    >>> g = ConsumptionGraph(g1)
    >>> print(fpap.find_allocation_for_graph(g).round(2))
    [[0.   0.   0.   0.99]
     [0.   0.33 1.   0.01]
     [1.   0.67 0.   0.  ]]
    >>> v = [ [465,0,535] , [0,0,1000]  ]  # This example exposed a bug in OSQP solver!
    >>> fpap =FairMaxProductAllocationProblem(v)
    >>> g1 = [[1,1,1],[0,0,1]]
    >>> g = ConsumptionGraph(g1)
    >>> print(fpap.find_allocation_for_graph(g).round(3))
    [[1.   1.   0.07]
     [0.   0.   0.93]]
    """

    def __init__(self, valuations:ValuationMatrix, tolerance=0.01):
        valuations = ValuationMatrix(valuations)
        mpa = max_product_allocation(valuations)
        mpa_utilities = mpa.utility_profile(valuations)
        logger.info("The max-product allocation is:\n%s,\nwith utility profile: %s",mpa,mpa_utilities)
        thresholds = mpa_utilities * (1-tolerance)
        logger.info("The thresholds are: %s",thresholds)
        logger.info("The proportionality thresholds are: %s", [
            sum(valuations[i]) / valuations.num_of_agents 
            for i in valuations.agents()])
        self.tolerance = tolerance
        super().__init__(valuations, thresholds)


    def fairness_adjective(self)->str:
        return "{}-max-product".format((1-self.tolerance))

if __name__ == '__main__':
    # import logging, sys
    # logger.addHandler(logging.StreamHandler(sys.stdout))
    # logger.setLevel(logging.INFO)

    # v = [ [465,0,535] , [0,0,1000]  ]
    # fpap =FairMaxProductAllocationProblem(v)
    # g1 = [[1,1,1],[0,0,1]]
    # g = ConsumptionGraph(g1)
    # print(fpap.find_allocation_for_graph(g).round(3))

    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))