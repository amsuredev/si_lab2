class Problem:
    def __init__(self, x, y, check):
        self.__solution = []
        for i in range(x):
            line = []
            for j in range(y):
                line.append(-1)
            self.__solution.append(line)

        self.check = check

    def check(self):
        pass

    def constraint(self):
        pass


if __name__ == "__main__":
    def printOk():
        print("Print ok")

    dwa = Problem(5, 5, printOk)
    jeden = Problem(1, 5, printOk)

    dwa.check()
    a = 76
