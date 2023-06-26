import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
# sys.path.append(parentdir)

from Register import register
from Memory import memory

# class for simulating the behavior of a microprogrammed CPU
class CPU:
    '''
    initializing processors registers:
    PC: program counter (11 bits)
    AR: address register (11 bits)
    DR: data register (16 bits)
    AC: accumulator (16 bits)
    CAR: control address register (7 bits)
    SBR: subroutine register (7 bits)
    ADR: address register for microprogram memory (7 bits)
    all with default value of zero

    initializing memory:
    main memory (1024 words of 16 bits)
    microprogram memory (128 words of 20 bits)
    all with default value of zero

    initializing fields as dictoinaries (hardwired):
        F1:
            000: None
            001: ADD (AC <- AC + DR)
            010: CLRAC (AC <- 0)
            011: INCAC (AC <- AC + 1)
            100: DRTAC (AC <- DR) 
            101: DRTAR (AR <- DR[10:0])
            110: PCTAR (AR <- PC)
            111: WRITE (M[AR] <- DR)
        F2:
            000: None
            001: SUB (AC <- AC - DR)
            010: OR (AC or DR)
            011: AND (AC and DR)
            100: READ (AC <- M[AR]) 
            101: ACTDR (DR <- AC)
            110: INCDR (DR <- DR + 1)
            111: PCTDR (DR <- PC)
        F3:
            000: None
            --001: XOR (AC xor DR)
            001: MUL (AC <- AC * DR)
            010: COM (AC <- not AC)
            011: SHL (AC <- AC << 1)
            100: SHR (AC <- AC >> 1)
            101: INCPC (PC <- PC + 1)
            110: ARTPC (PC <- AR)
            111: Reserved
        CD:
            00: U (unconditional)
            01: I (indirect, DR(15)) 
            10: S (sign, AC(15))
            11: Z (zero, not AC)
        BR:
                    (condition)  (not condition)
            00: JMP (CAR <- ADR) (CAR <- CAR + 1)
            01: CALL (CAR <- ADR, SBR <- CAR + 1) (CAR <- CAR + 1)
            10: RET (CAR <- SBR)
            11: MAP
    '''
    def __init__(self, start_of_program : str, start_of_microprogram : str) -> None:
        # initializing registers
        self.PC = register('PC', start_of_program, 11)
        self.AR = register('AR', '0b' + '0' * 11, 11)
        self.DR = register('DR', '0b' + '0' * 16, 16)
        self.AC = register('AC', '0b' + '0' * 16, 16)
        self.CAR = register('CAR', start_of_microprogram, 7)
        self.SBR = register('SBR', '0b' + '0' * 7, 7)
        # initializing copy of registers for simultinous change
        self.PC_copy = self.PC.read()
        self.AR_copy = self.AR.read()
        self.DR_copy = self.DR.read()
        self.AC_copy = self.AC.read()
        # initializing memory
        self.main_memory = memory('main_memory', 16, 2048)
        self.microprogram_memory = memory('microprogram_memory', 20, 128)
        # initializing fields
        self.F1 = {'000': 'NOP', '001': 'ADD', '010': 'CLRAC', '011': 'INCAC', '100': 'DRTAC', '101': 'DRTAR', '110': 'PCTAR', '111': 'WRITE'}
        self.F2 = {'000': 'NOP', '001': 'SUB', '010': 'OR', '011': 'AND', '100': 'READ', '101': 'ACTDR', '110': 'INCDR', '111': 'PCTDR'}
        self.F3 = {'000': 'NOP', '001': 'MUL', '010': 'COM', '011': 'SHL', '100': 'SHR', '101': 'INCPC', '110': 'ARTPC', '111': 'HLT'}
        self.CD = {'00': 'U', '01': 'I', '10': 'S', '11': 'Z'}
        self.BR = {'00': 'JMP', '01': 'CALL', '10': 'RET', '11': 'MAP'}
        # initializing fields inside
        self.f1 = '000'
        self.f2 = '000'
        self.f3 = '000'
        self.cd = '00'
        self.br = '00'
        self.ad = '0000000'
        self.condition = False
        # initializing carry bit
        self.carry = '0'
        # initializing flag for fetch state and halt state
        self.fetch_flag = False
        self.halt_flag = False
        self.start_flag = 0
        self.counter = 0

    # function for executing the next microinstruction
    def microexecute(self):
        if self.start_flag == 0:
            self.CAR.write('0b1' + '0' * 6)
            self.start_flag = 1
            self.CAR.reset_writable()
        # reading the microinstruction
        microinstruction = self.microprogram_memory.read(self.CAR.read())[2:]
        # reading the fields
        self.f1 = microinstruction[:3]
        self.f2 = microinstruction[3:6]
        self.f3 = microinstruction[6:9]
        self.cd = microinstruction[9:11]
        self.br = microinstruction[11:13]
        self.ad = microinstruction[13:]
        #_____________________________Testing_____________________________
        print(f'{self.counter}---Microinstruction of line {int(self.CAR.read()[2:], 2)} on execute')
        print(f'f1: {self.F1[self.f1]}, f2: {self.F2[self.f2]}, f3: {self.F3[self.f3]}, cd: {self.CD[self.cd]}, br: {self.BR[self.br]}, ad: {self.ad}')
        self.print_registers()
        #_________________________________________________________________
        # executing the microinstruction
        # checking the first functionality
        if self.f1 == '000':
            self.instruction_NOP()
        elif self.f1 == '001':
            self.instruction_ADD()
        elif self.f1 == '010':
            self.instruction_CLRAC()
        elif self.f1 == '011':
            self.instruction_INCAC()
        elif self.f1 == '100':
            self.instruction_DRTAC()
        elif self.f1 == '101':
            self.instruction_DRTAR()
        elif self.f1 == '110':
            self.instruction_PCTAR()
        elif self.f1 == '111':
            self.instruction_WRITE()
        # checking the second functionality
        if self.f2 == '000':
            self.instruction_NOP()
        elif self.f2 == '001':
            self.instruction_SUB()
        elif self.f2 == '010':
            self.instruction_OR()
        elif self.f2 == '011':
            self.instruction_AND()
        elif self.f2 == '100':
            self.instruction_READ()
        elif self.f2 == '101':
            self.instruction_ACTDR()
        elif self.f2 == '110':
            self.instruction_INCDR()
        elif self.f2 == '111':
            self.instruction_PCTDR()
        # checking the third functionality
        if self.f3 == '000':
            self.instruction_NOP()
        elif self.f3 == '001':
            #self.instruction_XOR()
            self.instruction_MUL()
        elif self.f3 == '010':
            self.instruction_COM()
        elif self.f3 == '011':
            self.instruction_SHL()
        elif self.f3 == '100':
            self.instruction_SHR()
        elif self.f3 == '101':
            self.instruction_INCPC()
        elif self.f3 == '110':
            self.instruction_ARTPC()
        elif self.f3 == '111':
            self.instruction_HLT()
        # checking the condition
        if self.cd == '00':
            self.condition_U()
        elif self.cd == '01':
            self.condition_I()
        elif self.cd == '10':
            self.condition_S()
        elif self.cd == '11':
            self.condition_Z()
        # checking the branch
        if self.br == '00':
            self.branch_JMP()
        elif self.br == '01':
            self.branch_CALL()
        elif self.br == '10':
            self.branch_RET()
        elif self.br == '11':
            self.branch_MAP()
        # resetting registers' flags and memory flags
        self.PC.reset_writable()
        self.AC.reset_writable()
        self.DR.reset_writable()
        self.AR.reset_writable()
        self.CAR.reset_writable()
        self.SBR.reset_writable()
        self.main_memory.reset_writable()
        self.main_memory.reset_readable()
        # control messages and flags
        self.counter += 1
        # settint registers' copies
        self.PC_copy = self.PC.read()
        self.AR_copy = self.AR.read()
        self.DR_copy = self.DR.read()
        self.AC_copy = self.AC.read()
        # setting FETCH flag
        if self.CAR.read() == '0b' + bin(64)[2:].zfill(7):
            self.fetch_flag = True
        else:
            self.fetch_flag = False

    # function for executing next instruction
    def execute(self):
        self.fetch_flag = False
        while not self.fetch_flag and not self.halt_flag:
            self.microexecute()
        print('Instruction executed')
        if self.halt_flag:
            print('Program has finished successfully')

    # function for executing all the program
    def run(self):
        while not self.halt_flag:
            self.execute()

    # _____________ Functionalities, Conditions and Branches (hardwired) _____________
    # function for executing NOP
    def instruction_NOP(self):
        pass

    # _____________ F1 _____________
    # function for executing ADD
    def instruction_ADD(self):
        result = int(self.AC_copy[2:], 2) + int(self.DR_copy[2:], 2)
        result = '0b' + bin(result)[2:].zfill(16)
        self.AC.write(result)
        self.AC.written()

    # function for executing CLRAC
    def instruction_CLRAC(self):
        self.AC.reset()
        self.AC.written()

    # function for executing INCAC
    def instruction_INCAC(self):
        result = int(self.AC_copy[2:], 2) + 1
        result = '0b' + bin(result)[2:].zfill(16)
        self.AC.write(result)
        self.AC.written()

    # function for executing DRTAC
    def instruction_DRTAC(self):
        self.AC.write(self.DR_copy)
        self.AC.written()

    # function for executing DRTAR
    def instruction_DRTAR(self):
        self.AR.write(self.DR_copy)
        self.AR.written()

    # function for executing PCTAR
    def instruction_PCTAR(self):
        self.AR.write(self.PC_copy)
        self.AR.written()

    # function for executing WRITE
    def instruction_WRITE(self):
        self.main_memory.write(self.DR_copy, self.AR_copy)
        self.main_memory.written()

    # _____________ F2 _____________
    # function for executing SUB
    def instruction_SUB(self):
        result = int(self.AC_copy[2:], 2) - int(self.DR_copy[2:], 2)
        result = '0b' + bin(result)[2:].zfill(16)
        self.AC.write(result)
        self.AC.written()
    
    # function for executing OR
    def instruction_OR(self):
        result = int(self.AC_copy[2:], 2) | int(self.DR_copy[2:], 2)
        result = '0b' + bin(result)[2:].zfill(16)
        self.AC.write(result)
        self.AC.written()

    # function for executing AND
    def instruction_AND(self):
        result = int(self.AC_copy[2:], 2) & int(self.DR_copy[2:], 2)
        result = '0b' + bin(result)[2:].zfill(16)
        self.AC.write(result)
        self.AC.written()

    # function for executing READ
    def instruction_READ(self):
        print(f'value of given memory address is {self.main_memory.read(self.AR_copy)}')
        self.DR.write(self.main_memory.read(self.AR_copy))
        self.main_memory.read_flag()
        self.DR.written()

    # function for executing ACTDR
    def instruction_ACTDR(self):
        self.DR.write(self.AC_copy)
        self.DR.written()

    # function for executing INCDR
    def instruction_INCDR(self):
        result = int(self.DR_copy[2:], 2) + 1
        result = '0b' + bin(result)[2:].zfill(16)
        self.DR.write(result)
        self.DR.written()

    # function for executing PCTDR
    def instruction_PCTDR(self):
        self.DR.write(self.PC_copy)
        self.DR.written()

    # _____________ F3 _____________    
    # function for executing XOR
    # def instruction_XOR(self):
    #     result = int(self.AC_copy[2:], 2) ^ int(self.DR_copy[2:], 2)
    #     result = '0b' + bin(result)[2:].zfill(16)
    #     self.AC.write(result)
    #     self.AC.written()

    # function for executing MUL
    def instruction_MUL(self):
        result = int(self.AC_copy[2:], 2) * int(self.DR_copy[2:], 2)
        result = '0b' + bin(result)[2:].zfill(16)
        self.AC.write(result)
        self.AC.written()

    # function for executing COM
    def instruction_COM(self):
        result = self.AC_copy[2:]
        for bit in range(len(result)):
            if result[bit] == '0':
                result = result[:bit] + '1' + result[bit+1:]
            else:
                result = result[:bit] + '0' + result[bit+1:]
        print(f'complement of AC is {result}')
        result = '0b' + str(result).zfill(16)
        self.AC.write(result)
        self.AC.written()

    # function for executing SHL
    def instruction_SHL(self):
        temp_carry = self.carry
        result = self.AC_copy[2:]
        self.carry = result[0]
        result = '0b' + result[1:] + temp_carry
        self.AC.write(result)
        self.AC.written()

    # function for executing SHR
    def instruction_SHR(self):
        temp_carry = self.carry
        result = self.AC_copy[2:]
        self.carry = result[-1]
        result = '0b' + temp_carry + result[:-1]
        self.AC.write(result)
        self.AC.written()

    # function for executing INCPC
    def instruction_INCPC(self):
        result = int(self.PC_copy[2:], 2) + 1
        result = '0b' + bin(result)[2:].zfill(11)
        self.PC.write(result)
        self.PC.written()

    # function for executing ARTPC
    def instruction_ARTPC(self):
        self.PC.write(self.AR_copy)
        self.PC.written()

    # function for executing HLT
    def instruction_HLT(self):
        self.halt_flag = True

    # _____________ CD _____________
    # function for executing U
    def condition_U(self):
        self.condition = True

    # function for executing I
    def condition_I(self):
        if self.DR_copy[2] == '1':
            self.condition = True
        else:
            self.condition = False

    # function for executing S
    def condition_S(self):
        if self.AC_copy[2] == '1':
            self.condition = True
        else:
            self.condition = False

    # function for executing Z
    def condition_Z(self):
        if self.AC_copy == '0b' + '0' * 16:
            self.condition = True
        else:
            self.condition = False

    # _____________ BR _____________
    # function for executing JMP
    def branch_JMP(self):
        if self.condition:
            self.CAR.write('0b' + self.ad)
            self.CAR.written()
        else:
            result = int(self.CAR.read()[2:], 2) + 1
            result = '0b' + bin(result)[2:].zfill(7)
            self.CAR.write(result)
            self.CAR.written()

    # function for executing CALL
    def branch_CALL(self):
        if self.condition:
            result = int(self.CAR.read()[2:], 2) + 1
            print(f'value of result: {result}')
            result = '0b' + bin(result)[2:].zfill(7)
            self.SBR.write(result)
            print(f'value {self.SBR.read()} is in SBR for returning, value of result: {result}, value of CAR: {self.CAR.read()}')
            self.SBR.written()
            self.CAR.write('0b' + self.ad)
            self.CAR.written()
        else:
            result = int(self.CAR.read()[2:], 2) + 1
            result = '0b' + bin(result)[2:].zfill(7)
            self.CAR.write(result)
            self.CAR.written()

    # function for executing RET
    def branch_RET(self):
        self.CAR.write(self.SBR.read())
        print(f'returned to {self.CAR.read()}, value of SBR: {self.SBR.read()}')
        self.CAR.written()

    # function for executing MAP
    def branch_MAP(self):
        result = '0b' + self.DR.read()[2:][::-1][11:15][::-1] + '00'
        print(f'mapped {self.DR.read()} to {result}')
        self.CAR.write(result)
        self.CAR.written()

    # fucntion to chaeck if the value is in binary format
    def check_binary(self, value : str) -> bool:
        if value[:2] != '0b':
            return False
        for i in value[2:]:
            if i != '0' and i != '1':
                return False
        return True

    # function to print value of all registers in decimal
    def print_registers(self):
        print(f'AC:  {self.AC.read()}, {int(self.AC.read()[2:], 2)}')
        print(f'PC:  {self.PC.read()},      {int(self.PC.read()[2:], 2)}')
        print(f'AR:  {self.AR.read()},      {int(self.AR.read()[2:], 2)}')
        print(f'DR:  {self.DR.read()}, {int(self.DR.read()[2:], 2)}')
        print(f'CAR: {self.CAR.read()},          {int(self.CAR.read()[2:], 2)}')
        print(f'SBR: {self.SBR.read()},          {int(self.SBR.read()[2:], 2)}')

    # function that returns the value of all registers in both binary and decimal alligned in a dictionary
    def get_registers(self) -> dict:
        return {
            'AC': [self.AC.read(), int(self.AC.read()[2:], 2)],
            'PC': [self.PC.read(), int(self.PC.read()[2:], 2)],
            'AR': [self.AR.read(), int(self.AR.read()[2:], 2)],
            'DR': [self.DR.read(), int(self.DR.read()[2:], 2)],
            'CAR': [self.CAR.read(), int(self.CAR.read()[2:], 2)],
            'SBR': [self.SBR.read(), int(self.SBR.read()[2:], 2)]
        }

    def get_memory(self) -> dict:
        return {
            str(i).zfill(4) : [self.main_memory.depository[i].read(), int(self.main_memory.depository[i].read() ,2)] for i in range(self.main_memory.height) 
        }

    def get_microprogram_memory(self) -> dict:
        return {
            str(i).zfill(3) : [self.microprogram_memory.depository[i].read(), int(self.microprogram_memory.depository[i].read() ,2)] for i in range(self.microprogram_memory.height)
        }