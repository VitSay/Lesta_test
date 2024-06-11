import argparse
from py_src.py_matrix import PyMatrix
from py_src.c_lib import CLib

def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("matrix1_path", type=str, help="Файл с первой матрицей")
    arg_parser.add_argument("matrix2_path", type=str, help="Файл со второй матрицей")
    arg_parser.add_argument("result_path", type=str, help="Файл для итоговой матрицы")
    args = arg_parser.parse_args()

    matrix_1 = PyMatrix()
    matrix_1.readPyMatrix(args.matrix1_path)
    matrix_2 = PyMatrix()
    matrix_2.readPyMatrix(args.matrix2_path)

    lib = CLib('c_src/lib.dll')
    lib.matrix_mult(matrix_1, matrix_2).writePyMatrix(args.result_path)

if __name__ == "__main__":
    main()