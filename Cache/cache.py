#Alex Shapovalov
#CS 5220
#Programming Assignment #2, Cache

class Block:
    def __init__(self, size):
        self.block = [0] * size
        #TODO:
        self.tag = 0
        self.clean = True
        self.status = False

class Cache:
    def __init__(self, address, cache, block, associativity, write):
        self.address = address #address size
        self.cache = cache #cache size
        self.block = block #block size
        self.associativity = associativity #number of blocks per set
        self.write = write #write type

        self.block = [Block(block)] * (cache // block) #create an array of blocks with size block

        numSets = (cache // associativity) // block #figure out how many sets we need
        self.set = {} #sets defined as a dictionary
        z = 0
        for x in range(1, numSets + 1): #creates sets based on block size and associativity, self.sets is a dictionary of 1 or more blocks
            self.set["set " + str(x)] = []
            for y in range(min(numSets, associativity)):
                if z < len(self.block):
                    self.set["set " + str(x)].append(self.block[z])
                    z += 1

def readWord(address):
    a = 1
def writeWord(address, word):
    a = 1

def main():
    addressLength = 16
    cache = Cache(addressLength, 256, 16, 1, "Null")
    memory = [0] * (2 ** addressLength)

    print(len(memory), len(cache.block), cache.set)

main()