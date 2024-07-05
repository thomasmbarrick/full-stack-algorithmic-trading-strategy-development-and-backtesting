import React, { useState, useEffect } from "react";

function App() {
  const [companies, setCompanies] = useState(null);

  useEffect(() => {
    fetch("/companies")
      .then(res => res.json())
      .then(data => {
        console.log(data); // Log the data to verify the structure
        setCompanies(data.Companies); // Update state with the companies data
      });
  }, []);

  return (
    <div>
      {companies === null ? (
        <p>Loading...</p>
      ) : (
        Object.entries(companies).map(([company, symbol], i) => (
          <p key={i}>{`${company}: ${symbol}`}</p>
        ))
      )}
    </div>
  );
}

export default App;
