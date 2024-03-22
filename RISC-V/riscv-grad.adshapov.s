jal x0, main

e:
  error  8

f1: # interger division
  addi   sp, sp, -32 # reserve 8 words on the stack
  sw     ra, 28(sp)  # save ra in mem[sp+28]
  sw     s0, 24(sp)  # save s0 in mem[sp+24]
  addi   s0, sp, 32  # s0 <- sp + 32
  sw     a0, 0(s0)   # save numerator
  sw     a1, 4(s0)   # save denominator
  lw     a0, 0(s0)   # load numerator
  lw     a1, 4(s0)   # load denominator
  addi   t0, x0, 1   # set t0 to 1 for comparison
  slt    t1, a1, t0  # error check denominator
  beq    t1, t0, e   # jump to error
  blt    a0, x0, e   # error
  addi   t0, x0, 0   # initialize q
  sw     t0, 8(s0)
L0:
  sub    a0, a0, a1  # numer = numer - denom
  blt    a0, x0, L1  # check if we should end loop
  addi   t0, t0, 1   # q = q + 1
  jal    x0, L0      # loop
L1:
  add    a0, t0, x0  # set a0 to q
  lw     ra, 28(sp)  # restore ra
  lw     s0, 24(sp)  # restore s0
  addi   sp, sp, 32  # deallocate stack space
  jalr   x0, ra, 0   # jump to return address

f2: #intsqrt, answer stored in a0
  addi   sp, sp, -32 # reserve 8 words on the stack
  sw     ra, 28(sp)  # save ra in mem[sp+28]
  sw     s0, 24(sp)  # save s0 in mem[sp+24]
  addi   s0, sp, 32  # s0 <- sp + 32
  sw     a0, 0(s0)   # store p
  lw     a0, 0(s0)   # load p
  blt    a0, x0, e   # error
  srai   t0, a0, 1   # get i0 (p / 2) https://msyksphinz-self.github.io/riscv-isadoc/html/rvi.html#srai
  sw     t0, 20(s0)  # store i0
  blt    x0, t0, L3  # move to if statement
  jalr   x0, ra, 0   # jump to return address
L3:
  # stuff here for int i1 = ( i0 + p / i0) >> 1
  add    a1, t0, x0  # set params for division
  jal    ra, f1      # call the function, result = a0
  lw     t0, 20(s0)  # load i0
  add    t1, t0, a0  # i0 + (result)
  srai   t1, t1, 1   # >> 1
L4:
  blt    t0, t1, L5  # should we enter the loop?
  add    t0, t1, x0  # set i0 = i1
  sw     t0, 20(s0)  # save i0
  lw     t0, 20(s0)  # load i0
  add    a1, t0, x0  # set params for division
  lw     a0, 0(s0)   # load p
  jal    ra, f1      # call the function, result = a0
  lw     t0, 20(s0)  # load i0
  add    t1, t0, a0  # i0 + (result)
  srai   t1, t1, 1   # >> 1
  blt    t1, t0, L4  # break loop?
L5:
  lw     a0, 20(s0)  # return i0
  lw     ra, 28(sp)  # restore ra
  lw     s0, 24(sp)  # restore s0
  addi   sp, sp, 32  # deallocate stack space
  jalr   x0, ra, 0   # jump to return address

main:
  addi sp, x0, 64    # set stack pointer to non-zero value
  addi a0, x0, 67    # set parameters
  jal ra, f2         # call the function