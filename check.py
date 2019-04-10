"""Мой тестовы код (основной).

sea_field - основное поле
    0 - пустота,
    1 - мимо,
    2 - корабль,
    3 - поподание,
    4 - потоплен

sea_field_chance - поле с конечными шансами
ships = [] - имеющиеся у нас корабли
ship - С каким кораблем мы имеем дело
wounded = []
"""

import copy

v = 0
FIELD_HEIGHT = 7
FIELD_WIDTH = 7

sea_field_original = [[0 for _ in range(FIELD_WIDTH)] for _ in
                      range(FIELD_HEIGHT)]
sea_field_tmp = copy.deepcopy(sea_field_original)
sea_field_chance = [[0 for _ in range(FIELD_WIDTH)] for _ in
                    range(FIELD_HEIGHT)]
all_ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]


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
        possible_coordinates = [(x, y + _) for _ in range(ship.get_length())]
    else:
        possible_coordinates = [(x + _, y) for _ in range(ship.get_length())]

    # начинаем проверку каждой клетки корабля
    for ship_x, ship_y in possible_coordinates:
        # проверяяем не вышли ли мы за границу
        if ship_x >= FIELD_WIDTH or ship_y >= FIELD_HEIGHT:
            return
        # пустая ли клетка
        for _i in [ship_x - 1, ship_x, ship_x + 1]:
            for _j in [ship_y - 1, ship_y, ship_y + 1]:
                if (-1 < _i < FIELD_HEIGHT) and (-1 < _j < FIELD_WIDTH):
                    if sea_field_tmp[_i][_j] != 0:
                        return
    # распологаем корабль
    for ship_x, ship_y in possible_coordinates:
        sea_field_tmp[ship_x][ship_y] = 2
    return possible_coordinates


def next_ship(ship_num, position):
    ship = Ship(all_ships[ship_num], position)
    for x in range(FIELD_HEIGHT):
        for y in range(FIELD_WIDTH):
            ship.set_coordinates(check_put_ship(x, y, ship))
            if ship.get_coordinates():
                if ship_num + 1 == len(all_ships):
                    add_chance()
                    print('V:', v)
                else:
                    next_ship(ship_num + 1, 'horizontal')
                for _x, _y in ship.get_coordinates():
                    sea_field_tmp[_x][_y] = 0
                ship.set_coordinates(None)

    if ship.get_position() == 'horizontal' and ship.get_length() > 1:
        next_ship(ship_num, 'vertical')




    # while -1 < ship_num < len(all_ships):
    #     ship_model = None
    #     for i in range(FIELD_HEIGHT):
    #         for j in range(FIELD_WIDTH):
    #             if not ship_tmp:
    #                 ship_tmp = [all_ships[ship_num], 'horizontal']
    #             ship_model = check_put_ship(i, j, ship_tmp)
    #             if ship_model:
    #                 new_ship = Ship(ship_tmp[0], ship_model, ship_tmp[1])
    #                 ship_tmp = None
    #                 ships_tmp.append(new_ship)
    #                 ship_num += 1
    #                 if ship_num == len(all_ships):
    #                     add_chance()
    #                     ship_num -= 1
    #                     ship_pop = ships_tmp.pop()
    #                     ship_model = ship_pop.get_coordinates()
    #                     ship_tmp = [ship_pop.get_length(),
    #                                 ship_pop.get_position()]
    #                     i, j = ship_model[0]
    #                     for x, y in ship_model:
    #                         sea_field_tmp[x][y] = 0
    #                 else:
    #                     break
    #             else:
    #                 if i == FIELD_HEIGHT - 1 and j == FIELD_WIDTH - 1:
    #                     if ship_tmp[1] == 'horizontal':
    #                         ship_tmp[1] = 'vertical'
    #                     else:
    #                         ship_num -= 1
    #                         ship_pop = ships_tmp.pop()
    #                         ship_model = ship_pop.get_coordinates()
    #                         ship_tmp = (ship_pop.get_length(),
    #                                     ship_pop.get_position())
    #                         i, j = ship_model[0]
    #                         for x, y in ship_model:
    #                             sea_field_tmp[x][y] = 0
    #
    #         if ship_model:
    #             break


def add_chance():
    """Добавление шансов."""
    global v
    v += 1
    for i in range(FIELD_HEIGHT):
        for j in range(FIELD_WIDTH):
            if sea_field_tmp[i][j] == 2:
                sea_field_chance[i][j] += 1


def main():
    ship_num = 0
    next_ship(ship_num, 'horizontal')
    print('V:', v)
    print(*sea_field_chance, sep='\n')



if __name__ == '__main__':
    main()
