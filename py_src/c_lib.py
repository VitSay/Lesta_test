import ctypes
from typing import List, Callable
from py_src.py_matrix import PyMatrix

class CLib:
    def __init__(self, txt_lib_path: str):
        self._lib = ctypes.CDLL(txt_lib_path)

        # Функция для умножения матриц из dll
        self._matrix_mult_func = self._lib.matrix_mult
        self._matrix_mult_func.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_int32)),
                                           ctypes.POINTER(ctypes.POINTER(ctypes.c_int32)),
                                           ctypes.c_int32, ctypes.c_int32,
                                           ctypes.c_int32, ctypes.c_int32]
        self._matrix_mult_func.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_int32))

        # Функция для очищения памяти выделенной в С из dll
        self._free_memory_func = self._lib.free_memory
        self._free_memory_func.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_int32)), ctypes.c_int32]
        self._free_memory_func.restype = None

    def matrix_mult(self, matrix_1: PyMatrix, matrix_2: PyMatrix) -> PyMatrix:
        # Проверка - либо обе матрицы пусты, либо обе матрицы не пусты
        assert (matrix_1.isEmpty() and matrix_2.isEmpty()) or (not matrix_1.isEmpty() and not matrix_2.isEmpty())
        # Проверка правильной размерности для перемножения
        assert matrix_1.getNCols() == matrix_2.getNRows()

        # Преобразуем Python матрицы в C массивы чтобы передать в С функцию
        c_matrix_1 = matrix_1.getCMatrix()
        c_matrix_2 = matrix_2.getCMatrix()

        # Вызов функции умножения матриц на С
        result_c_matrix = self._matrix_mult_func(c_matrix_1, c_matrix_2,
                                                 matrix_1.getNRows(), matrix_1.getNCols(),
                                                 matrix_2.getNRows(), matrix_2.getNCols())

        # Преобразуем С массив в Python List
        result_list = []
        for row in range(matrix_1.getNRows()):
            temp_row = []
            for col in range(matrix_2.getNCols()):
                temp_row.append(result_c_matrix[row][col])
            result_list.append(temp_row)

        result_PyMatrix = PyMatrix(result_list)
        self._free_memory_func(result_c_matrix, result_PyMatrix.getNRows()) # Очищаем память выделенную С
        return result_PyMatrix
