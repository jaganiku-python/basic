"""
refference
https://www.youtube.com/watch?v=lVFnq4zbs-g&list=PL5tcWHG-UPH112e7AN7C-fwDVPVrt0wpV

Stack Data Structure
"""

class Stack:
    #Constructor
    def __init__(self):
        self.item = []

    #append object
    def push(self, item):
        self.item.append(item)

    #delete last object
    def pop(self, location=-1):
        self.item.pop(location)

    #empty item field
    def empty(self):
        self.item = []

    #check empty or not
    def is_empty(self):
        return self.item == []

    #get last object
    def peek(self):
        if not self.is_empty():
            return self.item[-1]

    #get stack array
    def get_stack(self):
        return self.item

s = Stack()
s.push('A')
s.push('B')
print(s.get_stack())
s.push('C')
print(s.get_stack())
s.pop(0)
print(s.get_stack())
print(s.peek())
        
    
