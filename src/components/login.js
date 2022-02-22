import {useEffect, useState, useRef} from 'react';
import axios from "axios";
import {AgGridColumn, AgGridReact} from 'ag-grid-react';
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";

import 'ag-grid-community/dist/styles/ag-grid.css';
import 'ag-grid-community/dist/styles/ag-theme-alpine.css';
import { useNavigate } from "react-router-dom"
// import Button from "@mui/material/Button";
// import TextField from "@mui/material/TextField";

const LoginForm = () => {
    const [name, setName] = useState({
        name : ""
    })
    // const gridRef = useRef(null);
    //const [a, setA] = React.useState(1)
    // const [addFailmode, setAddFailmode] = useState({
    //     failModeName: "",
    //     failCode: "",
    // })

    let navigate = useNavigate();



    const handleChange = (event) => {
        event.preventDefault()
        const fieldName = event.target.getAttribute("name")
        const fieldValue = event.target.value
        const newName = {...name}
        newName[fieldName] = fieldValue

        setName(newName)
    }

    const handleNameSubmit = (event) => {
        // event.preventDefault()
        // const history = useHistory()
        // history.push("/uploadManifest")
        const newName = {
            // id: nanoid(),
            // id: addStudent.id,
            "name" : name.name
        }

        // console.log("click")

        axios.post('http://127.0.0.1:5000/login', newName)
            .then(res =>  {
                console.log(res)
                // if(response.data.code === 200){

                setName(newName)
                // }

            })

        navigate("/uploadManifest")

    }



    //     const onButtonClick = e => {
    //     const selectedNodes = gridRef.current.api.getSelectedNodes()
    //     const selectedData = selectedNodes.map(node => node.data)
    //     const selectedDataStringPresentation = selectedData.map(node => `${node.id} ${node.name}`).join(', ')
    //     alert(`Selected nodes: ${selectedDataStringPresentation}`)
    // }


    return (
        <div className="ag-theme-alpine" style={{height: 400, width: 605}}>
            {/*<button onClick={onButtonClick}>Add Student</button>*/}
            {/*<span>*/}
            {/*    <button onClick="window.location.href = 'http://127.0.0.1:5000/create'">*/}
            {/*    add*/}
            {/*    </button>*/}
            {/*</span>*/}
            <h1>Login</h1>

            <form onSubmit={handleNameSubmit}>
                <TextField
                    name="Name"
                    label="Name"
                    onChange={handleChange}
                />

                <Button variant="text" onClick={() => {
                handleNameSubmit()
            }}>Login</Button>
                {/*<Navigate from="/login" to="/uploadManifest" />*/}
            </form>
        </div>


    )

}

export default LoginForm