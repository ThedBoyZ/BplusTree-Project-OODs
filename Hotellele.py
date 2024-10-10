import time

splits = 0
parent_splits = 0
fusions = 0
parent_fusions = 0
manual_count = 1
# Memory Usage data byte 
tree_structure = []
# function recursive time usage
show_available_rooms_time = 0
inorder_leaf_time = 0
# dictionary keep execute_time list
execution_times = {}
room_number = []


class Node(object):
    """Base node object. It should be index node
    Each node stores keys and children.
    Attributes:
    parent
    """

    def __init__(self, parent=None):
        """Child nodes are stored in values. Parent nodes simply act as a medium to traverse the tree.
        :type parent: Node"""
        self.keys: list = []
        self.values: list[Node] = []
        self.parent: Node = parent

    def index(self, key):
        """Return the index where the key should be.
        :type key: str
        """
        for i, item in enumerate(self.keys):
            if key < item:
                return i

        return len(self.keys)

    def __getitem__(self, item):
        return self.values[self.index(item)]

    def __setitem__(self, key, value):
        i = self.index(key)
        self.keys[i:i] = [key]
        self.values.pop(i)
        self.values[i:i] = value

    def split(self):
        """Splits the node into two and stores them as child nodes.
        extract a pivot from the child to be inserted into the keys of the parent.
        @:return key and two children
        """
        global splits, parent_splits
        splits += 1
        parent_splits += 1

        left = Node(self.parent)

        mid = len(self.keys) // 2

        left.keys = self.keys[:mid]
        left.values = self.values[:mid + 1]
        for child in left.values:
            child.parent = left

        key = self.keys[mid]
        self.keys = self.keys[mid + 1:]
        self.values = self.values[mid + 1:]

        return key, [left, self]

    def __delitem__(self, key):
        i = self.index(key)
        del self.values[i]
        if i < len(self.keys):
            del self.keys[i]
        else:
            del self.keys[i - 1]

    def fusion(self):
        global fusions, parent_fusions
        fusions += 1
        parent_fusions += 1

        index = self.parent.index(self.keys[0])
        # merge this node with the next node
        if index < len(self.parent.keys):
            next_node: Node = self.parent.values[index + 1]
            next_node.keys[0:0] = self.keys + [self.parent.keys[index]]
            for child in self.values:
                child.parent = next_node
            next_node.values[0:0] = self.values
        else:  # If self is the last node, merge with prev
            prev: Node = self.parent.values[-2]
            prev.keys += [self.parent.keys[-1]] + self.keys
            for child in self.values:
                child.parent = prev
            prev.values += self.values

    def borrow_key(self, minimum: int):
        index = self.parent.index(self.keys[0])
        if index < len(self.parent.keys):
            next_node: Node = self.parent.values[index + 1]
            if len(next_node.keys) > minimum:
                self.keys += [self.parent.keys[index]]

                borrow_node = next_node.values.pop(0)
                borrow_node.parent = self
                self.values += [borrow_node]
                self.parent.keys[index] = next_node.keys.pop(0)
                return True
        elif index != 0:
            prev: Node = self.parent.values[index - 1]
            if len(prev.keys) > minimum:
                self.keys[0:0] = [self.parent.keys[index - 1]]

                borrow_node = prev.values.pop()
                borrow_node.parent = self
                self.values[0:0] = [borrow_node]
                self.parent.keys[index - 1] = prev.keys.pop()
                return True

        return False


