import { Fragment, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function ThirdPage(){

    const [run,setRun] = useState(null);
    const [error,setError] = useState(false);
    const [errorMsg,setErrorMsg] = useState([]);
    const [binary,setBinary] = useState(false);

    const url = 'http://127.0.0.1:5000/'
    const navigate = useNavigate()

    useEffect(()=>{
        firstfetchData();
    },[])

    function binaryHandler(){
        setBinary(!binary);
    }

    function goBack(){
        navigate('/', { replace: true });
    }

    function runAll(){
        fetch(url+'run')
        .then(response => {
            return response.json()}
        )
        .then(data => {
            setRun(data);
            const obj = Object.keys(data);
            if (obj.length == 1 ){
                setError(true);
                setErrorMsg(data);
            }
            console.log('Response run:', data);
        })
    }

    function runInstruction(){
        fetch(url+'execute')
        .then(response => {
            return response.json()}
        )
        .then(data => {
            setRun(data);            
            const obj = Object.keys(data);
            if (obj.length == 1 ){
                setError(true);
                setErrorMsg(data);
            }
            console.log('Response execute:', data);
        })
    }

    function runMicroinstruction(){
        fetch(url+'microexecute')
        .then(response => {
            return response.json()}
        )
        .then(data => {
            setRun(data);
            const obj = Object.keys(data);
            if (obj.length == 1 ){
                setError(true);
                setErrorMsg(data);
            }
            console.log('Response microexecute:', data);
        })
    }

    function firstfetchData(){

        fetch(url+'load')
        .then(response => {
            return response.json()}
        )
        .then(data => {
            if(run == null){
                setRun(data);
            }
            const obj = Object.keys(data);
            if (obj.length == 1 ){
                setError(true);
                setErrorMsg(data);
            }
            console.log('Response load:', data);
        })

        fetch(url+'initialize')
        .then(response => {
            return response.json()}
        )
        .then(data => {
            console.log('Response intis:', data);
        })
    }

    return(
        <Fragment>
            <div className="container-1">
                <div className="upper">
                    <h2>microprogram computer</h2>
                    <ul className="wrapper">
                        <li className="icon facebook">
                            <span className="tooltip">Facebook</span>
                            <span><i className="fab fa-facebook-f"></i></span>
                        </li>
                        <li className="icon twitter">
                            <span className="tooltip">Twitter</span>
                            <span><i className="fab fa-twitter"></i></span>
                        </li>
                        <li className="icon instagram">
                            <span className="tooltip">Instagram</span>
                            <span><i className="fab fa-instagram"></i></span>
                        </li>
                    </ul>
                </div>
                    
                {error && 
                    <div className="error-container" onClick={goBack}>
                        <h2 className="error">ERROR</h2>
                        <h2 className="error">{errorMsg.error}</h2>
                    </div>
                }
                {run !== null && !error && <div className="lower-p2">
                        <div className="program-container">
                            <label>your programs:</label>
                            <div className="table-container">
                                <table>
                                    <thead>
                                        <tr>
                                            <th>Line</th>
                                            <th>Code</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                    {
                                        !binary ?  Object.entries(run?.program).map(([key, value]) => (
                                                <tr key={key}>
                                                    <td>{key}</td>
                                                    <td>{value}</td>
                                                </tr>
                                        )) :  Object.entries(run?.main_memory).map(([key, value]) => (
                                                <tr key={key}>
                                                    <td>{key}</td>
                                                    <td>{value}</td>
                                                </tr>
                                        ))
                                    }
                                    </tbody>
                                </table>
                            </div>
                            <br/>
                        </div>

                        <div className="microprogram-container">
                            <label>your microprograms:</label>
                            <div className="table-container">
                                <table>
                                    <thead>
                                        <tr>
                                            <th>Line</th>
                                            <th>Code</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                    {
                                        !binary ?  Object.entries(run?.microprogram).map(([key, value]) => (
                                                <tr key={key}>
                                                    <td>{key}</td>
                                                    <td>{value}</td>
                                                </tr>
                                        )) :  Object.entries(run?.microprogram_memory).map(([key, value]) => (
                                                <tr key={key}>
                                                    <td>{key}</td>
                                                    <td>{value}</td>
                                                </tr>
                                        ))
                                    }
                                    </tbody>
                                </table>
                            </div>
                            <br/>
                                                         
                        </div>
                    <div className="button-p2-container">
                        <button  className="button-p2" onClick={binaryHandler}>
                            <span className="shadow"></span>
                            <span className="edge-binary"></span>
                            <span className="front-binary text"> binary</span>
                        </button>

                        <button  className="button-p2" onClick={runAll}>
                            <span className="shadow"></span>
                            <span className="edge"></span>
                            <span className="front text">run all</span>
                        </button>

                        <button  className="button-p2" onClick={runInstruction}>
                            <span className="shadow"></span>
                            <span className="edge"></span>
                            <span className="front text">run instruction</span>
                        </button>

                        <button  className="button-p2" onClick={runMicroinstruction}>
                            <span className="shadow"></span>
                            <span className="edge"></span>
                            <span className="front text">run microinstruction</span>
                        </button>
                        <button  className="button-p2" onClick={goBack}>
                            <span className="shadow"></span>
                            <span className="edge"></span>
                            <span className="front text">go first page</span>
                        </button>
                    </div>
                </div> }
                {run !== null && !error && <div className="register-container">
                <div>
                   <table>
                        <thead>
                            <tr>
                                <th>AC</th>
                                <th>PC</th>
                                <th>CAR</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <th>{run.registers.AC[0]}</th>
                                <th>{ run.registers.PC[0]}</th>
                                <th>{ run.registers.CAR[0]}</th>
                            </tr>
                        </tbody>
                    </table>
                    <table>
                        <thead>
                            <tr>
                                <th>DR</th>
                                <th>AR</th>
                                <th>SBR</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <th>{run.registers.AC[0]}</th>
                                <th>{ run.registers.AR[0]}</th>
                                <th>{ run.registers.SBR[0]}</th>
                            </tr>
                        </tbody>
                    </table>  
                </div>
                <div>
                   <table>
                        <thead>
                            <tr>
                                <th>AC</th>
                                <th>PC</th>
                                <th>CAR</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <th>{run.registers.AC[1]}</th>
                                <th>{ run.registers.PC[1]}</th>
                                <th>{ run.registers.CAR[1]}</th>
                            </tr>
                        </tbody>
                    </table>
                    <table>
                        <thead>
                            <tr>
                                <th>DR</th>
                                <th>AR</th>
                                <th>SBR</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <th>{run.registers.AC[1]}</th>
                                <th>{ run.registers.AR[1]}</th>
                                <th>{ run.registers.SBR[1]}</th>
                            </tr>
                        </tbody>
                    </table>  
                </div>
                    <div className="control">control message :<br/><br/>{run.control_message}</div>
                </div>}                
            </div>
        </Fragment>
            )
}