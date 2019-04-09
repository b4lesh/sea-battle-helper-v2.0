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

sea_field_original = [[0 for _ in range(4)] for _ in range(4)]
sea_field_tmp = copy.deepcopy(sea_field_original)
sea_field_chance = [[0 for _ in range(4)] for _ in range(4)]
ships = [4, 3]


class Ship:
    def __init__(self, length, coordinates, position):
        self._length = length
        self._coordinates = coordinates
        self._position = position

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
        ship_model - список который имеет возможные координаты
        ship_x и ship_y - координаты корабля
    """
    if ship[1] == 'horizontal':
        ship_model = [(x, y + _) for _ in range(ship[0])]
    else:
        ship_model = [(x + _, y) for _ in range(ship[0])]

    # начинаем проверку каждой клетки корабля
    for ship_x, ship_y in ship_model:
        # проверяяем не вышли ли мы за границу
        if ship_x > 9 or ship_y > 9:
            return
        # пустая ли клетка
        for _i in [ship_x - 1, ship_x, ship_x + 1]:
            for _j in [ship_y - 1, ship_y, ship_y + 1]:
                try:
                    if sea_field_tmp[_i][_j] != 0:
                        return
                except:
                    pass
    # распологаем корабль
    for ship_x, ship_y in ship_model:
        sea_field_tmp[ship_x][ship_y] = 2
    return ship_model


def f():
    ship_num = 0
    ships_tmp = []
    ship_tmp = None
    while ship_num < len(ships):
        ship_model = None
        for i in range(4):
            for j in range(4):
                if not ship_tmp:
                    ship_tmp = (ships[ship_num], 'horizontal')
                ship_model = check_put_ship(i, j, ship_tmp)
                if ship_model:
                    ship_tmp = None
                    new_ship = Ship(ship_tmp[0], ship_model, ship_tmp[1])
                    ships_tmp.append(new_ship)
                    ship_num += 1
                    if ship_num == len(ships):
                        add_chance()
                        ship_num -= 1
                        ship_pop = ships_tmp.pop()
                        ship_model = ship_pop.get_coordinates()
                        ship_tmp = (ship_pop.get_length(), ship_pop.get_position())
                        for x, y in ship_model:
                            sea_field_tmp[x][y] = 0
                    else:
                        break
                else:
                    pass
            if ship_model:
                break


def add_chance():
    """Добавление шансев."""
    for i in range(4):
        for j in range(4):
            if sea_field_tmp[i][j] == 2:
                sea_field_chance[i][j] += 1


def main():
    for i in range(4):
        for j in range(4):
            f()
            add_chance()
            print(*sea_field_chance, sep='\n')
            input()


if __name__ == '__main__':
    main()
