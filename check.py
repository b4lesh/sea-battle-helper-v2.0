"""Мой тестовы код (основной).
sea_field - основное поле
    ' ' - пустота,
    '.' - мимо,
    'm' - возможный корабль,
    'x' - сбитый корабль
    '/' - попадание,
sea_field_chance - поле с конечными шансами
ships = [] - имеющиеся у нас корабли
ship - С каким кораблем мы имеем дело
wounded = []
"""

import copy

v = 0
FIELD_HEIGHT = 10
FIELD_WIDTH = 10

# sea_field_original = [[' ' for _ in range(FIELD_WIDTH)] for _ in
#                       range(FIELD_HEIGHT)]
sea_field_original = [['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                      ['.', '.', 'x', '.', 'x', '.', '.', '.', 'x', '.'],
                      ['x', '.', '.', '.', 'x', '.', '.', '.', 'x', '.'],
                      ['x', '.', '.', '.', 'x', '.', '.', '.', 'x', '.'],
                      ['.', '.', '.', '.', '.', '.', 'x', '.', '.', '.'],
                      [' ', '.', '.', '.', 'x', '.', '.', '.', 'x', '.'],
                      [' ', ' ', '.', '.', 'x', '.', '.', '.', 'x', '.'],
                      ['.', ' ', ' ', '.', '.', '.', '.', '.', '.', '.'],
                      [' ', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                      [' ', '.', 'x', 'x', 'x', 'x', '.', '.', 'x', '.']]

sea_field_tmp = copy.deepcopy(sea_field_original)
sea_field_chance = [[0 for _ in range(FIELD_WIDTH)] for _ in
                    range(FIELD_HEIGHT)]
all_ships = [1]

wounded = [(x, y) for y in range(FIELD_WIDTH) for x in range(FIELD_HEIGHT) if
           sea_field_original[x][y] == '/']
print('wounded', wounded)


class Ship:
    def __init__(self, length, position, coordinates=None):
        self._length = length
        self._position = position
        self._coordinates = coordinates

    def set_coordinates(self, new_coordinates):
        self._coordinates = new_coordinates

    def set_position(self, new_position):
        self._position = new_position

    def get_length(self):
        return self._length

    def get_coordinates(self):
        return self._coordinates

    def get_position(self):
        return self._position


def check_put_ship(x, y, ship):
    """Проверяет могу ли я поставить корабль на эту клетку.
    В случае если я смогу разместить корабль, я рамещаю его на поле
    sea_field_tmp и возвращаю список из координат каждой ячейки этого корабля.
    Если не могу разместить, возвращаю None.
    Переменные:
        possible_coordinates - список который имеет возможные координаты
        ship_x и ship_y - координаты корабля
    """
    if ship.get_position() == 'horizontal':
        possible_coordinates = tuple(
            [(x, y + _) for _ in range(ship.get_length())])
    else:
        possible_coordinates = tuple(
            [(x + _, y) for _ in range(ship.get_length())])

    ship_x, ship_y = possible_coordinates[-1]
    if ship_x >= FIELD_WIDTH or ship_y >= FIELD_HEIGHT:
        return
    # начинаем проверку каждой клетки корабля
    for ship_x, ship_y in possible_coordinates:
        # проверяяем не вышли ли мы за границу

        # if ship_x >= FIELD_WIDTH or ship_y >= FIELD_HEIGHT:
        #     return

        if not (sea_field_tmp[ship_x][ship_y] == ' ' or
                sea_field_tmp[ship_x][ship_y] == '/'):
            return
        # пустая ли клетка
        for _i in [ship_x - 1, ship_x, ship_x + 1]:
            for _j in [ship_y - 1, ship_y, ship_y + 1]:
                if (-1 < _i < FIELD_HEIGHT) and (-1 < _j < FIELD_WIDTH):
                    if sea_field_tmp[_i][_j] == 'm' or \
                            sea_field_tmp[_i][_j] == 'x':
                        return
    # распологаем корабль
    for ship_x, ship_y in possible_coordinates:
        if sea_field_original[ship_x][ship_y] == '/':
            wounded.remove((ship_x, ship_y))
        sea_field_tmp[ship_x][ship_y] = 'm'
    return possible_coordinates


def next_ship(ship_num, position):
    ship = Ship(all_ships[ship_num], position)
    for x in range(FIELD_HEIGHT):
        for y in range(FIELD_WIDTH):
            ship.set_coordinates(check_put_ship(x, y, ship))
            if ship.get_coordinates():
                if ship_num + 1 == len(all_ships):
                    if len(wounded) == 0:
                        add_chance()
                        print('V:', v)
                else:
                    next_ship(ship_num + 1, 'horizontal')
                for _x, _y in ship.get_coordinates():
                    if sea_field_original[_x][_y] == '/':
                        wounded.append((_x, _y))
                        sea_field_tmp[_x][_y] = '/'
                    else:
                        sea_field_tmp[_x][_y] = ' '
                ship.set_coordinates(None)

    if ship.get_position() == 'horizontal' and ship.get_length() > 1:
        next_ship(ship_num, 'vertical')


def add_chance():
    """Добавление шансов."""
    global v
    v += 1
    for i in range(FIELD_HEIGHT):
        for j in range(FIELD_WIDTH):
            if sea_field_tmp[i][j] == 'm':
                sea_field_chance[i][j] += 1


def do_simple_chance():
    chances = []
    for x in range(FIELD_HEIGHT):
        for y in range(FIELD_WIDTH):
            if sea_field_chance[x][y] not in chances:
                chances.append(sea_field_chance[x][y])

    chances.sort()
    for x in range(FIELD_HEIGHT):
        for y in range(FIELD_WIDTH):
            if sea_field_chance[x][y] != 0:
                sea_field_chance[x][y] = chances.index(
                    sea_field_chance[x][y]) + 1
    print('\nБей', len(chances))


def main():
    ship_num = 0
    next_ship(ship_num, 'horizontal')

    print(*sea_field_chance, sep='\n')
    do_simple_chance()
    print(*sea_field_chance, sep='\n')


if __name__ == '__main__':
    main()
