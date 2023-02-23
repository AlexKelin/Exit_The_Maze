def generate_matrix():
    user_inpt = input('Enter the size of the field. (example: 10x10):')
    user_inpt_2 = input('\nPlease define the probability of a mine. example: 0.1:\n')
    if 0 < float(user_inpt_2) <= 1:
        chance = float(user_inpt_2)
    elif ',' in user_inpt_2:
        chance = float(user_inpt_2.replace(',', '.'))
    else:
        print('Please enter a valid probability')
        generate_matrix()
    for p in user_inpt:
        if not p.isnumeric():
            one, two = user_inpt.split(p)
    if int(one) < 3 or int(two) < 3:
        print('Please enter a valid size')
        generate_matrix()
    display_field = [['O' for _ in range(int(one))] for _ in range(int(two))]
    field = [['D' for _ in range(int(one))] for _ in range(int(two))]
    print('\nEmpty Matrix generated successfully:')
    for i in display_field:
        print(i)

    print()
    return field, display_field, chance


def apply_mines(matrix, view_matrix, probability):
    import random
    experiment = matrix
    optical = view_matrix

    for i in range(len(view_matrix)):
        for j in range(len(view_matrix[i])):
            if random.random() <= probability:
                experiment[i][j] = j
                optical[i][j] = 'X'
    new_list = [[item for item in sublist if item != 'D'] for sublist in experiment]  # for calculation only
    # for i in new_list:
    #     print(i)

    print('Mines applied successfully:')
    print()
    for i in optical:
        print(i)

    print()
    return new_list, optical


def find_exit(matrix, visual):  # sourcery skip: identity-comprehension

    one_line = [item for sublist in matrix for item in sublist]
    short_result = any(one_line.count(i) == len(visual) for i in one_line)
    if short_result:
        print('We Got a straight path!')
        exit()

    def lf_exit(whole_matrix):
        path = []
        history = []
        level = 0
        next_level = 1

        def add_level():
            nonlocal level
            nonlocal next_level
            level += 1
            next_level += 1
            return level, next_level

        def check_down(next_lev, char):
            if char in next_lev:
                return True

        def check_right(next_lev, char):
            if char + 1 in next_lev and char + 1 in whole_matrix[level]:
                return True

        def check_left(next_lev, char):
            if char != 0 and char - 1 in next_lev and char - 1 in whole_matrix[level]:
                return True

        def check_life(slate, char):
            passed = []
            for x in slate:
                result = [True]
                if char + 1 == x or char - 1 == x or char == x:
                    continue
                else:
                    if x < char:
                        look_for = [x for x in range(x + 1, char)]
                        for y in look_for:
                            if y not in whole_matrix[level]:
                                result.append(False)
                    elif x > char:
                        look_for = [x for x in range(char + 1, x)]
                        for y in look_for:
                            if y not in whole_matrix[level]:
                                result.append(False)
                    if result[-1] is True:
                        passed.append(x)
                    elif result[-1] is False:
                        pass
            if passed:
                return passed
            else:
                return False

        def start_check():
            for i in whole_matrix[0]:
                if check_down(whole_matrix[1], i):
                    path.append(i)
                    history.append(i)
            if path:
                # print(f'Ground level {path}')
                add_level()
                continuance()

            else:
                print('No ground exit found')
                exit()

        def continuance():
            for G in whole_matrix[level]:
                if G in path:
                    # print(f'Current level: {level} ====')
                    # print(f'Current path: {path}')
                    # print(f'Current value: {G}\n')
                    current_slate = [x for x in whole_matrix[level] if check_down(whole_matrix[next_level], x)]

                    if check_down(whole_matrix[next_level], G) and G not in path:
                        path.append(G)
                        history.append(G)

                    if check_right(whole_matrix[next_level], G) and G + 1 not in path:
                        path.append(G + 1)
                        history.append(G + 1)
                    if check_left(whole_matrix[next_level], G) and G - 1 not in path:
                        path.append(G - 1)
                        history.append(G - 1)
                    if check_life(current_slate, G):
                        for x in check_life(current_slate, G):
                            if x not in path:
                                path.append(x)
                                history.append(x)
                                # print(f'Added {x} to path           +++++++++')
                    if not check_down(whole_matrix[next_level], G):
                        path.remove(G)
            if next_level == len(whole_matrix) - 1 and path:
                print('Exit found')
                exit()
            if path:
                add_level()
                continuance()
            if not path:
                print('No exit found')
                exit()

        start_check()

    lf_exit(matrix)


def main():
    matrix, view_matrix, probability = generate_matrix()
    field_for_calc, visual_field = apply_mines(matrix, view_matrix, probability)
    find_exit(field_for_calc, visual_field)


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
