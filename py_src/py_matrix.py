import ctypes
import re

class PyMatrix:
    def __init__(self, matrix: list = None):
        if matrix is None:
            self._matrix = []
            self._n_rows = -1
            self._n_cols = -1
        else:
            self.setMatrix(matrix)

    def __str__(self):
        """
        Метод для красивой печати матрицы, используется для записи в файл.
        """
        res = ''
        for row in self._matrix:
            res += ''.join(["{:>6}".format(str(num)) for num in row])
            res += '\n'
        return res
    
    def __eq__(self, other: 'PyMatrix'):
        return self._matrix == other.getMatrix()
    
    def isEmpty(self):
        self._matrix == list()

    def getNRows(self):
        return self._n_rows
    
    def getNCols(self):
        return self._n_cols
    
    def getMatrix(self):
        return self._matrix
    
    def setMatrix(self, matrix: list[list[int]]) -> None:
        """
        Когда нужно задать матрицу не из файла, 
        например результирующая матрица после перемножения матриц
        """
        self.checkMatrixShape(matrix)
        self._matrix = matrix
        self._n_rows = len(matrix)
        self._n_cols = len(self.list_get(self._matrix, 0, list()))

    def readPyMatrix(self, txt_file_path: str) -> 'PyMatrix':
        """
        Считывает матрицу из .txt файла.
        Убирает все пробельные символы с начала и конца строки из файла.
        Делает сплит по любому количеству пробельных символов.
        """
        with open(txt_file_path, 'r') as file:
            row_counter = 0
            for line_ind, line in enumerate(file):
                line = re.sub(r"^\s+|\s+$", '', line) # Убираем все ненужные символы с начала и конца строки
                if re.search(r'\d', line) is None:  # Если строка пустая, сразу переходим на следующую строку
                    continue
                row_counter += 1
                matrix_row = [int(num) for num in re.split(r'\s+', line)] # Сплит по любому кол-ву пробелов
                if line_ind == 0:
                    self._n_cols = len(matrix_row)
                assert len(matrix_row) == self._n_cols, "Строки матрицы в исходном .txt файле разной длины"
                self._matrix.append(matrix_row)
            self._n_rows = row_counter
        return self
    
    def writePyMatrix(self, txt_file_path: str = "result.txt") -> None:
        with open(txt_file_path, 'w') as file:
            file.write(str(self))

    def getCMatrix(self) -> ctypes.POINTER(ctypes.POINTER(ctypes.c_int32)):
        """
        Преобразование Python матрицы в C матрицу, чтобы можно было 
        её передать в C функцию.
        """
        c_matrix_type = ctypes.POINTER(ctypes.c_int32) * self._n_rows
        c_matrix = c_matrix_type()
        for i in range(self._n_rows):
            c_matrix[i] = (ctypes.c_int32 * self._n_cols)(*self._matrix[i])
        return c_matrix
    
    @staticmethod
    def checkMatrixShape(matrix: list, assertion_messange: str = "Строки матрицы имеют разную длину") -> None:
        """
        Статический метод для проверки размера матрицы.
        В каждой строке должно быть одинаковое кол-во столбцов.
        """
        matrix_n_cols = len(PyMatrix.list_get(matrix, 0, list()))
        assert all([len(row) == matrix_n_cols for row in matrix]), assertion_messange

    @staticmethod
    def list_get(lst, ind, default=list()):
        """
        Для проверки кол-ва столбцов, надо обратиться по индексу
        листа. В пустых списках нет элементов, поэтому в них не к
        чему обратиться, и кол-во столбцов в них равно 0. Этот метод
        сделан для этого, чтобы когда обращаешься по индексу к пустой
        матрице, возвращалось дефолтное значение.
        """
        try:
            return lst[ind]
        except IndexError:
            return default
