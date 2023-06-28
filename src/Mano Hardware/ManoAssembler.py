# two classes is in this file, one for main program assembly and one for microprogram assembly

# calss for simulating the Mano assembler
class Assembler:
    # initializing assembly code, machine code, first and second pass tables
    # also dictionaries of OPCodes are needed in initialization
    def __init__(self, assembly_code: list, OPCode : dict) -> None:
        self.assembly_code = assembly_code
        #self.machine_code = []
        self.first_pass_table = {}
        self.second_pass_table = {}
        self.OPCode = OPCode
        self.start_of_program = '0b' + bin(0)[2:].zfill(11)
        self.lfirst = 1

    # function for assembler first pass to extract labels and their addresses
    def first_pass(self) -> None:
        # initializing line counter
        lc = 0
        # iterating over assembly code
        for line in self.assembly_code:
            if len(self.assembly_code) == self.lfirst:
                break
            if line == [] or line[0][0] == '#':
                self.lfirst += 1
                continue
            # if line is label
            if line[0][-1] == ',':
                # check if label is already in first pass table
                if line[0][:-1] in self.first_pass_table:
                    raise Exception(f'Label of line {str(self.lfirst)} is already defined in memory location {self.first_pass_table[line[0][:-1]]}: {line[0][:-1]}')
                # check if label is out of range
                if lc > 2047:
                    raise Exception(f'Label of line {str(self.lfirst)} is out of memory range: {line[0][:-1]}')
                # check if location of label is already defined
                if lc in self.first_pass_table.values():
                    raise Exception(f'Location of label of line {str(self.lfirst)} is already reserved in memory location by label {list(self.first_pass_table.keys())[list(self.first_pass_table.values()).index(lc)]}: {line[0][:-1]}') 
                # add label to first pass table together with the line number
                self.first_pass_table[line[0][:-1]] = lc
                lc += 1
                self.lfirst += 1
            # if line is not label
            else:
                # if line is ORG
                if line[0] == 'ORG':
                    # change line counter to the value of ORG
                    lc = int(line[1])
                # if line is END
                elif line[0] == 'END':
                    break
                # if line is not ORG or END, increment line counter
                else:
                    lc += 1
                self.lfirst += 1

    # function for assembler second pass to extract second pass table
    def second_pass(self) -> None:
        I = 0
        op = 0
        addr = 0
        # initializing line counter
        lc = 0
        l = 1
        # iterating over assembly code
        for line in self.assembly_code:
            if line == [] or line[0][0] == '#':
                l += 1
                continue
            # if line is psuedo instruction (ORG, END, DEC, HEX, BIN)
            if line[0] == 'ORG':
                # change line counter to the value of ORG
                lc = int(line[1]) - 1
            elif line[0] == 'END':
                break
            elif line[0][-1] == ',':
                if line[1] == 'DEC':
                    self.second_pass_table[self.first_pass_table[line[0][:-1]]] = bin(int(line[2]))[2:].zfill(16)
                elif line[1] == 'HEX':
                    self.second_pass_table[self.first_pass_table[line[0][:-1]]] = bin(int(line[2], 16))[2:].zfill(16)
                elif line[1] == 'BIN':
                    self.second_pass_table[self.first_pass_table[line[0][:-1]]] = line[2].zfill(16)
            # if line is not psuedo instruction
            # if line contains label
            if line[0][-1] == ',':
                if line[1] == 'DEC' or line[1] == 'HEX' or line[1] == 'BIN':
                    pass
                else:
                    # extract opcode from OPCode dictionary
                    if line[1] in self.OPCode:
                        op = bin(self.OPCode[line[1]] // 4)[2:].zfill(4)
                    else:
                        raise Exception('Invalid OPCode near line ' + str(l) + ' ' + line[1])
                    # extracting address
                    if len(line) == 2:
                        addr = '0' * 11
                    elif len(line) == 3:
                        if line[2] in self.first_pass_table.keys():
                            addr = bin(self.first_pass_table[line[2]])[2:].zfill(11)
                        else:
                            raise Exception('Invalid Address near line ' + str(l) + ' ' + line[2])
                        I = '0'
                    elif len(line) == 4:
                        if line[2] in self.first_pass_table.keys():
                            addr = bin(self.first_pass_table[line[2]])[2:].zfill(11)
                        else:
                            raise Exception('Invalid Address near line ' + str(l) + ' ' + line[2])
                        if line[3] == 'I':
                            I = '1'
                        else:
                            raise Exception('Invalid I near line ' + str(l) + ' ' + line[3])
                    self.second_pass_table[lc] = I + op + addr
            # if line does not contain label
            elif line[0] == 'ORG' or line[0] == 'END':
                pass
            else:
                # extract opcode from OPCode dictionary
                if line[0] in self.OPCode:
                    op = bin(self.OPCode[line[0]] // 4)[2:].zfill(4)
                else:
                    raise Exception('Invalid OPCode near line ' + str(l) + ' ' + line[0])
                # extracting address
                if len(line) == 1:
                    addr = '0' * 11
                elif len(line) == 2:
                    if line[1] in self.first_pass_table.keys():
                        addr = bin(self.first_pass_table[line[1]])[2:].zfill(11)
                    else:
                        raise Exception('Invalid Address near line ' + str(l) + ' ' + line[1])
                    I = '0'
                elif len(line) == 3:
                    if line[1] in self.first_pass_table.keys():
                        addr = bin(self.first_pass_table[line[1]])[2:].zfill(11)
                    else:
                        raise Exception('Invalid Address near line ' + str(l) + ' ' + line[1])
                    if line[2] == 'I':
                        I = '1'
                    else:
                        raise Exception('Invalid I near line ' + str(l) + ' ' + line[2])
                self.second_pass_table[lc] = I + op + addr
            lc += 1
            l += 1

    # fucntion to determine the starting address of the program
    def determine_starting_address(self) -> str:
        if 'MAIN' in self.first_pass_table.keys():
            self.start_of_program = '0b' + bin(self.first_pass_table['MAIN'])[2:].zfill(11)
            print('MAIN found at address ' + str(self.start_of_program) + ' (decimal: ' + str(int(self.start_of_program, 2)) + ')')
        else:
            self.start_of_program = '0b' + bin(100)[2:].zfill(11)
            print('MAIN not found, starting address set to ' + str(self.start_of_program) + ' (decimal: ' + str(int(self.start_of_program, 2)) + ')')
            #raise Exception('No MAIN function found')    

    # function to assemble assembly code
    def assemble(self) -> None:
        self.first_pass()
        self.second_pass()
        self.determine_starting_address()

    # function to return first pass table
    def get_first_pass_table(self) -> dict:
        return self.first_pass_table

    # function to return second pass table
    def get_second_pass_table(self) -> dict:
        return self.second_pass_table


       
# class for simulating the Mano microprogram assembler
# given list must contain one microprogram assembly code per line (splitted)
class MicroAssembler:
    # initializing assembly code, machine code and first and second pass tables
    def __init__(self, assembly_code: list) -> None:
        self.assembly_code = assembly_code
        #self.machine_code = []
        self.first_pass_table = {}
        self.second_pass_table = {}
        self.F1 = {'NOP': '000', 'ADD': '001', 'CLRAC': '010', 'INCAC': '011', 'DRTAC': '100', 'DRTAR': '101', 'PCTAR': '110', 'WRITE': '111'}
        self.F2 = {'NOP': '000', 'SUB': '001', 'OR': '010', 'AND': '011', 'READ': '100', 'ACTDR': '101', 'INCDR': '110', 'PCTDR': '111'}
        self.F3 = {'NOP': '000', 'MUL': '001', 'COM': '010', 'SHL': '011', 'SHR': '100', 'INCPC': '101', 'ARTPC': '110', 'HLT': '111'}
        self.CD = {'U': '00', 'I': '01', 'S': '10', 'Z': '11'}
        self.BR = {'JMP': '00', 'CALL': '01', 'RET': '10', 'MAP': '11'}
        self.start_of_microprogram = '0b' + bin(0)[2:].zfill(7)
        self.lfirst = 1

    # function for assembler first pass to extract labels and their addresses
    def first_pass(self) -> None:
        # initializing line counter
        lc = 0
        # iterating over assembly code
        for line in self.assembly_code:
            if len(self.assembly_code) == self.lfirst:
                break
            if line == [] or line[0][0] == '#':
                self.lfirst += 1
                continue
            # if line is label
            if line[0][-1] == ':':
                # check if label is already in first pass table
                if line[0][:-1] in self.first_pass_table:
                    raise Exception(f'Label of line {str(self.lfirst)} is already defined in microprogram memory location {self.first_pass_table[line[0][:-1]]}: {line[0][:-1]}')
                # check if the location is not out of range
                if lc > 127:
                    raise Exception(f'Label of line {str(self.lfirst)} is out of microprogram memory range: {line[0][:-1]}')
                # check if location is not already reserved
                if lc in self.first_pass_table.values():
                    raise Exception(f'Label of line {str(self.lfirst)} is already reserved in microprogram memory location by label {list(self.first_pass_table.keys())[list(self.first_pass_table.values()).index(lc)]}: {line[0][:-1]}')
                # add label to first pass table together with the value of line counter
                self.first_pass_table[line[0][:-1]] = lc
                lc += 1
                self.lfirst += 1
            # if line is not label
            else:
                # if line is ORG
                if line[0] == 'ORG':
                    # change line counter to the value of ORG
                    lc = int(line[1])
                # if line is END
                elif line[0] == 'END':
                    break
                # if line is not ORG or END, increment line counter
                else:
                    lc += 1
                self.lfirst += 1

    # function for assembler second pass to convert assembly code to machine code
    def second_pass(self) -> None:
        field1 = 0
        field2 = 0
        field3 = 0
        fieldcd = 0
        fieldbr = 0
        fieldaddr = 0
        # initializing line counter and line value
        l = 1
        lc = 0
        # iterating over assembly code
        for line in self.assembly_code:
            if line == [] or line[0][0] == '#':
                l += 1
                continue
            # if line is psuedo instruction (ORG, END, DEC, HEX, BIN)
            if line[0] == 'ORG':
                # change line counter to the value of ORG
                lc = int(line[1]) - 1
            elif line[0] == 'END':
                break
            elif line[0][-1] == ':':
                if line[1] == 'DEC':
                    self.second_pass_table[first_pass_table[line[0][:-1]]] = bin(int(line[2]))[2:].zfill(20)
                elif line[1] == 'HEX':
                    self.second_pass_table[first_pass_table[line[0][:-1]]] = bin(int(line[2], 16))[2:].zfill(20)
                elif line[1] == 'BIN':
                    self.second_pass_table[first_pass_table[line[0][:-1]]] = line[2].zfill(20)
            # if line is not psuedo instruction
            # if line contains label
            if line[0][-1] == ':':
                if line[1] == 'DEC' or line[1] == 'HEX' or line[1] == 'BIN':
                    pass
                else:
                    line[1] = line[1].split(',')
                    # checking function fields
                    if len(line[1]) == 1:
                        if line[1][0] in self.F1:
                            field1 = self.F1[line[1][0]]
                            field2 = '000'
                            field3 = '000'
                        elif line[1][0] in self.F2:
                            field1 = '000'
                            field2 = self.F2[line[1][0]]
                            field3 = '000'
                        elif line[1][0] in self.F3:
                            field1 = '000'
                            field2 = '000'
                            field3 = self.F3[line[1][0]]
                        else:
                            raise Exception('Invalid function field near line ' + str(l) + ': ' + line[1][0])
                    elif len(line[1]) == 2:
                        if line[1][0] in self.F1 and line[1][1] in self.F2:
                            field1 = self.F1[line[1][0]]
                            field2 = self.F2[line[1][1]]
                            field3 = '000'
                        elif line[1][0] in self.F2 and line[1][1] in self.F1:
                            field1 = self.F1[line[1][1]]
                            field2 = self.F2[line[1][0]]
                            field3 = '000'
                        elif line[1][0] in self.F1 and line[1][1] in self.F3:
                            field1 = self.F1[line[1][0]]
                            field2 = '000'
                            field3 = self.F3[line[1][1]]
                        elif line[1][0] in self.F3 and line[1][1] in self.F1:
                            field1 = self.F1[line[1][1]]
                            field2 = '000'
                            field3 = self.F3[line[1][0]]
                        elif line[1][0] in self.F2 and line[1][1] in self.F3:
                            field1 = '000'
                            field2 = self.F2[line[1][0]]
                            field3 = self.F3[line[1][1]]
                        elif line[1][0] in self.F3 and line[1][1] in self.F2:
                            field1 = '000'
                            field2 = self.F2[line[1][1]]
                            field3 = self.F3[line[1][0]]
                        else:
                            raise Exception('Invalid function field near line ' + str(l) + ': ' + line[1][0] + ',' + line[1][1])
                    elif len(line[1]) == 3:
                        if line[1][0] in self.F1 and line[1][1] in self.F2 and line[1][2] in self.F3:
                            field1 = self.F1[line[1][0]]
                            field2 = self.F2[line[1][1]]
                            field3 = self.F3[line[1][2]]
                        elif line[1][0] in self.F1 and line[1][1] in self.F3 and line[1][2] in self.F2:
                            field1 = self.F1[line[1][0]]
                            field2 = self.F2[line[1][2]]
                            field3 = self.F3[line[1][1]]
                        elif line[1][0] in self.F2 and line[1][1] in self.F1 and line[1][2] in self.F3:
                            field1 = self.F1[line[1][1]]
                            field2 = self.F2[line[1][0]]
                            field3 = self.F3[line[1][2]]
                        elif line[1][0] in self.F2 and line[1][1] in self.F3 and line[1][2] in self.F1:
                            field1 = self.F1[line[1][2]]
                            field2 = self.F2[line[1][0]]
                            field3 = self.F3[line[1][1]]
                        elif line[1][0] in self.F3 and line[1][1] in self.F1 and line[1][2] in self.F2:
                            field1 = self.F1[line[1][1]]
                            field2 = self.F2[line[1][2]]
                            field3 = self.F3[line[1][0]]
                        elif line[1][0] in self.F3 and line[1][1] in self.F2 and line[1][2] in self.F1:
                            field1 = self.F1[line[1][2]]
                            field2 = self.F2[line[1][1]]
                            field3 = self.F3[line[1][0]]
                        else:
                            raise Exception('Invalid function field near line ' + str(l) + ': ' + line[1][0] + ',' + line[1][1] + ',' + line[1][2])
                    # checking condition field
                    if line[2] in self.CD:
                        fieldcd = self.CD[line[2]]
                    else:
                        raise Exception('Invalid condition field near line ' + str(l) + ': ' + line[2])
                    # checking branch field
                    if line[3] in self.BR:
                        fieldbr = self.BR[line[3]]
                    else:
                        raise Exception('Invalid branch field near line ' + str(l) + ': ' + line[3])
                    # checking address field
                    if len(line) == 4:
                        fieldaddr = '0000000'
                    elif line[4] == "NEXT":
                        fieldaddr = bin(lc + 1)[2:].zfill(7)
                    elif line[4] in self.first_pass_table:
                        fieldaddr = bin(self.first_pass_table[line[4]])[2:].zfill(7)
                    else:
                        raise Exception('Invalid address field near line ' + str(l) + ': ' + line[4])
                    # adding machine code to second pass table
                    self.second_pass_table[lc] = field1 + field2 + field3 + fieldcd + fieldbr + fieldaddr
            # if line does not contain label
            elif line[0] == 'ORG' or line[0] == 'END':
                pass
            else:
                line[0] = line[0].split(',')
                # checking function fields
                if len(line[0]) == 1:
                    if line[0][0] in self.F1:
                        field1 = self.F1[line[0][0]]
                        field2 = '000'
                        field3 = '000'
                    elif line[0][0] in self.F2:
                        field1 = '000'
                        field2 = self.F2[line[0][0]]
                        field3 = '000'
                    elif line[0][0] in self.F3:
                        field1 = '000'
                        field2 = '000'
                        field3 = self.F3[line[0][0]]
                    else:
                        raise Exception('Invalid function field near line ' + str(l) + ': ' + line[0][0])
                elif len(line[0]) == 2:
                    if line[1][0] in self.F1 and line[1][1] in self.F2:
                        field1 = self.F1[line[0][0]]
                        field2 = self.F2[line[0][1]]
                        field3 = '000'
                    elif line[1][0] in self.F2 and line[1][1] in self.F1:
                        field1 = self.F1[line[0][1]]
                        field2 = self.F2[line[0][0]]
                        field3 = '000'
                    elif line[1][0] in self.F1 and line[1][1] in self.F3:
                        field1 = self.F1[line[0][0]]
                        field2 = '000'
                        field3 = self.F3[line[0][1]]
                    elif line[1][0] in self.F3 and line[1][1] in self.F1:
                        field1 = self.F1[line[0][1]]
                        field2 = '000'
                        field3 = self.F3[line[0][0]]
                    elif line[1][0] in self.F2 and line[1][1] in self.F3:
                        field1 = '000'
                        field2 = self.F2[line[0][0]]
                        field3 = self.F3[line[0][1]]
                    elif line[1][0] in self.F3 and line[1][1] in self.F2:
                        field1 = '000'
                        field2 = self.F2[line[0][1]]
                        field3 = self.F3[line[0][0]]
                    else:
                        raise Exception('Invalid function field near line ' + str(l) + ': ' + line[0][0])
                elif len(line[0]) == 3:
                    if line[0][0] in self.F1 and line[0][1] in self.F2 and line[0][2] in self.F3:
                        field1 = self.F1[line[0][0]]
                        field2 = self.F2[line[0][1]]
                        field3 = self.F3[line[0][2]]
                    elif line[0][0] in self.F1 and line[0][1] in self.F3 and line[0][2] in self.F2:
                        field1 = self.F1[line[0][0]]
                        field2 = self.F2[line[0][2]]
                        field3 = self.F3[line[0][1]]
                    elif line[0][0] in self.F2 and line[0][1] in self.F1 and line[0][2] in self.F3:
                        field1 = self.F1[line[0][1]]
                        field2 = self.F2[line[0][0]]
                        field3 = self.F3[line[0][2]]
                    elif line[0][0] in self.F2 and line[0][1] in self.F3 and line[0][2] in self.F1:
                        field1 = self.F1[line[0][2]]
                        field2 = self.F2[line[0][0]]
                        field3 = self.F3[line[0][1]]
                    elif line[0][0] in self.F3 and line[0][1] in self.F1 and line[0][2] in self.F2:
                        field1 = self.F1[line[0][1]]
                        field2 = self.F2[line[0][2]]
                        field3 = self.F3[line[0][0]]
                    elif line[0][0] in self.F3 and line[0][1] in self.F2 and line[0][2] in self.F1:
                        field1 = self.F1[line[0][2]]
                        field2 = self.F2[line[0][1]]
                        field3 = self.F3[line[0][0]]
                    else:
                        raise Exception('Invalid function field near line ' + str(l) + ': ' + line[0][0])
                # checking condition field
                if line[1] in self.CD:
                    fieldcd = self.CD[line[1]]
                else:
                    raise Exception('Invalid condition field near line ' + str(l) + ': ' + line[1])
                # checking branch field
                if line[2] in self.BR:
                    fieldbr = self.BR[line[2]]
                else:
                    raise Exception('Invalid branch field near line ' + str(l) + ': ' + line[2])
                # checking address field
                if len(line) == 3:
                    fieldaddr = '0000000'
                elif line[3] == 'NEXT':
                    fieldaddr = bin(lc + 1)[2:].zfill(7)
                elif line[3] in self.first_pass_table:
                    fieldaddr = bin(self.first_pass_table[line[3]])[2:].zfill(7)
                else:
                    raise Exception('Invalid address field near line ' + str(l) + ': ' + line[3])
                # adding machine code to second pass table
                self.second_pass_table[lc] = field1 + field2 + field3 + fieldcd + fieldbr + fieldaddr
            lc += 1
            l += 1

    # function to determine the start of the microprogram, which is FETCH
    def determine_starting_address(self) -> str:
        if 'FETCH' in self.first_pass_table.keys():
            self.start_of_program = '0b' + bin(self.first_pass_table['FETCH'])[2:].zfill(7)
            print('FETCH found at address ' + str(self.start_of_program) + ' (decimal: ' + str(int(self.start_of_program, 2)) + ')')
        else:
            self.start_of_program = '0b' + bin(64)[2:].zfill(7)
            print('FETCH not found! Starting address is ' + str(self.start_of_program) + ' (decimal: ' + str(int(self.start_of_program, 2)) + ')')
            #raise Exception('No FETCH function found')

    # function to assemble the code
    def assemble(self):
        self.first_pass()
        self.second_pass()
        self.determine_starting_address()

    # function to return the first pass table
    def get_first_pass_table(self):
        return self.first_pass_table

    # function to return the second pass table
    def get_second_pass_table(self):
        return self.second_pass_table