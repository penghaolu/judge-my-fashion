import { useState } from "react";
import logo from "./logo.svg";
import "./App.css";
import Upload from "./components/Upload";
import Insult from "./components/Insult";

function App() {
  const [series, setSeries] = useState(null);
  return (
    <div className="App">
      <h1 className="title">judge my fashion</h1>
      <Upload setSeries={setSeries} />
      {series && <Insult series={series} />}
    </div>
  );
}

export default App;
