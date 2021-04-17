import React from "react";
import "./Bubble.css";

const Bubble = (props) => {
  const { type = "test", percentage = 0 } = props;

  return (
    <>
      <div className="bubble">
        <div>
          <p className="type">{type}</p>
        </div>
        <div>
          <p className="percentage">{`${percentage} %`}</p>
        </div>
      </div>
    </>
  );
};

export default Bubble;
