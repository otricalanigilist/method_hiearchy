from fractions import Fraction
import numpy as np



class Unit:  # через списки смежности
    def __init__(self, name: str):
        self.name = name
        self.criteries = []  #первая таблица, отношение всех критериев
        self.alt_criteria = []  #вторая таблица, связь критерия с альтернативами [[]]



    def setName(self, name: str): #pohui potom sledau
        self.name = name

    def setCriteries(self,_values: list[float]):
        self.criteries = _values

    def setAlt_criteria(self,_values: list[list[float]]):
        self.alt_criteria = _values



class Graph(Unit):
    def __init__(self): #pohui potom sledau
        # self.adj_list = [self.name, self.criteries, self.alt_criteria]
        self.crit_names = []
        self.alt_names = []

        self.sum_of_criteries = []
        self.sum_of_alt_criteria = []


        self.adj_list = dict[str,Unit]()

    # def setEdgesName(self, names: list[str]):
    #
    #     self.adj_list.append(Unit(name))

    def init_edges(self,names: list[str]):
        for elem in names:
            self.adj_list[elem] = Unit(elem)


    def display(self):
        for node in self.adj_list:
            print(f'{node}:\n{self.adj_list[node].criteries}')
            for elem in self.adj_list[node].alt_criteria:
                print(elem)


    def add_values_for_existing_edges(self, name: str, _values: list[float]):
        if name not in self.adj_list:
            print(f'Вершины {name} не существует')
            return

        self.adj_list[name].setCriteries(_values)
        return


    def addAlt_criteria(self,name: str, _values: list[list[float]]):
        if name not in self.adj_list:
            print(f'Вершины {name} не существует')
            return

        self.adj_list[name].setAlt_criteria(_values)
        return

    def read_file(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            self.crit_names = file.readline().split()
            self.init_edges(self.crit_names)
            print(self.crit_names)

            i: int = 0
            for line in file:
                if(line.strip() == '@'):
                    break
                row = line.strip().split(',')
                for elem in row:
                    if elem not in ['\n', ' ', '']:
                        self.adj_list[self.crit_names[i]].criteries.append(float(Fraction(elem)))
                i += 1



            self.alt_names = file.readline().split()
            print(self.alt_names)

            name: str = file.readline().strip()
            for line in file:

                if (line.strip() == '@'):
                    name: str = file.readline().strip()
                    continue

                row = line.strip().split(',')
                arr = []
                for elem in row:
                    if elem not in ['\n', ' ', '']:
                        arr.append(float(Fraction(elem)))

                self.adj_list[name].alt_criteria.append(arr)



    def calculate_sum_crit(self) -> list:
        size: int = len(self.crit_names)
        arr = [0] * size
        for i in range (0,size):
            for j in range (0, size):
                arr[i] += self.adj_list[self.crit_names[j]].criteries[i]
        return arr

    def calculate_sum_Altcrit(self, name: str) -> list:
        size: int = len(self.alt_names)
        arr = [0] * size
        for i in range(0, size):
            for j in range(0, size):
                arr[i] += self.adj_list[name].alt_criteria[j][i]

        return arr

    def calculate_all_sums(self):
        print('\n\ncalculatoooor')
        arr1 = self.calculate_sum_crit()
        print(arr1)
        for elem in self.crit_names:
            print(self.calculate_sum_Altcrit(elem))



    def norm_crit(self):
        arr = self.calculate_sum_crit()
        size: int = len(self.crit_names)
        for i in range(0, size):
            for j in range(0, size):
                self.adj_list[self.crit_names[j]].criteries[i] /= arr[i]


    def norm_Altcrit(self):
        size: int = len(self.alt_names)

        for elem in self.crit_names:
            arr = self.calculate_sum_Altcrit(elem)

            for i in range(0, size):
                for j in range(0, size):
                    self.adj_list[elem].alt_criteria[i][j] /= arr[j]


    def sredn(self):
        print('\nsredn')
        size: int = len(self.crit_names)
        size_alt: int = len(self.alt_names)

        matrix_itog_slotbec = np.zeros(size)
        matrix_itog = np.zeros((size_alt,size))

        for i in range(0,size):
            val = sum(self.adj_list[self.crit_names[i]].criteries) / size
            print(val)
            matrix_itog_slotbec[i] = val
        print()

        for i in range(0,size):

            for j in range(0,size_alt):
                val = sum(self.adj_list[self.crit_names[i]].alt_criteria[j]) / size_alt
                print(val)
                matrix_itog[j][i]=val
            print()

        print(matrix_itog,'\n')
        print(matrix_itog_slotbec,'\n')

        otvet = matrix_itog * matrix_itog_slotbec
        for elem in otvet:
            print(sum(elem))





if __name__ == '__main__':

    rows: int = 5
    cols: int = 5

    test = Graph()
    test.read_file('k1.txt')
    test.display()

    test.calculate_all_sums()


    print('\n\nnorm')
    norm = test
    norm.norm_crit()
    norm.norm_Altcrit()

    norm.display()


    norm.sredn()
