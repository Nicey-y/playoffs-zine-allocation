class Person:
    name = ""
    max_piece_count = 0 # how many pieces they can do at maximum
    curr_piece_count = 0 # current number of allocations
    oos = 0 # flag - if they are willing to do section outside of their preference

    preferences = None # row from df
    slots = None # Slot object - list of sections they have been allocated, len == curr_piece_count

    # Constructor
    def __init__(self, name, oos, max_piece_count):
        self.name = name
        self.max_piece_count = max_piece_count
        self.oos = oos
    
    # Initialisation - Add to a person's preference
    def add_to_pref(self, rank):
        if self.preferences is None: 
            self.preferences = []
        self.preferences.append(rank)

    # Write allocation in csv format
    def get_allocation(self):
        output = self.name
        if self.slots is not None:
            for slot in self.slots:
                output = output + ',' + slot.get_name()
        
        return output
    
    # Write preference (row) in csv format
    def to_string(self):
        output = self.name
        for pref in self.preferences:
            output = output + ',' + str(pref)
        
        return output
    
    # Allocate - Add to allocation/slot of a person
    def add_to_slots(self, pref):
        if self.slots is None:
            self.slots = [pref]
        else:
            self.slots.append(pref)
        
        self.curr_piece_count = self.curr_piece_count + 1
    
    # Return 1 if a person is willing to do a piece that is outside the scope of their preference
    def get_oos(self):
        return self.oos
    
    def get_curr_piece_count(self):
        return self.curr_piece_count
    
    def get_name(self):
        return self.name
    
    def get_preferences(self):
        return self.preferences
    
    # return a bool
    def is_available(self):
        return self.curr_piece_count < self.max_piece_count

    def is_unallocated(self):
        return self.curr_piece_count == 0
    
    # return a bool if the Slot is in a person's preference list
    # a slot is identified by its index (this is probably a very bad way to do this im so sorry)
    def prefers(self, slot_indx):
        return self.preferences[slot_indx] > 0
    
    # deallocate from a Slot object
    def deallocate(self, out_slot):
        out_slot_name = out_slot.get_name()
        for i in range(len(self.slots)):
            slot_name = self.slots[i].get_name()
            if slot_name == out_slot_name:
                self.slots.pop(i)
                self.curr_piece_count -= 1
                break

    def get_last_allocation(self):
        if self.slots is None:
            return None
        return self.slots[-1]
    
    # check if this Slot object is in a person's allocation
    def has_been_allocated(self, slot1):
        slot1_name = slot1.get_name()

        if self.slots is None:
            return False
        
        for i in range(len(self.slots)):
            slot_name = self.slots[i].get_name()
            if slot_name == slot1_name:
                return True
        return False