class Leaf(Node):
    def __init__(self, parent=None, prev_node=None, next_node=None):
        """
        Create a new leaf in the leaf link
        :type prev_node: Leaf
        :type next_node: Leaf
        """
        super(Leaf, self).__init__(parent)
        self.next: Leaf = next_node
        if next_node is not None:
            next_node.prev = self
        self.prev: Leaf = prev_node
        if prev_node is not None:
            prev_node.next = self

    def __getitem__(self, item):
        return self.values[self.keys.index(item)]

    def __setitem__(self, key, value):
        i = self.index(key)
        if key not in self.keys:
            self.keys[i:i] = [key]
            self.values[i:i] = [value]
        else:
            self.values[i - 1] = value

    def split(self):
        global splits
        splits += 1

        left = Leaf(self.parent, self.prev, self)
        mid = len(self.keys) // 2

        left.keys = self.keys[:mid]
        left.values = self.values[:mid]

        self.keys: list = self.keys[mid:]
        self.values: list = self.values[mid:]

        # When the leaf node is split, set the parent key to the left-most key of the right child node.
        return self.keys[0], [left, self]

    def __delitem__(self, key):
        i = self.keys.index(key)
        del self.keys[i]
        del self.values[i]

    def fusion(self):
        global fusions
        fusions += 1

        if self.next is not None and self.next.parent == self.parent:
            self.next.keys[0:0] = self.keys
            self.next.values[0:0] = self.values
        else:
            self.prev.keys += self.keys
            self.prev.values += self.values

        if self.next is not None:
            self.next.prev = self.prev
        if self.prev is not None:
            self.prev.next = self.next

    def borrow_key(self, minimum: int):
        index = self.parent.index(self.keys[0])
        if index < len(self.parent.keys) and len(self.next.keys) > minimum:
            self.keys += [self.next.keys.pop(0)]
            self.values += [self.next.values.pop(0)]
            self.parent.keys[index] = self.next.keys[0]
            return True
        elif index != 0 and len(self.prev.keys) > minimum:
            self.keys[0:0] = [self.prev.keys.pop()]
            self.values[0:0] = [self.prev.values.pop()]
            self.parent.keys[index - 1] = self.keys[0]
            return True

        return False


class BPlusTree(object):
    """B+ tree object, consisting of nodes.
    Nodes will automatically be split into two once it is full. When a split occurs, a key will
    'float' upwards and be inserted into the parent node to act as a pivot.
    Attributes:
        maximum (int): The maximum number of keys each node can hold.
    """
    root: Node

    def __init__(self, maximum=4):
        self.root = Leaf()
        self.maximum: int = maximum if maximum > 2 else 2
        self.minimum: int = self.maximum // 2
        self.depth = 0


    def __getitem__(self, item):
        return self.find(item)[item]

    
    def __setitem__(self, key, value, leaf=None):
        """Inserts a key-value pair after traversing to a leaf node. If the leaf node is full, split
              the leaf node into two.
              """
        if leaf is None:
            leaf = self.find(key)
        leaf[key] = value
        if len(leaf.keys) > self.maximum:
            self.insert_index(*leaf.split())

    def find(self, key) -> Leaf:
        """ find the leaf
        Returns:
            Leaf: the leaf which should have the key
        """
        node = self.root
        # Traverse tree until leaf node is reached.
        while type(node) is not Leaf:
            node = node[key]

        return node

    def insert(self, key, value):
        """
        Returns:
            (bool,Leaf): the leaf where the key is inserted. return False if already has same key
        """
        leaf = self.find(key)
        if key in leaf.keys:
            return False, leaf
        else:
            self.__setitem__(key, value, leaf)
            return True, leaf

    def insert_index(self, key, values: list[Node]):
        """For a parent and child node,
                    Insert the values from the child into the values of the parent."""
        parent = values[1].parent
        if parent is None:
            values[0].parent = values[1].parent = self.root = Node()
            self.depth += 1
            self.root.keys = [key]
            self.root.values = values
            return

        parent[key] = values
        # If the node is full, split the  node into two.
        if len(parent.keys) > self.maximum:
            self.insert_index(*parent.split())
        # Once a leaf node is split, it consists of a internal node and two leaf nodes.
        # These need to be re-inserted back into the tree.

    def delete(self, key, node: Node = None):
        if node is None:
            node = self.find(key)
        del node[key]

        if len(node.keys) < self.minimum:
            if node == self.root:
                if len(self.root.keys) == 0 and len(self.root.values) > 0:
                    self.root = self.root.values[0]
                    self.root.parent = None
                    self.depth -= 1
                return

            elif not node.borrow_key(self.minimum):
                node.fusion()
                self.delete(key, node.parent)

    def print_tree(self, node=None, file=None, _prefix="", _last=True):
        """Prints the keys at each level."""
        if node is None:
            node = self.root
            
        print(_prefix, "- " if _last else "|- ", node.keys, sep="", file=file)
        _prefix += "   " if _last else "|  "
        if type(node) is Node:
            # Recursively print the key of child nodes (if these exist).
            for i, child in enumerate(node.values):
                _last = (i == len(node.values) - 1)
                self.print_tree(child, file, _prefix, _last)

    def append_tree(self, node=None, file=None, _prefix="", _last=True):
        """Prints the keys at each level."""
        if node is None:
            node = self.root
            
        tree_structure.append(node.keys)
        if type(node) is Node:
            # Recursively print the key of child nodes (if these exist).
            for i, child in enumerate(node.values):
                _last = (i == len(node.values) - 1)
                self.append_tree(child, file, _prefix, _last)


    def leftmost_leaf(self) -> Leaf:
        node = self.root
        while type(node) is not Leaf:
            node = node.values[0]
        return node

    
    def inorder_leaf(self):
        start_time = time.time()
        """Perform in-order traversal and return keys (room numbers) from the leaf nodes only."""
        leaf = bplustree.leftmost_leaf()  # Start from the leftmost leaf
        result = []
        
        while leaf is not None:
            result.extend(leaf.keys)  # Collect all keys in the current leaf
            leaf = leaf.next  # Move to the next leaf in the linked list
        end_time = time.time()
        inorder_leaf_time = end_time - start_time
        return result

