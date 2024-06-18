import ctypes
import re
import numpy as np
from py_src.c_lib import CLib
from py_src.timer import runTime

class PyMatrix:
    def __init__(self, matrix: list = None):
        self._clib = None
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
            res += ''.join(["{:>10}".format(str(num)) for num in row])
            res += '\n'
        return res
    
    def __eq__(self, other: 'PyMatrix'):
        return self._matrix == other.getMatrix()
    
    def readCLib(self, path: str='c_src/lib.dll'):
        self._clib = CLib(path)

    @runTime(10)
    def C_matrixMult(self, other: 'PyMatrix') -> 'PyMatrix':
        self.canBeMultiplied(self, other)

        c_matrix_1 = self.getCMatrix()
        c_matrix_2 = other.getCMatrix()

        result_c_matrix = self._clib.matrix_mult_func(c_matrix_1, c_matrix_2,
                                                       self.getNRows(), self.getNCols(),
                                                       other.getNRows(), other.getNCols())

        result_list = []
        for row in range(self.getNRows()):
            temp_row = []
            for col in range(other.getNCols()):
                temp_row.append(result_c_matrix[row][col])
            result_list.append(temp_row)

        self._clib.free_memory_func(result_c_matrix, len(result_list))
        return PyMatrix(result_list)

    @runTime(10)
    def Py_matrixMult(self, other: 'PyMatrix') -> 'PyMatrix':
        self.canBeMultiplied(self, other)
        res = []
        for row in range(self.getNRows()):
            new_row = []
            for col in range(other.getNCols()):
                tmp = 0
                for i in range(self.getNCols()):
                    tmp += self.getMatrix()[row][i] * other.getMatrix()[i][col]
                new_row.append(tmp)
            res.append(new_row)
        return PyMatrix(res)

    @runTime(10)
    def Numpy_matrixMult(self, other: 'PyMatrix'):
        self.canBeMultiplied(self, other)
        numpy_matrix_1 = np.array(self.getMatrix(), dtype='int32')
        numpy_matrix_2 = np.array(other.getMatrix(), dtype='int32')
        numpy_res_matrix = np.dot(numpy_matrix_1, numpy_matrix_2)
        return PyMatrix(numpy_res_matrix.tolist())

    def __mul__(self, other: 'PyMatrix'):
        return self.C_matrixMult(other)

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
        
    @staticmethod
    def canBeMultiplied(matrix1: 'PyMatrix', matrix2: 'PyMatrix'):
        assert matrix1.getNCols() == matrix2.getNRows()
        assert (matrix1.isEmpty() and matrix2.isEmpty()) or (not matrix1.isEmpty() and not matrix2.isEmpty())
        return True
    
def test_matrix():
    matrix_1 = PyMatrix().readPyMatrix('matrix1.txt')
    matrix_2 = PyMatrix().readPyMatrix('matrix2.txt')
    matrix_1.readCLib()

    (matrix_1 * matrix_2).writePyMatrix('result.txt')


    # clib_res_matrix = matrix_1.C_matrixMult(matrix_2)
    # py_res_matrix = matrix_1.Py_matrixMult(matrix_2)
    # numpy_res_matrix = matrix_1.Numpy_matrixMult(matrix_2)
