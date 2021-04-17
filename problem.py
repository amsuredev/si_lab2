from graph import Graph
from copy import deepcopy
from einshtein import Einshtein
class Problem:
    def __init__(self, x_size, y_size, check, d):
        self.__solution = []
        self.__x = x_size
        self.__y = y_size
        for i in range(x_size):
            line = []
            for j in range(y_size):
                line.append(-1)
            self.__solution.append(line)

        self.__check = check
        self.d = list(range(d))

        self.solutions = []

    @property
    def solution(self):
        return self.__solution

    @solution.setter
    def solution(self, solution):
        self.__solution = solution

    def is_save(self, point_ind, y, color):
        return self.__check(point_ind, y, color, self.__solution)


    def backtracking_statistic(self, x, y):
        for value in self.d:
            if self.is_save(x, y, value):
                self.__solution[x][y] = value
                if y + 1 < self.__y:
                    self.backtracking_statistic(x, y + 1)
                else:
                    self.solutions.append(deepcopy(self.__solution))
                    self.__solution[x][y] = -1
        self.__solution[x][y] = -1
        return

    def backtracking_first_solution(self, x, y):
        for val in self.d:
            if self.is_save(x, y, val):
                self.solution[x][y] = val
                if y != self.__y - 1:
                    if self.backtracking_first_solution(x, y+1):
                        return True
                elif y == self.__y - 1 and x != self.__x - 1:
                    if self.backtracking_first_solution(x + 1, 0):
                        return True
                else:
                    print("success; ", "solution found: ", self.__solution)
                    return True
        self.solution[x][y] = -1
        return

    def constraint(self):
        pass


if __name__ == "__main__":
    #graph = Graph(num_points=30, max_color_num=3)
    #graph_problem = Problem(1, 30, graph.is_save, graph.max_color_num)
    #graph_problem.backtracking(0, 0)
    #print(graph_problem.solutions)
    #solution_plot = graph_problem.solutions[0][0]
    #graph.colors = solution_plot
    #graph.plot_graph()
    graph = Graph(num_points=10, max_color_num=3)
    graph_problem = Problem(1, 10, graph.is_save, graph.max_color_num)
    graph_problem.backtracking_first_solution(0, 0)
    graph.colors = graph_problem.solution[0]
    graph.plot_graph()

    einshtein = Einshtein()
    einshtein_problem = Problem(5, 5, einshtein.is_save, 5)
    einshtein_problem.backtracking_first_solution(0, 0)
    einshtein.solution = einshtein_problem.solution
    einshtein.print_solution()