#----------------------------------------------------------------------------------------------------------------------------------------------------

def generate_room_number(num_walk_in=1, num_bus=1, num_ship=1, num_fleet=1): 
    start_time = time.time()
    global room_number
    room_number = []
    list_old_guest = bplustree.inorder_leaf()
    num_old_guest = len(list_old_guest)
    move_old_guest(list_old_guest)

    for o in range(num_old_guest):
        room_num = pow(2, o) * pow(3, 0) * pow(5, 0) * pow(7, 0)
        room_number.append((room_num, [0, 0, 0, 0, o]))

    for i in range(1, num_fleet + 1):
        for j in range(1, num_ship + 1):
            for k in range(1, num_bus + 1):
                for l in range(1, num_walk_in + 1):
                    room_num = pow(2, l) * pow(3, k) * pow(5, j) * pow(7, i)
                    room_number.append((room_num, [0, i, j, k, l]))

    
    end_time = time.time()
    execute_time = end_time - start_time

    execution_times["generate_room_number"] = execute_time
    print(f"generate_room_number - time used = {execute_time:.4f} seconds")
    return room_number

def receive_guests():
    global total_num_walk_in, total_num_bus, total_num_ship, total_num_fleet
    start_time = time.time()
    
    receive_guests = [x for x in input("Route of guest arrival : ").split('/')]
    
    for i in range(len(receive_guests)):
        route, amount = receive_guests[i].split(':')
        if route == 'walk_in':
            num_walk_in = int(amount)
            total_num_walk_in += num_walk_in
            list_room_number = generate_room_number(num_walk_in)
            add_room(list_room_number)
            
        elif route == 'bus':
            num_bus, num_walk_in = map(int, amount.split(','))
            total_num_bus += num_bus
            total_num_walk_in += num_walk_in
            list_room_number = generate_room_number(num_walk_in, num_bus)
            add_room(list_room_number)
        
        elif route == 'ship':
            num_ship, num_bus, num_walk_in = map(int, amount.split(','))
            total_num_ship += num_ship
            total_num_bus += num_bus
            total_num_walk_in += num_walk_in
            list_room_number = generate_room_number(num_walk_in, num_bus, num_ship)
            add_room(list_room_number)
        
        elif route == 'fleet':
            num_fleet, num_ship, num_bus, num_walk_in = map(int, amount.split(','))
            total_num_fleet += num_fleet
            total_num_ship += num_ship
            total_num_bus += num_bus
            total_num_walk_in += num_walk_in
            list_room_number = generate_room_number(num_walk_in, num_bus, num_ship, num_fleet)
            add_room(list_room_number)
                  
    end_time = time.time()
    execute_time = end_time - start_time
    execution_times["receive_guests"] = execute_time
    print(f"receive_guests - time used = {execute_time:.4f} seconds")


