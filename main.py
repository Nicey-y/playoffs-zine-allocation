from person import Person
from slot import Slot
import pandas as pd

############################### HELPER FUNCTIONS ##############################

def log(content, initial_log=False):
    # initial log is the first log to the file -> mode = 'w' to write
    if initial_log:
        mode = 'w'
    else:
        mode = 'a'

    with open("log.txt", mode) as file:
        file.write(content)
        if not initial_log:
            file.write('\n')

def allocate(person, slot):
    if (person.is_available() and slot.is_available()):
        log("Allocate " + person.get_name() + " to " + slot.get_name() + '\n')
        person.add_to_slots(slot)
        slot.add_to_people(person)
    else:
        log("Unable to allocate " + person.get_name() + " to " + slot.get_name() + '\n')

def deallocate(person, slot):
    log("! Deallocate "+ person.get_name() + " from " + slot.get_name() + '\n')
    person.deallocate(slot)
    slot.deallocate(person)

def find_best_fit_person_indx(slot_pref_ls, slot_indx, col_count, participants, case_unallocated=False, exclude_indx=-1):
    highest_rank = col_count # col_count > lowest rank, always
    highest_rank_indx = -1
    for j in range(len(slot_pref_ls)):

        if (j == exclude_indx): continue

        if case_unallocated:
            person_flag = participants[j].is_unallocated()
        else:
            person_flag = participants[j].is_available()

        if slot_pref_ls[j] < highest_rank and person_flag and participants[j].prefers(slot_indx):
            highest_rank = slot_pref_ls[j]
            highest_rank_indx = j # im sorry for identifying slot using index :sob:

    return highest_rank_indx

# Step 2: loop though unallocated slots and allocate them to the first available person
# based on priority: 
# 1. unallocated people - the FIRST person who ranks it the HIGHEST
# 2. available people - the FIRST person who ranks it the HIGHEST
# 3. people who are willing to do sections outside of their preference
def step2_loop(participants, slots, case_unallocated=True):
    allocated = False

    for i in range(len(slots)):
        sub_allocation = False
        slot = slots[i]
        
        # filter what type of slots to check
        if (case_unallocated):
            flag = slot.is_unallocated()
        else:
            flag = slot.is_available()

        if flag:
            log("Step2: Allocating " + slot.get_name())
            # 1. look for unallocated people first
            best_unallocated_person_indx = find_best_fit_person_indx(slot.get_pref(), i, col_count, participants, case_unallocated=True)
            log("  best fit indx: " + str(best_unallocated_person_indx))
            if (best_unallocated_person_indx != -1):
                log("Step2.1")
                allocate(participants[best_unallocated_person_indx], slot)
                sub_allocation = True
            
            # check if we had found an allocation
            if (sub_allocation):
                log("found at 2.1")
                continue # job done

            # 2. look for the FIRST person who ranks it the HIGHEST
            for k in range(4): # put a limit on how many times we are looping to ensure no infinite loop
                slot_pref_ls = slot.get_pref()

                highest_rank_indx = find_best_fit_person_indx(slot_pref_ls, i, col_count, participants, case_unallocated=False)
                log("  highest rank indx: " + str(highest_rank_indx))
                if highest_rank_indx != -1:
                    # found
                    person = participants[highest_rank_indx]
                    log("Step2.2")
                    allocate(person, slot)
                    sub_allocation = True
                    break
            
            # check if we had found an allocation
            if (sub_allocation):
                continue # job done
            
            # 3. pivot to people who are willing to do sections outside of their preference
            # first loop uses .is_unallocated() to prioritise unallocated people
            for person in participants:
                log("considering " + person.get_name())
                if (person.get_oos() == 1) and person.is_unallocated():
                    log("Step2.3 - unallocated person")
                    allocate(person, slot)
                    sub_allocation = True
                    break

            # check if we had found an allocation
            if (sub_allocation):
                continue # job done

            # second loop for everyone else
            for person in participants:
                if (person.get_oos() == 1) and person.is_available():
                    log("Step2.3 - available person")
                    allocate(person, slot)
                    sub_allocation = True
                    break
        # if any allocation has been made during the process
        allocated = allocated or sub_allocation
            
    return allocated

# Step 4: loop through all participants
# for unallocated people, give them their highest preference if available
def step4_loop(participants, slots, min_alloc=True):
    for person in participants:
        if person.get_curr_piece_count() == 0:
            log("found someone unallocated")
            # unallocated -> find their 1st preference
            person_pref_ls = person.get_preferences()

            highest_rank = col_count # col_count > lowest rank, always
            highest_rank_indx = -1
            for i in range(len(person_pref_ls)):
                
                if (min_alloc): flag = not slots[i].satisfied_minimum_allocation()
                else: flag = slots[i].is_available()

                if person_pref_ls[i] != 0 and person_pref_ls[i] < highest_rank and flag:
                    highest_rank = person_pref_ls[i]
                    highest_rank_indx = i
            
            if (highest_rank_indx != -1):
                # initialisation
                slot = slots[highest_rank_indx]
                # allocate
                allocate(person, slot)

def to_csv_artist(participants):
    with open("artist_allocation.csv", 'w') as file:
        for person in participants:
            file.write(person.get_allocation() + '\n')

def to_csv_writer(participants):
    with open("writer_allocation.csv", 'w') as file:
        for person in participants:
            file.write(person.get_allocation() + '\n')

def slot_to_csv_artist(slots):
    with open("slots_art.csv", "w") as file:
        for slot in slots:
            file.write(slot.get_people() + '\n')

