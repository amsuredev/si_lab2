from copy import deepcopy


class Einshtein():
    nationality = ["norweg", "dunczyk", "anglik", "niemiec", "szwed"]
    colors = ["zolty", "niebieski", "czerwony", "zielony", "bialy"]
    cigarettes = ["cygar", "light", "bez filtra", "fajka", "mentolowe"]
    drinks = ["herbata", "mleko", "woda", "piwo", "kawa"]
    pet = ["kot", "ptak", "pies", "kon", "rybka"]

    counter_backtracking = 0
    counter_forward_checking = 0

    def __init__(self):
        self.solution = []
        for i in range(5):
            add_array = []
            for j in range(5):
                add_array.append(-1)
            self.solution.append(add_array)

        self.__dziedzina = dict()
        for i in range(5):
            for j in range(5):
                self.__dziedzina[i,j] = list(range(5))


    @property
    def dziedzina(self):
        return self.__dziedzina

    @dziedzina.setter
    def dziedzina(self, dziedzina):
        self.__dziedzina = dziedzina

    def forward_checking(self, point_ind, option_index):
        # print(solution)
        dziedzina_copy = deepcopy(self.__dziedzina)
        for val in self.__dziedzina[point_ind, option_index]:
            Einshtein.counter_forward_checking += 1
            if self.is_save(point_ind, option_index, val, self.solution):
                self.solution[point_ind][option_index] = val
                if option_index != 4:
                    self.change_dziedzina(point_ind, option_index, val, self.__dziedzina)
                    if self.forward_checking(point_ind, option_index + 1):
                        return True
                    else:
                        self.__dziedzina = deepcopy(dziedzina_copy)
                elif option_index == 4 and point_ind != 4:
                    self.change_dziedzina(point_ind, option_index, val, self.__dziedzina)
                    if self.forward_checking(point_ind + 1, 0):
                        return True
                    else:
                        self.__dziedzina = deepcopy(dziedzina_copy)
                else:
                    #print("success", self.solution)
                    print("counter forward checking {counter}".format(counter=Einshtein.counter_forward_checking))
                    return True
        self.solution[point_ind][option_index] = -1
        self.__dziedzina = dziedzina_copy
        return False

    @classmethod
    def option_name_index(self, name):
        return {"czerwony": 3, "zielony": 1, "bialy": 2, "zolty": 0, "niebieski": 4,
                "herbata": 2, "mleko": 1, "woda": 0, "piwo": 3, "kawa": 4,
                "norweg": 0, "dunczyk": 1, "anglik": 2, "niemiec": 3, "szwed": 4,
                "light": 0, "cygar": 1, "fajka": 2, "bez filtra": 3, "mentolowe": 4,
                "kot": 0, "ptak": 1, "pies": 2, "kon": 3, "rybka": 4}[name]

    @classmethod
    def index_map_color(self, index):
        return {3: "czerwony", 1: "zielony", 2: "bialy", 0: "zolty", 4: "niebieski"}[index]

    @classmethod
    def index_map_drink(self, index):
        return {2: "herbata", 1: "mleko", 0: "woda", 3: "piwo", 4: "kawa"}[index]

    @classmethod
    def index_map_nationality(self, index):
        return {0: "norweg", 1: "dunczyk", 2: "anglik", 3: "niemiec", 4: "szwed"}[index]

    @classmethod
    def index_map_cig(self, index):
        return {0: "light", 1: "cygar", 2: "fajka", 3: "bez filtra", 4: "mentolowe"}[index]

    @classmethod
    def index_map_pet(self, index):
        return {0: "kot", 1: "ptak", 2: "pies", 3: "kon", 4: "rybka"}[index]

    @classmethod
    def column_name_index(self, name):
        return {"color": 0, "drink": 1, "nationality": 2, "cig": 3, "pet": 4}[name]

    def home_index_option(self, column_name, option_name, solution):
        column_index = self.column_name_index(column_name)
        option_index = self.option_name_index(option_name)
        index_home = -1
        for home_index in range(len(solution)):
            if solution[home_index][column_index] == option_index:
                index_home = home_index
        return index_home

    def backtracking(self, point_ind, option_index):
        # print(solution)
        for val in range(5):
            Einshtein.counter_backtracking += 1
            if self.is_save(point_ind, option_index, val, self.solution):
                self.solution[point_ind][option_index] = val
                if option_index != 4:
                    if self.backtracking(point_ind, option_index + 1):
                        return True
                elif option_index == 4 and point_ind != 4:
                    if self.backtracking(point_ind + 1, 0):
                        return True
                else:
                    print("counter backtracking: {counter}".format(counter=Einshtein.counter_backtracking))
                    #print("success", self.solution)
                    self.print_solution()
                    return True
        self.solution[point_ind][option_index] = -1
        return

    def print_solution(self):
        for home_index in range(len(self.solution)):
            print(home_index)
            data = []
            data.append(self.index_map_color(self.solution[home_index][0]))
            data.append(self.index_map_drink(self.solution[home_index][1]))
            data.append(self.index_map_nationality(self.solution[home_index][2]))
            data.append(self.index_map_cig(self.solution[home_index][3]))
            data.append(self.index_map_pet(self.solution[home_index][4]))
            print(data)

    def is_save(self, point_ind, option_index, val, solution):
        before_val = solution[point_ind][option_index]
        solution[point_ind][option_index] = val
        # if all_dif() and norweg_home_0() and anglik_eq_czerwony() and zielony_plus_1_bialy() and dunczyk_eq_herbata() and abs_light_minus_1_e1_koty() and zolty_eq_cygar() and niemiec_eq_fajka() and mleko_eq_2() and abs_light_minus_woda_eq1() and bez_filtra_eq_ptaki() and szwed_eq_psy() and abs_norweg_minus_niebieski_eq_1() and abs_koni_minus_zolty_eq_1() and mentolowe_eq_piwo() and zielony_eq_kawa():
        if self.all_dif(solution):
            if self.norweg_home_0(solution):
                if self.anglik_eq_czerwony(solution):
                    if self.zielony_plus_1_bialy(solution):
                        if self.dunczyk_eq_herbata(solution):
                            if self.abs_light_minus_1_e1_koty(solution):
                                if self.zolty_eq_cygar(solution):
                                    if self.niemiec_eq_fajka(solution):
                                        if self.mleko_eq_2(solution):
                                            if self.abs_light_minus_woda_eq1(solution):
                                                if self.bez_filtra_eq_ptaki(solution):
                                                    if self.szwed_eq_psy(solution):
                                                        if self.abs_norweg_minus_niebieski_eq_1(solution):
                                                            if self.abs_koni_minus_zolty_eq_1(solution):
                                                                if self.mentolowe_eq_piwo(solution):
                                                                    if self.zielony_eq_kawa(solution):
                                                                        return True
        else:
            solution[point_ind][option_index] = before_val
            return False

    def all_dif(self, solution):
        for option in range(5):
            options_values = []
            for home_ind in range(5):
                if solution[home_ind][option] != -1:
                    options_values.append(solution[home_ind][option])
            if len(set(options_values)) != len(options_values):
                return False
        return True

    def norweg_home_0(self, solution):
        home_index_norweg = self.home_index_option(column_name="nationality", option_name="norweg", solution=solution)
        return home_index_norweg == 0 or home_index_norweg == -1

    def anglik_eq_czerwony(self, solution):
        index_home_anglik = self.home_index_option(column_name="nationality", option_name="anglik", solution=solution)
        if index_home_anglik == -1:
            return True
        index_home_czerwony = self.home_index_option(column_name="color", option_name="czerwony", solution=solution)
        if index_home_czerwony == -1:
            return True
        else:
            return index_home_anglik == index_home_czerwony

    def zielony_plus_1_bialy(self, solution):
        zielony = self.home_index_option(column_name="color", option_name="zielony", solution=solution)
        if zielony == -1:
            return True
        bialy = self.home_index_option(column_name="color", option_name="bialy", solution=solution)
        if bialy == -1:
            return True
        return zielony + 1 == bialy

    def dunczyk_eq_herbata(self, solution):
        dunczyk = self.home_index_option(column_name="nationality", option_name="dunczyk", solution=solution)
        if dunczyk == -1:
            return True
        herbata = self.home_index_option(column_name="drink", option_name="herbata", solution=solution)
        if herbata == -1:
            return True
        return herbata == dunczyk

    def abs_light_minus_1_e1_koty(self, solution):
        light = self.home_index_option(column_name="cig", option_name="light", solution=solution)
        if light == -1:
            return True
        koty = self.home_index_option(column_name="pet", option_name="kot", solution=solution)
        if koty == -1:
            return True
        return koty == abs(light - 1)

    def zolty_eq_cygar(self, solution):
        zolty = self.home_index_option(column_name="color", option_name="zolty", solution=solution)
        if zolty == -1:
            return True
        cygar = self.home_index_option(column_name="cig", option_name="cygar", solution=solution)
        if cygar == -1:
            return True
        else:
            return cygar == zolty

    def niemiec_eq_fajka(self, solution):
        niemiec = self.home_index_option(column_name="nationality", option_name="niemiec", solution=solution)
        if niemiec == -1:
            return True
        fajka = self.home_index_option(column_name="cig", option_name="fajka", solution=solution)
        if fajka == -1:
            return True
        else:
            return niemiec == fajka

    def mleko_eq_2(self, solution):
        mleko = self.home_index_option(column_name="drink", option_name="mleko", solution=solution)
        return mleko == 2 or mleko == -1

    def abs_light_minus_woda_eq1(self, solution):
        light = self.home_index_option(column_name="cig", option_name="light", solution=solution)
        if light == -1:
            return True
        woda = self.home_index_option(column_name="drink", option_name="woda", solution=solution)
        if woda == -1:
            return True
        else:
            return abs(woda - light) == 1

    def bez_filtra_eq_ptaki(self, solution):
        bez_filtra = self.home_index_option(column_name="cig", option_name="bez filtra", solution=solution)
        if bez_filtra == -1:
            return True
        ptaki = self.home_index_option(column_name="pet", option_name="ptak", solution=solution)
        if ptaki == -1:
            return True
        else:
            return ptaki == bez_filtra

    def szwed_eq_psy(self, solution):
        szwed = self.home_index_option(column_name="nationality", option_name="szwed", solution=solution)
        if szwed == -1:
            return True
        psy = self.home_index_option(column_name="pet", option_name="pies", solution=solution)
        if psy == -1:
            return True
        else:
            return szwed == psy

    def abs_norweg_minus_niebieski_eq_1(self, solution):
        norweg = self.home_index_option(column_name="nationality", option_name="norweg", solution=solution)
        if norweg == -1:
            return True
        niebieski = self.home_index_option(column_name="color", option_name="niebieski", solution=solution)
        if niebieski == -1:
            return True
        else:
            return abs(norweg - niebieski) == 1

    def abs_koni_minus_zolty_eq_1(self, solution):
        koni = self.home_index_option(column_name="pet", option_name="kon", solution=solution)
        if koni == -1:
            return True
        zolty = self.home_index_option(column_name="color", option_name="zolty", solution=solution)
        if zolty == -1:
            return True
        return abs(koni - zolty) == 1

    def mentolowe_eq_piwo(self, solution):
        mentolowe = self.home_index_option(column_name="cig", option_name="mentolowe", solution=solution)
        if mentolowe == -1:
            return True
        piwo = self.home_index_option(column_name="drink", option_name="piwo", solution=solution)
        if piwo == -1:
            return True
        return piwo == mentolowe

    def zielony_eq_kawa(self, solution):
        zielony = self.home_index_option(column_name="color", option_name="zielony", solution=solution)
        if zielony == -1:
            return True
        kawa = self.home_index_option(column_name="drink", option_name="kawa", solution=solution)
        if kawa == -1:
            return True
        return kawa == zielony

    def change_all_dif(self, x, y, val, dziedzina):
        dziedzina[x,y] = [val]
        for i in range(5):
            if x != i:
                if val in dziedzina[i, y]:
                    dziedzina[i, y].remove(val)

    def change_anglik_eq_czerwony(self, x, y, val, dziedzina):
        if y == 2:
            if self.index_map_color(val) == "anglik":
                self.delete_values_from_dziedzina(0, self.option_name_index("czerwony"), dziedzina)
                dziedzina[x, 0] = [self.option_name_index("czerwony")]

        if y == 0:
            if self.index_map_color(val) == "czerwony":
                self.delete_values_from_dziedzina(2, self.option_name_index("anglik"), dziedzina)
                dziedzina[x, 2] = [self.option_name_index("anglik")]

    def change_ziel_plus_1_eq_bialy(self, x, y, val, dziedzina):
        if y == 0:
            if self.index_map_color(val) == "zielony":
                self.delete_values_from_dziedzina(y, self.option_name_index("bialy") , dziedzina)
                x_after = x + 1
                if x_after in range(5):
                    dziedzina[x_after, y].append(self.option_name_index("bialy"))
            if self.index_map_color(val) == "bialy":
                self.delete_values_from_dziedzina(y, self.option_name_index("zielony"), dziedzina)
                x_before = x - 1
                if x_before in range(5):
                    dziedzina[x_before, y].append(self.option_name_index("zielony"))

    def change_dunczyk_eq_herbata(self, x, y, val, dziedzina):
        if y == 2:
            if self.index_map_color(val) == "dunczyk":
                self.delete_values_from_dziedzina(1, self.option_name_index("herbata"))
                dziedzina[x, 1] = [self.option_name_index("herbata")]

        if y == 1:
            if self.index_map_color(val) == "herbata":
                self.delete_values_from_dziedzina(2, self.option_name_index("dunczyk"), dziedzina)
                dziedzina[x, 2] = [self.option_name_index("dunczyk")]

    def change_abs_light_minus_1_eq_koty(self, x, y, val, dziedzina):
        if y == 3:
            if self.index_map_color(val) == "light":
                self.delete_values_from_dziedzina(4, self.option_name_index("kot"), dziedzina)
                x_after = x + 1
                x_before = x - 1
                if x_after in range(5):
                    dziedzina[x_after, 4].append(self.option_name_index("kot"))
                if x_before in range(5):
                    dziedzina[x_before, 4].append(self.option_name_index("kot"))

        if y == 4:
            if self.index_map_color(val) == "kot":
                self.delete_values_from_dziedzina(3, self.option_name_index("light"), dziedzina)
                x_after = x + 1
                x_before = x - 1
                if x_after in range(5):
                    dziedzina[x_after, 3].append(self.option_name_index("light"))
                if x_before in range(5):
                    dziedzina[x_before, 3].append(self.option_name_index("light"))

    def change_zolty_eq_cygar(self, x, y, val, dziedzina):
        if y == 0:
            if self.index_map_color(val) == "zolty":
                self.delete_values_from_dziedzina(3, self.option_name_index("cygar"), dziedzina)
                dziedzina[x, 3] = [self.option_name_index("cygar")]

        if y == 3:
            if self.index_map_color(val) == "cygar":
                self.delete_values_from_dziedzina(0, self.option_name_index("zolty"), dziedzina)
                dziedzina[x, 0] = [self.option_name_index("zolty")]

    def change_niemiec_eq_fajka(self, x, y, val, dziedzina):
        if y == 2:
            if self.index_map_color(val) == "niemiec":
                self.delete_values_from_dziedzina(3, self.option_name_index("fajka"), dziedzina)
                dziedzina[x, 3] = [self.option_name_index("fajka")]

        if y == 3:
            if self.index_map_color(val) == "fajka":
                self.delete_values_from_dziedzina(2, self.option_name_index("niemiec"), dziedzina)
                dziedzina[x, 2] = [self.option_name_index("niemiec")]

    def change_abs_light_minus_woda_eq_1(self, x, y, val, dziedzina):
        if y == 3:
            if self.index_map_color(val) == "light":
                self.delete_values_from_dziedzina(1, self.option_name_index("woda"), dziedzina)
                x_after = x + 1
                x_before = x - 1
                if x_after in range(5):
                    dziedzina[x_after, 1].append(self.option_name_index("woda"))
                if x_before in range(5):
                    dziedzina[x_before, 1].append(self.option_name_index("woda"))

        if y == 1:
            if self.index_map_color(val) == "woda":
                self.delete_values_from_dziedzina(3, self.option_name_index("light"), dziedzina)
                x_after = x + 1
                x_before = x - 1
                if x_after in range(5):
                    dziedzina[x_after, 3].append(self.option_name_index("light"))
                if x_before in range(5):
                    dziedzina[x_before, 3].append(self.option_name_index("light"))

    def change_bez_filtra_eq_ptaki(self, x, y, val, dziedzina):
        if y == 3:
            if self.index_map_color(val) == "bez filtra":
                self.delete_values_from_dziedzina(4, self.option_name_index("ptak"), dziedzina)
                dziedzina[x, 4] = [self.option_name_index("ptak")]

        if y == 4:
            if self.index_map_color(val) == "ptak":
                self.delete_values_from_dziedzina(3, self.option_name_index("bez filtra"), dziedzina)
                dziedzina[x, 3] = [self.option_name_index("bez filtra")]

    def change_szwed_eq_psy(self, x, y, val, dziedzina):
        if y == 2:
            if self.index_map_color(val) == "szwed":
                self.delete_values_from_dziedzina(4, self.option_name_index("pies"), dziedzina)
                dziedzina[x, 4] = [self.option_name_index("pies")]

        if y == 4:
            if self.index_map_color(val) == "pies":
                self.delete_values_from_dziedzina(2, self.option_name_index("szwed"), dziedzina)
                dziedzina[x, 2] = [self.option_name_index("szwed")]

    def change_abs_norweg_minus_niebieski_eq_1(self, x, y, val, dziedzina):
        if y == 2:
            if self.index_map_color(val) == "norweg":
                self.delete_values_from_dziedzina(0, self.option_name_index("niebieski"), dziedzina)
                x_after = x + 1
                x_before = x - 1
                if x_after in range(5):
                    dziedzina[x_after, 0].append(self.option_name_index("niebieski"))
                if x_before in range(5):
                    dziedzina[x_before, 0].append(self.option_name_index("niebieski"))

        if y == 0:
            if self.index_map_color(val) == "niebieski":
                self.delete_values_from_dziedzina(2, self.option_name_index("norweg"), dziedzina)
                x_after = x + 1
                x_before = x - 1
                if x_after in range(5):
                    dziedzina[x_after, 2].append(self.option_name_index("norweg"))
                if x_before in range(5):
                    dziedzina[x_before, 2].append(self.option_name_index("norweg"))

    def change_abs_kon_zolty(self, x, y, val, dziedzina):
        if y == 4:
            if self.index_map_color(val) == "kon":
                self.delete_values_from_dziedzina(0, self.option_name_index("zolty"), dziedzina)
                x_after = x + 1
                x_before = x - 1
                if x_after in range(5):
                    dziedzina[x_after, 0].append(self.option_name_index("zolty"))
                if x_before in range(5):
                    dziedzina[x_before, 0].append(self.option_name_index("zolty"))

        if y == 0:
            if self.index_map_color(val) == "zolty":
                self.delete_values_from_dziedzina(4, self.option_name_index("kon"), dziedzina)
                x_after = x + 1
                x_before = x - 1
                if x_after in range(5):
                    dziedzina[x_after, 4].append(self.option_name_index("kon"))
                if x_before in range(5):
                    dziedzina[x_before, 4].append(self.option_name_index("kon"))

    def change_mentolowe_eq_piwo(self, x, y, val, dziedzina):
        if y == 3:
            if self.index_map_color(val) == "mentolowe":
                self.delete_values_from_dziedzina(1, self.option_name_index("piwo"), dziedzina)
                dziedzina[x, 1] = [self.option_name_index("piwo")]

        if y == 1:
            if self.index_map_color(val) == "piwo":
                self.delete_values_from_dziedzina(3, self.option_name_index("mentolowe"), dziedzina)
                dziedzina[x, 3] = [self.option_name_index("mentolowe")]

    def change_zielony_eq_kawa(self, x, y, val, dziedzina):
        if y == 0:
            if self.index_map_color(val) == "zielony":
                self.delete_values_from_dziedzina(1, self.option_name_index("kawa"), dziedzina)
                dziedzina[x, 1] = [self.option_name_index("kawa")]

        if y == 1:
            if self.index_map_color(val) == "kawa":
                self.delete_values_from_dziedzina(0, self.option_name_index("zielony"), dziedzina)
                dziedzina[x, 0] = [self.option_name_index("zielony")]

    def delete_values_from_dziedzina(self, y, val, dziedzina):
        for home in range(5):
            if val in dziedzina[home, y]:
                dziedzina[home, y].remove(val)

    def change_dziedzina(self, x, y, val, dziedzina):
        self.change_all_dif(x, y, val, dziedzina)
        self.change_anglik_eq_czerwony(x, y, val, dziedzina)
        self.change_ziel_plus_1_eq_bialy(x, y, val, dziedzina)
        self.change_dunczyk_eq_herbata(x, y, val, dziedzina)
        self.change_abs_light_minus_1_eq_koty(x, y, val, dziedzina)
        self.change_zolty_eq_cygar(x, y, val, dziedzina)
        self.change_niemiec_eq_fajka(x, y, val, dziedzina)
        self.change_abs_light_minus_woda_eq_1(x, y, val, dziedzina)
        self.change_bez_filtra_eq_ptaki(x, y, val, dziedzina)
        self.change_szwed_eq_psy(x, y, val, dziedzina)
        self.change_abs_norweg_minus_niebieski_eq_1(x, y, val, dziedzina)
        self.change_abs_kon_zolty(x, y, val, dziedzina)
        self.change_mentolowe_eq_piwo(x, y, val, dziedzina)
        self.change_zielony_eq_kawa(x, y, val, dziedzina)


if __name__ == "__main__":
    #Einshtein().backtracking(point_ind=0, option_index=0)
    e1=Einshtein()
    e1.backtracking(0, 0)
    e1.print_solution()

    e = Einshtein()
    e.forward_checking(0, 0)
    e.print_solution()