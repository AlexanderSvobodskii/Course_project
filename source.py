import tkinter as tk
import numpy as np
import random

######## библиотеки вызова функций для Гаусса
def SwapLines (A, B, line1, line2): #меняет две строки line1 и line2 местами
    A[line1], A[line2] = A[line2], A[line1]
    B[line1], B[line2] = B[line2], B[line1]

def DivideLine (A, B, line, divider): #деление строки line на число
    A[line] = [a / divider for a in A[line]]
    B[line] /= divider

def CombineLine (A, B, line, source_line, weight): #сложение строки line со строкой source_line, умноженной на число
    A[line] = [(a + k * weight) for a,k in zip(A[line], A[source_line])]
    B[line] += B[source_line] * weight
#Функция zip объединяет в кортежи элементы из последовательностей переданных в качестве аргументов

def Gauss(A, B): #функция, решающая систему методом Гаусса
    j = 0
    while (j < len(B)):

        current_line = None #None - эквивалент Null в Python
        for i in range(j, len(A)): #Ищем максимальный по модулю элемент в {j}-м столбце (column)
            if current_line is None or abs(A[i][j]) > abs(A[current_line][j]):
                current_line = i
        if current_line is None:
            print("Решений нет")
            return None

        if current_line != j:
            SwapLines(A, B, current_line, j) #Переставляем строку с найденным элементом повыше

        DivideLine(A, B, j, A[j][j]) #Нормализуем строку с найденным элементом

        for r in range(j + 1, len(A)): #Обрабатываем нижележащие строки
            CombineLine(A, B, r, j, -A[r][j])

        j += 1

    #Здесь матрица приведена к треугольному виду, считаем решение
    X = [0 for b in B]
    for i in range(len(B) - 1, -1, -1):
        X[i] = B[i] - sum(x * a for x, a in zip(X[(i + 1):], A[i][(i + 1):]))#sum суммирует объекты и возвращает результат
        X[i] = float("{0:.2f}".format(X[i])) # форматирует X[i], оставляя два знака после запятой
        
    for i in range(len(X)):
        print("X" + str(i+1), " = ", X[i])
        x_def = tk.Label(win, text = X[i])
        eq = tk.Label(win, text = '=')
        x_i = tk.Label(win, text = "X" + str(i+1))
        i_mod = i + 5
        x_i.grid(column = '5', row = str(i_mod))
        eq.grid(column = '6', row = str(i_mod))
        x_def.grid(column = '7', row = str(i_mod))
        

    return X
########

######## работа с интерфейсом
def get_name():   
    value = name.get()
    if value:
         if  int(value) > 0:
             n = int(value)                 
                     
             def clear_all(): # функция,очищающая область ввода
                 list = win.grid_slaves()
                 i = 0
                 for l in list:
                    if i < len(list)-5:
                        l.destroy()
                    i += 1 
             
             A = [[0]*n for i in range(n)]
             B = [0]*n

             for i in range(n):
                 for j in range(n):
                     A[i][j] = random.randint(1, 10)

             for i in range(n):
                B[i] = random.randint(1, 10)                

             s0 = 0
             for k in range(n):
                matrix = tk.Label(win, text = A[k], anchor = 'w')
                equals = tk.Label(win, text = '=')
                free_v = tk.Label(win, text = B[k])
                k_mod = k + 5
                matrix.grid(column = '1', row = str(k_mod))
                equals.grid(column = '2', row = str(k_mod))
                free_v.grid(column = '3', row = str(k_mod))
                s0 += 1
                print(' '.join(map(str, A[k])), " = ", str(B[k]))
                
             s0_mod = 5 + s0                
             clear = tk.Button(win, text = 'Очистить область', command = clear_all) # создается кнопка очищения области расчета
             clear.grid(column = '4', row = str(s0_mod))
             
             det = np.linalg.det(A)
             s = 0
             if det == 0:
                 print("Система несовместна")
             else:
               Gauss(A, B)
             
         else:
            win.destroy()
            print('-1')
    else:
        win.destroy()
        print('Пустое значение')
        

win = tk.Tk()  # инициализация окна
photo = tk.PhotoImage(file='math.png')
win.iconphoto(False, photo) # заменяем дефолтный значок окна на пользовательский
win.title("Решение СЛАУ методом Гаусса с выделением главного элемента") # задание окна 
win.geometry('500x600') # разрешение окна

lbl = tk.Label(win, text = 'Введите размерность СЛАУ')
lbl.grid(column = '4', row = '0')


name = tk.Entry(win)
name.grid(column = '4', row = '1')

btn = tk.Button(win, text = 'Ввод', command = get_name)
btn.grid(column = '5', row = '1')


lbl_1 = tk.Label(win, text = '') # межстрочный отступ
lbl_1.grid(column = '4', row = '2') 

lbl_2 = tk.Label(win, text = 'СЛАУ и ее решение:')
lbl_2.grid(column = '4', row = '3') 

lbl_3 = tk.Label(win, text = '') # межстрочный отступ
lbl_3.grid(column = '4', row = '4')

lbl_4 = tk.Label(win, text = '         ') # межстрочный отступ
lbl_4.grid(column = '4', row = '4')

win.mainloop() # вызов окна