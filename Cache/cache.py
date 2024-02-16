#Alex Shapovalov
#CS 5220
#Programming Assignment #2, Cache

import re

ADDRESS_LENGTH = 16
CACHE_SIZE = 1024
CACHE_BLOCK_SIZE = 64
ASSOCIATIVITY = 1

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

        self.block = [Block(block)] * (cache // block) #create an array of blocks with size block

        numSets = (cache // associativity) // block #figure out how many sets we need
        self.set = {} #sets defined as a dictionary, didn't make it its own class because it's simply a grouping of blocks, not its own thing
        z = 0
        for x in range(1, numSets + 1): #creates sets based on block size and associativity, self.sets is a dictionary of 1 or more blocks
            self.set["set " + str(x)] = []
            for y in range(min(numSets, associativity)):
                if z < len(self.block):
                    self.set["set " + str(x)].append(self.block[z])
                    z += 1

        self.block_offset = logb2(block)
        self.index = logb2(numSets)
        self.tag = ADDRESS_LENGTH - self.block_offset - self.index
        self.block_address = ADDRESS_LENGTH - self.tag

#global cache and memory
cache = Cache(ADDRESS_LENGTH, CACHE_SIZE, CACHE_BLOCK_SIZE, ASSOCIATIVITY, "Null")
memory = bytearray(2 ** ADDRESS_LENGTH)
#prefill memory
for i in range(0, len(memory), 4):
    memory[i:i+4] = [i & 255, (i >> 8) & 255, (i >> 16) & 255, (i >> 24) & 255]

tag_queue = [0, 0, 0, 0]

def readWord(address):
    #from addr, compute the tag t, index i and block offset b (use cache.block_offset, tag, index etc.)
    tag = address >> cache.block_address
    index = address >> cache.block_address & ((1 << cache.index) - 1)
    block_offset = address &  ((1 << cache.block_offset) - 1)
    block_index = 0

    # compute the range of the desired block in memory: start to start+blocksize-1
    binary = (('{0:16b}'.format(address))[:-cache.tag]) + ("0" * cache.tag)
    start = int(binary, 2)
    end = start + (CACHE_BLOCK_SIZE - 1)

    #look at the information in the cache for set i (there is only one block in the set)
    if cache.set["set " + str(index)][cache.associativity - 1].valid and cache.set["set " + str(index)][cache.associativity - 1].tag == tag: #cache hit
        word = 0
        for x in range(4):
            #return the word (the four bytes) at positions b, b+1, b+2, b+3 from the block in set i
            word += (256 ** x) * cache.set["set " + str(index)][cache.associativity - 1].data[block_offset + x]
        print("read hit  [address=" + str(address) + " tag=" + str(tag) + " index=" + str(index) + " block_offset=" + str(block_offset) + " block_index=" + str(block_index) + " : word=" + str(word) + " (" + str(start) + " - " + str(end) + ")]")
        print(binary)
        print("")
        return word
    else: #cache miss
        #read the blocksize bytes of memory from start to start+blocksize-1 into set i of the cache set the valid bit for set i to true
        for x in range(CACHE_BLOCK_SIZE - 1):
            cache.set["set " + str(index)][cache.associativity - 1].data[x] = memory[x + start]

        #set the valid bit for set i to true
        cache.set["set " + str(index)][cache.associativity - 1].valid = True

        #set the tag set i to t
        cache.set["set " + str(index)][cache.associativity - 1].tag = tag

        #return the word at positions b, b+1, b+2, b+3 from the block in set i
        word = 0
        for x in range(4):
            #read 4 bytes at a time, little endian conversion 256^0*mem[value0] + 256^1*mem[value1] + 256^2*mem[value2] ... etc.
            #return the word (the four bytes) at positions b, b+1, b+2, b+3 from the block in set i
            word += (256 ** x) * cache.set["set " + str(index)][cache.associativity - 1].data[block_offset + x]
        print("read miss [address=" + str(address) + " tag=" + str(tag) + " index=" + str(index) + " block_offset=" + str(block_offset) +  " block_index=" + str(block_index) + " : word=" + str(word) + " (" + str(start) + " - " + str(end) + ")]")
        print(binary)
        print("")
        return word

def writeWord(address, word):
    pass

def main():
    #TODO: change to allow for hexadecimal commands

    filename = "part-one-addresses.txt"

    with open(filename, 'r') as file:
        for line in file:
            #this is extremely lazy determination of what function is on each line (doesn't catch syntax errors etc.)
            #but i'm not being tested on my ability to properly read in inputs from a file, so i don't really care
            line = line.strip()
            operation = line[0]
            if (operation == 'r'):
                values = [int(d) for d in re.findall(r'-?\d+', line)]
                readWord(values[0])

            elif (operation == 'w'):
                values = [int(d) for d in re.findall(r'-?\d+', line)]
                writeWord(values[0], values[1])

            else:
                pass

    #TODO: keep track of statistics

main()