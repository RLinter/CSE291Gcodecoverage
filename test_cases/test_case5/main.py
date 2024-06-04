class LinkedList(object):

    def __init__(self, items=None):
        """Initialize this LinkedList and append items if specified"""
        self.head = None
        self.tail = None
        
        # append items to linked list
        if items is not None:
            for item in items:
                self.append(item)

    def append(self, item):
        """Append an item to the LinkedList"""

        # create a new node
        new_node = Node(item)
        
        # if the list is empty, set self.head to new node
        if self.head is None:
            self.head = new_node
        else:
            # otherwise insert new node after tail
            self.tail.next = new_node
        
        # set tail to new node
        self.tail = new_node
        
    def items(self):
        """Return a list of items in the LinkedList"""
        
        # create empty list
        items = []
        
        # start from the head of the linked list
        cur_node = self.head  
        
        # loop until the end
        while cur_node is not None:  

            # append item to items
            items.append(cur_node.data)
            
            # move to next node
            cur_node = cur_node.next 
        
        # return items
        return items

    def find_by_key(self, key):
        """Return data found by key in LinkedList or None if key is not found"""

        # start from the head of the linked list
        cur_node = self.head  
        
        # loop until the end
        while cur_node is not None:  

            # if we find the key, return the data
            if cur_node.data[0] == key:
                return cur_node.data[1] 
            
            # move to next node
            cur_node = cur_node.next 
            
        # if item was not found, return None
        return None

    def delete_by_key(self, key):
        """Return True if item is successfully deleted from LinkedList by key,
        otherwise return False"""
        
        # start from the head of the linked list
        cur_node = self.head  
        
        # keep track of previous node no we can update its next
        # property when we delete a node
        prev_node = None
        
        # loop until we find and delete the item or the end of the linked list
        while cur_node is not None:
            
            # if we find the key, delete the node and return True
            if cur_node.data[0] == key:
                
                # delete item from linked list
                if cur_node is self.head:
                    self.head = cur_node.next
                    cur_node.next = None 
                elif cur_node is self.tail:
                    prev_node.next = None
                    self.tail = prev_node
                else:
                    prev_node.next = cur_node.next
                    cur_node.next = None
                
                # return True if item was deleted successfully
                return True

            # move to next node
            prev_node = cur_node
            cur_node = cur_node.next
            
        # if the item was not found, return False
        return False
    
    def reverse(self):
        """Reverse the order of the LinkedList"""
        
        # start from the head of the linked list
        cur_node = self.head  
        
        # keep track of previous node
        prev_node = None
        
        # loop until the end
        while cur_node is not None:  
            
            # keep track of next node
            next_node = cur_node.next
            
            # reverse the current node
            cur_node.next = prev_node
            
            # move to next node
            prev_node = cur_node
            cur_node = next_node
        
        # set tail to head
        self.tail = self.head
        
        # set head to prev_node
        self.head = prev_node