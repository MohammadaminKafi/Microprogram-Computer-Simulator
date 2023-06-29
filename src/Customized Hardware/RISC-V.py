# class for simulating a RISC-V processor behaviour
class RV:
    # initialize the RISC-V processor
    def __init__(self, memory, registers, pc, instructions):
        self.memory = memory
        self.registers = registers
        self.pc = pc
        self.instructions = instructions
        self.instruction = None
        self.opcode = None
        self.rd = None
        self.rs1 = None
        self.rs2 = None
        self.imm = None
        # dictionary for mapping the opcode to the I-type instructions
        # dictionary for mapping the opcode to the I-type instructions
        self.I_type = {
            '0b0000011': self.LOAD,    # Load instructions
            '0b0010011': self.I_IMM,   # Immediate instructions
            '0b1100111': self.JALR,    # Jump and link register
            '0b0100011': self.STORE,   # Store instructions
            '0b0110011': self.I_R,     # Register instructions
            '0b0011011': self.I_IMM,   # Immediate instructions
            '0b0001111': self.FENCE,   # Fence instructions
            '0b1110011': self.I_SYSTEM # System instructions
        }

        # dictionary for mapping the opcode to the R-type instructions
        self.R_type = {
            '0b0110011': self.R_R,     # Register-register instructions
            '0b0111011': self.R_R,     # Register-register instructions
            '0b1100011': self.BRANCH,  # Branch instructions
            '0b1110011': self.R_SYSTEM # System instructions
        }

        # dictionary for mapping the opcode to the S-type instructions
        self.S_type = {
            '0b0100011': self.STORE    # Store instructions
        }

        # dictionary for mapping the opcode to the SB-type instructions
        self.SB_type = {
            '0b1100011': self.BRANCH   # Branch instructions
        }

        # dictionary for mapping the opcode to the U-type instructions
        self.U_type = {
            '0b0110111': self.U_IMM,   # Upper immediate instructions
            '0b0010111': self.U_IMM    # Upper immediate instructions
        }
    
    # fucntion for executing LOAD in the instruction set with given at least 3 registers as its inputs
    def LOAD(self, rd, rs1, imm):
        self.registers[rd] = self.memory[self.registers[rs1] + imm]

    # fucntion for executing STORE in the instruction set with given at least 3 registers as its inputs
    def STORE(self, rs1, rs2, imm):
        self.memory[self.registers[rs1] + imm] = self.registers[rs2]

    # fucntion for executing I_IMM in the instruction set with given at least 2 registers as its inputs and 1 immediate value
    def I_IMM(self, rd, rs1, imm):
        self.registers[rd] = self.ALU.I_IMM(self.registers[rs1], imm, self.opcode)

    # fucntion for executing I_R in the instruction set with given at least 3 registers as its inputs
    def I_R(self, rd, rs1, rs2):
        self.registers[rd] = self.ALU.I_R(self.registers[rs1], self.registers[rs2], self.opcode)

    # fucntion for executing JALR in the instruction set with given at least 3 registers as its inputs
    def JALR(self, rd, rs1, imm):
        self.registers[rd] = self.pc + 4
        self.pc = self.registers[rs1] + imm

    # fucntion for executing R_R in the instruction set with given at least 3 registers as its inputs
    def R_R(self, rd, rs1, rs2):
        self.registers[rd] = self.ALU.R_R(self.registers[rs1], self.registers[rs2], self.opcode)

    # fucntion for executing BRANCH in the instruction set with given at least 3 registers as its inputs
    def BRANCH(self, rs1, rs2, imm):
        self.pc += self.ALU.BRANCH(self.registers[rs1], self.registers[rs2], imm, self.opcode)

    # fucntion for executing U_IMM in the instruction set with given at least 1 register as its inputs and 1 immediate value
    def U_IMM(self, rd, imm):
        self.registers[rd] = self.ALU.U_IMM(imm, self.opcode)