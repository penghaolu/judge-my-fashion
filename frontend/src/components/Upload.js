import React, { useState } from "react";
import axios from "axios";
import "./Upload.css";

function Upload() {
  const [selectedFile, setSelectedFile] = useState(null);

  // On file select (from the pop up)
  function onFileChange(event) {
    // Update the state
    setSelectedFile(event.target.files[0]);
  }

  // On file upload (click the upload button)
  function onFileUpload() {
    // Create an object of formData
    const formData = new FormData();

    // Update the formData object
    formData.append("myFile", selectedFile, selectedFile.name);

    // Details of the uploaded file
    console.log(selectedFile);

    // Request made to the backend api
    // Send formData object
    axios
      .post("/upload", formData)
      .then((response) => {
        console.log(response);
        getResults();
      })
      .catch((error) => {
        console.log("Error:", error);
      });
  }

  function getResults() {
    axios
      .get("/results")
      .then((response) => {
        console.log(response);
      })
      .catch((error) => {
        console.log("Error:", error);
      });
  }

  // File content to be displayed after
  // file upload is complete
  function fileData() {
    if (selectedFile) {
      return (
        <div className="general">
          <h2>File Details:</h2>

          <p>File Name: {selectedFile.name}</p>

          <p>File Type: {selectedFile.type}</p>

          <p>Last Modified: {selectedFile.lastModifiedDate.toDateString()}</p>
        </div>
      );
    } else {
      return (
        <div className="general">
          <br />
          <h4>select an image</h4>
        </div>
      );
    }
  }

  return (
    <div className="general">
      <h3>feed me ur fit pics</h3>
      <div>
        <label className="label">
          click here to upload
          <input className="input" type="file" onChange={onFileChange} />
        </label>
      </div>
      {fileData()}
      <button onClick={onFileUpload}>i'm ready, roast me</button>
    </div>
  );
}

export default Upload;
