from Register import register
from math import log2
# class for simulating memory behavior in a computer
# note that all the values must set in binary with format '0bxx..x'
class memory:
    '''
    initilizing with name, width of a word (default is 16) and height of the memory (default is 1024)
    also there is an optional part for memory being dual ported (defualt is False)
    '''
    def __init__(self, name : str, word_width : int = 16, height : int = 1024, dual_port : bool = False) -> None:
        self.name = name
        self.width = word_width
        # checking if the height is a power of 2
        if log2(height) != int(log2(height)):
            raise ValueError(f'The height of {self.name} must be a power of 2: ' + height)
        self.height = height
        self.number_of_address_bits = log2(height)
        self.dual_port = dual_port
        # initializing the memory with all zeros
        self.depository = [register('cell' + str(i), '0b' + '0' * self.width, self.width) for i in range(self.height)]
        self.writable = True 
        self.readable = True

    # (if the memory is not dual ported) function to write a value in the word of the momory to the given address in binary
    def write(self, value : str, address : str) -> None:
        if not self.writable:
            raise ValueError(f'The {self.name} port is already in use in this clock pulse')
        # value will be checked in the register write function
        # checking if the address is in binary format
        if not self.check_binary(address):
            raise ValueError('The address must be in binary format: ' + address)
        # checking if the address is valid
        if len(address[2:]) != self.number_of_address_bits:
            raise ValueError(f'The address must be {self.number_of_address_bits} bits: ' + address)
        # setting the value
        self.depository[int(address[2:], 2)].write(value)
        # print(f'writing {value} to {int(address[2:], 2)}')
        # print(self.depository[int(address[2:], 2)].read())

    # (if the memory is not dual ported) function to read a value from the word of the memory from the given address in binary
    def read(self, address : str) -> str:
        if not self.readable:
            raise ValueError(f'The {self.name} port is already in use in this clock pulse')
        # checking if the address is in binary format
        if not self.check_binary(address):
            raise ValueError('The address must be in binary format: ' + address)
        # checking if the address is valid
        if len(address[2:]) != self.number_of_address_bits:
            raise ValueError(f'The address must be {self.number_of_address_bits} bits: ' + address)
        # reading the value
        return self.depository[int(address[2:], 2)].read()


    # (if the memory is dual ported) function to read/write a value according to flags r/w for each port using address_r for read and address_w for write
    def read_write(self, value : str, address_r : str, address_w : str, r : bool, w : bool) -> str:
        # checking if the memory is dual ported
        if self.dual.port:
            # value will be checked in the register write function
            # addresses will be checked in the read and write functions
            if w:
                self.write(value, address_w)
            if r:
                return self.read(address_r)

    # function to set the write flag to written
    def written(self) -> None:
        self.writable = False
        if not self.dual_port:
            self.readable = False

    def reset_writable(self) -> None:
        self.writable = True

    # function to set the read flag to read
    def read_flag(self) -> None:
        self.readable = False
        if not self.dual_port:
            self.writable = False

    def reset_readable(self) -> None:
        self.readable = True
        
    # fucntion to chaeck if the value is in binary format
    def check_binary(self, value : str) -> bool:
        if value[:2] != '0b':
            return False
        for i in value[2:]:
            if i != '0' and i != '1':
                return False
        return True

    #function to create the dictionary of the number of memory cell and its value
    def get_memory(self) -> dict:
        return {i : [self.depository[i].read(), int(self.depository[i].read()[2:], 2)] for i in range(self.height)}


if __name__ == '__main__':
    m1 = memory('m1', 16, 1024)
    m1.write('0b1010101010101011', '0b0000000000')
    print(m1.depository[0].read())
    print(m1.depository[956].get_name())
        