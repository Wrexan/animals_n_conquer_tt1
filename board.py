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
        self._chosen_cell_idx = None

    def create_animals(self, animals: dict):
        self._empty_cell = self.Animal(name='-', domination_level=0)
        _animal_types = []
        for name, domination_level in animals.items():
            animal = self.Animal(name=name, domination_level=domination_level)
            _animal_types.append(animal)
        return _animal_types

    def create_safari_board(self) -> list:
        _board = []
        _animal_types = len(self._animal_types)
        for _y in range(self._height):
            for _x in range(self._width):
                _board.append(self._animal_types[random.randrange(_animal_types)])
        return _board

    def show(self):
        for _y in range(self._height):
            row = ' '.join([_animal.symbol
                            for _animal in self._board[_y * self._width: _y * self._width + self._width]])
            print(row)

    def select_random_cell(self):
        self._chosen_cell_idx = random.randrange(len(self._board))
        # self._chosen_cell = self._board[_rand_cell_num]
        print(f'Chosen cell: ['
              f'{self._chosen_cell_idx % self._width},'
              f'{self._chosen_cell_idx // self._width}]: '
              f'{self._board[self._chosen_cell_idx]}')

    def dominate(self):
        _cell_coords_x = (-1, 0, 1)
        _cell_coords_y = (-self._width, 0, self._width)

        def conquer_cells_around(_cell_idx):
            for _y_cell in _cell_coords_y:
                for _x_cell in _cell_coords_x:
                    _next_cell_idx = _cell_idx + _y_cell + _x_cell
                    if not (0 <= _next_cell_idx < len(self._board)):
                        continue
                    _row_num = _cell_idx % self._width
                    _next_row_diff = _cell_idx - _next_cell_idx
                    print(f'{_row_num=} {_next_row_diff=}')
                    if (_row_num - _next_row_diff) < 0 or (_row_num + _next_row_diff) >= self._width:
                        continue
                    if self._board[_next_cell_idx].domination_level == 0:
                        continue
                    if self._board[_next_cell_idx].domination_level \
                            < self._board[self._chosen_cell_idx].domination_level:
                        self._board[_next_cell_idx] = self._empty_cell
                        # print(_cell_index)
                        conquer_cells_around(_next_cell_idx)
                        # row.append(self._board[_cell_index].symbol)
                    # else:
                    #     row.append(' ')
                # print(row)

        conquer_cells_around(self._chosen_cell_idx)


animals = {'Lion': 4, 'Tiger': 3, 'Wolf': 2, 'Deer': 1}
safari_board = SafariBoard(width=5, height=5, animals=animals)
safari_board.show()
safari_board.select_random_cell()
safari_board.dominate()
safari_board.show()
