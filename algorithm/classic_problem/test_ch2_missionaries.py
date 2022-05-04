from ch2_missionaries import *

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