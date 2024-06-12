# Команда для компиляции dll библиотеки на MacOS
/usr/bin/clang++ -shared -o s_src/lib.dll c_src/mylib.cpp -std=c++11 -fdeclspec

# Команда для запуска пайтон скрипта
python matrix_mul.py matrix1.txt matrix2.txt result.txt 