def add_room(list_room_number):
    start_time = time.time()

    for room_number,route_data in list_room_number:
            bplustree.insert(room_number,route_data)
            
    end_time = time.time()
    execute_time = end_time - start_time
    execution_times["add_room"] = execute_time
    print(f"add_room - time used = {execute_time:.4f} seconds")


def move_old_guest(list_old_guest):
    start_time = time.time()
    
    global manual_count
    manual_count = 1
    for guest in list_old_guest :
      bplustree.delete(guest)
      
    end_time = time.time()
    execute_time = end_time - start_time
    execution_times["move_old_guest"] = execute_time
    print(f"----------------Time usage of each functionc-------------------")
    print(f"move_old_guest - time used = {execute_time:.4f} seconds")

#-----------------------------------------------------------------------------------------------------------------------------------------------
# Function Group 2 - Manual Room Management
def add_room_manual():
    start_time = time.time()
    
    global manual_count
    room_number_add = input("Enter room number : ")
    if room_number_add == '0' or (not room_number_add.isnumeric()) :
        print("Room number must be countable number ")
        return
    room_number_add  =int(room_number_add)
    if search_room(room_number_add) :
        return
    else :
        bplustree.insert(room_number_add,[manual_count,0,0,0,0])
        manual_count += 1
        print(f"Room number {room_number_add} added successfully.")


    end_time = time.time()
    execute_time = end_time - start_time
    execution_times["add_room_manual"] = execute_time
    print(f"add_room_manual - time used = {execute_time:.4f} seconds")

def remove_room_manual():
    start_time = time.time()
    
    room_number_remove = int(input("Enter room number : "))
    if not search_room(room_number_remove) :
        print (f"Room {room_number_remove} does not exist in the hotel.")
        return
    else :
        bplustree.delete(room_number_remove)
        print(f"Room number {room_number_remove} removed successfully.")
        
    end_time = time.time()
    execute_time = end_time - start_time
    execution_times["remove_room_manual"] = execute_time
    print(f"remove_room_manual - time used = {execute_time:.4f} seconds")
#-------------------------------------------------------------------------------------------------------------------------------------------
# Function Group 3 - Room Operations and Display

def search_room(find_room = None) :
    start_time = time.time()
    
    p = 0
    if find_room == None :
        room_number = int(input("Seacrh Room Number: "))
    else :
        p = 1
        room_number = find_room
    leaf = bplustree.find(room_number) #Function that this Tree already give so use it why not only BigO (log N) :D
    if room_number in leaf.keys :
        if p == 0 :
            print (f"Room {room_number} exists in the hotel.")  #print for DEBUG you can delete if you want
            end_time = time.time()
            execute_time = end_time - start_time
            execution_times["search_room"] = execute_time
            print(f"----------------Time usage of each functionc-------------------")
            print(f"search_room - time used = {execute_time:.4f} seconds")
        return True #Return if room already in hotel
    else:
        if find_room == None :
            print (f"Room {room_number} does not exist in the hotel.")
            end_time = time.time()
            execute_time = end_time - start_time
            execution_times["search_room"] = execute_time
            print(f"----------------Time usage of each functionc-------------------")
            print(f"search_room - time used = {execute_time:.4f} seconds")
        return False #Return if room is not in hotel


def show_available_rooms():
    start_time = time.time()
    
    room = bplustree.inorder_leaf() #list that contain number of Room from leaf inorder that only get leaf
    if len(room) == 0:
        end_time = time.time()
        execute_time = end_time - start_time
        execution_times["show_available_rooms"] = execute_time
        print(f"show_available_rooms - time used = {execute_time:.4f} seconds")
        return 0
    
    end_time = time.time()
    show_available_rooms_time = end_time - start_time
    return int(room[-1] - len(room))
#----------------------------------------------------------------------------------------------------------------------------------------
# Function Group 4: Performance Monitoring and Reporting
def calculate_nested_list_memory(data):
    total_elements = 0

    def count_elements(node):
        nonlocal total_elements
        if isinstance(node, list):
            total_elements += len(node)
            for element in node:
                if isinstance(element, list):
                    count_elements(element)
    
    count_elements(data)

    # Suppose that each element (number) is approximately 8 bytes (for integers).
    element_size = 8
    memory_usage = total_elements * element_size
    
    return memory_usage, total_elements

