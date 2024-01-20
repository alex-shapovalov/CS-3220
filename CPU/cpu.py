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
SUB = 8
SUBI = 9
JALR = 10

class CPU:
    def __init__(self):
        pc = 0
        next_pc = 0
        memory = [0] * 65536
        regs = [0] * 16


class Instruction:
    def __init__(self):
        opcode = 0
        Rd = 0
        Rs1 = 0
        Rs2 = 0
        immed = 0

def build_instruction(opcode, Rd, Rs1, Rs2, immed):
    insrt = opcode << 28
    return_int = 0
    return return_int

def main():
    i0 = build_instruction(NOOP, None, None, None, None)