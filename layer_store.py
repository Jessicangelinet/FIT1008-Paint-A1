from __future__ import annotations
from abc import ABC, abstractmethod
from layer_util import *
from layers import *
from data_structures.stack_adt import ArrayStack
from data_structures.queue_adt import CircularQueue
from data_structures.array_sorted_list import ArraySortedList
from data_structures.sorted_list_adt import ListItem
from data_structures.bset import BSet


class LayerStore(ABC):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        pass

    @abstractmethod
    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def special(self):
        """
        Special mode. Different for each store implementation.
        """
        pass

    
class SetLayerStore(LayerStore):
    """
    Set layer store. A single layer can be stored at a time (or nothing at all)
    - add: Set the single layer.
    - erase: Remove the single layer. Ignore what is currently selected.
    - special: Invert the colour output.
    """

    def __init__(self) -> None:
        LayerStore.__init__(self)
        self.color = (None, None, None)
        self.layer = None
        self.inverted = False

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        Args:
        - layer: the current layer type

        Raises:
        - None

        Returns:
        - Boolean of the state if the LayerStore was actually changed.

        Complexity:
        - Worst case: O(1)
        - Best case: O(1), same as worst case since the input does not affect the growth speed of the algorithm
        """
        if layer != self.layer:
            self.layer = layer
            return True
        return False
    
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers. 
        Args:
        - start: a tuple of the starting color
        - timestamp:
        - x: the current grid point x
        - y: the current grid point y

        Raises:
        - None

        Returns:
        - self.color: tuple of colors integer

        Complexity:
        - Worst case: O(1)
        - Best case: O(1), same as worst case since the input does not affect the growth speed of the algorithm
        """
        if self.inverted:
            if self.layer != None:
                self.color = invert.apply(self.layer.apply(start, timestamp, x, y), timestamp, x, y)
            else:
                self.color = invert.apply(start, timestamp, x, y)
        else:
            if self.layer != None:
                self.color = self.layer.apply(start, timestamp, x, y)
            else:
                self.color = start
        return self.color
            

    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        Args:
        - layer: the current layer type

        Raises:
        - None

        Returns:
        - Boolean of the state if the LayerStore was actually changed.

        Complexity:
        - Worst case: O(1)
        - Best case: O(1), same as worst case since the input does not affect the growth speed of the algorithm
        """
        if layer != None:
            self.layer = None
            return True
        return False

    def special(self):
        """
        Invert the colour output.
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
        if not self.inverted: #O(1)
            self.inverted = True #O(1)
        else:
            self.inverted = False #O(1)


