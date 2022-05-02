"""Test codes for ch2_search.py module"""

from ch2_search import *

if __name__ == '__main__':
    maze : Maze = Maze()
    print(maze)
    
    #print(maze.goal_test(MazeLocation(4, 5)))  ## False
    #print(maze.goal_test(MazeLocation(9, 9)))  ## True
    #print(maze.successors(MazeLocation(0, 0)))
    
    ## Test dfs algorithm
    solution_1: Optional[Node[MazeLocation]] = dfs(
        maze.start, maze.goal_test, maze.successors)
    
    if solution_1 is None:
        print('No path found by dfs algorithm')
    else:
        path_1: List[MazeLocation] = node_to_path(solution_1)
        maze.mark(path_1)
        print(maze)
        maze.clear(path_1)
    
    ## Test bfs algorithm
    solution_2: Optional[Node[MazeLocation]] = bfs(
        maze.start, maze.goal_test, maze.successors)
    if solution_2 is None:
        print('No path found by bfs algorithm')
    else:
        path_2: List[MazeLocation] = node_to_path(solution_2)
        maze.mark(path_2)
        print(maze)
        maze.clear(path_2)
    