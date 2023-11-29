import math
import tkinter as tk
import random
from tkinter.scrolledtext import ScrolledText

output_steps = []
output_log = []
steps_counter = 0
sequence_array = []


def append_step(sets, block_address, action, cache_hit, cache_miss):
    global output_steps
    i = 0
    j = 0
    text = ''
    for set_ in sets:
        text += "set " + str(i) + ": \n\n"
        i += 1
        for block in set_.blocks:
            text += "\tblock %d: %d" % (j, block.address_in_decimal)

            if block.address_in_decimal == block_address:
                text += '    <-----'

            j += 1

            text += '\n'
        text += '\n'
        j = 0

    text += 'memory block read: ' + str(block_address) + '\n'

    text += 'memory access count: ' + str(cache_hit + cache_miss) + '\n'

    if action == 'Hit':
        text += 'CACHE HIT! \n'
    else:
        text += 'CACHE MISS! \n'

    text += 'Cache hit counter: ' + str(cache_hit) + '\n'
    text += 'Cache miss counter: ' + str(cache_miss) + '\n'

    output_steps.append(text)

    log_text = ''

    i = 0

    sequence_array.append(str(block_address))

    stripped_list = map(str.strip, sequence_array)
    temp_sequence = ', '.join(stripped_list)

    log_text += 'Sequence: ' + temp_sequence + '\n\n'

    for set_ in sets:
        log_text += "set " + str(i) + ": \n\n"
        i += 1
        for block in set_.blocks:
            log_text += "\tblock %d: " % (j)

            for block_log in block.log:
                log_text += str(block_log) + ', '

            j += 1

            log_text += '\n'
        log_text += '\n'
        j = 0

    output_log.append(log_text)

class blocks:
    def __init__(self):
        self.valid = True
        self.tag = -1
        self.count = 0
        self.address_in_decimal = -1
        self.address = -1
        self.log = []


class sets:
    def __init__(self, SD_SetDegree):
        self.blocks = [blocks() for i in range(SD_SetDegree)]


