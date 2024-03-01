#Alex Shapovalov
#CS 5220
#Programming Assignment #2, Cache Graduate

import random

CACHE_SIZE = 1024
CACHE_BLOCK_SIZE = 64
ADDRESS_LENGTH = 16
ASSOCIATIVITY = 4
WRITETYPE = "write-back"
#WRITETYPE = "write-through"

#statistics declarations (it is nonsensical that i had to put global here but the program broke if i didn't, python plz fix)
global reads
reads = 0
global read_misses
read_misses = 0
global read_hits
read_hits = 0
global writes
writes = 0
global write_misses
write_misses = 0
global write_hits
write_hits = 0

def logb2(val):
    i=0
    while val > 0:
        i=i+1
        val = val >> 1
    return i-1

class Block:
    def __init__(self, size):
        self.data = bytearray(size)
        self.tag = -1
        self.address = -1
        self.dirty = False
        self.valid = False

class Cache:
    def __init__(self, address, cache, block, associativity, write):
        self.address = address #address size
        self.cache = cache #cache size
        self.block = block #block size
        self.associativity = associativity #number of blocks per set
        self.write = write #write type

        #this caused issues because the way python works with mutability, changing one parameter in any Block() caused all of them to change
        #self.block = [Block(block)] * (cache // block) #create an array of blocks with size block

        numSets = (cache // associativity) // block #figure out how many sets we need
        self.set = {} #sets defined as a dictionary, didn't make it its own class because it's simply a grouping of blocks, not its own thing
        z = 0
        for x in range(0, numSets): #creates sets based on block size and associativity, self.sets is a dictionary of 1 or more blocks
            self.set["set " + str(x)] = []
            for y in range(min(numSets, associativity)):
                if z < (CACHE_SIZE // CACHE_BLOCK_SIZE):
                    self.set["set " + str(x)].append(Block(block))
                    z += 1

        self.block_offset = logb2(block)
        self.index = logb2(numSets)
        self.tag = self.address - self.block_offset - self.index
        self.block_address = self.address - self.tag #address + tag

#global cache and memory
cache = Cache(ADDRESS_LENGTH, CACHE_SIZE, CACHE_BLOCK_SIZE, ASSOCIATIVITY, WRITETYPE)
memory = bytearray(2 ** ADDRESS_LENGTH)
#prefill memory
for i in range(0, len(memory), 4):
    memory[i:i+4] = [i & 255, (i >> 8) & 255, (i >> 16) & 255, (i >> 24) & 255]

def readWord(address):
    global read_misses
    global read_hits

    #from addr, compute the tag t, index i and block offset b (use block_offset, block_address, tag, index etc.)
    tag = address >> cache.block_address
    index = ((address >> cache.block_offset) & (1 << cache.index) - 1)
    block_offset = address & ((1 << cache.block_offset) - 1)
    block_index = 0
    #compute the range of the desired block in memory: start to start+blocksize-1
    binary = ((('{0:0' + str(ADDRESS_LENGTH) + 'b}').format(address))[:-cache.block_offset]) + ("0" * cache.block_offset)
    start = int(binary, 2)
    end = start + (CACHE_BLOCK_SIZE - 1)

    #read from next available empty block in set
    if cache.associativity > 1 and cache.set["set " + str(index)][block_index].valid:
        for x in range(cache.associativity):
            if cache.set["set " + str(index)][x].valid:
                block_index += 1

    change = False
    #if block_index = associativity then we are full and must evict from tag_queue, set block_index to cache.associativity - 1
    if block_index == cache.associativity:
        block_index = cache.associativity - 1
        change = True

    #do we have a read hit?
    hit = False
    hit_index = 0
    #check the current set to see if we have a read hit
    for x in range(cache.associativity):
        if cache.set["set " + str(index)][x].valid and cache.set["set " + str(index)][x].tag == tag:
            hit = True
            hit_index = x

    #look at the information in the cache for set i
    if hit == True: #cache hit
        #tag queue alteration on read hit
        if change == True:
            temp = cache.set["set " + str(index)][cache.associativity - 1]
            cache.set["set " + str(index)][cache.associativity - 1] = cache.set["set " + str(index)][hit_index]
            for x in range(hit_index, cache.associativity - 1):
                if x == cache.associativity - 2:
                    cache.set["set " + str(index)][x] = temp
                else:
                    cache.set["set " + str(index)][x] = cache.set["set " + str(index)][x + 1]

        word = 0

        #set address for write-back cache
        cache.set["set " + str(index)][block_index].address = address

        if cache.associativity > 1:
            #screw tag queues, this works great too
            print("[ ", end = "")
            for x in range(cache.associativity):
                print(cache.set["set " + str(index)][0 + x].tag, end=", ")
            print(" ]")

        #keep track of hits
        read_hits += 1
        print("read hit  [address=" + str(address) + " tag=" + str(tag) + " index=" + str(index) + " block_offset=" + str(block_offset) + " block_index=" + str(block_index) + " : word=" + str(word) + " (" + str(start) + " - " + str(end) + ")]")
        print(('{0:0' + str(ADDRESS_LENGTH) + 'b}').format(address))
        print("")
        return word
    else: #cache miss
        #evicting on a miss
        if change == True:
            for x in range(cache.associativity):
                if x == cache.associativity - 1:
                    cache.set["set " + str(index)][x] = Block(CACHE_BLOCK_SIZE)
                else:
                    cache.set["set " + str(index)][x] = cache.set["set " + str(index)][x + 1]

        #set the valid bit for set i to true
        cache.set["set " + str(index)][block_index].valid = True

        if cache.write == "write-back":
            cache.set["set " + str(index)][block_index].dirty = True

        #set the tag set i to t
        cache.set["set " + str(index)][block_index].tag = tag

        #return the word at positions b, b+1, b+2, b+3 from the block in set i
        word = 0

        #set address for write-back cache
        cache.set["set " + str(index)][block_index].address = address

        if cache.associativity > 1:
            #screw tag queues, this works great too
            print("[ ", end = "")
            for x in range(cache.associativity):
                print(cache.set["set " + str(index)][0 + x].tag, end=", ")
            print("\b", end="")
            print(" ]")

        #keep track of misses
        read_misses += 1
        if change == True:
            print("read miss + replace [address=" + str(address) + " tag=" + str(tag) + " index=" + str(index) + " block_offset=" + str(block_offset) + " block_index=" + str(block_index) + " : word=" + str(word) + " (" + str(start) + " - " + str(end) + ")]")
            print("evict tag " + str(cache.set["set " + str(index)][0].tag) + " in block_index 0")
        else:
            print("read miss [address=" + str(address) + " tag=" + str(tag) + " index=" + str(index) + " block_offset=" + str(block_offset) + " block_index=" + str(block_index) + " : word=" + str(word) + " (" + str(start) + " - " + str(end) + ")]")
        print(('{0:0' + str(ADDRESS_LENGTH) + 'b}').format(address))
        print("")
        return word

def writeWord(address, write_word):
    global write_misses
    global write_hits

    #from addr, compute the tag t, index i and block offset b (use cache.block_offset, tag, index etc.)
    tag = address >> cache.block_address
    index = (address >> cache.block_offset) & cache.index
    block_offset = address & ((1 << cache.block_offset) - 1)
    block_index = 0
    #compute the range of the desired block in memory: start to start+blocksize-1
    binary = ((('{0:0' + str(ADDRESS_LENGTH) + 'b}').format(address))[:-cache.block_offset]) + ("0" * cache.block_offset)
    start = int(binary, 2)
    end = start + (CACHE_BLOCK_SIZE - 1)

    #read from next available empty block in set
    if cache.associativity > 1 and cache.set["set " + str(index)][block_index].valid:
        for x in range(cache.associativity):
            if cache.set["set " + str(index)][x].valid:
                block_index += 1

    change = False
    # if block_index = associativity then we are full and must evict from tag_queue, set block_index to cache.associativity - 1
    if block_index == cache.associativity:
        block_index = cache.associativity - 1
        change = True

    # do we have a write hit?
    hit = False
    hit_index = 0
    # check the current set to see if we have a write hit
    for x in range(cache.associativity):
        if cache.set["set " + str(index)][x].valid and cache.set["set " + str(index)][x].tag == tag:
            hit = True
            hit_index = x

    if hit == True: #cache hit
        # tag queue alteration on write hit
        if change == True:
            temp = cache.set["set " + str(index)][cache.associativity - 1]
            cache.set["set " + str(index)][cache.associativity - 1] = cache.set["set " + str(index)][hit_index]
            for x in range(hit_index, cache.associativity - 1):
                if x == cache.associativity - 2:
                    cache.set["set " + str(index)][x] = temp
                else:
                    cache.set["set " + str(index)][x] = cache.set["set " + str(index)][x + 1]

        word = 0

        #write to memory
        memory[address:address + 4] = [write_word & 255, (write_word >> 8) & 255, (write_word >> 16) & 255, (write_word >> 24) & 255]

        #set address for write-back cache
        cache.set["set " + str(index)][block_index].address = address

        if cache.associativity > 1:
            # screw tag queues, this works great too
            print("[ ", end="")
            for x in range(cache.associativity):
                print(cache.set["set " + str(index)][0 + x].tag, end=", ")
            print(" ]")

        #keep track of hits
        write_hits += 1
        print("write hit  [address=" + str(address) + " tag=" + str(tag) + " index=" + str(index) + " block_offset=" + str(block_offset) + " block_index=" + str(block_index) + " : word=" + str(word) + " (" + str(start) + " - " + str(end) + ")]")
        print(('{0:0' + str(ADDRESS_LENGTH) + 'b}').format(address))

        if cache.write == "write-through":
            print("write-through cache: write " + str(write_word) + " to memory[" + str(address) + "]")
        elif cache.write == "write-back":
            print("write-back cache: write " + str(write_word) + " to memory[" + str(address) + "]")
            print("read in (" + str(start) + " - " + str(end) + ")")
            print("")
        else:
            print("error: cache write type")
        print("")

    else: #cache miss
        #evicting on a miss
        if change == True:
            if cache.write == "write-back":
                evicted_block_address = cache.set["set " + str(index)][0].address
                print(evicted_block_address)
                evicted_binary = (('{0:016b}'.format(evicted_block_address))[:-cache.block_offset]) + ("0" * cache.block_offset)
                evicted_start = int(evicted_binary, 2)
                evicted_end = evicted_start + (CACHE_BLOCK_SIZE - 1)

            for x in range(cache.associativity):
                if x == cache.associativity - 1:
                    cache.set["set " + str(index)][x] = Block(CACHE_BLOCK_SIZE)
                else:
                    cache.set["set " + str(index)][x] = cache.set["set " + str(index)][x + 1]

        # set the valid bit for set i to true
        cache.set["set " + str(index)][block_index].valid = True

        if cache.write == "write-back":
            cache.set["set " + str(index)][block_index].dirty = True

        # set the tag set i to t
        cache.set["set " + str(index)][block_index].tag = tag

        # return the word at positions b, b+1, b+2, b+3 from the block in set i
        word = 0
        for x in range(4):
            # read 4 bytes at a time, little endian conversion 256^0*mem[value0] + 256^1*mem[value1] + 256^2*mem[value2] ... etc.
            # return the word (the four bytes) at positions b, b+1, b+2, b+3 from the block in set i
            word += (256 ** x) * cache.set["set " + str(index)][block_index].data[block_offset + x]

        if cache.write == "write-through":
            memory[address:address+4] = [write_word & 255, (write_word >> 8) & 255, (write_word >> 16) & 255, (write_word >> 24) & 255]

        #set address for write-back cache
        cache.set["set " + str(index)][block_index].address = address

        if cache.associativity > 1:
            # screw tag queues, this works great too
            print("[ ", end="")
            for x in range(cache.associativity):
                print(cache.set["set " + str(index)][0 + x].tag, end=", ")
            print("\b", end="")
            print(" ]")

        #keep track of misses
        write_misses += 1
        if change == True:
            print("write miss + replace [address=" + str(address) + " tag=" + str(tag) + " index=" + str(index) + " block_offset=" + str(block_offset) + " block_index=" + str(block_index) + " : word=" + str(word) + " (" + str(start) + " - " + str(end) + ")]")
            print("evict tag " + str(cache.set["set " + str(index)][0].tag) + " in block_index 0")
        else:
            print("write miss [address=" + str(address) + " tag=" + str(tag) + " index=" + str(index) + " block_offset=" + str(block_offset) + " block_index=" + str(block_index) + " : word=" + str(word) + " (" + str(start) + " - " + str(end) + ")]")
        print(('{0:0' + str(ADDRESS_LENGTH) + 'b}').format(address))

        if cache.write == "write-through":
            print("write-through cache: write " + str(write_word) + " to memory[" + str(address) + "]")
        elif cache.write == "write-back" and change == True:
            print("write-back (" + str(evicted_start) + " - " + str(evicted_end) + ")")
            print("read in (" + str(start) + " - " + str(end) + ")")
            print("")
        elif cache.write == "write-back" and change == False:
            print("read in (" + str(start) + " - " + str(end) + ")")
            print("")
        else:
            print("error: cache write type")
        print("")

def main():
    global reads
    global writes

    filename = "cholesky.atrace.txt"

    with open(filename, 'r') as file:
        for line in file:
            instruction = line.split()
            if len(instruction) == 1:
                pass

            else:
                if instruction[1] == "R":
                    address = int(instruction[2], 16)
                    print(address)
                    readWord(address)
                    reads += 1

                elif instruction[1] == "W":
                    address = int(instruction[2], 16)
                    print(address)
                    rand_word = random.randint(1, 255)
                    writeWord(address, rand_word)
                    writes += 1

                else:
                    pass

    #print statistics
    print("---------------------------------------------------------------------------------")
    print("")
    print("cache size = " + str(CACHE_SIZE))
    print("cache block size = " + str(CACHE_BLOCK_SIZE))
    print("number of blocks = " + str(CACHE_SIZE // CACHE_BLOCK_SIZE))
    print("number of sets = " + str(len(cache.set)))
    print("cache associativity = " + str(ASSOCIATIVITY))
    print("cache tag length = " + str(cache.tag))
    print("cache index length = " + str(cache.index))
    print("cache block offset length = " + str(cache.block_offset))
    print("write type = " + str(WRITETYPE))
    print("")
    print("---------------------------------------------------------------------------------")
    print("")
    print("reads = " + str(reads))
    print("read misses = " + str(read_misses) + " (" + str('{:.2f}'.format((read_misses / reads) * 100)) + "%)")
    print("reads hits = " + str(read_hits) + " (" + str('{:.2f}'.format((read_hits / reads) * 100)) + "%)")
    print("writes = " + str(writes))
    print("write misses = " + str(write_misses) + " (" + str('{:.2f}'.format((write_misses / writes) * 100)) + "%)")
    print("write hits = " + str(write_hits) + " (" + str('{:.2f}'.format((write_hits / writes) * 100)) + "%)")
    print("")
    print("total (reads & writes) = " + str(reads + writes))
    print("")
    print("---------------------------------------------------------------------------------")

main()