def slot_to_csv_writer(slots):
    with open("slots_write.csv", "w") as file:
        for slot in slots:
            file.write(slot.get_people() + '\n')

########################### END OF HELPER FUNCTIONS ###########################

# Read csv file
# file_path = "tests/writer-tests/test7.csv" # for testing
file_path = "writer.csv" # change to whatever your file name is
df = pd.read_csv(file_path)
log("", True)

row_count = df.shape[0]
col_count = df.shape[1]

# ---------------Initialisation---------------
# artist mode is 0, writer mode is 1
exec_mode = 1
# need [1, 2] art pieces
# need [2, 4] writing pieces
if (exec_mode == 0):
    # artist mode
    min_alloc = 1
    max_alloc = 2
elif (exec_mode == 1):    
    # writer mode
    min_alloc = 2
    max_alloc = 4

# read data
# columns: Participant, OOS,        Max Piece, Slot1, Slot2, Slot3, Slot4, Slot5, Slot6,...
#          iloc[0, 0]   iloc[0, 1]  iloc[0, 2]

# Read participant data
participants = [] # list of Person object
for i in range(row_count):
    person = Person(df.iloc[i, 0], df.iloc[i, 1], df.iloc[i, 2])

    for j in range(3, col_count): # starts at 3 to skip over first 3 columns
        person.add_to_pref(df.iloc[i, j])

    participants.append(person)

# Read section data
slots = [] # list of Slot object
for i in range(3, col_count):
    slot = Slot(df.columns[i], max_alloc, min_alloc)

    slot_col_sr = df.iloc[:, i] # all rows of column i
    for rank in slot_col_sr:
        slot.add_to_pref(rank)
    
    slots.append(slot)

# ---------------Allocation---------------

# Step 1: loop through all slots and allocate the first 1's in the column
for slot in slots:
    # log("Step1: Allocating " + slot.get_name())
    slot_pref = slot.get_pref()

    for i in range(len(slot_pref)):
        if slot_pref[i] == 1:
            # log("1st pref at index " + str(i))
            # initialisation
            person = participants[i]

            # allocation
            allocate(person, slot)
            
            break # job done

# Step 2: loop though unallocated slots and allocate them to the first available person
# based on priority: 
# 1. unallocated people 
# 2. the FIRST person who ranks it the HIGHEST
# 3. people who are willing to do sections outside of their preference

# prioritising unallocated slots
log("go through unallocated slots")
step2_loop(participants, slots)

# Step 3: If there is still unallocated slots -> switching is needed
switching_occurred = True
while(switching_occurred):
    unit_switching_occurred = False
    for slot in slots:
        if slot.is_unallocated():
            log("found unallocated slot!!!!")
            slot_pref_ls = slot.get_pref()
            latest_person_indx = slot.get_latest_rank_indx()
            person = participants[latest_person_indx] # person to allocate to

            # now we have to reallocate the slot that was held by this person previously
            # deallocate
            old_slot = person.get_last_allocation()
            if old_slot is not None:
                deallocate(person, old_slot)

            # new allocation
            allocate(person, slot)

            unit_switching_occurred = True
    switching_occurred = unit_switching_occurred

# Step 4: loop through all participants
# for unallocated people, give them their highest preference if available
step4_loop(participants, slots) # prioritise slots that haven't met minimum allocations

##### WRITER MODE ONLY - ROUND 2 ALLOCATION #####
if (exec_mode == 1):
    log("ROUND 2 ALLOCATION")
    for j in range(len(slots)):
        slot = slots[j]
        if not slot.satisfied_minimum_allocation():
            log("Allocating slot: " + slot.get_name())
            slot_pref_ls = slot.get_pref()

            highest_rank = col_count
            highest_rank_indx = -1
            
            for i in range(len(slot_pref_ls)):
                if slot_pref_ls[i] < highest_rank:
                    person = participants[i]
                    if person.is_available() and not person.has_been_allocated(slot) and person.prefers(j):
                        highest_rank = slot_pref_ls[i]
                        highest_rank_indx = i
                
            if (highest_rank_indx == -1):
                # forced to duplicate a slot to a person
                for i in range(len(slot_pref_ls)):
                    if slot_pref_ls[i] < highest_rank:
                        person = participants[i]
                        if person.is_available() and person.prefers(j):
                            highest_rank = slot_pref_ls[i]
                            highest_rank_indx = i
            
            if (highest_rank_indx == -1):
                # look into people who are willing to do sections outside of their preference
                for i in range(len(participants)):
                    person = participants[i]
                    if (person.get_oos() == 1) and person.is_unallocated(): # prioritise unallocated ppl
                        highest_rank_indx = i
                        break
                
                if (highest_rank_indx == -1):
                    # again, now for any1 available
                    for i in range(len(participants)):
                        person = participants[i]
                        if (person.get_oos() == 1) and person.is_available():
                            highest_rank_indx = i
                            break
            
            # allocate
            if (highest_rank_indx == -1):
                log("Unable to allocate 2nd round")
            else:
                allocate(participants[highest_rank_indx], slot)

step4_loop(participants, slots, False)

################################## RESULTS ####################################

for person in participants:
    log(person.get_allocation()) # print result to log.txt

# Get artist allocation result as .csv file, uncomment to use
# to_csv_artist(participants)
# slot_to_csv_artist(slots)

# Get writer allocation result as .csv file, uncomment to use
# to_csv_writer(participants)
# slot_to_csv_writer(slots)