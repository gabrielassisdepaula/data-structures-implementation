import ctypes
import gc
 
class DynamicArray(object):
        
    def __init__(self, capacity = 10):
        self.length = 0  # Count actual elements (Default is 0)
        self.capacity = capacity  # Default Capacity
        self.array = self.__make_array(self.capacity)

    def __make_array(self, capacity):
        return (capacity * ctypes.py_object)()
    
    def __len__(self):
        return self.length
    
    def __getitem__(self, index):
        if self.length == 0 or not 0 <= index < self.capacity:
            raise IndexError('Index out of range.')
        
        return self.array[index]

    def is_empty(self):
        return self.length == 0
    
    def __copy_array(self, new_capacity):
        new_array = self.__make_array(new_capacity)

        for i in range(self.capacity):
            new_array[i] = self.array[i]
        
        self.capacity = new_capacity
        self.array = new_array

    def __grow(self):
        self.__copy_array(self.capacity*2)

    def __shrink(self):
        self.__copy_array(self.capacity//2)

    def append(self, item):
        if self.length == self.capacity:
            self.__grow()
        
        self.array[self.length] = item
        self.length += 1 
    
    def get(self, item):
        for i in range(self.length):
            if self.array[i] == item:
                return i
        return -1
    
    def pop(self):
        if self.length == 0:
            return


        self.length -= 1

        if self.length/self.capacity < 1/3:
            self.__shrink()

    def clear(self):
        if self.length == 0:
            return

        del self.array
        gc.collect()

        self.length = 0
        self.capacity = 10
        self.array = self.__make_array(self.capacity)

    def insert(self, index, item):
        if index > self.length:
            index = self.length
            self.append(item)
        
        if index < 0:
            if self.length - abs(index) < 0:
                index = 0
            else:
                index = self.length - abs(index)
        
        if self.length == self.capacity:
            self.__grow()

        for i in range(self.length-1, index-1, -1):
            self.array[i+1] = self.array[i]

        self.array[index] = item
        self.length += 1

    def delete_at(self, index):
        if self.length == 0:
            return

        if index >= self.length or self.length - abs(index) < 0: 
            raise IndexError('Delete index out of range.')
        
        if ((self.length - abs(index)) == self.length-1) or index == self.length-1: 
            self.pop()
            return

        if index < 0:
            index = self.length - abs(index)

        for i in range(index, self.length-1):
            self.array[i] = self.array[i+1]
        
        self.length -= 1

        if self.length/self.capacity < 1/3:
            self.__shrink()

    def delete(self, item):
        if self.length == 0:
            return

        index = None
        for i in range(self.length):
            if self.array[i] == item:
                index = i

        if index == None:
            return

        for i in range(index, self.length-1):
            self.array[i] = self.array[i+1]
        
        self.length -= 1

        if self.length/self.capacity < 1/3:
            self.__shrink()

    def __str__(self):
        if self.length == 0:
            return '[]'
        string = ''

        for i in range(self.length):
            string += str(self.array[i]) + ', '
        
        return '[' + string[:-2] + ']'

