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
        self.__used_values = dict()
        for val in self.d:
            self.__used_values[val] = 0

    def getSortedValsUpDown(self):
        up_down_values = {k: v for k, v in
                                sorted(self.__used_values.items(), key=lambda item: item[1], reverse=True)}
        return up_down_values.keys()

    @property
    def solution(self):
        return self.__solution

    @solution.setter
    def solution(self, solution):
        self.__solution = solution

    def is_save(self, point_ind, y, color):
        return self.__check(point_ind, y, color, self.__solution)

    def change_dziedzina(self, x, y ,val):
        return self.change_dziedzina_pers(x, y, val, self.__dziedzina)


    def backtracking_statistic(self, x, y):
        for value in self.d:
            Problem.counter_backtracking += 1
            if self.is_save(x, y, value):
                self.__solution[x][y] = value
                if y + 1 < self.__y:
                    self.backtracking_statistic(x, y + 1)
                else:
                    self.solutions.append(deepcopy(self.__solution))
                    self.__solution[x][y] = -1
        self.__solution[x][y] = -1
        return


    def forward_checking_statistic(self, point_ind, option_index):
        dziedzina_copy = deepcopy(self.__dziedzina)
        array_loop = deepcopy(self.__dziedzina[point_ind, option_index])
        for val in array_loop:
            Problem.counter_forward_checking += 1
            if self.is_save(point_ind, option_index, val):
                self.solution[point_ind][option_index] = val
                if option_index != self.__y - 1:
                    self.change_dziedzina(point_ind, option_index, val)
                    self.forward_checking_statistic(point_ind, option_index + 1)
                    self.__dziedzina = deepcopy(dziedzina_copy)
                elif option_index == self.__y - 1 and point_ind != self.__x - 1:
                    self.change_dziedzina(point_ind, option_index, val)
                    self.forward_checking_statistic(point_ind + 1, 0)
                    self.__dziedzina = deepcopy(dziedzina_copy)
                else:
                    #print("success", self.solution)
                    self.solutions.append(deepcopy(self.solution))
                    #print(Einshtein.counter_forward_checking)
                    self.solution[point_ind][option_index] = -1
                    #self.__dziedzina = dziedzina_copy
        self.solution[point_ind][option_index] = -1
        self.__dziedzina = dziedzina_copy
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

    def get_most_used_value_first(self, x, y):
        up_down = self.getSortedValsUpDown()
        for val in up_down:
            Problem.counter_backtracking += 1
            if self.is_save(x, y, val):
                self.solution[x][y] = val
                used = True
                self.__used_values[val] += 1
                if y != self.__y - 1:
                    #print(self.solution)
                    if self.get_most_used_value_first(x, y+1):
                        return True
                    else:
                        self.__used_values[val] -= 1
                elif y == self.__y - 1 and x != self.__x - 1:
                    if self.get_most_used_value_first(x + 1, 0):
                        #print(self.solution)
                        return True
                    else:
                        self.__used_values[val] -= 1
                else:
                    #print("success; ", "solution found: ", self.__solution)
                    print("Counter backtracking: {count}".format(count=Problem.counter_backtracking))
                    return True
        self.solution[x][y] = -1
        return

    def forward_checking_first_solution(self, point_ind, option_index):
        dziedzina_copy = deepcopy(self.__dziedzina)
        for val in self.__dziedzina[point_ind, option_index]:
            Einshtein.counter_backtracking += 1
            if self.is_save(point_ind, option_index, val):
                self.solution[point_ind][option_index] = val
                if option_index != self.__y - 1:
                    self.change_dziedzina(point_ind, option_index, val)
                    if self.forward_checking_first_solution(point_ind, option_index + 1):
                        return True
                    else:
                        self.__dziedzina = deepcopy(dziedzina_copy)
                elif option_index == self.__y - 1 and point_ind != self.__x - 1:
                    self.change_dziedzina(point_ind, option_index, val)
                    if self.forward_checking_first_solution(point_ind + 1, 0):
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
    graph = Graph(num_points=30, max_color_num=3)
    graph_problem = Problem(1, 30, graph.is_save, graph.max_color_num)
    graph_problem.get_most_used_value_first(0, 0)
    print(graph_problem.solutions)
    solution_plot = graph_problem.solution[0]
    graph.colors = solution_plot
    graph.plot_graph()


    einshtein = Einshtein()
    einshtein_problem = Problem(5, 5, einshtein.is_save, 5)
    einshtein_problem.get_most_used_value_first(0, 0)
    einshtein.solution = einshtein_problem.solution
    einshtein.print_solution()


    # graph = Graph(num_points=10, max_color_num=3)
    # graph_problem = Problem(1, 10, graph.is_save, graph.max_color_num)
    # graph_problem.backtracking_statistic(0, 0)
    # print("Num of soltions backtracking: {}".format(len(graph_problem.solutions)))
    # graph.colors = graph_problem.solutions[0]

    #graph.plot_graph()
    #
    # einshtein = Einshtein()
    # einshtein_problem = Problem(5, 5, einshtein.is_save, 5)
    # einshtein_problem.backtracking_first_solution(0, 0)
    # einshtein.solution = einshtein_problem.solution
    # einshtein.print_solution()

    # einshtein1 = Einshtein()
    # einshtein_problem1 = Problem(5, 5, einshtein1.is_save, d=None, dziedzina=einshtein1.dziedzina, change_dziedzina=einshtein1.change_dziedzina)
    # einshtein_problem1.forward_checking_first_solution(0, 0)
    # einshtein1.solution = einshtein_problem1.solution
    # einshtein1.print_solution()

    # graph3 = Graph(num_points=10, max_color_num=3)
    # graph4 = deepcopy(graph3)
    # graph_problem = Problem(1, 10, graph3.is_save, d=None, dziedzina=graph3.dziedzina, change_dziedzina=graph3.change_dziedzina)
    # graph_problem.forward_checking_statistic(0, 0)
    # print("Solutions find count: {count}".format(count=len(graph_problem.solutions)))
    # print("Forward checking counter: {count}".format(count=Problem.counter_forward_checking))
    #
    # Problem.counter_forward_checking = 0
    #
    # graph_problem4 = Problem(1, 10, graph4.is_save, d=graph4.max_color_num, dziedzina=graph4.dziedzina,
    #                         change_dziedzina=graph4.change_dziedzina)
    # graph_problem4.backtracking_statistic(0, 0)
    # # print(graph_problem.solution)
    # print("Solutions find count: {count}".format(count=len(graph_problem4.solutions)))
    # print("Backtracking counter: {count}".format(count=Problem.counter_backtracking))