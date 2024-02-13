#Alex Shapovalov
#CS 5220
#Programming Assignment #2, Cache

class Block:
    def __init__(self, size):
        # TODO: bytearrays
        #value = bytearray(regArray)
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

def readWord(address):
    #TODO: read 4 bytes at a time, little endian conversion 256^0*mem[value] + 256^1*mem[value] + 256^2*mem[value] ... etc.
    pass
#   from addr, compute the tag t, index i and block offset b
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
    addressLength = 16
    cache = Cache(addressLength, 1024, 64, 1, "Null")
    #TODO: init memory four bytes init memory[0] is [0,0,0,0], memory[4] is [4,0,0,0], memory[256] is [0,1,0,0]
    memory = [0] * (2 ** addressLength)

    print(len(memory), len(cache.block), cache.set)

    #TODO: preload memory with some values
        #46916 = 101101 1101 000100
        #13388 = 001101 0001 001100

    #TODO: part 1 algorithm for accessing memory location A

    #TODO: reads from .txt file (part_one_addresses.txt)

    #TODO: keep track of statistics

main()