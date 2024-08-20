from __future__ import annotations
from data_structures.referential_array import ArrayR, T
from layer_store import *

class Grid:
    DRAW_STYLE_SET = "SET"
    DRAW_STYLE_ADD = "ADD"
    DRAW_STYLE_SEQUENCE = "SEQUENCE"
    DRAW_STYLE_OPTIONS = (
        DRAW_STYLE_SET,
        DRAW_STYLE_ADD,
        DRAW_STYLE_SEQUENCE
    )

    DEFAULT_BRUSH_SIZE = 2
    MAX_BRUSH = 5
    MIN_BRUSH = 0

    def __init__(self, draw_style, x, y) -> None:
        """
        Initialise the grid object.
        - draw_style:
            The style with which colours will be drawn.
            Should be one of DRAW_STYLE_OPTIONS
            This draw style determines the LayerStore used on each grid square.
        - x, y: The dimensions of the grid.

        Should also intialise the brush size to the DEFAULT provided as a class variable.
        Args:
        - draw_style:
            The style with which colours will be drawn.
            Should be one of DRAW_STYLE_OPTIONS
            This draw style determines the LayerStore used on each grid square.
        - x, y: The dimensions of the grid.

        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(nm) where n is the range(x) and m is the range(y) 
        - Best case: O(nm), same as worst case since the no matter what, all the loops will happen
        """
        self.draw_style = draw_style
        self.x_size = x
        self.y_size = y
        self.grid = ArrayR(x) #O(n) 

        for row in range(x): #O(n) where n is the range(x)
            self.grid[row] = ArrayR(y) #O(n)

        # instantiate the layer store in each grid boxes
        for row in range(x): #O(n) where n is the range(x)
            for column in range(y): #O(m) where m is the range(y) * O(n) 
                if draw_style == self.DRAW_STYLE_OPTIONS[0]: #O(1) * O(m) * O(n) 
                    self.grid[row][column] = SetLayerStore() #O(1) * O(m) * O(n) 
                elif draw_style == self.DRAW_STYLE_OPTIONS[1]: #O(1) * O(m) * O(n) 
                    self.grid[row][column] = AdditiveLayerStore() #O(1) * O(m) * O(n) 
                elif draw_style == self.DRAW_STYLE_OPTIONS[2]: #O(1) * O(m) * O(n) 
                    self.grid[row][column] = SequenceLayerStore() #O(1) * O(m) * O(n) 

        self.brush_size = Grid.DEFAULT_BRUSH_SIZE #O(1)

    def __getitem__(self, key):
        """
        Returns the object in position index.
        :pre: index in between 0 and length - self.array[] checks it
        Args:
        - None

        Raises:
        - None

        Returns:
        - self.grid[key]: the grid according to the coordinate key passed in

        Complexity:
        - Worst case: O(1)
        - Best case: O(1), same as worst case since the input does not affect the growth speed of the algorithm
        """
        return self.grid[key] #O(1)

    def increase_brush_size(self):
        """
        Increases the size of the brush by 1,
        if the brush size is already MAX_BRUSH,
        then do nothing.
        Args:
        - None

        Raises:
        - None

        Returns:
        - self.action: PaintAction data type of the current action being passed in

        Complexity:
        - Worst case: O(1)
        - Best case: O(1), same as worst case since the input does not affect the growth speed of the algorithm
        """
        if self.brush_size < self.MAX_BRUSH: #O(1)
            self.brush_size += 1

    def decrease_brush_size(self):
        """
        Decreases the size of the brush by 1,
        if the brush size is already MIN_BRUSH,
        then do nothing.
        Args:
        - None

        Raises:
        - None

        Returns:
        - self.action: PaintAction data type of the current action being passed in

        Complexity:
        - Worst case: O(1)
        - Best case: O(1), same as worst case since the input does not affect the growth speed of the algorithm
        """
        if self.brush_size > self.MIN_BRUSH: #O(1)
            self.brush_size -= 1

    def special(self):
        """
        Activate the special affect on all grid squares.
        Args:
        - None

        Raises: ~in special()~
        - Exception: if self.layer_queue is empty (for serve()) or self.layer_stack is empty (for pop())
                    or if self.layer_queue is full (for append()) or self.layer_stack is full (for push())

        Returns:
        - None

        Complexity:
        - Worst case: O(nm*special())  where n is the length of self.grid and m is the length of row. if the action is a special action in AdditiveLayerStore or SequenceLayerStore
        - Best case: O(nm), if the action is a special action in SetLayerStore
        """
        for row in self.grid: #O(n) where n is the length of self.grid
            for column in row: #O(n) * O(m)  where m is the length of row
                column.special() #from layer_store.py #O(n) * O(m) *[worst: O(special()) if the action is a special action in AdditiveLayerStore or SequenceLayerStore]
