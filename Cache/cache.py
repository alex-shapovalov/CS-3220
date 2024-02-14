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
        self.tag = logb2(numSets)
        self.index = self.block_offset - self.tag

def readWord(address):
    #TODO: read 4 bytes at a time, little endian conversion 256^0*mem[value0] + 256^1*mem[value1] + 256^2*mem[value2] ... etc.
    pass
#   from addr, compute the tag t, index i and block offset b (use cache.block_offset, tag, index etc.)
#   look at the information in the cache for set i (there is only one block in the set)
#   if the block in set i is valid {
#      if the tag for set i == t {
#      // this is a hit
#         return the word (the four bytes) at positions b, b+1, b+2, b+3 from the block in set i
#      }
#   }
#   // this is a miss
#   compute the range of the desired block in memory: start to start+blocksize-1
#   read the blocksize bytes of memory from start to start+blocksize-1 into set i of the cache set the valid bit for set i to true
#   set the tag set i to t
#   return the word at positions b, b+1, b+2, b+3 from the block in set i

def writeWord(address, word):
    pass

def main():
    cache = Cache(ADDRESS_LENGTH, CACHE_SIZE, CACHE_BLOCK_SIZE, ASSOCIATIVITY, "Null")
    memory = bytearray(2 ** ADDRESS_LENGTH)

    print(len(memory), len(cache.block), cache.set)

    #46916 = 101101 1101 000100
    memory[46916] = int('1011', 2)
    memory[46917] = int('0111', 2)
    memory[46918] = int('0100', 2)
    memory[46919] = int('0100', 2)

    #13388 = 001101 0001 001100
    memory[13388] = int('0011', 2)
    memory[13389] = int('0100', 2)
    memory[13390] = int('0100', 2)
    memory[13391] = int('1100', 2)

    filename = "part-one-addresses.txt"

    with open(filename, 'r') as file:
        #this is extremely lazy determination of what function is on each line (doesn't catch syntax errors etc.)
        #but i'm not being tested on my ability to properly read in inputs from a file, so i don't really care
        line = file.readline()
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