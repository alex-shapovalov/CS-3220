#Alex Shapovalov
#CS 5220
#Programming Assignment #1, Instruction Processing

NOOP = 0
ADD = 1
ADDI = 2
BEQ = 3
JAL = 4
LW = 5
SW = 6
RETURN = 7
SUB = 9
SUBI = 10
JALR = 12

class CPU:
    def __init__(self):
        self.pc = 0 #index in memory array
        self.next_pc = 0
        self.memory = [0] * 65536
        self.regs = [0] * 16

class Instruction:
    def __init__(self, instr):
        self.opcode = 0 #actual instruction
        self.Rd = 0 #destination register
        self.Rs1 = 0 #1st source register
        self.Rs2 = 0 #2nd source register
        self.immed = 0 #immediate value

        #TODO: deal with each instruction

def build_instruction(opcode, Rd, Rs1, Rs2, immed):
    instr = opcode << 28
    if Rd is not None:
        instr = instr + (Rd << 24)
    if Rs1 is not None:
        instr = instr + (Rs1 << 20)
    if Rs2 is not None:
        instr = instr + (Rs2 << 16)
    if immed is not None:
        #TODO: two's compliment negative values
        instr = instr + immed
    print(instr)
    return instr

def main():
    cpu = CPU()

    file = open("assembly.txt", "r")
    lines = file.readlines()
    line_count = len(lines)
    file.close()

    a = 0
    n = 0
    opcode = lines[n].rstrip('\n')
    opcode, sep, tail = opcode.partition(' ')
    while a < line_count - 1:
        if opcode == "noop":
            i = build_instruction(NOOP, None, None, None, None)
            #TODO: change depending on what line we are on
            cpu.memory[100] = i
            pass
        elif a == line_count - 2 and lines[a + 1].rstrip('\n') != "return":
            print("Syntax error: no return at eof")
        elif opcode in ["add", "addi", "beq", "jal", "lw", "sw", "sub", "subi", "jalr"]:
            #TODO: continue reading the rest of the instruction
            print(tail.rstrip('\n'))

            # build each line

            # put everything into memory

        else:
            print("Syntax error: opcode line " + str(n))
            a = line_count + 1
        a += 1
        n += 1
        opcode = lines[n].rstrip('\n')
        opcode, sep, tail = opcode.partition(' ')

    #while loop going through memory from 100 until reaching 0

main()