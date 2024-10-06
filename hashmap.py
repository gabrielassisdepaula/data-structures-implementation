
class Node:
    def __init__(self, key, value):
        self.key: int | str = key
        self.value = value
        self.next: Node = None


class HashMap:
    def __init__(self, capacity: int | None = 7):
        self.size: int = 0
        self.capacity: int = capacity
        self.map = [None] * capacity


    def _rehash(self):
        self.capacity *= 2
        new_map = [None] * self. capacity
        old_map = self.map
        self.map = new_map
        self.size = 0

        for node in old_map:
            if node:
                self.put(node.key, node.value)
                next = node.next
                while next is not None:
                    self.put(next.key, next.value)
                    next = next.next


    def _hash(self, key):
        if type(key) is int:
            return key
        
        hash = 5381
        
        for char in key:
            hash = hash * 33 + ord(char)
        return hash % self.capacity


    def get(self, key):
        hashed_key = self._hash(key)
        if self.map[hashed_key] is None:
            return -1 
       
        node = self.map[hashed_key]
        if node.key != key:
            next = node.next
            while next is not None:
                if next.key == key: 
                    return (next.key, next.value)
                next = next.next
            return -1
        
        return (node.key, node.value)


    def _insert(self, hashed_key: int, key, value):
        self.map[hashed_key] = Node(key, value)
        self.size += 1

        if (self.size / self.capacity) > 0.5:
            self._rehash() 

    
    def _update_linked_list(self, node: Node, key, value):
        if node.key != key:
            next = node.next
            last_node = node
            
            while next is not None:
                if next.key == key:
                    node.value = value
                last_node = next
                next = next.next

            last_node.next = Node(key, value)
        else:
            node.value = value


    def put(self, key, value):
        hashed_key = self._hash(key)
        node = self.map[hashed_key]

        if node is not None:
            self._update_linked_list(node, key, value)
        else:
            self._insert(hashed_key, key, value)


    def remove(self, key):
        hashed_key = self._hash(key)
        node = self.map[hashed_key]

        if node is not None:
            if node.key != key:
                last_node = node
                next = node.next

                while next is not None:
                    if next.key == key:
                        last_node.next = next.next
                        return (next.key, next.value)
                    last_node = next
                    next = next.next
                return -1
            else:
                self.map[hashed_key] = node.next
                return (node.key, node.value)
        
        return -1
        

    def __str__(self):
        if self.size == 0:
            return '{}'
        
        result = ''
        for index, node in enumerate(self.map):
            if node:
                result += f'\n{index} {hash(node.key)} = ({node.key}, {node.value})'
                next = node.next
                while next is not None:
                    result += f' -> ({next.key}, {next.value})'
                    next = next.next
        return result