from __future__ import annotations
from action import PaintAction
from grid import Grid

from data_structures.stack_adt import ArrayStack
from data_structures.queue_adt import CircularQueue

class UndoTracker:
    history_stack = ArrayStack(10000) #PaintAction data types # O(1)  #a stack to keep in track of the actions history
    undo_stack = ArrayStack(10000) #a stack to keep in track of the undid actions history # O(1) 

    def add_action(self, action: PaintAction) -> None:
        """
        Adds an action to the undo tracker.

        If your collection is already full,
        feel free to exit early and not add the action.

        Args:
        - action: PaintAction data type of the current action being passed in

        Raises:
        - Exception: if self.undo_stack is empty (from pop()) and if self.undo_stack is full push())

        Returns:
        - None

        Complexity:
        - Worst case: O(n) where n is the len(self.undo_stack)
        - Best case: O(1), self.history_stack is full
        """
        if self.history_stack.is_full():
            pass
        
        if not self.undo_stack.is_empty():
            self.undo_stack.clear()
            for each_history in range(len(self.undo_stack)): #O(n) where n is the len(self.undo_stack)
                self.history_stack.pop() #O(1) * O(n) where n is the len(self.undo_stack)

        self.history_stack.push(action) #O(1)


    def undo(self, grid: Grid) -> PaintAction|None:
        """
        Undo an operation, and apply the relevant action to the grid.
        If there are no actions to undo, simply do nothing.
        Args:
        - grid: Grid instance which is the grid the mouse is painting currently

        Raises:
        - Exception: if self.undo_stack is empty (from pop()) and if self.undo_stack is full push())

        Returns:
        - :return: The action that was undone, or None.

        Complexity:
        - Worst case: O(1) self.history_stack is not empty
        - Best case: O(1), if self.history_stack is empty
        """
        if self.history_stack.is_empty(): # O(1)
            return None # O(1)
        undid_action = self.history_stack.pop() #PaintAction data type      
        self.undo_stack.push(undid_action) # O(1)

        undid_action.undo_apply(grid) # O(1)
        return undid_action # O(1)

    def redo(self, grid: Grid) -> PaintAction|None:
        """
        Redo an operation that was previously undone.
        If there are no actions to redo, simply do nothing.
        Args:
        - grid: Grid instance which is the grid the mouse is painting currently

        Raises:
        - Exception: if self.undo_stack is empty (from pop()) and if self.undo_stack is full push())

        Returns:
        - :return: The action that was redone, or None.

        Complexity:
        - Worst case: O(1) self.history_stack is not empty
        - Best case: O(1), if self.history_stack is empty
        """
        if self.undo_stack.is_empty(): # O(1)
            return None # O(1)
        redid_action = self.undo_stack.pop() # O(1)

        self.history_stack.push(redid_action) # O(1)
        redid_action.redo_apply(grid) # O(1)
        return redid_action # O(1)