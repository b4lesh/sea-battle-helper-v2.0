"""Главный  и единственный пока модуль.

Переменные:
    sea_field_original - оснвное не изменяемое поле
    sea_field_tmp - изменяемое поле основанное на sea_field_original
    sea_field_chance - поле с шансами
    all_ships - список оставшихся на поле кораблей
    wounded - список с координатами раненых кораблей
Обозначения на поле:
    ' ' - пустота
    '.' - мимо
    'm' - возможный корабль
    '/' - попадание
    'x' - сбитый корабль
"""


class SeaField:
    """Класс для поля."""

    def __init__(self, sea_field, field_height, field_width, all_ships):
        """init."""
        from copy import deepcopy
        self._sea_field_original = deepcopy(sea_field)
        self._sea_field_tmp = deepcopy(sea_field)
        self._field_height = field_height
        self._field_width = field_width
        self._all_ships = all_ships
        self._sea_field_chance = [[0 for _ in range(field_width)]
                                  for _ in range(field_height)]
        self._wounded = [(x, y) for y in range(field_width) for x in
                         range(field_height)
                         if sea_field[x][y] == '/']
        self._location_options = 0

    def get_ship(self, ship_num):
        """По порядковому номеру корабля возвращает его длину."""
        return self._all_ships[ship_num]

    def get_field_height(self):
        """Вовзращает высоту поля.

        Станет бесполезной при окончательном варианте
        """
        return self._field_height

    def get_field_width(self):
        """Вовзращает ширину поля.

        Станет бесполезной при окончательном варианте
        """
        return self._field_width

    def get_all_ships(self):
        """Возвращет весь список кораблей."""
        return self._all_ships

    def get_wounded(self):
        """Возвращет список клеток раненых кораблей."""
        return self._wounded

    def get_sea_field_chance(self):
        """Возвращет поле с шансами."""
        return self._sea_field_chance

    def check_put_ship(self, x, y, ship):
        """Проверяет могу ли я поставить корабль на эту клетку.

        В случае если я смогу разместить корабль, я рамещаю его на поле
        sea_field_tmp и возвращаю список из координат каждой ячейки этого
            корабля.
        Если не могу разместить, возвращаю None.
        Переменные:
            possible_coordinates - список возможных координат
            ship_x и ship_y - координаты корабля
        """
        if ship.get_orientation() == 'horizontal':
            possible_coordinates = [(x, y + _) for _ in
                                    range(ship.get_length())]
        else:
            possible_coordinates = [(x + _, y) for _ in
                                    range(ship.get_length())]

        # проверка не выходит ли последняя координата за поле
        ship_x, ship_y = possible_coordinates[-1]
        if ship_x >= self._field_height or ship_y >= self._field_width:
            return
        # проверка всех клеток корабля
        for ship_x, ship_y in possible_coordinates:
            if self._sea_field_tmp[ship_x][ship_y] not in (' ', '/'):
                return
        # проверка всех клеток вокруг кооробля
        for x, y in possible_coordinates:
            for i in (x - 1, x, x + 1):
                for j in (y - 1, y, y + 1):
                    if (-1 < i < self._field_height) and \
                            (-1 < j < self._field_width) and \
                            self._sea_field_tmp[i][j] in ('m', 'x'):
                        return

        # распологаем корабль если еще не вышли из функции
        for ship_x, ship_y in possible_coordinates:
            if self._sea_field_original[ship_x][ship_y] == '/':
                self._wounded.remove((ship_x, ship_y))
            self._sea_field_tmp[ship_x][ship_y] = 'm'
        return possible_coordinates

    def add_chance(self):
        """Добавление шансов."""
        self._location_options += 1
        for i in range(self._field_height):
            for j in range(self._field_width):
                if self._sea_field_tmp[i][j] == 'm':
                    self._sea_field_chance[i][j] += 1

        # print('Вариантов:', self._location_options)

    def remove_ship_from_field(self, x, y):
        """Удаляет корабль с поля tmp.

        Возвращает попадания в wounded и на поле tmp
        """
        if self._sea_field_original[x][y] == '/':
            self._wounded.append((x, y))
            self._sea_field_tmp[x][y] = '/'
        else:
            self._sea_field_tmp[x][y] = ' '


class Ship:
    """Класс для работы с кораблями для поля."""

    def __init__(self, length, orientation, coordinates=None):
        """Инициализация объекта."""
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