class cache:
    def __init__(self, BS_BlockSize, CS_CacheSize, SD_SetDegree):

        self.BS_BlockSize = BS_BlockSize
        self.CS_CacheSize = CS_CacheSize
        self.SD_SetDegree = SD_SetDegree

        self.CBN_CacheBlockNumber = 16
        print("\nThere are %d Cache Blocks" % (self.CBN_CacheBlockNumber))
        self.SN_SetNumber = 4

        self.sets = [sets(SD_SetDegree) for i in range(self.SN_SetNumber)]
        print(str(self.SD_SetDegree) + "-way associative cache, with " + str(self.SN_SetNumber) + " sets.")

        self.hit_count = 0
        self.miss_count = 0

    def read_from_cache(self, address_in_decimal):
        global output_steps
        block_address = address_in_decimal
        set_number = int(address_in_decimal % self.SN_SetNumber)  # set
        tag = math.floor(address_in_decimal / self.SN_SetNumber)  # tag


        if self.IsEmpty(set_number):
            #print("Set %d is empty" % (set_number))
            #print("Cache MISS")
            self.miss_count += 1
            self.sets[set_number].blocks[0].valid = False
            self.sets[set_number].blocks[0].tag = tag
            self.sets[set_number].blocks[0].address_in_decimal = block_address
            self.add_count(set_number)

            #append to steps
            self.sets[set_number].blocks[0].log.append(block_address)
            append_step(self.sets, block_address, 'Miss', self.hit_count, self.miss_count)


        else:
            if not self.IsFull(set_number):
                #print("Set %d is NOT FULL" % (set_number))
                hit = False
                for block in self.sets[set_number].blocks:
                    if not block.valid and block.tag == tag:
                        # print("Cache HIT")
                        hit = True
                        self.hit_count += 1
                        self.add_count(set_number)
                        block.count = 1
                        block.address_in_decimal = block_address
                        # append to steps
                        block.log.append(block_address)
                        append_step(self.sets, block_address, 'Hit', self.hit_count, self.miss_count)
                        break

                if not hit:
                    for block in self.sets[set_number].blocks:
                        if block.valid:
                            # print("Cache MISS")
                            self.miss_count += 1
                            block.valid = False
                            block.tag = tag
                            block.address_in_decimal = block_address
                            self.add_count(set_number)
                            # append to steps
                            block.log.append(block_address)
                            append_step(self.sets, block_address, 'Miss', self.hit_count, self.miss_count)
                            break

            else:  # the set is full, replace the least recent used block, by MRU algorithm.
                # print("Set %d is FULL" % (set_number))
                self.MRU(set_number, tag, block_address)
                # append to steps

        # print("hit_count: %d, miss_count: %d" % (self.hit_count, self.miss_count))

        # for block in self.sets[set_number].blocks:
        # print("tag: %d" % block.tag)

    def MRU(self, set_number, tag, block_address):
        # print("the set is full")
        hit = False
        for block in self.sets[set_number].blocks:
            if block.tag == tag:  # cache hit, the wanted data is in cache, set count to 0
                # print("Cache HIT")
                hit = True
                self.hit_count += 1
                self.add_count(set_number)
                block.count = 1
                block.address_in_decimal = block_address
                block.log.append(block_address)
                append_step(self.sets, block_address, 'Hit', self.hit_count, self.miss_count)
                break
        if not hit:
            # print("Cache MISS")
            self.miss_count += 1
            max_count = 10  # the MRU block count，
            MRU_index = -1
            for i in range(self.SD_SetDegree):
                if self.sets[set_number].blocks[i].count < max_count:
                    max_count = self.sets[set_number].blocks[i].count
                    MRU_index = i

            self.sets[set_number].blocks[MRU_index].tag = tag
            self.sets[set_number].blocks[MRU_index].address_in_decimal = block_address
            self.add_count(set_number)
            self.sets[set_number].blocks[MRU_index].log.append(block_address)
            append_step(self.sets, block_address, 'Miss', self.hit_count, self.miss_count)
            self.sets[set_number].blocks[MRU_index].count = 1

    def add_count(self, set_number):
        for block in self.sets[set_number].blocks:
            if not block.valid: block.count += 1

    def IsEmpty(self, set_number):
        for block in self.sets[set_number].blocks:
            if block.valid == False:
                return False
        return True

    def IsFull(self, set_number):
        for block in self.sets[set_number].blocks:
            if block.valid == True:
                return False
        return True

    def print(self):
        i = 0
        j = 0
        for set_ in self.sets:
            print("set " + str(i) + ": ")
            i += 1
            for block in set_.blocks:
                print("\tblock %d: valid: %s, tag: %d, address: %d" % (j, block.valid, block.tag, block.address_in_decimal))
                j += 1
            j = 0

def parse(string_inp):
    address = []

    string_inp = string_inp.split(' ')

    for idx in range(int(string_inp[0])):
        address.append(idx)

    return address


#fills memory sequence with necessary test case
def selectionFill(selected, addresses):
    address_array = []



    range_of_address = int(addresses)
    print('range of address: ', range_of_address)

    if selected == 'Sequential':
        temp_address = range_of_address * 2
        for i in range(4):
            for idx in range(temp_address):
                address_array.append(idx)
    elif selected == 'Random':
        temp_address = range_of_address * 4
        for idx in range(temp_address):
            address_array.append(random.randint(0, temp_address -1))
    elif selected == 'Mid-repeat':
        temp_address = range_of_address * 2
        for i in range(4):
            for idx in range(range_of_address):
                if idx != range_of_address - 1:
                    address_array.append(idx)

            for idx in range(temp_address):
                if idx != 0:
                    address_array.append(idx)

    return address_array

