import { Fragment, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function SecPage(){

    const navigate = useNavigate()

    const [microProgram,setMicroProgram] = useState(null);
    const [program,setProgram] = useState(null);
    const [error,setError] = useState(false);
    const [errorMsg,setErrorMsg] = useState([]);

    const [binary,setBinary] = useState(false);

    const url = 'http://127.0.0.1:5000/'

    useEffect(()=>{
        fetchData();
    },[])

    function binaryHandler(){
        setBinary(!binary);
    }

    function goBack(){
        navigate('/', { replace: true });
    }

    function goNext(){
        navigate('/third', { replace: true });
    }

    function fetchData(){

        fetch(url+'microassemble')
        .then(response => {
            return response.json()}
        )
        .then(data => {
            console.log(data)
            if(microProgram == null){
                setMicroProgram(data);
            }            
            const obj = Object.keys(data);
            if (obj.length == 1 ){
                setError(true);
                setErrorMsg(data);
            }
            
        })

        fetch(url+'assemble')
        .then(response => {
            return response.json()}
        )   
        .then(data => {
            console.log(data)
            if(program == null){
                setProgram(data);
            }
            const obj = Object.keys(data);
            if (obj.length == 1 ){
                setError(true);
                setErrorMsg(data);
            }
        })
    }

    return(
        <Fragment>
            { program !== null && microProgram !== null &&
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
                {!error &&  <div className="lower-p2">
                        <div className="program-container">
                            <label>your programs:</label>
                            <div className="table-container">
                                <table>
                                    <thead>
                                        <tr>
                                            <th>Label</th>
                                            <th>Location</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                            {
                                               !binary ?  Object.entries(program?.first_pass_table).sort().map(([key, value]) => (
                                                        <tr key={key}>
                                                            {console.log(key, value)}
                                                            <td>{value}</td>
                                                            <td>{key}</td>
                                                        </tr>
                                                )) :  Object.entries(program?.second_pass_table).sort().map(([key, value]) => (
                                                        <tr>
                                                            <td>{value}</td>
                                                            <td>{key}</td>
                                                        </tr>
                                                ))
                                            }
                                    </tbody>
                                </table>
                            </div>
                        </div>
                        <div className="microprogram-container">
                            <label>your microprograms:</label>
                            <div className="table-container">
                                <table>
                                    <thead>
                                        <tr>
                                            <th>Label</th>
                                            <th>Location</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                    {
                                               !binary ?  Object.entries(microProgram?.first_pass_table).sort().map(([key, value]) => (
                                                        <tr>
                                                            <td>{value}</td>
                                                            <td>{key}</td>
                                                        </tr>
                                                )) :  Object.entries(microProgram?.second_pass_table).sort().map(([key, value]) => (
                                                        <tr>
                                                            <td>{value}</td>
                                                            <td>{key}</td>
                                                        </tr>
                                                ))
                                    }
                                    </tbody>
                                </table>
                            </div>
                        </div>
                        <div className="button-p2-container">
                        <button  className="button-p2" onClick={binaryHandler}>
                            <span className="shadow"></span>
                            <span className="edge-binary"></span>
                            <span className="front-binary text">{!binary? "Seccond pass table": "First pass table"}</span>
                        </button>

                        <button  className="button-p2" onClick={goNext}>
                            <span className="shadow"></span>
                            <span className="edge"></span>
                            <span className="front text"> Load to memory</span>
                        </button>
                        <button  className="button-p2" onClick={goBack}>
                            <span className="shadow"></span>
                            <span className="edge"></span>
                            <span className="front text">Back to first page</span>
                        </button>
                    </div>
                </div>}    
            </div>
            }
    </Fragment>
            )
}