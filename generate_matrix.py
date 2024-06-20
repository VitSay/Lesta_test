import numpy as np
from py_src.py_matrix import PyMatrix

shape = 50

matrix1 = np.random.randint(1, 101, size=(shape, shape))
matrix2 = np.random.randint(1, 101, size=(shape, shape))

PyMatrix(matrix1.tolist()).writePyMatrix('matrix1.txt')
PyMatrix(matrix2.tolist()).writePyMatrix('matrix2.txt')