from graph import Graph
from copy import deepcopy
from einshtein import Einshtein
class Problem:
    counter_backtracking = 0
    counter_forward_checking = 0
    count= 0
    def __init__(self, x_size, y_size, check, d=None, dziedzina=None, change_dziedzina = None):
        self.__solution = []
        self.__x = x_size
        self.__y = y_size
        for i in range(x_size):
            line = []
            for j in range(y_size):
                line.append(-1)
            self.__solution.append(line)

        self.__check = check
        if d is not None:
            self.d = list(range(d))

        self.solutions = []
        self.__dziedzina = dziedzina

        self.change_dziedzina_pers = change_dziedzina



    @property
    def solution(self):
        return self.__solution

    @solution.setter
    def solution(self, solution):
        self.__solution = solution

    def is_save(self, point_ind, y, color):
        return self.__check(point_ind, y, color, self.__solution)

    def change_dziedzina(self, x, y ,val):
        return self.change_dziedzina_pers(x, y, val)


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
            Problem.counter_backtracking += 1
            if self.is_save(x, y, val):
                self.solution[x][y] = val
                if y != self.__y - 1:
                    #print(self.solution)
                    if self.backtracking_first_solution(x, y+1):
                        return True
                elif y == self.__y - 1 and x != self.__x - 1:
                    if self.backtracking_first_solution(x + 1, 0):
                        #print(self.solution)
                        return True
                else:
                    #print("success; ", "solution found: ", self.__solution)
                    print("Counter backtracking: {count}".format(count=Problem.counter_backtracking))
                    return True
        self.solution[x][y] = -1
        return

    def forward_checking(self, point_ind, option_index):
        # print(solution)
        dziedzina_copy = deepcopy(self.__dziedzina)
        for val in self.__dziedzina[point_ind, option_index]:
            Problem.counter_forward_checking += 1
            if self.is_save(point_ind, option_index, val):
                self.solution[point_ind][option_index] = val
                if option_index != 4:
                    self.change_dziedzina(point_ind, option_index, val)
                    #print(self.__solution)
                    if self.forward_checking(point_ind, option_index + 1):
                        return True
                    else:
                        self.__dziedzina = deepcopy(dziedzina_copy)
                elif option_index == 4 and point_ind != 4:
                    self.change_dziedzina(point_ind, option_index, val)
                    #print(self.__solution)
                    if self.forward_checking(point_ind + 1, 0):
                        return True
                    else:
                        self.__dziedzina = deepcopy(dziedzina_copy)
                else:
                    print("success", self.solution)
                    print("Counter forward checking: {count}".format(count=Problem.counter_forward_checking))
                    return True
        self.solution[point_ind][option_index] = -1
        self.__dziedzina = deepcopy(dziedzina_copy)
        return False

    def forward_checking_new(self, point_ind, option_index):
        dziedzina_copy = deepcopy(self.__dziedzina)
        for val in self.__dziedzina[point_ind, option_index]:
            Einshtein.counter_backtracking += 1
            if self.is_save(point_ind, option_index, val):
                self.solution[point_ind][option_index] = val
                if option_index != 4:
                    self.change_dziedzina(point_ind, option_index, val)
                    print(self.solution)
                    if self.forward_checking(point_ind, option_index + 1):
                        return True
                    else:
                        self.__dziedzina = deepcopy(dziedzina_copy)
                elif option_index == 4 and point_ind != 4:
                    self.change_dziedzina(point_ind, option_index, val)
                    print(self.solution)
                    if self.forward_checking(point_ind + 1, 0):
                        return True
                    else:
                        self.__dziedzina = deepcopy(dziedzina_copy)
                else:
                    print("success", self.solution)
                    print(Einshtein.counter_backtracking)
                    return True
        self.solution[point_ind][option_index] = -1
        self.__dziedzina = dziedzina_copy
        return False

    def constraint(self):
        pass


if __name__ == "__main__":
    # graph = Graph(num_points=30, max_color_num=3)
    # graph_problem = Problem(1, 30, graph.is_save, graph.max_color_num)
    # graph_problem.backtracking_first_solution(0, 0)
    # print(graph_problem.solutions)
    # solution_plot = graph_problem.solution[0]
    # graph.colors = solution_plot
    # graph.plot_graph()

    # graph = Graph(num_points=10, max_color_num=3)
    # graph_problem = Problem(1, 10, graph.is_save, graph.max_color_num)
    # graph_problem.backtracking_statistic(0, 0)
    # graph.colors = graph_problem.solutions[0][0]
    # graph.plot_graph()

    # einshtein = Einshtein()
    # einshtein_problem = Problem(5, 5, einshtein.is_save, 5)
    # einshtein_problem.backtracking_first_solution(0, 0)
    # einshtein.solution = einshtein_problem.solution
    # einshtein.print_solution()

    einshtein1 = Einshtein()
    einshtein_problem1 = Problem(5, 5, einshtein1.is_save, d=None, dziedzina=einshtein1.dziedzina, change_dziedzina=einshtein1.change_dziedzina)
    einshtein_problem1.forward_checking_new(0, 0)
    einshtein1.solution = einshtein_problem1.solution
    einshtein1.print_solution()