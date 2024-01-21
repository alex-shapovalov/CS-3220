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
    def __init__(self, pc, next_pc):
        self.pc = pc #index in memory array
        self.next_pc = pc
        memory = [0] * 65536
        regs = [0] * 16


class Instruction:
    def __init__(self, opcode, Rd, Rs1, Rs2, immed):
        self.opcode = opcode
        self.Rd = Rd #destination register
        self.Rs1 = Rs1 #1st source register
        self.Rs2 = Rs2 #2nd source register
        self.immed = immed #immediate value

def build_instruction(opcode, Rd, Rs1, Rs2, immed):
    instr = opcode << 28
    if Rd is not None:
        instr = instr + (Rd << 24)
    if Rs1 is not None:
        instr = instr + (Rs1 << 20)
    if Rs2 is not None:
        instr = instr + (Rs2 << 16)
    if immed is not None:
        instr = instr + immed
    return instr

def main():
    cpu = CPU(0, 1)
    count = 0
    #read from file
        #read until first space, this is the opcode, if noop or return, nextline
        #comma seperated reading

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
            pass
        elif a == line_count - 2 and lines[a + 1].rstrip('\n') != "return":
            print("Syntax error: no return at eof")
        elif opcode in ["add", "addi", "beq", "jal", "lw", "sw", "sub", "subi", "jalr"]:
            #continue reading the rest of the instruction
            print(tail)

            # build each line

            # put everything into memory
            pass
        else:
            print("Syntax error: opcode line " + str(n))
            a = line_count + 1
        a += 1
        n += 1
        opcode = lines[n].rstrip('\n')
        opcode, sep, tail = opcode.partition(' ')

    #for loop with amount of lines inputted

main()