# class for simulating the behaviour of a fully customized microprogrammed CPU

# list of customized components:
# number of general purpose registers
# instruction set
# main memory height and width
# microprogrammed control unit
# microprogram memory height and width
# pipeline stages
# cache
# layers of cache
# cache block size
# cache replacement policy
# cache write policy
class CPU:
    # initializing all the variables
    def __init__(self, memory_width, memory_height, number_of_gp_regs, cache_en : bool, cache_width, cache_height, instruction_set = RV(), pipeline_stages = 5, cache_layers = 1, cache_block_size = 1, cache_replacement_policy = 'LRU', cache_write_policy = 'WBWA'):
        self.memory_width = memory_width
        self.memory_height = memory_height
        self.number_of_gp_regs = number_of_gp_regs
        self.cache_en = cache_en
        self.cache_width = cache_width
        self.cache_height = cache_height
        self.instruction_set = instruction_set
        self.pipeline_stages = pipeline_stages
        self.cache_layers = cache_layers
        self.cache_block_size = cache_block_size
        self.cache_replacement_policy = cache_replacement_policy
        self.cache_write_policy = cache_write_policy
        self.memory = memory(memory_width, memory_height)
        self.registers = register(number_of_gp_regs)
        self.pc = 0
        self.instructions = []
        self.instruction = None
        self.opcode = None
        self.rd = None
        self.rs1 = None
        self.rs2 = None
        self.imm = None
        
