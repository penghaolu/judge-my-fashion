import React, { Component } from "react";
import axios from "axios";
import "./Upload.css";

class Upload extends Component {
  state = {
    // Initially, no file is selected
    selectedFile: null,
  };

  // On file select (from the pop up)
  onFileChange = (event) => {
    // Update the state
    this.setState({ selectedFile: event.target.files[0] });
  };

  // On file upload (click the upload button)
  onFileUpload = () => {
    // Create an object of formData
    const formData = new FormData();

    // Update the formData object
    formData.append(
      "myFile",
      this.state.selectedFile,
      this.state.selectedFile.name
    );

    // Details of the uploaded file
    console.log(this.state.selectedFile);

    // Request made to the backend api
    // Send formData object
    axios.post("api/uploadfile", formData);
  };

  // File content to be displayed after
  // file upload is complete
  fileData = () => {
    if (this.state.selectedFile) {
      return (
        <div className="general">
          <h2>File Details:</h2>

          <p>File Name: {this.state.selectedFile.name}</p>

          <p>File Type: {this.state.selectedFile.type}</p>

          <p>
            Last Modified:{" "}
            {this.state.selectedFile.lastModifiedDate.toDateString()}
          </p>
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
  };

  render() {
    return (
      <div className="general">
        <h3>feed me ur fit pics</h3>
        <div>
          <label className="label">
            click here to upload
            <input className="input" type="file" onChange={this.onFileChange} />
          </label>
        </div>
        {this.fileData()}
        <button onClick={this.onFileUpload}>i'm ready, roast me</button>
      </div>
    );
  }
}

export default Upload;
