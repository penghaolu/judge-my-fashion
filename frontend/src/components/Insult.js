import React from "react";

function Insult(props) {
  const labels = ["grunge", "island vacation", "formal", "preppy", "techwear"];
  let intSeries = props.series.map((x) => Math.trunc(x));
  const i = intSeries.indexOf(Math.max(...intSeries));
  console.log(i);
  return (
    <div>
      <p>u disgust me. do u enjoy dressing like a {labels[i]} snob?</p>
    </div>
  );
}

export default Insult;
