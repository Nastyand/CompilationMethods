# Реализация нисходящего анализатора
# Определение правил грамматики в виде словаря
rules = {
    1: {'left': 'A', 'alternative': 1, 'right': '!B!'},
    2: {'left': 'B', 'alternative': 1, 'right': 'T'},
    3: {'left': 'B', 'alternative': 2, 'right': 'T+B'},
    4: {'left': 'T', 'alternative': 1, 'right': 'M'},
    5: {'left': 'T', 'alternative': 2, 'right': 'M*T'},
    6: {'left': 'M', 'alternative': 1, 'right': 'a'},
    7: {'left': 'M', 'alternative': 2, 'right': 'b'},
    8: {'left': 'M', 'alternative': 3, 'right': '(B)'}
}

# Стек для хранения состояния разбора
L1 = []
# Стек для текущей строки разбора
L2 = ['A']

# Входная строка для разбора
str = '!a*(b+(a*b))!'
#str ='!a+b!'
#str ='!a*b!'
#str ='!(a+b)*(b+a)!'
#str = '!b*a+a*b!'
#str ='!(a+b)*a+b*a!'
#str ='!(a+b*a)*(b*b+a*(a+b+a))+!'
#str ='!a+*b!'
#str ='a!b'
#str ='a+b*a+b'
#str ='!a(b+a()!'

# Первый шаг - замена нетерминала на правую часть правила
def stepOne(key):
    L1.append([])
    L1[-1].append(L2[-1])  # Сохраняем верхний элемент L2 в L1
    L1[-1].append(1)  # Записываем альтернативу правила
    L2.pop()  # Удаляем верхний элемент L2
    right = rules[key]['right']
    for i in range(len(right)-1, -1, -1):  # Добавляем символы справа налево
        L2.append(right[i])

# Второй шаг - проверка на соответствие символу строки
def stepTwo(str_index):
    L1.append([])
    L1[-1].append(L2[-1])  # Сохраняем текущий символ
    L2.pop()  # Удаляем из стека
    str_index += 1  # Переход к следующему символу входной строки
    return str_index

# Третий шаг - если строка разобрана успешно, выводим результат
def stepThree():
    result = []
    for i in range(len(L1)):
        if len(L1[i]) == 2:
            for key in rules:
                if L1[i][0] == rules[key]['left'] and int(L1[i][1]) == rules[key]['alternative']:
                    result.append(key)
    print(f'result: {result}')

# Пятый шаг - возврат к предыдущему состоянию
def stepFive(str_index):
    L2.append(f'{L1[-1][0]}')  # Восстанавливаем символ
    str_index -= 1  # Отмена последнего сдвига
    L1.pop()  # Удаляем последний элемент из L1
    return str_index

# Шестой шаг (A) - переключение на альтернативное правило
def stepSixA(key):
    for _ in range(len(rules[key-1]['right'])):
        L2.pop()  # Удаляем правую часть предыдущего правила
    L1[-1][1] += 1  # Переход к следующей альтернативе
    right = rules[key]['right']
    for i in range(len(right)-1, -1, -1):  # Добавляем новую правую часть
        L2.append(right[i])

# Шестой шаг (B) - ошибка разбора
def stepSixB():
    print('Error')

# Шестой шаг (C) - возврат к предыдущему нетерминалу
def stepSixC():
    for key in rules:
        if L1[-1][0] == rules[key]['left'] and L1[-1][1] == rules[key]['alternative']:
            for _ in range(len(rules[key]['right'])):
                L2.pop()  # Удаляем правую часть правила
            L1.pop()  # Удаляем запись из стека L1
            L2.append(rules[key]['left'])  # Восстанавливаем нетерминал
            return

# Основной алгоритм нисходящего анализа с возвратом
def topDownAlgorithm(state, str_index):
    while True:
        flag_continue = 0  # Флаг для пропуска итерации
        if state == 'q':  # Основное состояние
            for key in rules:
                if L2[-1] == rules[key]['left']:  # Если верхний элемент - нетерминал
                    stepOne(key)
                    flag_continue = 1
                    break
            if flag_continue:
                continue

            if L2[-1] == str[str_index]:  # Если символ совпадает с входной строкой
                str_index = stepTwo(str_index)
                if len(str) == str_index:  # Если строка полностью разобрана
                    if len(L2) == 0:
                        return stepThree()
                    else:
                        state = 'b'  # Переход в состояние возврата
                elif len(L2) == 0:
                    state = 'b'
            else:
                state = 'b'  # Ошибка или необходимость возврата

        elif state == 'b':  # Состояние возврата
            if len(L1[-1]) == 1:  # Если в L1 только 1 элемент
                str_index = stepFive(str_index)
            else:
                for key in rules:
                    if rules[key]['left'] == L1[-1][0] and rules[key]['alternative'] == L1[-1][1] + 1:
                        stepSixA(key)
                        flag_continue = 1
                        state = 'q'
                        break
                if flag_continue:
                    continue
                if L1[-1][0] == 'A':  # Если возврат невозможен
                    stepSixB()
                    return
                else:
                    stepSixC()  # Продолжение разбора

# Запуск алгоритма с начальным состоянием
topDownAlgorithm('q', 0)
