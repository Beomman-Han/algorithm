from ch2_missionaries import *
from ch2_search import bfs, Node, node_to_path

if __name__ == "__main__":
    
    ## test 1
    mc_state = MCState(3, 3, True)
    possible_list = mc_state.successors()
    for scene in possible_list:
        print(scene)
    print()
    
    ## test 2
    mc_state = MCState(3, 1, False)
    possible_scenarios = mc_state.successors()
    for scenario in possible_scenarios:
        print(scenario)
    
    ## solve problem
    mc_state = MCState(3, 3, True)
    #solution = bfs(mc_state, mc_state.goal_test, mc_state.successors)
    solution = bfs(mc_state, MCState.goal_test, MCState.successors)
    path = node_to_path(solution)
    for scenario in path:
        print(scenario)