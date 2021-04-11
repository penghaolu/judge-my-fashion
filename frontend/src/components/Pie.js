import React from "react";
import Chart from "react-apexcharts";
import Bubble from "./Bubble";

function Pie(props) {
  const settings = props.settings || {
    chart: {
      width: 800,
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
    <div
      style={{
        display: "flex",
        flex: "1",
        flexDirection: "row",
        margin: "auto",
        justifyContent: "center",
      }}
    >
      <div>
        <h3 style={{ transform: "translateX(-5px)" }}>
          among the five categories, you are:
        </h3>
        <Chart
          options={settings}
          series={props.series.map((x) => Math.trunc(x))}
          type="pie"
          width={500}
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