def finalSnapshot():
    typeSelection = getSelected()
    cache_access_time = 1
    miss_penalty = 321 # 1 + 32(10)

    print('this is type: ', typeSelection)
    SD = [4]

    for SD_SetDegree in SD:  # 一 set cache block

        BS_BlockSize = 16
        CS_CacheSize = 1024

        test = cache(BS_BlockSize, CS_CacheSize, SD_SetDegree)

        f = input_text.get("1.0",'end-1c')
        address = selectionFill(typeSelection[0], f)
        print(address)

        for idx in range(len(address)):
            address_in_decimal = int(address[idx])
            # print("Address in decimal: %d" % (address_in_decimal))
            test.read_from_cache(address_in_decimal)
        # test.print()
        test.print()
        print("The number of request: %d, Hit_count: %d" % (len(address), test.hit_count))
        print("Miss rate: %f\n-" % (1.0 - (test.hit_count) / len(address)))

    # access time init
    hit_rate = (test.hit_count) / len(address)
    miss_rate = (test.miss_count) / len(address)
    ave_access_time = (hit_rate*cache_access_time) + (miss_rate*miss_penalty)
    total_access_time = (test.hit_count*32*1) + (test.miss_count*(miss_penalty))
    # testing
    print("Hit Rate: %f" % hit_rate)
    print("Miss Rate: %f" % miss_rate)
    print("Ave Access Time: %f" % ave_access_time)
    # concat
    access_time = output_steps[-1] + 'Hit Rate: ' + str(hit_rate) + '\n' + 'Miss Rate: ' + str(miss_rate) + '\n' + 'Average Access Time: ' + str(ave_access_time) + '\n' + 'Total Access Time: ' + str(total_access_time) + '\n'

    instructions_text.config(state=tk.NORMAL)
    instructions_text.delete("1.0", "end")
    instructions_text.insert(tk.INSERT, access_time)
    instructions_text.config(state=tk.DISABLED)

    text_log.config(state=tk.NORMAL)
    text_log.delete("1.0", "end")
    text_log.insert(tk.INSERT, output_log[-1])
    text_log.config(state=tk.DISABLED)

    reset_btn['state'] = tk.NORMAL
    compute_btn['state'] = tk.DISABLED
    steps_btn['state'] = tk.NORMAL

def steps_snapshot():
    global steps_counter


    if steps_counter < len(output_steps):
        instructions_text.config(state=tk.NORMAL)
        instructions_text.delete("1.0", "end")
        instructions_text.insert(tk.INSERT, output_steps[steps_counter])
        instructions_text.config(state=tk.DISABLED)

        text_log.config(state=tk.NORMAL)
        text_log.delete("1.0", "end")
        text_log.insert(tk.INSERT, output_log[steps_counter])
        text_log.config(state=tk.DISABLED)
    steps_counter +=1

    if steps_counter == len(output_steps):
        steps_btn['state'] = tk.DISABLED


def reset():
    global  output_steps, steps_counter, output_log, sequence_array
    steps_counter = 0
    output_steps = []
    output_log = []
    reset_btn['state'] = tk.DISABLED
    compute_btn['state'] = tk.NORMAL
    steps_btn['state'] = tk.DISABLED
    sequence_array = []

    temp_text = "set 0:\n\n" \
    "\tblock 0: 0\n" \
    "\tblock 1: 0\n"\
    "\tblock 2: 0\n"\
    "\tblock 3: 0\n\n"\
    "set 1:\n\n"\
    "\tblock 0: 0\n"\
    "\tblock 1: 0\n"\
    "\tblock 2: 0\n"\
    "\tblock 3: 0\n\n"\
    "set 2:\n\n"\
    "\tblock 0: 0\n"\
    "\tblock 1: 0\n"\
    "\tblock 2: 0\n"\
    "\tblock 3: 0\n\n"\
    "set 3:\n\n"\
    "\tblock 0: 0\n"\
    "\tblock 1: 0\n"\
    "\tblock 2: 0\n"\
    "\tblock 3: 0\n\n"\

    instructions_text.config(state=tk.NORMAL)
    instructions_text.delete("1.0", "end")
    instructions_text.insert(tk.INSERT, temp_text)
    instructions_text.config(state=tk.DISABLED)


    temp_text = "set 0:\n\n"\
    "\tblock 0: \n"\
    "\tblock 1: \n"\
    "\tblock 2: \n"\
    "\tblock 3: \n\n"\
    "set 1:\n\n"\
    "\tblock 0: \n"\
    "\tblock 1: \n"\
    "\tblock 2: \n"\
    "\tblock 3: \n\n"\
    "set 2:\n\n"\
    "\tblock 0: \n"\
    "\tblock 1: \n"\
    "\tblock 2: \n"\
    "\tblock 3: \n\n"\
    "set 3:\n\n"\
    "\tblock 0: \n"\
    "\tblock 1: \n"\
    "\tblock 2: \n"\
    "\tblock 3: \n\n"\

    text_log.config(state=tk.NORMAL)
    text_log.delete("1.0", "end")
    text_log.insert(tk.INSERT, temp_text)
    text_log.config(state=tk.DISABLED)


