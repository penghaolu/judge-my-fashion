import React, { useState } from "react";
import axios from "axios";
import "./Upload.css";

function Upload(props) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadReady, setUploadReady] = useState(false);
  const [roastReady, setRoastReady] = useState(false);

  // On file select (from the pop up)
  function onFileChange(event) {
    // Update the state
    setSelectedFile(event.target.files[0]);
    setUploadReady(true);
  }

  // On file upload (click the upload button)
  function onFileUpload() {
    // Create an object of formData
    const formData = new FormData();

    // Update the formData object
    formData.append("file", selectedFile);
    formData.append("filename", selectedFile.name);

    // Details of the uploaded file
    console.log(selectedFile);

    // Request made to the backend api
    // Send formData object
    axios
      .post("http://127.0.0.1:5000/upload", formData)
      .then((response) => {
        console.log(response);
        // getResults();
      })
      .catch((error) => {
        console.log("Error:", error);
      });
    setUploadReady(false);
    setRoastReady(true);
  }

  function getResults() {
    axios
      .get(`http://127.0.0.1:5000/results?filename=${selectedFile.name}`)
      .then((response) => {
        console.log(response);
        let percentages = response.data.map((elem) => {
          return (elem * 100).toFixed(2);
        });
        props.setSeries(percentages);
      })
      .catch((error) => {
        console.log("Error:", error);
      });
    setRoastReady(false);
  }

  // File content to be displayed after
  // file upload is complete
  function fileData() {
    if (selectedFile) {
      return (
        <div className="details">
          <h3>File Details:</h3>

          <p className="details">File Name: {selectedFile.name}</p>

          <p className="details">File Type: {selectedFile.type}</p>

          <p className="details">
            Last Modified: {selectedFile.lastModifiedDate.toDateString()}
          </p>
        </div>
      );
    } else {
      return (
        <div className="general">
          <h4>select an image</h4>
        </div>
      );
    }
  }

  return (
    <div className="general">
      <h2>i'm a mean neural net</h2>
      <h2>feed me ur best fit pic and i'll roast them</h2>
      <div>
        <label className="label">
          <div className="container">click here to pick ur fit pic</div>
          <input className="input" type="file" onChange={onFileChange} />
        </label>
      </div>
      {fileData()}
      {uploadReady && (
        <button className="button" onClick={onFileUpload}>
          upload my ugly photo please
        </button>
      )}
      <br />
      {roastReady && (
        <div>
          <h4>pic succesfully uploaded</h4>
          <button className="button" onClick={getResults}>
            i'm ready, roast me
          </button>
        </div>
      )}
    </div>
  );
}

export default Upload;
