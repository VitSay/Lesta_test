import ctypes
import re

class PyMatrix:
    def __init__(self):
        self._matrix = []
        self._n_rows = -1
        self._n_cols = -1

    def __str__(self):
        #Метод для красивой печати матрицы, используется для записи в файл
        res = ''
        for row in self._matrix:
            res += ''.join(["{:>6}".format(str(num)) for num in row])
            res += '\n'
        return res

    def getNRows(self):
        return self._n_rows
    
    def getNCols(self):
        return self._n_cols
    
    def setMatrix(self, matrix: list[list[int]]) -> None:
        # Когда нужно задать матрицу не из файла, например результирующая матрица после перемножения матриц
        self._matrix = matrix
        self._n_rows = len(matrix)
        self._n_cols = len(matrix[0])

    def readPyMatrix(self, txt_file_path: str) -> None:
        """
        Считывает матрицу из .txt файла.
        Убирает все пробельные символы с начала и конца строки из файла.
        Делает сплит по любому количеству пробельных символов.
        """
        with open(txt_file_path, 'r') as file:
            for line_ind, line in enumerate(file):
                line = re.sub(r"^\s+|\s+$", '', line)
                matrix_row = [int(num) for num in re.split(r'\s+', line)] # Сплит по любому кол-ву пробелов
                if line_ind == 0:
                    self._n_cols = len(matrix_row)
                assert len(matrix_row) == self._n_cols, "Строки матрицы в исходном .txt файле разной длины"
                self._matrix.append(matrix_row)
            self._n_rows = line_ind+1
    
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