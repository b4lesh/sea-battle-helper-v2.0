"""Главный  и единственный пока модуль.

Переменные:
    sea_field_original - оснвное не имзеняемое поле
    sea_field_chance - поле с конечными шансами
    sea_field_tmp - изменяемое поле основанное на sea_field_original
    wounded - список с координатами раненых кораблей
    all_ships - список оставшихся на поле кораблей

Обозначения на поле:
    ' ' - пустота
    '.' - мимо
    'm' - возможный корабль
    '/' - попадание
    'x' - сбитый корабль
"""


class Ship:
    """Класс для работы с кораблями для поля."""

    def __init__(self, length, orientation, coordinates=None):
        """init."""
        self._length = length
        self._orientation = orientation
        self._coordinates = coordinates

    def set_orientation(self, new_orientation):
        """Изменение ориентации корабля."""
        self._orientation = new_orientation

    def set_coordinates(self, new_coordinates):
        """Изменения координат."""
        self._coordinates = new_coordinates

    def get_length(self):
        """Возвращает длину корабля."""
        return self._length

    def get_orientation(self):
        """Возвращает положение корабля."""
        return self._orientation

    def get_coordinates(self):
        """Возвращает список координат."""
        return self._coordinates


def check_put_ship(x, y, ship):
    """Проверяет могу ли я поставить корабль на эту клетку.

    В случае если я смогу разместить корабль, я рамещаю его на поле
    sea_field_tmp и возвращаю список из координат каждой ячейки этого корабля.
    Если не могу разместить, возвращаю None.
    Переменные:
        possible_coordinates - список возможных координат
        ship_x и ship_y - координаты корабля
    """
    if ship.get_orientation() == 'horizontal':
        possible_coordinates = tuple(
            [(x, y + _) for _ in range(ship.get_length())])
    else:
        possible_coordinates = tuple(
            [(x + _, y) for _ in range(ship.get_length())])

    # проверка не выходит ли последняя координата за поле
    ship_x, ship_y = possible_coordinates[-1]
    if ship_x >= FIELD_HEIGHT or ship_y >= FIELD_WIDTH:
        return
    # проверка всех клеток корабля
    for ship_x, ship_y in possible_coordinates:
        if sea_field_tmp[ship_x][ship_y] not in (' ', '/'):
            return
    # проверка всех клеток вокруг кооробля
    for x, y in possible_coordinates:
        for i in (x - 1, x, x + 1):
            for j in (y - 1, y, y + 1):
                if (-1 < i < FIELD_HEIGHT) and (-1 < j < FIELD_WIDTH) and \
                        sea_field_tmp[i][j] in ('m', 'x'):
                    return

    # распологаем корабль если еще не вышли из функции
    for ship_x, ship_y in possible_coordinates:
        if sea_field_original[ship_x][ship_y] == '/':
            wounded.remove((ship_x, ship_y))
        sea_field_tmp[ship_x][ship_y] = 'm'
    return possible_coordinates


def next_ship(ship_num, orientation):
    """Рекурсивная функция которая перебирает все окрабли."""
    ship = Ship(all_ships[ship_num], orientation)
    for x in range(FIELD_HEIGHT):
        for y in range(FIELD_WIDTH):
            ship.set_coordinates(check_put_ship(x, y, ship))
            if ship.get_coordinates():
                if ship_num + 1 == len(all_ships):
                    if len(wounded) == 0:
                        add_chance()
                        print('V:', location_options)
                else:
                    next_ship(ship_num + 1, 'horizontal')
                for _x, _y in ship.get_coordinates():
                    if sea_field_original[_x][_y] == '/':
                        wounded.append((_x, _y))
                        sea_field_tmp[_x][_y] = '/'
                    else:
                        sea_field_tmp[_x][_y] = ' '
                ship.set_coordinates(None)

    if ship.get_orientation() == 'horizontal' and ship.get_length() > 1:
        next_ship(ship_num, 'vertical')


def add_chance():
    """Добавление шансов."""
    global location_options
    location_options += 1
    for i in range(FIELD_HEIGHT):
        for j in range(FIELD_WIDTH):
            if sea_field_tmp[i][j] == 'm':
                sea_field_chance[i][j] += 1


def do_simple_chance():
    """Подчитывает количетсво шансов."""
    chances = []

    for x in range(FIELD_HEIGHT):
        for y in range(FIELD_WIDTH):
            if sea_field_tmp[x][y] == '/':
                sea_field_chance[x][y] = 0

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
    """Основная функция."""
    ship_num = 0
    next_ship(ship_num, 'horizontal')

    do_simple_chance()
    print(*sea_field_chance, sep='\n')


if __name__ == '__main__':
    from copy import deepcopy

    # количесто вариантов расположения кораблей на поле tmp
    location_options = 0

    FIELD_HEIGHT = 7
    FIELD_WIDTH = 7

    # sea_field_original = [[' ' for _ in range(FIELD_WIDTH)] for _ in
    #                       range(FIELD_HEIGHT)]

    sea_field_original = [[' ', ' ', ' ', ' ', ' ', ' ', ' '],
                          [' ', ' ', ' ', ' ', '.', ' ', ' '],
                          ['/', ' ', ' ', ' ', ' ', ' ', '.'],
                          [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                          [' ', '.', ' ', ' ', ' ', ' ', ' '],
                          [' ', ' ', ' ', ' ', '.', ' ', ' '],
                          ['.', ' ', ' ', ' ', ' ', ' ', '/']]
    all_ships = [4, 3, 3, 2]

    sea_field_tmp = deepcopy(sea_field_original)
    sea_field_chance = [[0 for _ in range(FIELD_WIDTH)]
                        for _ in range(FIELD_HEIGHT)]

    wounded = [(x, y) for y in range(FIELD_WIDTH) for x in range(FIELD_HEIGHT)
               if sea_field_original[x][y] == '/']

    import time

    a = time.time()
    main()
    print('time: ', round(time.time() - a, 3))
