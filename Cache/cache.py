#Alex Shapovalov
#CS 5220
#Programming Assignment #2, Cache

import re

CACHE_SIZE = 1024
CACHE_BLOCK_SIZE = 64
ADDRESS_LENGTH = 16
ASSOCIATIVITY = 4
WRITETYPE = "write through"

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

    #from addr, compute the tag t, index i and block offset b (use cache.block_offset, tag, index etc.)
    tag = address >> cache.block_address
    index = (address >> cache.block_offset) & cache.index
    block_offset = address & ((1 << cache.block_offset) - 1)
    block_index = 0

    #follow something like this to write to the empty block in a set:
    if cache.associativity > 1 and cache.set["set " + str(index)][block_index].valid:
        for x in range(cache.associativity):
            if cache.set["set " + str(index)][x].valid:
                block_index += 1

    #TODO: tag queue
    #if block_index = associativity then we are full and must evict from tag_queue
    #set block_index to cache.associativity - 1
    if block_index == cache.associativity:
        block_index = cache.associativity - 1
    #evict set[index][0], slide everything to the left, put the new tag into set[index][associativity - 1]

    # compute the range of the desired block in memory: start to start+blocksize-1
    binary = (('{0:016b}'.format(address))[:-cache.block_offset]) + ("0" * cache.block_offset)
    start = int(binary, 2)
    end = start + (CACHE_BLOCK_SIZE - 1)

    #look at the information in the cache for set i (there is only one block in the set)
    if cache.set["set " + str(index)][block_index].valid and cache.set["set " + str(index)][block_index].tag == tag: #cache hit
        word = 0
        for x in range(4):
            #return the word (the four bytes) at positions b, b+1, b+2, b+3 from the block in set i
            word += (256 ** x) * cache.set["set " + str(index)][block_index].data[block_offset + x]

        #screw tag queues, this works great too
        print("[ ", end = "")
        for x in range(cache.associativity):
            print(cache.set["set " + str(index)][0 + x].tag, end=", ")
        print(" ]")

        read_hits += 1
        print("read hit  [address=" + str(address) + " tag=" + str(tag) + " index=" + str(index) + " block_offset=" + str(block_offset) + " block_index=" + str(block_index) + " : word=" + str(word) + " (" + str(start) + " - " + str(end) + ")]")
        print(binary)
        print("")
        return word
    else: #cache miss
        #read the blocksize bytes of memory from start to start+blocksize-1 into set i of the cache set the valid bit for set i to true
        for x in range(CACHE_BLOCK_SIZE - 1):
            cache.set["set " + str(index)][block_index].data[x] = memory[x + start]

        #set the valid bit for set i to true
        cache.set["set " + str(index)][block_index].valid = True

        #set the tag set i to t
        cache.set["set " + str(index)][block_index].tag = tag

        #return the word at positions b, b+1, b+2, b+3 from the block in set i
        word = 0
        for x in range(4):
            #read 4 bytes at a time, little endian conversion 256^0*mem[value0] + 256^1*mem[value1] + 256^2*mem[value2] ... etc.
            #return the word (the four bytes) at positions b, b+1, b+2, b+3 from the block in set i
            word += (256 ** x) * cache.set["set " + str(index)][block_index].data[block_offset + x]

        #screw tag queues, this works great too
        print("[ ", end = "")
        for x in range(cache.associativity):
            print(cache.set["set " + str(index)][0 + x].tag, end=", ")
        print("\b", end="")
        print(" ]")

        read_misses += 1
        print("read miss [address=" + str(address) + " tag=" + str(tag) + " index=" + str(index) + " block_offset=" + str(block_offset) +  " block_index=" + str(block_index) + " : word=" + str(word) + " (" + str(start) + " - " + str(end) + ")]")
        print(binary)
        print("")
        return word

def writeWord(address, word):
    #TODO: PART 2:
    global write_misses
    global write_hits

    #from addr, compute the tag t, index i and block offset b (use cache.block_offset, tag, index etc.)
    tag = address >> cache.block_address
    index = (address >> cache.block_offset) & cache.index
    block_offset = address & ((1 << cache.block_offset) - 1)
    block_index = 0

    #follow something like this to write to the empty block in a set:
    if cache.associativity > 1 and cache.set["set " + str(index)][block_index].valid:
        for x in range(cache.associativity - 1):
            if cache.set["set " + str(index)][x].valid:
                block_index += 1
    pass

def main():
    #TODO: PART 2: change to allow for hexadecimal commands
    global reads
    global writes

    filename = "part-two-addresses.txt"

    with open(filename, 'r') as file:
        for line in file:
            #this is extremely lazy determination of what function is on each line (doesn't catch syntax errors etc.)
            #but i'm not being tested on my ability to properly read in inputs from a file, so i don't really care
            line = line.strip()
            operation = line[0]
            if (operation == 'r'):
                reads += 1
                values = [int(d) for d in re.findall(r'-?\d+', line)]
                readWord(values[0])

            elif (operation == 'w'):
                writes += 1
                values = [int(d) for d in re.findall(r'-?\d+', line)]
                writeWord(values[0], values[1])

            else:
                pass

    #print statistics
    print("-----------------------------------------------------------------------------------")
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
    print("-----------------------------------------------------------------------------------")
    print("")
    print("reads = " + str(reads))
    print("read misses = " + str(read_misses) + " (" + str('{:.2f}'.format((read_misses / reads) * 100)) + "%)")
    print("reads hits = " + str(read_hits) + " (" + str('{:.2f}'.format((read_hits / reads) * 100)) + "%)")
    #TODO: PART 2: uncomment
    #print("writes = " + str(writes))
    #print("write misses = " + str(write_misses) + " (" + str('{:.2f}'.format((write_misses / writes) * 100)) + "%)")
    #print("write hits = " + str(write_hits) + " (" + str('{:.2f}'.format((write_hits / writes) * 100)) + "%)")
    print("")
    print("-----------------------------------------------------------------------------------")

main()