def getSelected():
    currVar = listbox.curselection()

    return [items[item] for item in currVar]

if __name__ == "__main__":

    window = tk.Tk()
    window.geometry("1800x1100")
    window.overrideredirect(True)
    window.overrideredirect(False)
    window.state('zoomed')

    window.title("4-Way BSA with MRU")

    listbox = tk.Listbox(window, exportselection=False)

    sample_input = "16"

    listbox_label = tk.Label(text="Type:", font=("Courier 13"))
    listbox_label.pack(anchor='nw')

    listbox.pack(anchor='nw')


    items = ['Sequential', 'Random', 'Mid-repeat']

    for item in items:
        listbox.insert(tk.END, item)

    listbox.config()


    input_text_label = tk.Label(text="Input", font=("Courier 13"))
    input_text = tk.Text(window, font=("Courier 13"), height=3, width=30)
    input_text.insert(tk.END, sample_input)
    input_text_label.pack(padx=30,anchor='n', side='left')
    input_text.pack(expand=False,padx=30, anchor='n', side='left')



    instructions_text = ScrolledText(window, width=50,  height=30)

    instructions_text.pack(side=tk.LEFT)


    text = "set 0:\n\n" \
    "\tblock 0: 0\n" \
    "\tblock 1: 0\n"\
    "\tblock 2: 0\n"\
    "\tblock 3: 0\n\n"\
    "set 1:\n\n"\
    "\tblock 0: 0\n"\
    "\tblock 1: 0\n"\
    "\tblock 2: 0\n"\
    "\tblock 3: 0\n\n"\
    "set 2:\n\n"\
    "\tblock 0: 0\n"\
    "\tblock 1: 0\n"\
    "\tblock 2: 0\n"\
    "\tblock 3: 0\n\n"\
    "set 3:\n\n"\
    "\tblock 0: 0\n"\
    "\tblock 1: 0\n"\
    "\tblock 2: 0\n"\
    "\tblock 3: 0\n\n"\

    instructions_text.insert(tk.INSERT, text)

    instructions_text.config(state = tk.DISABLED)

    text_log_label = tk.Label(text="Text Log:", font=("Courier 13"))
    text_log_label.pack(padx=(30,0), anchor = "w", side = 'left')
    text_log = ScrolledText(window, width=50,  height=30)
    text_log.pack(side = 'left')

    text = "set 0:\n\n"\
    "\tblock 0: \n"\
    "\tblock 1: \n"\
    "\tblock 2: \n"\
    "\tblock 3: \n\n"\
    "set 1:\n\n"\
    "\tblock 0: \n"\
    "\tblock 1: \n"\
    "\tblock 2: \n"\
    "\tblock 3: \n\n"\
    "set 2:\n\n"\
    "\tblock 0: \n"\
    "\tblock 1: \n"\
    "\tblock 2: \n"\
    "\tblock 3: \n\n"\
    "set 3:\n\n"\
    "\tblock 0: \n"\
    "\tblock 1: \n"\
    "\tblock 2: \n"\
    "\tblock 3: \n\n"\

    text_log.insert(tk.INSERT, text)

    text_log.config(state = tk.DISABLED)


    compute_btn = tk.Button(window, text="Final Snapshot",width=30, command=finalSnapshot)
    reset_btn = tk.Button(window, text="Reset", width=30, state=tk.DISABLED, command=reset)
    reset_btn.pack(anchor='s')
    steps_btn = tk.Button(window, text="Next", width=30, state=tk.DISABLED, command=steps_snapshot)

    steps_btn.pack(anchor='s')
    compute_btn.pack(anchor='s')

    window.mainloop()
