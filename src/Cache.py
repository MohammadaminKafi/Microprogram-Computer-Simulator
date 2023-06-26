# class for simulating Cache
class cache:
    def __init__(self, number_of_layers : int = 1,
                cache_size : int = 1024,
                block_size : int = 32,
                word_width : int = 32,
                associativity : bool = True, # True -> Set Associative, False -> Direct Mapped
                replacement_policy : str = "LRU", # RR -> Random Replacement, LRU -> Least Recently Used, FIFO -> First In First Out, LFU -> Least Frequently Used
                write_policy : str = "WBWA" # WBWA -> Write-Back with Write Allocate, WTh -> Write-Through, WAr -> Write-Around, WNA -> Write-No-Allocate
                ):
        self.replacement_policies = ["RR", "LRU", "FIFO", "LFU"]
        self.write_policies = ["WBWA", "WTh", "WAr", "WNA"]
        # check if number of layers is valid
        if number_of_layers < 1:
            raise ValueError("Number of layers must be at least 1")
        elif number_of_layers > 3:
            raise ValueError("Number of layers must be at most 3")
        else:
            self.number_of_layers = number_of_layers
        # check if cache size is a power of 2
        if (cache_size & (cache_size - 1)) != 0:
            raise ValueError("Cache size must be a power of 2")
        else:
            self.cache_size = cache_size
        # check if block size is a power of 2
        if (block_size & (block_size - 1)) != 0:
            raise ValueError("Block size must be a power of 2")
        else:
            self.block_size = block_size
        self.number_of_blocks = self.cache_size // self.block_size
        self.word_width = word_width
        self.associativity = associativity
        # check if replacement policy is valid
        if replacement_policy not in self.replacement_policies:
            raise ValueError("Invalid Replacement Policy")
        else:
            self.replacement_policy = replacement_policy
        # check if write policy is valid
        if write_policy not in self.write_policies:
            raise ValueError("Invalid Write Policy")
        else:
            self.write_policy = write_policy
        # initialize cache layers
        if self.number_of_layers == 1:
            self.layer = cache_layer("L1", self.cache_size, self.block_size, self.word_width, self.associativity)
        elif self.number_of_layers == 2:
            # TODO: how to devide cache size between L1 and L2
            pass
        elif self.number_of_layers == 3:
            # TODO: how to devide cache size between L1, L2 and L3
            pass


    # TODO: implement cache layer fucntionalities based on policies

# class for simulating cache layer
class cache_layer:
    def __init__(self, name : str, size : int, block_size : int, word_width : int, associativity : bool):
        # check if cache size is a power of 2
        if (size & (size - 1)) != 0:
            raise ValueError("Cache size must be a power of 2")
        else:
            self.size = size
        # check if block size is a power of 2
        if (block_size & (block_size - 1)) != 0:
            raise ValueError("Block size must be a power of 2")
        else:
            self.block_size = block_size
        self.word_width = word_width
        self.associativity = associativity
        self.number_of_blocks = self.size // self.block_size
        self.blocks = [cache_block(f'{name}_black{i}', self.block_size, self.word_width) for i in range(self.number_of_blocks)]
        
# class for simulating cache block
# note that we consider cache block as a single port memory
class cache_block:
    def __init__(self, name : str, block_size : int, word_width : int):
        # check if block size is a power of 2
        if (block_size & (block_size - 1)) != 0:
            raise ValueError("Block size must be a power of 2")
        self.block = memory(name, block_size, word_width)
    
    