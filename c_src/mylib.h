#pragma once
#include <stdint.h>

#ifdef _WIN32
#define DLL_EXPORT __declspec(dllexport)
#else
#define DLL_EXPORT
#endif

DLL_EXPORT int32_t** matrix_mult(const int32_t** matrix_1,
                                 const int32_t** matrix_2,
                                 int32_t matrix_1_n_rows,
                                 int32_t matrix_1_n_cols,
                                 int32_t matrix_2_n_rows,
                                 int32_t matrix_2_n_cols);
                                    
DLL_EXPORT void free_memory(int32_t** matrix, int32_t n_rows);
