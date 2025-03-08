# Метод простого предшествования (с использованием функций предшествования,
# построенных итерационным методом Флойда)

# Пример вводимой строки: !a*(b+(a*b))!

# T = { !, +, *, (, ), a, b }
# N = ['A', 'B', "B'", 'T', "T'", 'M']   , A - стартовый символ
# Продукции (e - пустая строка):
# 1) А -> !В!
# 2) В -> В'
# 3) В' -> Т
# 4) В' -> B’ + Т
# 5) Т -> Т'
# 6) Т' -> M
# 7) Т' -> T’ * M
# 8) М -> a
# 9) М -> b
# 10) М -> (В)


class SimplePrecedenceMethod:
    def __init__(self):
        self.productions = {
            1: {
                'left': "A",
                'right': ['!', 'B', '!']
            },
            2: {
                'left': 'B',
                'right': ["B'"]
            },
            3: {
                'left': "B'",
                'right': ['T']
            },
            4: {
                'left': "B'",
                'right': ["B'", '+', "T"]
            },
            5: {
                'left': 'T',
                'right': ["T'"]
            },
            6: {
                'left': "T'",
                'right': ['M']
            },
            7: {
                'left': "T'",
                'right': ["T'", '*', "M"]
            },
            8: {
                'left': 'M',
                'right': ['a']
            },
            9: {
                'left': 'M',
                'right': ['b']
            },
            10: {
                'left': 'M',
                'right': ['c']
            },
            11: {
                'left': 'M',
                'right': ['(', 'B', ')']
            }
        }

        self.notterminal = ['A', 'B', "B'", 'T', "T'", 'M']
        self.terminal = ['(', 'a', 'b', 'c', '*', '+', ')', '!']
        self.ordered_symbols = ['(', 'a', 'b', 'c', 'M', '*', "T'", 'T', '+', "B'", ')', 'B', '!']

        self.L, self.R = self.step1()
        self.L2, self.R2 = self.step2(self.L), self.step2(self.R)
        print(f'L2{self.L2}')
        print(f'R2{self.R2}')
        self.matrix = self.draw_matrix()

        # Вызов функции и вывод результатов
        self.f_values, self.g_values = self.floyd_algorithm(self.matrix)

        if self.f_values is not None:
            print("Функции предшествования существуют:")
            print("g(S_j):", self.g_values)
            print("f(S_i):", self.f_values)

        else:
            print("Функции предшествования не существуют.")

        # Переформатирование исходной матрицы
        self.reordered_matrix = self.reformat_matrix(self.matrix, self.f_values, self.g_values)

        # Вывод переформатированной матрицы
        print("Переформатированная матрица:")
        for row in self.reordered_matrix:
            print(row)

        self.alphabet_f, self.alphabet_g = self.returning_g_f_in_alphabet(self.f_values, self.g_values)
        print(f"alphabet g:{self.alphabet_g} \nalphabet f:{self.alphabet_f}")

        print("Булева матрица")
        self.bool_matrix = self.draw_bool_matrix(self.reordered_matrix)

        input_str = input('Введите строку: ')
        self.simple_precedence(input_str)

    def draw_L(self):
        L = {}
        for rule_num, rule_data in self.productions.items():
            left_symbol = rule_data['left']
            right_symbols = rule_data['right'][0]
            if left_symbol in L:
                L[left_symbol].append(right_symbols)
            else:
                L[left_symbol] = [right_symbols]
        # print(f"L: {self.L}")
        return L

    def draw_R(self):
        R = {}
        for rule_num, rule_data in self.productions.items():
            left_symbol = rule_data['left']
            right_symbols = rule_data['right'][-1]
            if left_symbol in R:
                R[left_symbol].append(right_symbols)
            else:
                R[left_symbol] = [right_symbols]

        # print(f"R: {self.R}")
        return R

    def step1(self):
        return self.draw_L(), self.draw_R()

    def step2(self, L):
        while True:
            changed = False
            for U in L:
                for i in range(len(L[U])):
                    if L[U][i] in L and L[U][i] != U:
                        for element in L[L[U][i]]:
                            if element not in L[U]:
                                L[U].append(element)
                                changed = True
                L[U] = list(set(L[U]))
            if not changed:
                break
        return L

    def draw_matrix(self):
        precedence_matrix = [['  ' for _ in range(len(self.ordered_symbols))] for _ in range(len(self.ordered_symbols))]

        # Заполняем матрицу с учетом отношений <. Терминал - нетерминал
        pairs = []
        for production_id, production in self.productions.items():
            right = production['right']
            for i in range(len(right) - 1):
                if right[i] in self.terminal and right[i + 1] in self.notterminal:
                    pairs.append([right[i], right[i + 1]])

        for pair in pairs:
            for j in self.L2[pair[1]]:
                precedence_matrix[self.ordered_symbols.index(pair[0])][self.ordered_symbols.index(j)] = '<.'

        # Заполняем матрицу с учетом отношений >. Нетерминал - терминал и нетерминал - нетерминал
        pairs = []
        for production_id, production in self.productions.items():
            right = production['right']
            for i in range(len(right) - 1):
                if right[i] in self.notterminal and right[i + 1] in self.terminal:
                    pairs.append([right[i], right[i + 1]])

        for pair in pairs:
            for j in self.R2[pair[0]]:
                precedence_matrix[self.ordered_symbols.index(j)][self.ordered_symbols.index(pair[1])] = '.>'

        # Заполняем матрицу с учетом отношений =. Все символы стоящие справа рядом
        pairs = []
        for production_id, production in self.productions.items():
            right = production['right']
            for i in range(len(right) - 1):
                pairs.append([right[i], right[i + 1]])

        for pair in pairs:
            precedence_matrix[self.ordered_symbols.index(pair[0])][self.ordered_symbols.index(pair[1])] = '=.'

        # Выведем матрицу предшествования
        print("Матрица предшествования:")
        print("Sij   ", end='')
        for i in self.ordered_symbols:
            seps = "   " if len(i) == 2 else "     "
            print(i + seps, end='')
        print()
        # print(ordered_symbols)
        for index, row in enumerate(precedence_matrix):
            seps = " " if len(row[index]) == 2 else "  "
            ends = " " if len(self.ordered_symbols[index]) == 2 else "  "
            print(self.ordered_symbols[index], end=ends)
            print(row, sep=seps)
        return precedence_matrix

    def floyd_algorithm(self, matrix):
        n = len(matrix)
        # Шаг 1
        f_values = [1] * n
        g_values = [1] * n
        changed = True

        while changed:
            changed = False

            # Шаг 2
            for i in range(n):
                for j in range(n):
                    if matrix[i][j] == '.>':
                        if f_values[i] <= g_values[j]:
                            f_values[i] = g_values[j] + 1
                            changed = True

            # Шаг 3
            for j in range(n):
                for i in range(n):
                    if matrix[i][j] == '<.':
                        if f_values[i] >= g_values[j]:
                            g_values[j] = f_values[i] + 1
                            changed = True

            # Шаг 4
            for i in range(n):
                for j in range(n):
                    if matrix[i][j] == '=.' and f_values[i] != g_values[j]:
                        f_values[i] = g_values[j] = max(f_values[i], g_values[j])
                        changed = True

            # Проверка условия завершения алгоритма
            if max(max(f_values), max(g_values)) > 2 * n:
                return None  # Функции предшествования не существуют

            if not changed:
                return f_values, g_values  # Возвращаем значения функций предшествования

    def reformat_matrix(self, matrix, f_values, g_values):
        # Заполнение матрицы значениями g(S_j) по столбцам
        column_indices = sorted(range(len(f_values)), key=lambda i: g_values[i], reverse=True)

        # Меняем столбцы матрицы в соответствии с новым порядком
        matrix_reordered = [[r[i] for i in column_indices] for r in matrix]

        row_indices = sorted(range(len(g_values)), key=lambda i: f_values[i], reverse=True)

        # Меняем строки матрицы в соответствии с новым порядком
        matrix_reordered2 = [matrix_reordered[i] for i in row_indices]

        return matrix_reordered2

    def returning_g_f_in_alphabet(self, f, g):
        ordered_symbols_start = ['(', 'a', 'b', 'c', 'M', '*', "T'", 'T', '+', "B'", ')', 'B', '!']

        # Создаем новый список, отсортированный по убыванию значений из f_values
        sorted_indices_f = sorted(range(len(f)), key=lambda k: f[k], reverse=True)
        sorted_symbols_f = [ordered_symbols_start[i] for i in sorted_indices_f]

        sorted_indices_g = sorted(range(len(g)), key=lambda k: g[k], reverse=True)
        sorted_symbols_g = [ordered_symbols_start[i] for i in sorted_indices_g]

        f_dict, g_dict = {}, {}
        f1, g1 = sorted(f, reverse=True), sorted(g, reverse=True)

        for i in range(len(f)):
            f_dict[sorted_symbols_f[i]] = f1[i]
        for i in range(len(g)):
            g_dict[sorted_symbols_g[i]] = g1[i]

        return f_dict, g_dict

    def draw_bool_matrix(self, matrix):
        new_matrix = [[False for _ in range(len(matrix))] for _ in range(len(matrix))]
        for row in range(len(matrix)):
            for column in range(len(matrix)):
                if matrix[row][column] != '  ':
                    new_matrix[row][column] = True

        print("    ", end='')
        for i in list(self.alphabet_g.values()):
            seps = " " * 6
            print(str(i) + seps, end='')
        print()
        print("    ", end='')
        for i in list(self.alphabet_g.keys()):
            seps = " " * 6
            print(str(i) + seps, end='')
        print()

        for index, row in enumerate(new_matrix):
            print(list(self.alphabet_f.values())[index], end=' ')
            print(list(self.alphabet_f.keys())[index], end=' ')
            print(row, sep='')

        return new_matrix

    def simple_precedence(self, input_string):
        prod_rule = []
        str_index = 0
        stack = [input_string[str_index]]
        str_index += 1
        while True:
            i_row, j_row, i_col, j_col = None, None, None, None
            if str_index > len(input_string) - 1:
                basis = []

                if '<.' in stack:
                    while stack[-1] != '<.':
                        if stack[-1] != '=.':
                            basis.append(stack[-1])
                        stack.pop()
                else:
                    while len(stack) != 0:
                        if stack[-1] != '=.':
                            basis.append(stack[-1])
                        stack.pop()
                basis = basis[::-1]

                for key in self.productions:
                    if self.productions[key]['right'] == basis:
                        stack.append(self.productions[key]['left'])
                        prod_rule.append(key)
                        break

            if stack == ['A']:
                print('Result:')
                print(prod_rule)
                return

            if stack != ['A'] and str_index > len(input_string) - 1:
                print('error1')
                return

            for i in range(len(list(self.alphabet_f.keys()))):
                if list(self.alphabet_f.keys())[i] == stack[-1]:
                    i_row = i
            for i in range(len(list(self.alphabet_g.keys()))):
                if list(self.alphabet_g.keys())[i] == input_string[str_index]:
                    i_col = i

            if not self.bool_matrix[i_row][i_col]:
                print('error2')
                return

            if list(self.alphabet_f.items())[i_row][1] <= list(self.alphabet_g.items())[i_col][1]:

                if len(stack) > 2:
                    for j in range(len(list(self.alphabet_f.keys()))):
                        if list(self.alphabet_f.keys())[j] == stack[-3]:
                            j_row = j
                    for j in range(len(list(self.alphabet_g.keys()))):
                        if list(self.alphabet_g.keys())[j] == stack[-1]:
                            j_col = j

                    if list(self.alphabet_f.items())[j_row][1] < list(self.alphabet_g.items())[j_col][1]:
                        temp = '<.'
                    elif list(self.alphabet_f.items())[j_row][1] == list(self.alphabet_g.items())[j_col][1]:
                        temp = '=.'
                    else:
                        temp = '.>'

                    stack[-2] = temp
                if list(self.alphabet_f.items())[i_row][1] < list(self.alphabet_g.items())[i_col][1]:
                    temp = '<.'
                elif list(self.alphabet_f.items())[i_row][1] == list(self.alphabet_g.items())[i_col][1]:
                    temp = '=.'
                else:
                    temp = '.>'
                stack.append(temp)

                stack.append(input_string[str_index])
                str_index += 1

            elif list(self.alphabet_f.items())[i_row][1] > list(self.alphabet_g.items())[i_col][1]:
                if len(stack) > 2:
                    for i in range(len(list(self.alphabet_f.keys()))):
                        if list(self.alphabet_f.keys())[i] == stack[-3]:
                            i_row = i
                    for i in range(len(list(self.alphabet_g.keys()))):
                        if list(self.alphabet_g.keys())[i] == stack[-1]:
                            i_col = i

                    if list(self.alphabet_f.items())[i_row][1] < list(self.alphabet_g.items())[i_col][1]:
                        temp = '<.'
                    elif list(self.alphabet_f.items())[i_row][1] == list(self.alphabet_g.items())[i_col][1]:
                        temp = '=.'
                    else:
                        temp = '.>'
                    stack[-2] = temp

                basis = []

                if '<.' in stack:
                    while stack[-1] != '<.':
                        if stack[-1] != '=.':
                            basis.append(stack[-1])
                        stack.pop()
                else:
                    while len(stack) != 0:
                        if stack[-1] != '=.':
                            basis.append(stack[-1])
                        stack.pop()
                basis = basis[::-1]

                for key in self.productions:
                    if self.productions[key]['right'] == basis:
                        stack.append(self.productions[key]['left'])
                        prod_rule.append(key)
                        break


if __name__ == "__main__":
    method = SimplePrecedenceMethod()