def display_memory_usage(data):
    memory_usage, total_elements = calculate_nested_list_memory(data)
    print(f"Memory usage: {memory_usage} bytes for {total_elements} elements.")

def write_to_file(filename="hotel_report.txt"):
    global room_number, total_num_walk_in, total_num_bus, total_num_ship, total_num_fleet
    
    with open(filename, "w") as file:
        
        leaf = bplustree.leftmost_leaf()  # Start from the leftmost leaf
        room_in_hotel = []
        while leaf is not None:
            room_in_hotel.append(leaf)  # Collect all keys in the current leaf
            leaf = leaf.next  # Move to the next leaf in the linked list

        for room in room_in_hotel :
            for i in range(len(room.keys)):
                file.write(f'room_number : {room.keys[i]} , route : no_{room.values[i][0]}_{room.values[i][1]}_{room.values[i][2]}_{room.values[i][3]}_{room.values[i][4]}\n')
       

    print(f"Data written to {filename}")

def print_measure_time():  
    print("\nExecution times:")
    for func_name, exec_time in execution_times.items():
        print(f"{func_name} : {exec_time:.4f} seconds")
    
    
#------------------------------------------------------------------------------------------------------------------------------------------
def set_up_hotel():
    for i in range(1,6):
        bplustree.insert(i,[0,0,0,0,i])
    
def manage_command():
    command = input("Enter your command : ").upper()
#     fleet:5,4,7,10/bus:3,4
    if command == 'RG':      # receive guests
        receive_guests()
        return True
    elif command == 'C':     # cancle command
        return False
    elif command == "SR":    # search room
        search_room()
        return True
    elif command == "AR":    # availble room
        print(show_available_rooms())
        print(f"----------------Time usage of each functionc-------------------")
        execution_times["inorder_leaf"] = inorder_leaf_time
        print(f"inorder_leaf - time used = {inorder_leaf_time:.4f} seconds")
        execution_times["show_available_rooms"] = show_available_rooms_time
        print(f"show_available_rooms - time used = {show_available_rooms_time:.4f} seconds")
        return True
    elif command == "ADD" :   # add room manual
        add_room_manual()
        return True
    elif command == 'RM' :   # remove room manual
        remove_room_manual()
        return True
    elif command == 'SH' :   
        print(bplustree.inorder_leaf())
        print(f"----------------Time usage of each functionc-------------------")
        execution_times["inorder_leaf"] = inorder_leaf_time
        print(f"inorder_leaf - time used = {inorder_leaf_time:.4f} seconds")
        return True
    elif command == 'PT' :  
        bplustree.print_tree()
        return True
    elif command == 'DM' :    # Data Memmory Usage
        bplustree.append_tree()
        # print(tree_structure)
        display_memory_usage(tree_structure)
        # display_memory_usage(room_number)
        return True
    elif command == 'EX':     # Write export file
        write_to_file()
        return True
    elif command == 'HELP':
        print("ADD : add room manual\n")
        print("RM : remove room manual\n")
        print("RG : receive_guests (add and sort room number in B+tree)")
        print("\tfleet:{number of fleet},{number of ship},{number of bus},{number of walk in}\n\tship:{number of ship},{number of bus},{number of walk in}\n\tbus:{number of bus},{number of walk in}\n\twalk_in:{number of walk in}")
        print("\texample : fleet:5,4,7,10/bus:3,4 or walk_in:10\n")
        print("SR : search room\n")
        print("AR : show number of availble room\n")
        print("EX : write export file hotel_report.txt\n")
        print("DM : Display memory usage\n")

        print("Extra command\n")
        print("C : cancle command\n")
        print("SH : show occupied room\n")
        print("PT : print B+tree\n")
        return True
    else:
        return True

if __name__ == '__main__':
    bplustree = BPlusTree()
    set_up_hotel()
    recieve_command = True
    while recieve_command :
        recieve_command = manage_command()



    
    