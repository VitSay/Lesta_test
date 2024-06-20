import pytest
import sys
from py_src.c_lib import CLib
from py_src.py_matrix import PyMatrix
from matrix_mul import main

# Фикстура пити .dll библиотеки
@pytest.fixture(scope='session')
def clib_path():
    return "c_src/lib.dll"

# Фикстура для использования одного и того же объекта CLib во всех тестах
@pytest.fixture(scope='session')
def clib(clib_path):
    clib_obj = CLib(clib_path)
    yield clib_obj

# Тестирование функции перемножения на корректных данных
@pytest.mark.parametrize(
        "matrix1,matrix2,result",
        [(PyMatrix([[1,2],[3,4]]), PyMatrix([[2,3],[4,5]]), PyMatrix([[10,13],[22,29]])),
         (PyMatrix([[1,2]]), PyMatrix([[-3],[5]]), PyMatrix([[7]])),
         (PyMatrix([[2],[-4]]), PyMatrix([[2,-3,4,-5,6]]), PyMatrix([[4,-6,8,-10,12],[-8,12,-16,20,-24]]))]
)
def test_correct_input(clib, monkeypatch, matrix1: PyMatrix, matrix2: PyMatrix, result: PyMatrix):
    actual_result = clib.matrix_mult(matrix1, matrix2)
    assert actual_result == result

# Тестирование перемножения на матрицах из одного числа
@pytest.mark.parametrize(
        "matrix1,matrix2,result",
        [(PyMatrix([[1]]), PyMatrix([[2]]), PyMatrix([[2]])),
         (PyMatrix([[-20]]), PyMatrix([[6]]), PyMatrix([[-120]])),
         (PyMatrix([[25]]), PyMatrix([[-3]]), PyMatrix([[-75]]))]
)
def test_matrix_with_one_number(clib, matrix1, matrix2, result):
    actual_result = clib.matrix_mult(matrix1, matrix2)
    assert actual_result == result


# Тестирование когда одна матрица пустая, в этом случае вызывается AssertionError
@pytest.mark.parametrize(
        "matrix1,matrix2",
        [(PyMatrix([[1,2],[3,4]]), PyMatrix([])),
         (PyMatrix([]), PyMatrix([[4,5], [6,7]]))]
)
def test_one_matrix_empty(clib, matrix1, matrix2):
    with pytest.raises(AssertionError):
        clib.matrix_mult(matrix1, matrix2)

# Тестирование когда обе матрицы пустые, результат - пустая матрица
def test_both_matrix_are_empty(clib):
    actual_result = clib.matrix_mult(PyMatrix([]), PyMatrix([]))
    assert actual_result == PyMatrix([])

# Тестирование умножения при матрицах не подходящих размерностей, вызывается AssertionError
def test_wrong_dimension_for_mult(clib):
    with pytest.raises(AssertionError):
        clib.matrix_mult(PyMatrix([[2,3,4],[5,6,7]]), PyMatrix([[5],[6],[7],[8]]))

# Тестирование метода PyMatrix().setMatrix(), если в строках разное количество элементов - вызывается AssertionError
@pytest.mark.parametrize(
        "matrix",
        [([[1,2],[3,4,5]]),
         ([[-5], [6,7,8,9]]),
         ([5,6,7,8,9], [-90], [67,95,5])]
)
def test_different_number_of_columns_in_rows(matrix):
    with pytest.raises(AssertionError):
        PyMatrix(matrix)

# Тестирование main() функции с использованием monkeypatch
@pytest.mark.parametrize(
        "input_matrixes,result",
        [((PyMatrix([[-9,2,90],[1,4,3]]), PyMatrix([[2,3],[4,5],[-8,-9]])), PyMatrix([[-730,-827],[-6,-4]])),
         ((PyMatrix([[1,2]]), PyMatrix([[3],[5]])), PyMatrix([[13]])),
         ((PyMatrix([[2],[-4]]), PyMatrix([[1,-3,4,-5,6]])), PyMatrix([[2,-6,8,-10,12],[-4,12,-16,20,-24]]))]
)
def test_main(monkeypatch, clib, input_matrixes, result):
    class getMatrix:
        def __init__(self, matrixes):
            self._matrixes = matrixes
            self._count = 0

        def __call__(self, path):
            self._count += 1
            return self._matrixes[self._count-1]
    get_matrix = getMatrix(input_matrixes)

    mult_result = PyMatrix()
    def save_result(matr, path):
        nonlocal mult_result
        mult_result = matr

    monkeypatch.setattr(sys, 'argv', ['fict1','fict2','fict3','fict4'])
    monkeypatch.setattr(CLib, '__call__', clib)
    monkeypatch.setattr(PyMatrix, 'readPyMatrix', get_matrix)
    monkeypatch.setattr(PyMatrix, 'writePyMatrix', save_result)

    main()
    assert mult_result == result





