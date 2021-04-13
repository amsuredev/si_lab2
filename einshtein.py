
def main():
    homes = [1, 2, 3, 4, 5]
    # colors = ["czerwony", "zielony", "bialy", "zolty", "niebieski"]
    # drinks = ["herbata", "mleko", "woda", "piwo", "kawa"]
    # nationality = ["norweg", "anglik", "dunczyk", "niemiec", "szwed"]
    # cigarettes = ["light", "cygar", "fajka", "bez filtra", "mentolowe"]
    # pet = ["kot", "ptak", "pies", "kon", "rybka"]

    nationality = ["norweg", "dunczyk", "anglik", "niemiec", "szwed"]
    colors = ["zolty", "niebieski", "czerwony", "zielony", "bialy"]
    cigarettes = ["cygar", "light", "bez filtra", "fajka", "mentolowe"]
    drinks = ["herbata", "mleko", "woda", "piwo", "kawa"]
    pet = ["kot", "ptak", "pies", "kon", "rybka"]

    #solution = [[0, 0, 0, 1, 0], [4, 2, 1, 0, 3], [3, 1, 2, 3, 1], [1, 4, 3, 2, 4], [2, 3, 4, 4, 2]]#test

    def option_name_index(name):
        return {"czerwony": 3, "zielony": 1, "bialy": 2, "zolty": 0, "niebieski": 4,
                "herbata": 2, "mleko": 1, "woda": 0, "piwo": 3, "kawa": 4,
                "norweg": 0, "dunczyk": 1, "anglik": 2, "niemiec": 3, "szwed": 4,
                "light": 0, "cygar": 1, "fajka": 2, "bez filtra": 3, "mentolowe": 4,
                "kot": 0, "ptak": 1, "pies": 2, "kon": 3, "rybka": 4}[name]

    def index_map_color(index):
        return {3:"czerwony", 1: "zielony", 2: "bialy", 0: "zolty", 4: "niebieski"}[index]

    def index_map_drink(index):
        return {2: "herbata", 1: "mleko", 0: "woda", 3: "piwo", 4: "kawa"}[index]

    def index_map_nationality(index):
        return {0: "norweg", 1: "dunczyk", 2: "anglik", 3: "niemiec", 4: "szwed"}[index]

    def index_map_cig(index):
        return {0: "light", 1: "cygar", 2: "fajka", 3: "bez filtra", 4: "mentolowe"}[index]

    def index_map_pet(index):
        return {0: "kot", 1: "ptak", 2: "pies", 3: "kon", 4: "rybka"}[index]



    def column_name_index(name):
        return {"color": 0, "drink": 1, "nationality": 2, "cig": 3, "pet": 4}[name]

    def home_index_option(column_name, option_name):
        column_index = column_name_index(column_name)
        option_index = option_name_index(option_name)
        index_home = -1
        for home_index in range(len(solution)):
            if solution[home_index][column_index] == option_index:
                index_home = home_index
        return index_home

    #solution = [[0, 0, 0, 1, 0], [4, 2, 1, 0, 3], [3, 1, 2, 3, 1], [1, 4, 3, 2, 4], [2, 3, -1, -1, -1]]
    solution = []
    for i in range(len(homes)):
        add_array = []
        for j in range(len(colors)):
            add_array.append(-1)
        solution.append(add_array)

    def backtrz(point_ind, option_index):
        #print(solution)
        for val in range(5):
            if is_save(point_ind, option_index, val):
                solution[point_ind][option_index] = val
                if option_index != 4:
                    if einshtein(point_ind, option_index + 1):
                        return True
                elif option_index == 4 and point_ind != 4:
                    if einshtein(point_ind + 1, 0):
                        return True
                else:
                    print("success", solution)
                    for home_index in range(len(solution)):
                        print(home_index)
                        data = []
                        data.append(index_map_color(solution[home_index][0]))
                        data.append(index_map_drink(solution[home_index][1]))
                        data.append(index_map_nationality(solution[home_index][2]))
                        data.append(index_map_cig(solution[home_index][3]))
                        data.append(index_map_pet(solution[home_index][4]))
                        print(data)
                    return True
        solution[point_ind][option_index] = -1
        return

    def is_save(point_ind, option_index, val):
        before_val = solution[point_ind][option_index]
        solution[point_ind][option_index] = val
        #if all_dif() and norweg_home_0() and anglik_eq_czerwony() and zielony_plus_1_bialy() and dunczyk_eq_herbata() and abs_light_minus_1_e1_koty() and zolty_eq_cygar() and niemiec_eq_fajka() and mleko_eq_2() and abs_light_minus_woda_eq1() and bez_filtra_eq_ptaki() and szwed_eq_psy() and abs_norweg_minus_niebieski_eq_1() and abs_koni_minus_zolty_eq_1() and mentolowe_eq_piwo() and zielony_eq_kawa():
        if all_dif():
            if norweg_home_0():
                if anglik_eq_czerwony():
                    if zielony_plus_1_bialy():
                        if dunczyk_eq_herbata():
                            if abs_light_minus_1_e1_koty():
                                if zolty_eq_cygar():
                                    if niemiec_eq_fajka():
                                        if mleko_eq_2():
                                            if abs_light_minus_woda_eq1():
                                                if bez_filtra_eq_ptaki():
                                                    if szwed_eq_psy():
                                                        if abs_norweg_minus_niebieski_eq_1():
                                                            if abs_koni_minus_zolty_eq_1():
                                                                if mentolowe_eq_piwo():
                                                                    if zielony_eq_kawa():
                                                                        return True
        else:
            solution[point_ind][option_index] = before_val
            return False

    def all_dif():
        for option in range(5):
            options_values = []
            for home_ind in range(5):
                if solution[home_ind][option] != -1:
                    options_values.append(solution[home_ind][option])
            if len(set(options_values)) != len(options_values):
                return False
        return True


    def norweg_home_0():
        home_index_norweg = home_index_option(column_name="nationality", option_name="norweg")
        return home_index_norweg == 0 or home_index_norweg == -1

    def anglik_eq_czerwony():
        index_home_anglik = home_index_option(column_name="nationality", option_name="anglik")
        if index_home_anglik == -1:
            return True
        index_home_czerwony = home_index_option(column_name="color", option_name="czerwony")
        if index_home_czerwony == -1:
            return True
        else:
            return index_home_anglik == index_home_czerwony

    def zielony_plus_1_bialy():
        zielony = home_index_option(column_name="color", option_name="zielony")
        if zielony == -1:
            return True
        bialy = home_index_option(column_name="color", option_name="bialy")
        if bialy == -1:
            return True
        return zielony + 1 == bialy

    def dunczyk_eq_herbata():
        dunczyk = home_index_option(column_name="nationality", option_name="dunczyk")
        if dunczyk == -1:
            return True
        herbata = home_index_option(column_name="drink", option_name="herbata")
        if herbata == -1:
            return True
        return herbata == dunczyk

    def abs_light_minus_1_e1_koty():
        light = home_index_option(column_name="cig", option_name="light")
        if light == -1:
            return True
        koty = home_index_option(column_name="pet", option_name="kot")
        if koty == -1:
            return True
        return koty == abs(light - 1)

    def zolty_eq_cygar():
        zolty = home_index_option(column_name="color", option_name="zolty")
        if zolty == -1:
            return True
        cygar = home_index_option(column_name="cig", option_name="cygar")
        if cygar == -1:
            return True
        else:
            return cygar == zolty

    def niemiec_eq_fajka():
        niemiec = home_index_option(column_name="nationality", option_name="niemiec")
        if niemiec == -1:
            return True
        fajka = home_index_option(column_name="cig", option_name="fajka")
        if fajka == -1:
            return True
        else:
            return niemiec == fajka

    def mleko_eq_2():
        mleko = home_index_option(column_name="drink", option_name="mleko")
        return mleko == 2 or mleko == -1

    def abs_light_minus_woda_eq1():
        light = home_index_option(column_name="cig", option_name="light")
        if light == -1:
            return True
        woda = home_index_option(column_name="drink", option_name="woda")
        if woda == -1:
            return True
        else:
            return abs(woda - light) == 1

    def bez_filtra_eq_ptaki():
        bez_filtra = home_index_option(column_name="cig", option_name="bez filtra")
        if bez_filtra == -1:
            return True
        ptaki = home_index_option(column_name="pet", option_name="ptak")
        if ptaki == -1:
            return True
        else:
            return ptaki == bez_filtra

    def szwed_eq_psy():
        szwed = home_index_option(column_name="nationality", option_name="szwed")
        if szwed == -1:
            return True
        psy = home_index_option(column_name="pet", option_name="pies")
        if psy == -1:
            return True
        else:
            return szwed == psy

    def abs_norweg_minus_niebieski_eq_1():
        norweg = home_index_option(column_name="nationality", option_name="norweg")
        if norweg == -1:
            return True
        niebieski = home_index_option(column_name="color", option_name="niebieski")
        if niebieski == -1:
            return True
        else:
            return abs(norweg - niebieski) == 1

    def abs_koni_minus_zolty_eq_1():
        koni = home_index_option(column_name="pet", option_name="kon")
        if koni == -1:
            return True
        zolty = home_index_option(column_name="color", option_name="zolty")
        if zolty == -1:
            return True
        return abs(koni - zolty) == 1

    def mentolowe_eq_piwo():
        mentolowe = home_index_option(column_name="cig", option_name="mentolowe")
        if mentolowe == -1:
            return True
        piwo = home_index_option(column_name="drink", option_name="piwo")
        if piwo == -1:
            return True
        return piwo == mentolowe

    def zielony_eq_kawa():
        zielony = home_index_option(column_name="color", option_name="zielony")
        if zielony == -1:
            return True
        kawa = home_index_option(column_name="drink", option_name="kawa")
        if kawa == -1:
            return True
        return kawa == zielony

    #print(is_save(0, 0, 0))
    einshtein(0, 0)

    #einshtein(4, 2)
    #print(is_save(4, 4, 2))
    # print(solution)
main()
