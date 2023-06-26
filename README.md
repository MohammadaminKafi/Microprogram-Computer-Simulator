# Microprogram-Computer-Simulator

Simulator for Mano Microprogram Computer and some customized versions

Please install dependancies using `pip install flask` and `pip install -U flask-cors`

In Mano Hardware directory, write microprogram code in `assembly_microprogram.txt` and program code in `assembly_program.txt` and run the program using `python main.py` or `flask --app ManoWebApplication.py run` for web application version

The following instructions are applicable (in this format: F1,F2,F3,CD,BR,ADDR):

F1:
| Instruction | Code |
| --- | ----------- |
| NOP | 000 |
| ADD | 001 |
| CLRAC | 010 |
| INCAC | 011 |
| DRTAC | 100 |
| DRTAR | 101 |
| PCTAR | 110 |
| WRITE | 111 |

F2:
| Instruction | Code |
| --- | ----------- |
| NOP | 000 |
| SUB | 001 |
| OR | 010 |
| AND | 011 |
| READ | 100 |
| ACTDR | 101 |
| INCDR | 110 |
| PCTDR | 111 |

F3:
| Instruction | Code |
| --- | ----------- |
| NOP | 000 |
| XOR | 001 |
| MUL | 001 |
| COM | 010 |
| SHL | 011 |
| SHR | 100 |
| INCPC | 101 |
| ARTPC | 110 |
| HLT | 111 |

CD:
| Instruction | Code |
| --- | ----------- |
| U | 00 |
| I | 01 |
| S | 10 |
| Z | 11 |

BR:
| Instruction | Code |
| --- | ----------- |
| JMP | 00 |
| CALL | 01 |
| RET | 10 |
| MAP | 11 |
