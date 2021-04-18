from random import randint
from point import Point
from copy import deepcopy
from matplotlib import pyplot as plt
from matplotlib import collections as mc
from shapely.geometry import LineString


class Graph():
    def __init__(self, dimension=10, num_points=10, max_color_num=3):
        self.__relations = []
        self.__max_color_num = max_color_num
        self.__points = self.generate_points(num_points, dimension)
        self.start_making_relations()
        # print("points")
        # for point in self.__points:
        #     print(point)
        # for relation in self.__relations:
        #     print("relations")
        #     print(relation[0])
        #     print(relation[1])
        self.__table_conections = []

        for point in self.__points:
            table_add = []
            for point_check in self.__points:
                table_add.append(0)
            points_connection = self.get_relations_with_point(point)
            for point_connection in points_connection:
                table_add[self.__points.index(point_connection)] = 1

            self.__table_conections.append(table_add)
        self.__colors = []
        for index in range(len(self.__points)):
            self.__colors.append(-1)

        self.__dziedzina = dict()
        for point_ind in range(len(self.__points)):
            self.__dziedzina[0, point_ind] = list(range(self.__max_color_num))

        self.__colors_count = dict()
        for i in range(self.__max_color_num):
            self.__colors_count[i] = 0

    @property
    def max_color_num(self):
        return self.__max_color_num

    @max_color_num.setter
    def max_color_num(self, max_color_num):
        self.__max_color_num = max_color_num

    @property
    def colors(self):
        return self.__colors

    @colors.setter
    def colors(self, colors):
        self.__colors = colors

    @property
    def dziedzina(self):
        return self.__dziedzina

    @dziedzina.setter
    def dziedzina(self, dziedzina):
        self.__dziedzina = dziedzina

    def generate_points(self, num_points, dimension=10):
        points = []
        while len(points) != num_points:
            new_point = Point(randint(0, dimension - 1), randint(0, dimension - 1))
            if new_point not in points:
                points.append(new_point)
        return points

    def get_max_colors_sorted(self):
        down_up_color_values = {k: v for k, v in sorted(self.__colors_count.items(), key=lambda item: item[1], reverse=True)}
        return down_up_color_values.keys()

    def get_color(self, color_ind):
        return {0: "red", 1: "black", 2: "blue", 3: "green"}[color_ind]

    def make_relations(self, point_to_make_connection, max_connections_num=3):
        possible_connections = max_connections_num - self.get_relations_with_point_count(point_to_make_connection)
        if possible_connections > 0:
            for point in self.get_closed_points(point_to_make_connection):
                if max_connections_num - self.get_relations_with_point_count(point) > 0:
                    potential_relation = [point, point_to_make_connection]
                    if point != point_to_make_connection and not self.exist_relation(potential_relation):
                        if not self.have_crosses(potential_relation):
                            self.__relations.append(potential_relation)
                            possible_connections -= 1
                            # self.plot_graph()
                            if possible_connections == 0:
                                return

    def start_making_relations(self):
        for point in self.__points:
            self.make_relations(point, max_connections_num=self.__max_color_num)

    def backtracking(self, point_ind, y):
        for color in range(self.__max_color_num):
            if self.is_save(point_ind, 0, color):
                self.__colors[point_ind] = color
                if point_ind + 1 < len(self.__points):
                    self.backtracking(point_ind + 1, 0)
                else:
                    return

    def is_save(self, point_ind, y, color, solution):
        for i in range(len(solution[point_ind])):
            if self.__table_conections[y][i] == 1 and color == solution[point_ind][i]:
                return False
        return True

    #def change_dziedzina(self, x, y, val, dziedzina):

    def change_dziedzina(self, x, y, color, dziedzina):
        neigbours = self.get_neighbours(self.__points[y])
        for neigbour in neigbours:
            if color in dziedzina[0, self.__points.index(neigbour)]:
                dziedzina[0, self.__points.index(neigbour)].remove(color)

    def forward_checking(self, point_ind):
        for color in self.__dziedzina[0, point_ind]:
            if self.is_save(point_ind, 0, color):
                self.__colors[point_ind] = color
                if point_ind + 1 < len(self.__points):
                    neigbours = self.get_neighbours(self.__points[point_ind])
                    for neigbour in neigbours:
                        if color in self.__dziedzina[0, self.__points.index(neigbour)]:
                            self.__dziedzina[0, self.__points.index(neigbour)].remove(color)
                    self.forward_checking(point_ind + 1)
                else:
                    return

    def mrv(self, point_ind):
        for color in self.get_max_colors_sorted():
            if self.is_save(point_ind, 0, color):
                self.__colors[point_ind] = color
                if point_ind + 1 < len(self.__points):
                    self.__colors_count[color] += 1
                    self.mrv(point_ind + 1)
                else:
                    return

    def get_closed_points(self, point):
        closed_points_not_sorted = deepcopy(self.__points)
        closed_points_not_sorted.remove(point)
        closed_points = sorted(closed_points_not_sorted, key=lambda p: (p.x - point.x) ** 2 + (p.y - point.y) ** 2,
                               reverse=False)
        return closed_points

    def get_relations_with_point_count(self, point):
        relations_with_point = 0
        for relation in self.__relations:
            if point in relation:
                relations_with_point += 1
        return relations_with_point

    def get_relations_with_point(self, point):
        points = []
        for relation in self.__relations:
            if point in relation:
                point_connect = relation[0] if relation[0] != point else relation[1]
                points.append(point_connect)
        return points

    def exist_relation(self, relation_check):
        return relation_check in self.__relations or relation_check.reverse() in self.__relations

    def have_crosses(self, relation_check):
        for relation in self.__relations:
            if not self.match_segments(relation[0], relation[1], relation_check[0], relation_check[1]):
                return True
        return False

    @classmethod
    def match_segments(cls, point_11, point_12, point_21, point_22):
        line_1 = LineString([(point_11.x, point_11.y), (point_12.x, point_12.y)])
        line_2 = LineString([(point_21.x, point_21.y), (point_22.x, point_22.y)])
        point_inter = line_1.intersection(line_2)

        if isinstance(point_inter, LineString):
            return True
        if point_inter.is_empty:
            return False

        result_point = Point(point_inter.x, point_inter.y)
        point_list = [point_11, point_12, point_21, point_22]

        return point_list.count(result_point) == 2

    def get_neighbours(self, point_check):
        neighbours = []
        for relation in self.__relations:
            if point_check in relation:
                point_neigbour = relation[0] if relation[0] != point_check else relation[1]
                neighbours.append(point_neigbour)
        return neighbours


    def plot_graph(self):
        edges = list()
        x = list()
        y = list()
        for relation in self.__relations:
            edges.append([[relation[0].x, relation[0].y], [relation[1].x, relation[1].y]])
            x.append(relation[0].x)
            y.append(relation[0].y)
            x.append(relation[1].x)
            y.append(relation[1].y)

        lc = mc.LineCollection(edges, linewidths=3)
        fig, ax = plt.subplots()
        ax.add_collection(lc)
        ax.autoscale()
        ax.margins(0.1)
        colors_list = [self.get_color(color_ind) for color_ind in self.__colors]
        c = [self.__get_point_color_name(x[index], y[index], colors_list) for index in range(len(x))]
        plt.scatter(x, y, c=c)

        plt.show()

    def __get_point_color_name(self, x, y, color_list):
        for point in self.__points:
            if point == Point(x, y):
                return self.get_color(self.__colors[self.__points.index(point)])


if __name__ == "__main__":
    graph = Graph(num_points=10, max_color_num=3)
    graph.backtracking(0,0)
    #graph.mrv(0)
    #graph.forward_checking(0)
    graph.plot_graph()
    #
