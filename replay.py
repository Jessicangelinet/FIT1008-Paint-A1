from __future__ import annotations
from action import PaintAction
from grid import Grid
from data_structures.queue_adt import CircularQueue
from data_structures.stack_adt import ArrayStack

from action import PaintStep
from layers import blue, green, red, invert


class ActionBoolean:

    def __init__(self, action: PaintAction, is_undo: bool=False):
        self.action = action
        self.is_undo = is_undo

    def get_action(self):
        """
        storing the action: PaintAction value
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
        return self.action # O(1)
    
    def get_is_undo(self):
        """
        storing the is_undo: boolean value
        Args:
        - None

        Raises:
        - None

        Returns:
        - self.is_undo: boolean of whether the action is an undo or not

        Complexity:
        - Worst case: O(1)
        - Best case: O(1), same as worst case since the input does not affect the growth speed of the algorithm
        """
        return self.is_undo # O(1)

class ReplayTracker:

    def __init__(self) -> None:
 
        self.replay_queue = CircularQueue(10000) #O(1)

    def start_replay(self) -> None:
        """
        Called whenever we should stop taking actions, and start playing them back.

        Useful if you have any setup to do before `play_next_action` should be called.
        Args:
        - None

        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(1)
        - Best case: O(1), same as worst case since the input does not affect the growth speed of the algorithm
        """
        pass

    def add_action(self, action: PaintAction, is_undo: bool=False) -> None:
        """
        Adds an action to the replay.

        `is_undo` specifies whether the action was an undo action or not.
        Special, Redo, and Draw all have this is False.
        Args:
        - action: PaintAction data type of the current action being passed in
        - is_undo: boolean of stating whether the action is an undo or not, is set to False by default if no 'is_undo' parameter being passed in

        Raises:
        - Exception: if self.replay_queue is full (in append())

        Returns:
        - None

        Complexity:
        - Worst case: O(1)
        - Best case: O(1), same as worst case since the input does not affect the growth speed of the algorithm
        """
        action_obj = ActionBoolean(action, is_undo) # O(1)
        self.replay_queue.append(action_obj) #a queue of ActionBooleans # O(1)

    def play_next_action(self, grid: Grid) -> bool:
        """
        Plays the next replay action on the grid.

        Args:
        - grid: Grid instance which is the grid the mouse is painting currently

        Raises:
        - Exception: if self.replay_queue is empty (from serve) but it will not happen in this function as the first if
        statement will check if it is empty or not

        Returns:
        - Returns a boolean.
            - If there were no more actions to play, and so nothing happened, return True.
            - Otherwise, return False. 

        Complexity:
        - Worst case: O(special) if the action is a special action in AdditiveLayerStore or SequenceLayerStore
        - Best case: O(1), if self.replay_queue is empty
        """
        if self.replay_queue.is_empty(): # O(1)
            return True # O(1)
        
        each_action_obj = self.replay_queue.serve() # O(1)

        if each_action_obj.get_is_undo(): # O(1)
            each_action_obj.get_action().undo_apply(grid) # O(special) if the action is a special action in AdditiveLayerStore or SequenceLayerStore 
        else:
            each_action_obj.get_action().redo_apply(grid) # O(special) 
        return False # O(1)

if __name__ == "__main__":
    action1 = PaintAction([], is_special=True)
    action2 = PaintAction([])

    g = Grid(Grid.DRAW_STYLE_SET, 5, 5)

    r = ReplayTracker()
    # add all actions
    r.add_action(action1)
    r.add_action(action2)
    r.add_action(action2, is_undo=True)
    # Start the replay.
    r.start_replay()
    f1 = r.play_next_action(g) # action 1, special
    f2 = r.play_next_action(g) # action 2, draw
    f3 = r.play_next_action(g) # action 2, undo
    t = r.play_next_action(g)  # True, nothing to do.
    # assert (f1, f2, f3, t) == (False, False, False, True)

    steps1 = [PaintStep((4, 4), green), PaintStep((4, 5), green), PaintStep((5, 4), green)]
    steps2 = [PaintStep((5, 5), red), PaintStep((4, 4), red)]

    r.add_action(PaintAction(steps1[:]))
    r.add_action(PaintAction(steps2[:]))
    # Do the replay
    r.start_replay()
    v1 = r.play_next_action(g)
    v2 = r.play_next_action(g)
    v3 = r.play_next_action(g)
    print(f1, f2, f3, t)
    print(v2)