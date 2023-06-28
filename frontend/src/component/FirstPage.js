import { Fragment, useEffect, useState } from "react";
import {useNavigate} from "react-router-dom"


export default function FirstPage(){
    
    const [error,setError] = useState(false);

    const navigate = useNavigate()
    const url = 'http://127.0.0.1:5000/'



    function PostData(){

        const program = document.getElementById("program").value
        const microprogram = document.getElementById("microprogram").value

        // console.log(typeof(program))

        const obj ={
            main_program : program,
            microprogram : microprogram,
        }

        console.log(obj)


        fetch(url+'POST_programs',{
            headers: { 'Content-Type': 'application/json' },
            method : 'POST',
            body : JSON.stringify(obj)
        }).then(response => {
            return response.json();

        }).then(data => {
                setTimeout(() => {
                  navigate('/sec', { replace: true });
                }, 2000);
        })
        
    }

    return(
        <Fragment>
            <div className="container-1">

                <div className="upper">
                    <h2>microprogram computer</h2>
                    <ul class="wrapper">
                        <li class="icon facebook">
                            <span class="tooltip">Facebook</span>
                            <span><i class="fab fa-facebook-f"></i></span>
                        </li>
                        <li class="icon twitter">
                            <span class="tooltip">Twitter</span>
                            <span><i class="fab fa-twitter"></i></span>
                        </li>
                        <li class="icon instagram">
                            <span class="tooltip">Instagram</span>
                            <span><i class="fab fa-instagram"></i></span>
                        </li>
                    </ul>
                </div>
                    
                <div className="lower">

                    <div className="program-container">
                        <label>write your programs here</label>
                        <textarea type="text" id="program" required className="program" defaultValue={`
                        # use this format to comment, comments at the end of the line is not allowed
                        # start of program would be from MAIN, else from location 100 of memory
                        
                        # use this format for writting code:
                        # LABEL,         INSTRUCTION      ADDRESS
                        # VARIABLE,      (DEC, HEX, BIN)  VALUE
                        
                        ORG 100
                        MAIN,   FACT    NUM
                                STRAC   SUM
                                HALT
                        SUM,    DEC 0
                        NUM,    DEC 8
                        END
                        `}/>
                    </div>

                    <div className="microprogram-container">
                        <label>write your microprograms here</label>
                        <textarea type="text"  id="microprogram" required className="microprogram" defaultValue={`
                        "# use this format to comment, comments at the end of the line is not allowed
                        # start of control would be from FETCH, else from location 64 of microprogram memory
                        
                        # use this format for writting code:
                        # LABEL: F1,F2,F3       CD      BR      ADDRESS
                        # NEXT will be replaced by next address of memory 
                        
                                ORG 0
                        FACT:   CLRAC               I   CALL    INDRCT
                                READ                U   JMP     CNTNU   
                        
                                ORG 4
                        STRAC:  NOP                 I   CALL    INDRCT
                                DRTAC,ACTDR         U   JMP     NEXT
                                WRITE               U   JMP     NEXT
                                DRTAC,ACTDR         U   JMP     FETCH
                        
                                ORG 60
                        HALT:   HLT                 U   JMP     HALT
                        
                                ORG 64
                        FETCH:  PCTAR               U   JMP     NEXT
                                READ,INCPC          U   JMP     NEXT
                                DRTAR               U   MAP
                        INDRCT: READ                U   JMP     NEXT
                                DRTAR               U   RET
                        
                                ORG 70
                        CNTNU:  DRTAC,ACTDR         S   JMP     FETCH
                                NOP                 Z   JMP     FETCH   
                                DRTAC,ACTDR         U   JMP     NEXT
                                INCAC               U   JMP     NEXT
                        LOOP:   MUL                 U   JMP     NEXT
                                DRTAC,ACTDR         U   JMP     NEXT
                                COM                 U   JMP     NEXT
                                INCAC               U   JMP     NEXT
                                INCAC               U   JMP     NEXT
                                COM                 U   JMP     NEXT
                                INCAC               Z   JMP     FETCH
                                DRTAC,ACTDR         U   JMP     LOOP
                        END"
                        `}/>
                    </div>

                    <div>
                        <button onClick={PostData} className="button-p1">
                            <span class="shadow"></span>
                            <span class="edge"></span>
                            <span class="front text"> Assemble</span>
                        </button>
                        {error && 
                        <div className="error">
                            
                        </div>}
                    </div>
                   
                </div>                
            </div>
        </Fragment>
        )
}