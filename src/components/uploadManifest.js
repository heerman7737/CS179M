import {useEffect, useState, useRef} from 'react';
import axios from "axios";
import {AgGridColumn, AgGridReact} from 'ag-grid-react';
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";

import 'ag-grid-community/dist/styles/ag-grid.css';
import 'ag-grid-community/dist/styles/ag-theme-alpine.css';
// import Button from "@mui/material/Button";
// import TextField from "@mui/material/TextField";

function FileUpload() {
    // State to store uploaded file
    const [file, setFile] = useState("");

    // Handles file upload event and updates state
    function handleUpload(event) {
        // setFile(event.target.files[0]);
        axios.post('http://127.0.0.1:5000/uploadManifest',)
            .then(function (response) {
                // if(response.data.code === 200){
                setFile(event.target.files[0]);
                // }

            })

        // Add code here to upload file to server
        // ...
    }

    return (
        <div id="upload-box">
            <input type="file" onChange={handleUpload}/>
            <p>Filename: {file.name}</p>
            <p>File type: {file.type}</p>
            <p>File size: {file.size} bytes</p>
            {/*{file && <ImageThumb image={file}/>}*/}
        </div>
    );
}




export default FileUpload