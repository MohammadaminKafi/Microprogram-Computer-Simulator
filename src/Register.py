# class for simulating register in a processor
# note that all the values must set in binary with format '0bxx..x'
class register:

    # initializing with name, initial value in binary (saved as string and default is 0) and width (default is 16)
    def __init__(self, name : str, value : str = '0b0', width : int = 16) -> None:
        self.name = name
        # if the value is not in binary format, raise an error, else set the value
        if not self.check_binary(value):
            raise ValueError('The value must be in binary format: ' + value)
        self.value = value
        self.width = width
        self.writable = True # if false, already has been written in current clock pulse

    # fucntion to chaeck if the value is in binary format
    def check_binary(self, value : str) -> bool:
        if value[:2] != '0b':
            return False
        for i in value[2:]:
            if i != '0' and i != '1':
                return False
        return True

    # function to write a value in the register from to the given i-th and j-th index of the register with defualt values i = 0 and j = width
    def write(self, value : str, i : int = 0, j : int = None) -> None:
        if not self.writable:
            raise ValueError('The register is double-written in this clock pulse')
        if j is None:
            j = self.width - 1
        # checking if the value is in binary format
        if not self.check_binary(value):
            raise ValueError('The value must be in binary format: ' + value)
        # checking if i and j are valid
        if i < 0 or j > self.width - 1 or i > j:
            raise ValueError('Invalid range')
        # setting the value
        value = value[2:][::-1]
        self.value = self.value[2:][::-1] # n bits
        if len(value) < j - i + 1:
            value += '0' * (j - i + 1 - len(value))
        elif len(value) > j - i + 1:
            value = value[:j - i + 1]
        self.value = '0b' + (self.value[:i] + value + self.value[j + 1:])[::-1]
            
    # function to read the value in the register
    def read(self) -> str:
        return self.value

    # function to get the name of the register
    def get_name(self) -> str:
        return self.name
    
    # function to get the width of the register
    def get_width(self) -> int:
        return self.width

    # function to reset the value of the register to 0
    def reset(self) -> None:
        self.value = '0b' + '0' * self.width

    # function to set the write flag to written
    def written(self) -> None:
        self.writable = False

    def reset_writable(self) -> None:
        self.writable = True


    

if __name__ == '__main__':
    r1 = register('r1', '0b00001111', 8)
    print(r1.read())
    r1.write('0b11111111', 0, 7)
    print(r1.read())
    r1.reset()
    print(r1.read())
    r1.write('0b11111111', 0, 5)
    print(r1.read())
    r1.reset()
    r1.write('0b11111111', 7, 7)
    print(r1.read())
    print(r1.get_name())
    print(r1.get_width())
    