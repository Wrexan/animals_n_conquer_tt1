import random


class SafariBoard:
    class Animal:
        def __init__(self, name: str, domination_level: int):
            self.name = name
            self.symbol = name[0].upper()
            self.domination_level = domination_level

        def __str__(self):
            return self.symbol

    def __init__(self, width: int, height: int, animals: dict):
        if not (0 < height < 31 and 0 < width < 31):
            ValueError(f'The board height and width must be between: min=1, max=30')
        self._height = height
        self._width = width
        self._empty_cell = None
        self._animal_types = self.create_animals(animals)
        self._board = self.create_safari_board()
        self._chosen_cell_x = 0
        self._chosen_cell_y = 0
        self._chosen_animal = None

    def create_animals(self, animals: dict):
        self._empty_cell = self.Animal(name='-', domination_level=65536)
        _animal_types = []
        for name, domination_level in animals.items():
            animal = self.Animal(name=name, domination_level=domination_level)
            _animal_types.append(animal)
        return _animal_types

    def create_safari_board(self) -> list:
        _board = []
        _animal_types = len(self._animal_types)
        for _y in range(self._height):
            _row = []
            for _x in range(self._width):
                _row.append(self._animal_types[random.randrange(_animal_types)])
            _board.append(_row)
        return _board

    def show(self):
        for _y in range(self._height):
            row = ' '.join([_animal.symbol for _animal in self._board[_y]])
            print(row)

    def select_random_cell(self):
        self._chosen_cell_x = random.randrange(self._width)
        self._chosen_cell_y = random.randrange(self._height)
        self._chosen_animal = self._board[self._chosen_cell_y][self._chosen_cell_x]
        print(f'Chosen cell: '
              f'[{self._chosen_cell_y + 1},{self._chosen_cell_x + 1}]: '
              f'{self._chosen_animal.symbol}')

    def dominate(self):
        _working_area_cells = (-1, 0, 1)

        def conquer_cells_around(_cell_x_idx: int, _cell_y_idx: int) -> None:
            self._board[_cell_y_idx][_cell_x_idx] = self._empty_cell
            for _y_cell in _working_area_cells:
                for _x_cell in _working_area_cells:
                    _x_cell_to_check = _cell_x_idx + _x_cell
                    _y_cell_to_check = _cell_y_idx + _y_cell

                    if not (0 <= _x_cell_to_check < self._width):
                        continue

                    if not (0 <= _y_cell_to_check < self._height):
                        continue

                    if self._board[_y_cell_to_check][_x_cell_to_check].domination_level \
                            < self._chosen_animal.domination_level:
                        self._board[_y_cell_to_check][_x_cell_to_check] = self._empty_cell
                        conquer_cells_around(_x_cell_to_check, _y_cell_to_check)

        conquer_cells_around(self._chosen_cell_x, self._chosen_cell_y)


if __name__ == '__main__':
    animals = {'Lion': 3, 'Tiger': 2, 'Wolf': 1, 'Deer': 0}
    safari_board = SafariBoard(width=10, height=10, animals=animals)
    safari_board.show()
    safari_board.select_random_cell()
    safari_board.dominate()
    safari_board.show()
