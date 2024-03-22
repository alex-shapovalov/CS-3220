jal x0, main

f1:
  addi   sp, sp, -16 # reserve 4 words on the stack
  sw     ra, 12(sp)  # save ra
  sw     s0, 8(sp)   # save s0
  addi   s0, sp, 16  # set s0: top of stack
  sw     a0, -12(s0) # save p
  lw     a0, -12(s0) # load p
  addi   a1, x0, 18  # set k to 18
  sw     a0, -8(s0)  # save k
  lw     a0, -8(s0)  # load k
  add    a0, a0, a1  # add k to p
  sw     a0, -16(s0) # store a0
  lw     a0, -16(s0) # load a0
  lw     s0, 8(sp)   # restore s0
  lw     ra, 12(sp)  # restore ra
  addi   sp, sp, 16  # restore the stack pointer
  jalr   x0, ra, 0.  # return (jump to ra)

f2:
  addi   sp, sp, -32 # reserve 8 words on the stack
  sw     ra, 28(sp)  # save ra in mem[sp+28]
  sw     s0, 24(sp)  # save ra 
  addi   s0, sp, 32  # s0 <- sp + 32
  sw     a0, -12(s0) # save a0 in mem[s0-12]
  sw     a1, -16(s0) # save a1 in mem[s0-16]
  lw     a0, -12(s0) # load a0 from mem[s0-12]
  lw     a1, -16(s0) # load a1 from mem[s0-16]
  beq    a0, a1, L1  # if a0 == a1, set a0 = 0
  slt    a2, a0, a1  # put smaller value in a2
  beq    a2, x0, L0  # if a0 is larger, avoid change
  lw     a0, -16(s0) # if a1 is larger, set a0 to a1
  jal    ra, L2      # done modifying, go to L2
L0:
  jal    ra, L2      # do nothing, go to L2
L1:
  lw     a0, -12(s0) # load a0
  addi   a0, x0, 0   # set a0 to 0
  sw     a0, -12(s0) # set a0 to 0
  jal    ra, L2      # done modifying, go to L2
L2:
  lw     s0, 24(sp)  # load s0 from mem[sp+24]
  lw     ra, 28(sp)  # load ra from mem[sp+28]
  addi   sp, sp, 32  # sp <- sp + 32
  jalr   x0, ra, 0   # jump to return address

main:
  addi sp, x0, 64    # set stack pointer to non-zero value
  addi a0, x0, 12    # set parameter 12
  jal ra, f1         # call the function

  # reset
  addi sp, x0, 64    # set stack pointer to non-zero value
  addi a0, x0, 10    # set parameters
  addi a1, x0, 12
  jal ra, f2         # call the function

  addi a2, x0, 0