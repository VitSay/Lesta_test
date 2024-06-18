import ctypes

class CLib:
    def __init__(self, txt_lib_path: str):
        self._lib = ctypes.CDLL(txt_lib_path)

        # Функция для умножения матриц из dll
        self.matrix_mult_func = self._lib.matrix_mult
        self.matrix_mult_func.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_int32)),
                                           ctypes.POINTER(ctypes.POINTER(ctypes.c_int32)),
                                           ctypes.c_int32, ctypes.c_int32,
                                           ctypes.c_int32, ctypes.c_int32]
        self.matrix_mult_func.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_int32))

        # Функция для очищения памяти выделенной в С из dll
        self.free_memory_func = self._lib.free_memory
        self.free_memory_func.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_int32)), ctypes.c_int32]
        self.free_memory_func.restype = None
