import React from "react";

function Insult(props) {
  const labels = ["grunge", "island vacation", "formal", "preppy", "techwear"];
  const i = props.series.indexOf(Math.max(...props.series));
  return (
    <div>
      <p>u disgust me. do u enjoy dressing like a {labels[i]} snob?</p>
    </div>
  );
}

export default Insult;
