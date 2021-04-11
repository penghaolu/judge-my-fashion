import logo from "./logo.svg";
import "./App.css";
import Upload from "./components/Upload";

function App() {
  return (
    <div className="App">
      {/* <div className="card">
        <button>UPLOAD</button>
      </div>

      <button className="upload__btn">UPLOAD</button> */}

      <h1 className="title">judge my fashion</h1>
      <Upload />
    </div>
  );
}

export default App;
