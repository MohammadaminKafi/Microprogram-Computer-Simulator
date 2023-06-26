from ManoMicroprogramCPU import CPU

# class for simulating a programmer for the Mano microprogrammed CPU
class programmer:
    # initializing the programmer with a given processor, which is a Mano CPU, and list of instructions
    def __init__(self, processor : CPU, main_program : dict, microprogram : dict) -> None:
        self.processor = processor
        self.main_program = main_program
        self.microprogram = microprogram

    # function for loading the program into the main memory of the processor
    def load_program(self) -> None:
        for key in self.main_program.keys():
            self.processor.main_memory.write('0b' + self.main_program[key], '0b' + bin(key)[2:].zfill(11))
            #print(f'writing {self.main_program[key]} to {key}')
            
    # function for loading the microprogram into the microprogram memory of the processor
    def load_microprogram(self) -> None:
        for key in self.microprogram.keys():
            self.processor.microprogram_memory.write('0b' + self.microprogram[key], '0b' + bin(key)[2:].zfill(7))
            #print(f'writing {self.main_program[key]} to {key}')
    
    def load_all(self) -> None:
        self.load_program()
        self.load_microprogram()