class AdditiveLayerStore(LayerStore):
    """
    Additive layer store. Each added layer applies after all previous ones.
    - add: Add a new layer to be added last.
    - erase: Remove the first layer that was added. Ignore what is currently selected.
    - special: Reverse the order of current layers (first becomes last, etc.)
    """
    
    def __init__(self) -> None:
        LayerStore.__init__(self)
        self.layer_queue = CircularQueue(len(get_layers())*100)
        self.layer_stack = ArrayStack(len(get_layers())*100)
    
    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        Add a new layer to be added last.
        Args:
        - layer: the current layer type

        Raises:
        - Exception: if self.layer_queue is full (from append())

        Returns:
        - Boolean: the state of if the LayerStore was actually changed.

        Complexity:
        - Worst case: O(1)
        - Best case: O(1), same as worst case since the input does not affect the growth speed of the algorithm
        """
        added_queue_length = len(self.layer_queue) + 1    
        self.layer_queue.append(layer)
        if len(self.layer_queue) == added_queue_length:
            return True
        return False      

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        Args:
        - start: a tuple of the starting color
        - timestamp:
        - x: the current grid point x
        - y: the current grid point y

        Raises:
        - Exception: if self.layer_queue is empty (from serve) and if self.layer_queue is full (from append())

        Returns:
        - color: tuple of colors integer

        Complexity:
        - Worst case: O(f(apply)*n) where n is len(self.layer_queue) and O(f(apply)) is the asymptotic upper bound of the apply function
        - Best case: O(1), where self.layer_queue is empty
        """
        color = start 
        
        if self.layer_queue.is_empty(): #O(1)
            return color #O(1)

        for element in range(len(self.layer_queue)): #O(n) where n is len(self.layer_queue)

            current_layer = self.layer_queue.serve() # O(1) * O(n) where n is len(self.layer_queue)
            color = current_layer.apply(color, timestamp, x, y)  # O(apply) * O(n) where n is len(self.layer_queue)
            self.layer_queue.append(current_layer) # O(1) * O(n) where n is len(self.layer_queue)

        return color #O(1)
    
    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        Args:
        - layer: the current layer type

        Raises:
        - Exception: if self.layer_queue is empty 

        Returns:
        - Boolean: the state of if the LayerStore was actually changed.

        Complexity:
        - Worst case: O(1)
        - Best case: O(1), same as worst case since the input does not affect the growth speed of the algorithm
        """
        erased_queue_length = len(self.layer_queue)-1 #O(1)
        self.layer_queue.serve() #O(1)
        if len(self.layer_queue) == erased_queue_length: #O(1)
            return True #O(1)
        return False #O(1)

    def special(self):
        """
        special: Reverse the order of current layers (first becomes last, etc.)

         Args:
        - None

        Raises:
        - Exception: if self.layer_queue is empty (for serve()) or self.layer_stack is empty (for pop())
                    or if self.layer_queue is full (for append()) or self.layer_stack is full (for push())

        Returns:
        - None

        Complexity:
        - Worst case: O(n) where n is len(self.layer_queue) or O(m) where n is len(self.layer_stack)
        - Best case: O(n), same as worst case since we need to iterate both no matter what
        """
        for element in range(len(self.layer_queue)): #O(n) where n is len(self.layer_queue)
            current_element = self.layer_queue.serve() #O(1) * O(n) where n is len(self.layer_queue)
            self.layer_stack.push(current_element) #O(1) * O(n) where n is len(self.layer_queue)

        for element in range(len(self.layer_stack)): #O(m) where n is len(self.layer_stack)
            reversed_element = self.layer_stack.pop() #O(1) * O(m) where n is len(self.layer_stack)
            self.layer_queue.append(reversed_element) #O(1) * O(m) where n is len(self.layer_stack)


class SequenceLayerStore(LayerStore):
    """
    Sequential layer store. Each layer type is either applied / not applied, and is applied in order of index.
    - add: Ensure this layer type is applied.
    - erase: Ensure this layer type is not applied.
    - special:
        Of all currently applied layers, remove the one with median `name`.
        In the event of two layers being the median names, pick the lexicographically smaller one.
    """

    def __init__(self) -> None:        
        self.layer_set = BSet(9)
        self.is_specialized = False
        self.layer_list = get_layers()

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        Ensure this layer type is applied.
        Args:
        - layer: the current layer type

        Raises:
        - TypeError: if the passed Set elements are not be integers in add()

        Returns:
        - Boolean of the state if the LayerStore was actually changed.

        Complexity:
        - Worst case: O(1)
        - Best case: O(1), same as worst case since the input does not affect the growth speed of the algorithm
        """
        layer_index = layer.index + 1

        if layer_index in self.layer_set: #O(1)
            return False #O(1)
        self.layer_set.add(layer_index) #O(1)
        return True #O(1)

    
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        Args:
        - start: a tuple of the starting color
        - timestamp: special integer that is required by a certain animation layers, e.g. rainbow.
        - x: the current grid point x
        - y: the current grid point y

        Raises:
        - None

        Returns:
        - color: tuple of colors integer

        Complexity:
        - Worst case: O(f(apply)*n) where n is len(self.layer_queue) and O(f(apply)) is the asymptotic upper bound of the apply function
        - Best case: O(n), where each_layer in self.layer_list is None or each_layer.index + 1 is not in self.layer_set
        """
        color = start #O(1)

        for each_layer in self.layer_list: # O(n) where n is the length of layer_list
                if each_layer != None and each_layer.index + 1 in self.layer_set: #O(1) * O(n) where n is the length of layer_list
                    color = each_layer.apply(color, timestamp, x, y) # O(apply) * O(n) where n is the length of layer_list
        
        return color #O(1)

    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        Ensure this layer type is not applied.
        Args:
        - layer: the current layer type

        Raises: ~in remove()~
        - TypeError: if the item is not integer or if not positive.
        - KeyError: if the item is not in the set.

        Returns:
        - Boolean of the state if the LayerStore was actually changed.

        Complexity:
        - Worst case: O(1)
        - Best case: O(1), same as worst case since the input does not affect the growth speed of the algorithm
        """
        layer_index = layer.index + 1 #O(1)
        if layer_index not in self.layer_set: #O(1)
            return False #O(1)
        self.layer_set.remove(layer_index) #O(1)
        return True #O(1)

    def special(self):
        """
        Of all currently applied layers, remove the one with median `name`.
        In the event of two layers being the median names, pick the lexicographically smaller one.
        Args:
        - None

        Raises:
        - TypeError: if the item is not integer or if not positive in remove() and if the passed Set elements are not be integers in add()
        - KeyError: if the item is not in the set in remove()

        Returns:
        - None

        Complexity:
        - Worst case: O(n) where n is the length of self.layer_list
        - Best case: O(n), same as worst case since we need to iterate the first for loop no matter what
        """
        layer_sortedList = ArraySortedList(10000) #O(1)
        # making the bset into a sorted list
        for each_layer in self.layer_list: # O(n) where n is the length of self.layer_list
            if each_layer != None and each_layer.index + 1 in self.layer_set: #O(1) * O(n) where n is the length of self.layer_list
                item = ListItem(each_layer, each_layer.name) #O(1) ? * O(n) where n is the length of self.layer_list
                layer_sortedList.add(item) #O(1) * O(n) where n is the length of self.layer_list
        
        # removing the  median `name`
        if not layer_sortedList.is_empty(): #O(1)
            if len(layer_sortedList) % 2 == 0: #O(1)
                chosen_index = (len(layer_sortedList) // 2) - 1 #O(1)
            else:
                chosen_index = (len(layer_sortedList) // 2) #O(1)

            removed_item_index = layer_sortedList[chosen_index].value.index #O(1) ??
            self.layer_set.remove(removed_item_index + 1) #O(1)
