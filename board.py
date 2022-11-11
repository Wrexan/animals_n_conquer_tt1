import random


class SafariBoard:
    """This class can: create board, fill it with animals, show and emulate simple natural selection\n
    Parameters :
    `width` - width of the board
    `height` - height of the board
    `animals` - dict like {name:domination_level}, containing all animal types you want to simulate\n
    Returns: the SafariBoard object
    """
    def __init__(self, width: int, height: int, animals: dict):
        if not (0 < height < 31 and 0 < width < 31):
            ValueError(f'The board height and width must be between: min=1, max=30')
        self._height = height
        self._width = width
        self._empty_cell = None
        self._animal_types = self.create_animals(animals)
        self._board = self.create_safari_board()
        # the animal and coords of chosen cell
        self._chosen_cell_x = 0
        self._chosen_cell_y = 0
        self._chosen_animal = None

    class Animal:
        """The main creature class. Contains basic parameters\n
        Parameters :
        `name` - name of the animal
        `domination_level: int (1 to n)` - how strong is the animal.
         All animals having this parameter lower, will be eaten by this animal\n
        Returns: an Animal object
        """
        def __init__(self, name: str, domination_level: int):
            self.name = name
            self.symbol = name[0].upper()  # Get first letter for pic4a
            self.domination_level = domination_level  # Get first letter for pic4a

    def create_animals(self, animals: dict) -> list:
        """Converts dict of animal params\n
         Returns: list of animal objects"""
        # creating an empty cell to replace eaten animals
        self._empty_cell = self.Animal(name='-', domination_level=0)
        # creating animals provided by the user
        _animal_types = []
        for name, domination_level in animals.items():
            animal = self.Animal(name=name, domination_level=domination_level)
            _animal_types.append(animal)
        return _animal_types

    def create_safari_board(self) -> list:
        """Returns: a list(y coord) of lists(x coords, rows) of the board"""
        _board = []
        _animal_types = len(self._animal_types)
        for _y in range(self._height):
            _row = []
            for _x in range(self._width):
                _row.append(self._animal_types[random.randrange(_animal_types)])
            _board.append(_row)
        return _board

    def show(self):
        """Print the board to the command line"""
        for _y in range(self._height):
            row = ' '.join([_animal.symbol for _animal in self._board[_y]])
            print(row)

    def select_random_cell(self):
        """Selects and print one random cell of the board"""
        self._chosen_cell_x = random.randrange(self._width)
        self._chosen_cell_y = random.randrange(self._height)
        self._chosen_animal = self._board[self._chosen_cell_y][self._chosen_cell_x]
        print(f'\n'
              f'Chosen cell: '
              f'[{self._chosen_cell_y + 1},{self._chosen_cell_x + 1}]: '
              f'{self._chosen_animal.symbol}'
              f'\n')

    def start_natural_selection(self):
        """Emulates simple natural selection, saves changes back to the board object.\n
         You need board.show() to see result"""
        _working_area_cells = (-1, 0, 1)
        _founded_cells = []

        # recursive method
        def conquer_cells_around(_cell_y_idx: int, _cell_x_idx: int) -> None:
            # clean chosen cell, others will go away, deer will die :(
            self._board[_cell_y_idx][_cell_x_idx] = self._empty_cell
            # founded cell cache, to not check twice
            _founded_cells.append((_cell_y_idx, _cell_x_idx))
            # looking for animals in _working_area_cells*_working_area_cells area
            for _y_cell in _working_area_cells:
                for _x_cell in _working_area_cells:
                    _x_cell_to_check = _cell_x_idx + _x_cell
                    _y_cell_to_check = _cell_y_idx + _y_cell
                    # skip cells out of the board and central cell
                    if not (0 <= _x_cell_to_check < self._width):
                        continue
                    if not (0 <= _y_cell_to_check < self._height):
                        continue
                    # if animal can be eaten, let's go there first and add it to the cache! recursively.
                    # otherwise skipping cell
                    if self._board[_y_cell_to_check][_x_cell_to_check].domination_level \
                            < self._chosen_animal.domination_level\
                            and (_y_cell_to_check, _x_cell_to_check) not in _founded_cells:
                        _founded_cells.append((_y_cell_to_check, _x_cell_to_check))
                        conquer_cells_around(_y_cell_to_check, _x_cell_to_check)

        conquer_cells_around(self._chosen_cell_y, self._chosen_cell_x)
        # final update of board from cache
        for y, x in _founded_cells:
            self._board[y][x] = self._empty_cell


if __name__ == '__main__':
    animals = {'Lion': 4, 'Tiger': 3, 'Wolf': 2, 'Deer': 1}
    safari_board = SafariBoard(width=10, height=10, animals=animals)
    safari_board.show()
    safari_board.select_random_cell()
    safari_board.start_natural_selection()
    safari_board.show()
