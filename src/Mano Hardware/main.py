import os

from ManoAssembler import MicroAssembler, Assembler
from ManoMicroprogramCPU import CPU
from ManoProgrammer import programmer

# extracting code
assembly_program = open('sample_factorial_program.txt', 'r').read().split('\n')
for i in range(len(assembly_program)):
    assembly_program[i] = assembly_program[i].split()

assembly_microprogram = open('sample_factorial_microprogram.txt', 'r').read().split('\n')
for i in range(len(assembly_microprogram)):
    assembly_microprogram[i] = assembly_microprogram[i].split()

 
# assembling code
microassembler = MicroAssembler(assembly_microprogram)
microassembler.assemble()
assembler = Assembler(assembly_program, microassembler.get_first_pass_table())
assembler.assemble()

print("Programs assembled successfully")

for item in assembler.second_pass_table.keys():
    print(item, assembler.second_pass_table[item])
for item in assembler.first_pass_table.keys():
    print(item, assembler.first_pass_table[item])
for item in microassembler.second_pass_table.keys():
    print(item, microassembler.second_pass_table[item])
for item in microassembler.first_pass_table.keys():
    print(item, microassembler.first_pass_table[item])

pritn("-------------------------------------------------------------------")

# initializing processor
processor = CPU(assembler.start_of_program, microassembler.start_of_microprogram)

# loading program to memory 
programmer = programmer(processor, assembler.get_second_pass_table(), microassembler.get_second_pass_table())
programmer.load_program()
programmer.load_microprogram()

print("Programs loaded successfully")
print("-------------------------------------------------------------------")

while True:
    print("Enter 1 to run one microinstruction, 2 to run one instruction, 3 ro run till halt")
    choice = int(input())
    if choice == 1:
        processor.microexecute()
    elif choice == 2:
        processor.execute()
    elif choice == 3:
        processor.run()
        break