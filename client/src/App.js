import React, { useState, useEffect } from "react";

function App() {
  const [data, setData] = useState({});

  useEffect(() => {
    fetch("/companies")
      .then(res => res.json())
      .then(data => {
        setData(data);
        console.log(data);
      });
  }, []);

  return (
    <div>
      {typeof data.companies === "undefined" ? (
        <p>Loading...</p>
      ) : (
        data.companies.map((company, i) => (
          <p key={i}>{company}</p>
        ))
      )}
    </div>
  );
}

export default App;