def next_ship(sea_field, ship_num, orientation):
    """Рекурсивная функция которая перебирает все корабли."""
    ship = Ship(sea_field.get_ship(ship_num), orientation)
    for x in range(sea_field.get_field_height()):
        for y in range(sea_field.get_field_width()):
            ship.set_coordinates(sea_field.check_put_ship(x, y, ship))
            if ship.get_coordinates():
                if ship_num + 1 == len(sea_field.get_all_ships()):
                    if not sea_field.get_wounded():
                        sea_field.add_chance()
                else:
                    next_ship(sea_field, ship_num + 1, 'horizontal')
                for _x, _y in ship.get_coordinates():
                    sea_field.remove_ship_from_field(_x, _y)
                ship.set_coordinates(None)

    if ship.get_orientation() == 'horizontal' and ship.get_length() > 1:
        next_ship(sea_field, ship_num, 'vertical')


def do_simple_chance(field_height, field_width, sea_field, sea_field_chance):
    """Подчитывает количетсво шансов."""
    # выписываем все шансы в append и делаем нулевой шанс в клетка с попаданием
    chances = []
    for x in range(field_height):
        for y in range(field_width):
            if sea_field[x][y] == '/':
                sea_field_chance[x][y] = 0
            if sea_field_chance[x][y] not in chances:
                chances.append(sea_field_chance[x][y])

    # переписываем поле с шансами с упрошенными числами
    # сортировка нужна, так как от нее зависят индексы в упрощенной таблице
    chances.sort()
    for x in range(field_height):
        for y in range(field_width):
            if sea_field_chance[x][y] != 0:
                sea_field_chance[x][y] = chances.index(
                    sea_field_chance[x][y]) + 1
    return len(chances)


def get_hit(field_height, field_width, sea_field_chance, length_chances):
    """Возвращает координаты наилучшего удара."""
    for x in range(field_height):
        for y in range(field_width):
            if sea_field_chance[x][y] == length_chances:
                return x + 1, y + 1


def test_func(all):
    sea_field_t, field_height, field_width, all_ships, x, y = all
    sea_field = SeaField(sea_field_t, field_height, field_width, all_ships)
    ship_num = 0
    orientation = 'horizontal'
    ship = Ship(sea_field.get_ship(ship_num), orientation)
    ship.set_coordinates(sea_field.check_put_ship(x, y, ship))
    if ship.get_coordinates():
        if ship_num + 1 == len(sea_field.get_all_ships()):
            if not sea_field.get_wounded():
                sea_field.add_chance()
        else:
            next_ship(sea_field, ship_num + 1, 'horizontal')
        for _x, _y in ship.get_coordinates():
            sea_field.remove_ship_from_field(_x, _y)
        ship.set_coordinates(None)

    if ship.get_orientation() == 'horizontal' and ship.get_length() > 1:
        orientation = 'vertical'
        ship = Ship(sea_field.get_ship(ship_num), orientation)
        ship.set_coordinates(sea_field.check_put_ship(x, y, ship))
        if ship.get_coordinates():
            if ship_num + 1 == len(sea_field.get_all_ships()):
                if not sea_field.get_wounded():
                    sea_field.add_chance()
            else:
                next_ship(sea_field, ship_num + 1, 'horizontal')
            for _x, _y in ship.get_coordinates():
                sea_field.remove_ship_from_field(_x, _y)
            ship.set_coordinates(None)

    sea_field_chance = sea_field.get_sea_field_chance()
    return sea_field_chance


def main():
    """Основная функция."""

    from multiprocessing import Pool, TimeoutError
    field_height = 10
    field_width = 10

    # sea_field_original = [[' ' for _ in range(field_width)] for _ in
    #                       range(field_height)]
    # sea_field_t = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    #                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    #                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    #                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    #                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    #                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    #                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    #                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    #                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    #                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
    sea_field_t = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
    all_ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    hit = None
    p = Pool()
    timeout = 15
    try:
        for l in range(1, len(all_ships) + 1):
            all_data = (
                (sea_field_t, field_height, field_width, all_ships[:l], x, y)
                for x in range(field_height) for y in range(field_width))

            sea_field_chances = p.map_async(test_func, all_data)
            sea_field_chance_end = [[0 for _ in range(field_width)] for _ in
                                    range(field_height)]
            result = sea_field_chances.get(timeout)
            for field in result:
                for x in range(field_height):
                    for y in range(field_width):
                        sea_field_chance_end[x][y] += field[x][y]

            length_chances = do_simple_chance(field_height, field_width,
                                              sea_field_t,
                                              sea_field_chance_end)
            # print(*sea_field_chance_end, sep='\n')
            hit = get_hit(field_height, field_width, sea_field_chance_end,
                          length_chances)
    except TimeoutError:
        print('Почти наилучший удар:', hit)
    else:
        print('Наилучший удар:', hit)
    finally:
        p.terminate()
        p.join()
        return


if __name__ == '__main__':
    import time

    a = time.time()
    main()
    print('time: ', round(time.time() - a, 3))
