from ManoAssembler import MicroAssembler, Assembler
from ManoMicroprogramCPU import CPU
from ManoProgrammer import programmer

from flask import Flask, jsonify, request
from flask_cors import CORS

import json
import logging

app = Flask(__name__)
app.logger.setLevel(logging.INFO)
CORS(app)

# set the ip and port of the flask API
#app.run(host='127.0.0.1', port=5000)

# API for testing
@app.route("/")
def hello():
    app.logger.info('Received GET request on root')
    return "<p>Hello, Mano!</p>"

# API for getting the programs from user and write into the files
@app.route("/POST_programs", methods=['GET', 'POST'])
def POST_programs():
    if request.method == 'GET':
        app.logger.info('Received GET request for POST_programs')
    elif request.method == 'POST':
        app.logger.info('Received POST request for POST_programs')
        app.logger.debug(f'Request data: {request.data}')
        app.logger.debug(f'Request JSON: {request.json}')
    main_program = request.json['main_program']
    microprogram = request.json['microprogram']
    # write the programs into the files
    try:
        with open('main_code.txt', 'w') as f:
            json.dump(main_program, f)
        with open('microprogram_code.txt', 'w') as f:
            json.dump(microprogram, f)
        app.logger.info('Programs written successfully')
        return jsonify({'message': 'Programs written successfully'})
    except Exception as e:
        app.logger.error(f'Error writing programs: {e}')
        return jsonify({'error': str(e)})
    

# extracting code
assembly_program = open('main_code.txt', 'r').read().split('\n')
for i in range(len(assembly_program)):
    assembly_program[i] = assembly_program[i].split()

assembly_microprogram = open('main_microprogram_code.txt', 'r').read().split('\n')
for i in range(len(assembly_microprogram)):
    assembly_microprogram[i] = assembly_microprogram[i].split()
 
# assembling code
microassembler = MicroAssembler(assembly_microprogram)
# API for assembling the microprogram code
@app.route("/microassemble")
def microassembler_assemble():
    app.logger.info('Received GET request for microassemble')
    try:
        microassembler.assemble()
        app.logger.info('Microprogram assembled successfully')
        return jsonify({'control message' : 'microprogram assembled succesfully', 'second pass table' : microassembler.get_second_pass_table(), 'first pass table' : microassembler.get_first_pass_table()})
    except Exception as e:
        app.logger.error(f'Error assembling microprogram: {e}')
        return jsonify({'error' : str(e)})

assembler = Assembler(assembly_program, microassembler.get_first_pass_table())
# API for assembling the main program code
@app.route("/assemble")
def assembler_assemble():
    app.logger.info('Received GET request for assemble')
    try:
        assembler.assemble()
        app.logger.info('Program assembled successfully')
        return jsonify({'control message' : 'program assembled succesfully', 'second pass table' : assembler.get_second_pass_table(), 'first pass table' : assembler.get_first_pass_table()})
    except Exception as e:
        app.logger.error(f'Error assembling program: {e}')
        return jsonify({'error' : str(e)})

# initializing processor
processor = CPU(assembler.start_of_program, microassembler.start_of_microprogram)
# API for initializing the processor, just a quick show of processor status, not necessary
@app.route("/initialize")
def initialize():
    app.logger.info('Received GET request for initialize')
    return jsonify({'registers' : processor.get_registers(),
                    'main memory' : processor.get_memory(),
                    'microprogram memory' : processor.get_microprogram_memory()})

# loading program to memory 
programmer = programmer(processor, assembler.get_second_pass_table(), microassembler.get_second_pass_table())
# API for loading the programs to memories of processor
@app.route("/load")
def load():
    app.logger.info('Received GET request for load')
    try:
        programmer.load_program()
        programmer.load_microprogram()
        app.logger.info('Programs loaded successfully')
        return jsonify({'control message' : 'programs loaded succesfully',
                        'registers' : processor.get_registers(),
                        'main memory' : processor.get_memory(),
                        'program' : assembly_program,
                        'microprogram memory' : processor.get_microprogram_memory(),
                        'microprogram' : assembly_microprogram})
    except Exception as e:
        app.logger.error(f'Error loading programs: {e}')
        return jsonify({'error' : str(e)})

# API for getting the status of processor after a single clock pulse
@app.route("/microexecute")
def microexecute():
    app.logger.info('Received GET request for microexecute')
    try:
        processor.microexecute()
        app.logger.info('Microexecuted successfully')
        return jsonify({'control message' : processor.get_microexecute_control_message(),
                        'registers' : processor.get_registers(),
                        'main memory' : processor.get_memory(),
                        'program' : assembly_program,
                        'microprogram memory' : processor.get_microprogram_memory(),
                        'microprogram' : assembly_microprogram})
    except Exception as e:
        app.logger.error(f'Error microexecuting: {e}')
        return jsonify({'error' : str(e)})
    
# API for getting the status of processor after execution of a single instruction
@app.route("/execute")
def execute():
    app.logger.info('Received GET request for execute')
    try:
        processor.execute()
        app.logger.info('Executed successfully')
        return jsonify({'control message' : processor.get_execute_control_message(),
                        'registers' : processor.get_registers(),
                        'main memory' : processor.get_memory(),
                        'program' : assembly_program,
                        'microprogram memory' : processor.get_microprogram_memory(),
                        'microprogram' : assembly_microprogram})
    except Exception as e:
        app.logger.error(f'Error executing: {e}')
        return jsonify({'error' : str(e)})

# API for running the whole program
@app.route("/run")
def run():
    app.logger.info('Received GET request for run')
    try:
        processor.run()
        app.logger.info('Program run successfully')
        return jsonify({'control message' : processor.get_run_control_message(),
                        'registers' : processor.get_registers(),
                        'main memory' : processor.get_memory(),
                        'program' : assembly_program,
                        'microprogram memory' : processor.get_microprogram_memory(),
                        'microprogram' : assembly_microprogram})
    except Exception as e:
        app.logger.error(f'Error running program: {e}')
        return jsonify({'error' : str(e)})


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)