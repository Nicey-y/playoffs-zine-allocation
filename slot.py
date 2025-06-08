class Slot:
    name = ""
    max_allocations = 1 # default at 1
    min_allocations = 1 # default at 1, 2 for writer
    curr_alloc_count = 0 # current number of allocations

    preferences = None # column from df
    people = None # People object who have been allocated this section

    # Constructor
    def __init__(self, name, max_alloc, min_alloc):
        self.name = name
        self.max_allocations = max_alloc
        self.min_allocations = min_alloc

    
    # Initialisation - Add to a slot's preference (made by Person)
    def add_to_pref(self, rank):
        if self.preferences is None:
            self.preferences = []
        self.preferences.append(rank)

    def get_name(self):
        return self.name

    # Write preference (column) in csv format
    def to_string(self):
        output = self.name
        for pref in self.preferences:
            output = output + ',' + str(pref)
        
        return output

    # Get the list of preference
    def get_pref(self):
        return self.preferences
    
    # Allocation - record people who is allocated this slot
    def add_to_people(self, person):
        if self.people is None:
            self.people = [person]
        else:
            self.people.append(person)
        
        self.curr_alloc_count = self.curr_alloc_count + 1
    
    # return a bool
    def is_available(self):
        return self.curr_alloc_count < self.max_allocations
    
    def is_unallocated(self):
        return self.curr_alloc_count == 0
    
    # identify (through index) the lastest person to rank this slot
    def get_latest_rank_indx(self):
        indx = len(self.preferences) - 1
        for rank in self.preferences[::-1]:
            if (rank != 0):
                return indx
            else:
                indx -= 1
    
    # deallocate from a Person object
    def deallocate(self, person):
        out_person_name = person.get_name()
        for i in range(len(self.people)):
            person_name = self.people[i].get_name()
            if person_name == out_person_name:
                self.people.pop(i)
                self.curr_alloc_count -= 1
                break
    
    def satisfied_minimum_allocation(self):
        return self.curr_alloc_count >= self.min_allocations
    
    # Write people in csv format
    def get_people(self):
        output = self.name
        if self.people is not None:
            for person in self.people:
                output = output + ',' + person.get_name()
        
        return output