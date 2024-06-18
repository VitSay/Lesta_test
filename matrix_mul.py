import sys
from py_src.py_matrix import PyMatrix
from py_src.py_matrix import test_matrix
from py_src.c_lib import CLib

def main():
    args = sys.argv

    matrix_1 = PyMatrix().readPyMatrix(args[1])
    matrix_2 = PyMatrix().readPyMatrix(args[2])
    matrix_1.readCLib('c_src/lib.dll')

    (matrix_1 * matrix_2).writePyMatrix(args[3])

if __name__ == "__main__":
    main()