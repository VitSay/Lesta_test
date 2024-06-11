#include <cstdint>
#include <memory>

#ifdef _WIN32
#define DLL_EXPORT __declspec(dllexport)
#else
#define DLL_EXPORT
#endif


extern "C" {
    DLL_EXPORT int32_t** matrix_mult(const int32_t** matrix_1, 
                                     const int32_t** matrix_2,
                                     int32_t matrix_1_n_rows,
                                     int32_t matrix_1_n_cols,
                                     int32_t matrix_2_n_rows,
                                     int32_t matrix_2_n_cols)
        {
            /*
            Количество столбцов первой матрицы должно быть равно количеству строк второй матрицы

            Проверка:
            */

            /*
            Результирующая матрица будет иметь размерность:
            количество строк 1 матрицы Х количество столбцов 2 матрицы
            */
            int32_t** result = (int32_t**)calloc(matrix_1_n_rows, sizeof(int32_t*));
            for (int row = 0; row < matrix_1_n_rows; ++row)
            {
                result[row] = (int32_t*)calloc(matrix_2_n_cols, sizeof(int32_t));
                for (int col = 0; col < matrix_2_n_cols; ++col)
                {
                    int32_t temp = 0;
                    for (int i = 0; i < matrix_1_n_cols; ++i)
                    {
                        temp += matrix_1[row][i] * matrix_2[i][col];
                    }
                    result[row][col] = temp;
                }
            }
            return result;
        }


    DLL_EXPORT void free_memory(int32_t** matrix, int32_t n_rows)
    {
        for (int i = 0; i < n_rows; ++i)
        {
            free(matrix[i]);
        }
        free(matrix);
    }
}

