import { useState } from "react";
import logo from "./logo.svg";
import "./App.css";
import Upload from "./components/Upload";
import Insult from "./components/Insult";
import Pie from "./components/Pie";

function App() {
  const [series, setSeries] = useState(null);

  const [chartVis, setChartVis] = useState(false);
  function showChart() {
    setChartVis(true);
  }

  return (
    <div className="App">
      <h1 className="title">judge my fashion</h1>
      <Upload setSeries={setSeries} />
      {series && <Insult series={series} />}
      {series && <button onClick={showChart}>show secret chart</button>}
      {chartVis && (
        <div className="pie">
          <Pie series={series} />
        </div>
      )}
    </div>
  );
}

export default App;
