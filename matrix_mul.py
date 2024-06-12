import sys
from py_src.py_matrix import PyMatrix
from py_src.c_lib import CLib

def main():
    args = sys.argv

    matrix_1 = PyMatrix().readPyMatrix(args[1])
    matrix_2 = PyMatrix().readPyMatrix(args[2])

    lib = CLib('c_src/lib.dll')
    lib.matrix_mult(matrix_1, matrix_2).writePyMatrix(args[3])

if __name__ == "__main__":
    main()