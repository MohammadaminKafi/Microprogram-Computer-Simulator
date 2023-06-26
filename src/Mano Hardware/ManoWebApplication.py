from ManoAssembler import MicroAssembler, Assembler
from ManoMicroprogramCPU import CPU
from ManoProgrammer import programmer

from flask import Flask, jsonify, request

app = Flask(__name__)

# set the ip and port of the flask API
#app.run(host='127.0.0.1', port=5000)

# API for testing
@app.route("/")
def hello():
    return "<p>Hello, Mano!</p>"

# API for getting the programs from user and write into the files
@app.route("/POST_programs", methods=['POST'])
def POST_programs():
    main_program = request.json['main_program']
    microprogram = request.json['microprogram']
    return f"You entered Program: {main_program} and Microprogram: {microprogram}"

# extracting code
assembly_program = open('assembly_program.txt', 'r').read().split('\n')
for i in range(len(assembly_program)):
    assembly_program[i] = assembly_program[i].split()

assembly_microprogram = open('assembly_microprogram.txt', 'r').read().split('\n')
for i in range(len(assembly_microprogram)):
    assembly_microprogram[i] = assembly_microprogram[i].split()
 
# assembling code
microassembler = MicroAssembler(assembly_microprogram)
# API for assembling the microprogram code
@app.route("/microassemble")
def microassembler_assemble():
    try:
        microassembler.assemble()
        return jsonify({'second pass' : microassembler.get_second_pass_table(), 'first pass' : microassembler.get_first_pass_table()})
    except Exception as e:
        return jsonify({'error' : str(e)})

assembler = Assembler(assembly_program, microassembler.get_first_pass_table())
# API for assembling the main program code
@app.route("/assemble")
def assembler_assemble():
    try:
        assembler.assemble()
        return jsonify({'second pass' : assembler.get_second_pass_table(), 'first pass' : assembler.get_first_pass_table()})
    except Exception as e:
        return jsonify({'error' : str(e)})

# initializing processor
processor = CPU(assembler.start_of_program, microassembler.start_of_microprogram)
# API for initializing the processor, just a quick show of processor status, not necessary
@app.route("/initialize")
def initialize():
    return jsonify({'registers' : processor.get_registers(),
                    'main memory' : processor.get_memory(),
                    'microprogram memory' : processor.get_microprogram_memory()})

# loading program to memory 
programmer = programmer(processor, assembler.get_second_pass_table(), microassembler.get_second_pass_table())
# API for loading the programs to memories of processor
@app.route("/load")
def load():
    try:
        programmer.load_program()
        programmer.load_microprogram()
        return jsonify({'main' : processor.main_memory.get_memory(), 'microprogram' : processor.microprogram_memory.get_memory()})
    except Exception as e:
        return jsonify({'error' : str(e)})

# API for getting the status of processor after a single clock pulse
@app.route("/microexecute")
def microexecute():
    try:
        processor.microexecute()
        return jsonify({'registers' : processor.get_registers(),
                        'main memory' : processor.get_memory(),
                        'microprogram memory' : processor.get_microprogram_memory()})
    except Exception as e:
        return jsonify({'error' : str(e)})
    
# API for getting the status of processor after execution of a single instruction
@app.route("/execute")
def execute():
    try:
        processor.execute()
        return jsonify({'registers' : processor.get_registers(),
                        'main memory' : processor.get_memory(),
                        'microprogram memory' : processor.get_microprogram_memory()})
    except Exception as e:
        return jsonify({'error' : str(e)})

# API for running the whole program
@app.route("/run")
def run():
    try:
        processor.run()
        return jsonify({'registers' : processor.get_registers(),
                        'main memory' : processor.get_memory(),
                        'microprogram memory' : processor.get_microprogram_memory()})
    except Exception as e:
        return jsonify({'error' : str(e)})


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)