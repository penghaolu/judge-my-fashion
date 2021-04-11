import React from "react";
import Chart from "react-apexcharts";
import Bubble from "./Bubble";

function Pie(props) {
  const settings = props.settings || {
    chart: {
      width: 380,
      type: "pie",
    },
    labels: ["grunge", "island vacation", "formal", "preppy", "techwear"],
    responsive: [
      {
        breakpoint: 480,
        options: {
          chart: {
            width: 200,
          },
          legend: {
            position: "bottom",
          },
        },
      },
    ],
  };

  return (
    <div stlye={{ display: "flex", flex: "1", flexDirection: "row" }}>
      <div>
        <Chart
          options={settings}
          series={props.series}
          type="pie"
          width={props.width || 380}
        />
      </div>
      <div>
        {props.series.map((x, i) => {
          return <Bubble type={settings.labels[i]} percentage={x} key={i} />;
        })}
      </div>
    </div>
  );
}

export default Pie;
