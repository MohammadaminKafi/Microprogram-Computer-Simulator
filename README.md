# Microprogram Computer Simulator

A simulator for the Mano Microprogram Computer and various customized versions.

## Installation

Install the necessary dependencies using:
```bash
pip install flask
pip install -U flask-cors
```

## Usage

1. Navigate to the `Mano Hardware` directory.
2. Write the microprogram code in `assembly_microprogram.txt`.
3. Write the program code in `assembly_program.txt`.
4. Run the program using one of the following commands:
   ```bash
   python main.py
   ```
   or, for the web application version:
   ```bash
   flask --app ManoWebApplication.py run
   ```

## Instruction Set

The following instructions are applicable, formatted as `F1, F2, F3, CD, BR, ADDR`:

### F1:
| Instruction | Code |
|-------------|------|
| NOP         | 000  |
| ADD         | 001  |
| CLRAC       | 010  |
| INCAC       | 011  |
| DRTAC       | 100  |
| DRTAR       | 101  |
| PCTAR       | 110  |
| WRITE       | 111  |

### F2:
| Instruction | Code |
|-------------|------|
| NOP         | 000  |
| SUB         | 001  |
| OR          | 010  |
| AND         | 011  |
| READ        | 100  |
| ACTDR       | 101  |
| INCDR       | 110  |
| PCTDR       | 111  |

### F3:
| Instruction | Code |
|-------------|------|
| NOP         | 000  |
| XOR         | 001[^1] |
| MUL         | 001  |
| COM         | 010  |
| SHL         | 011  |
| SHR         | 100  |
| INCPC       | 101  |
| ARTPC       | 110  |
| HLT         | 111  |

### CD:
| Instruction | Code |
|-------------|------|
| U           | 00   |
| I           | 01   |
| S           | 10   |
| Z           | 11   |

### BR:
| Instruction | Code |
|-------------|------|
| JMP         | 00   |
| CALL        | 01   |
| RET         | 10   |
| MAP         | 11   |

[^1]: In this version, 'MUL' is used instead of 'XOR'. To use the 'XOR' version, uncomment the lines related to 'XOR' and add 'XOR' to the dictionaries instead of 'MUL' in `src/Mano Hardware/ManoAssembler.py` and `src/Mano Hardware/ManoMicroprogramCPU.py`.
