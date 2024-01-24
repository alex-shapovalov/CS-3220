#Alex Shapovalov
#CS 5220
#Programming Assignment #1, Instruction Processing

#used to filter .txt strings into workable ints without losing negatives
#https://stackoverflow.com/questions/42751063/python-filter-positive-and-negative-integers-from-string
import re

#assign global constant ints to opcodes
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
        self.pc = pc #index in memory
        self.next_pc = next_pc #next index in memory
        self.memory = [0] * 65536 #memory
        self.regs = [0] * 16 #registers

#instantiate global cpu class
cpu = CPU(0, 1)

class Instruction:
    def __init__(self, instr):
        self.opcode = instr >> 28 #actual instruction
        self.Rd = (instr >> 24) & 0b1111 #destination register
        self.Rs1 = (instr >> 20) & 0b1111 #1st source register
        self.Rs2 = (instr >> 16) & 0b1111 #2nd source register
        self.immed = int('{:032b}'.format(instr), 2) & 0xFFFF #immediate value
        #2's compliment implementation
        if (self.immed & (1 << (16 - 1))) != 0:
            self.immed = self.immed - (1 << 16)

        # convert to binary:
        #binary = '{:032b}'.format(instr)
        #print(binary)

        #values test:
        #values = [self.opcode, self.Rd, self.Rs1, self.Rs2, self.immed]
        #print(values)

        #cpu registers step by step test:
        #print(cpu.regs)

        if self.opcode == NOOP:
            pass

        elif self.opcode == ADD:
            cpu.regs[self.Rd] = cpu.regs[self.Rs1] + cpu.regs[self.Rs2]

        elif self.opcode == ADDI:
            cpu.regs[self.Rd] = cpu.regs[self.Rs1] + self.immed

        elif self.opcode == BEQ:
            if cpu.regs[self.Rs1] == cpu.regs[self.Rs2]:
                cpu.next_pc = cpu.pc + self.immed
            else:
                pass

        elif self.opcode == JAL:
            cpu.regs[self.Rd] = cpu.pc + 1
            cpu.next_pc = cpu.pc + self.immed

        elif self.opcode == LW:
            cpu.regs[self.Rd] = cpu.memory[self.immed + cpu.regs[self.Rs1]]

        elif self.opcode == SW:
            cpu.memory[self.immed + cpu.regs[self.Rs2]] = cpu.regs[self.Rs1]

        elif self.opcode == RETURN:
            cpu.regs[0] = 0

        elif self.opcode == SUB:
            cpu.regs[self.Rd] = cpu.regs[self.Rs1] - cpu.regs[self.Rs2]

        elif self.opcode == SUBI:
            cpu.regs[self.Rd] = cpu.regs[self.Rs1] - self.immed

        elif self.opcode == JALR:
            cpu.regs[self.Rd] = cpu.pc + 1
            cpu.next_pc = cpu.regs[self.Rs1] + self.immed

        else:
            print("Instruction error")

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
    file_name = "assembly2.txt"
    file = open(file_name, "r")
    lines = file.readlines()
    line_count = len(lines)
    file.close()

    #read in from file:
    a = 0
    n = 0
    opcode = lines[n].rstrip('\n')
    opcode, sep, tail = opcode.partition(' ')
    while a < line_count:
        values = [int(d) for d in re.findall(r'-?\d+', tail)]

        #two special opcodes in their own section
        if opcode == "noop":
            i = build_instruction(NOOP, None, None, None, None)
            cpu.memory[a + 100] = i

        elif opcode == "return":
            i = build_instruction(RETURN, None, None, None, None)
            cpu.memory[a + 100] = i
            a = line_count
            break

        #error if no return statement
        elif a == line_count - 2 and lines[a + 1].rstrip('\n') != "return":
            print("Syntax error: no return at eof")
            cpu.memory = [0] * 65536
            break

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
                i = build_instruction(SW, None, values[0], values[2], values[1])
                cpu.memory[a + 100] = i

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
            cpu.memory = [0] * 65536
            break

        #reset for next line
        a += 1
        n += 1
        values = []
        opcode = lines[n].rstrip('\n')
        opcode, sep, tail = opcode.partition(' ')

    #set pc to 100 and next_pc to 101
    cpu.pc = 100
    cpu.next_pc = 101

    #while loop for the amount of instructions
    count = 0
    while count < a:
        Instruction(cpu.memory[cpu.pc])
        cpu.pc = cpu.next_pc
        cpu.next_pc += 1
        count += 1

    #added some other tests for subi, jalr, and negative numbers in assembly2.txt
    print(cpu.regs)
    if file_name == "assembly.txt":
        print(cpu.memory[28])
    elif file_name == "assembly2.txt":
        print(cpu.memory[40])

main()