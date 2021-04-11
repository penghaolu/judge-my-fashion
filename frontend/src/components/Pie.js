import React from "react";
import Chart from "react-apexcharts";

function Pie(props) {
  const settings = props.settings || {
    chart: {
      width: 380,
      type: "pie",
    },
    labels: ["grunge", "hawaiian", "mens semi-formal", "preppy", "techwear"],
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
    <>
      <Chart
        options={settings}
        series={props.series}
        type="pie"
        width={props.width || 380}
      />
    </>
  );
}

export default Pie;
