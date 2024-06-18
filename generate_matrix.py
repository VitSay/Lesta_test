import numpy as np
from py_src.py_matrix import PyMatrix

# Создаем две матрицы размером 20x20 из случайных целых чисел от 1 до 100
matrix1 = np.random.randint(1, 101, size=(100, 100))
matrix2 = np.random.randint(1, 101, size=(100, 100))

# Преобразуем матрицы в списки Python
PyMatrix(matrix1.tolist()).writePyMatrix('matrix1.txt')
PyMatrix(matrix2.tolist()).writePyMatrix('matrix2.txt')