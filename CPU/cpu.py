#Alex Shapovalov
#CS 5220
#Programming Assignment #1, Instruction Processing

#used to filter .txt strings into workable ints
#https://stackoverflow.com/questions/42751063/python-filter-positive-and-negative-integers-from-string
import re

class CPU:
    def __init__(self):
        self.pc = 0 #index in memory array
        self.next_pc = 0
        self.memory = [0] * 65536
        self.regs = [0] * 16

cpu = CPU()
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
    file = open("assembly.txt", "r")
    lines = file.readlines()
    line_count = len(lines)
    file.close()

    #read in from file:
    a = 0
    n = 0
    values = []
    opcode = lines[n].rstrip('\n')
    opcode, sep, tail = opcode.partition(' ')
    while a < line_count - 1:
        values = [int(d) for d in re.findall(r'-?\d+', tail)]

        #two special opcodes in their own section
        if opcode == "noop":
            i = build_instruction(NOOP, None, None, None, None)
            cpu.memory[a + 100] = i

        elif opcode == "return":
            i = build_instruction(RETURN, None, None, None, None)
            cpu.memory[a + 100] = i

        #error if no return statement
        elif a == line_count - 2 and lines[a + 1].rstrip('\n') != "return":
            print("Syntax error: no return at eof")

        #grouping like operations
        elif opcode in ["jal", "jalr"]:
            if opcode == "jal":
                i = build_instruction(JAL, values[0], None, None, values[1])
                cpu.memory[a + 100] = i
            else:
                i = build_instruction(JALR, values[0], values[1], None, values[2])
                cpu.memory[a + 100] = i

        elif opcode in ["lw", "sw"]:
            if opcode == "lw":
                i = build_instruction(LW, values[0], values[2], None, values[1])
                cpu.memory[a + 100] = i
            else:
                i = build_instruction(SW, values[0], values[2], None, values[1])
                cpu.memory[a + 100] = i
            values = []

        elif opcode in ["addi", "subi"]:
            if opcode == "addi":
                i = build_instruction(ADDI, values[0], values[1], None, values[2])
                cpu.memory[a + 100] = i
            else:
                i = build_instruction(SUBI, values[0], values[1], None, values[2])
                cpu.memory[a + 100] = i

        elif opcode in ["add", "beq", "sub"]:
            if opcode == "add":
                i = build_instruction(ADD, values[0], values[1], values[2], None)
                cpu.memory[a + 100] = i
            elif opcode == "sub":
                i = build_instruction(ADD, values[0], values[1], values[3], None)
                cpu.memory[a + 100] = i
            else:
                i = build_instruction(BEQ, None, values[0], values[1], values[2])
                cpu.memory[a + 100] = i

        #error if incorrect syntax
        else:
            print("Syntax error: opcode line " + str(n))
            a = line_count + 1

        #reset for next line
        a += 1
        n += 1
        values = []
        opcode = lines[n].rstrip('\n')
        opcode, sep, tail = opcode.partition(' ')

    #while loop going through memory from 100 until reaching 0

main()