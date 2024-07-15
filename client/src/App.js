import React, { useState, useEffect } from "react";

function App() {
  const [companies, setCompanies] = useState(null);
  const [selectedCompany, setSelectedCompany] = useState("");
  const [strategies, setStrategies] = useState(null);
  const [selectedStrategy, setSelectedStrategy] = useState("");

  useEffect(() => {
    fetch("/companies")
      .then(res => res.json())
      .then(data => {
        console.log(data); // Log the data to verify the structure
        setCompanies(data.Companies); // Update state with the companies data
      })
      .catch(error => {
        console.error("Error fetching companies:", error);
      });

    fetch("/strategies")
      .then(res => res.json())
      .then(data => {
        console.log(data); // Log the data to verify the structure
        setStrategies(data.Strategies); // Update state with the strategies data
      })
      .catch(error => {
        console.error("Error fetching strategies:", error);
      });
  }, []);

  const handleCompanyChange = event => {
    const selectedValue = event.target.value;
    setSelectedCompany(selectedValue);
    fetch("/submit", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ selectedCompany: selectedValue })
    })
    .then(res => res.json())
    .then(data => {
      console.log(data);
    })
    .catch(error => {
      console.error("Error submitting company selection:", error);
    });
  };

  const handleStrategyChange = event => {
    const selectedValue = event.target.value;
    setSelectedStrategy(selectedValue);
    fetch("/submitStrategy", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ selectedStrategy: selectedValue })
    })
    .then(res => res.json())
    .then(data => {
      console.log(data);
    })
    .catch(error => {
      console.error("Error submitting strategy selection:", error);
    });
  };

  return (
    <div>
      {companies === null || strategies === null ? (
        <p>Loading...</p>
      ) : (
        <>
          <h1>Select an Option</h1>
          <select value={selectedCompany} onChange={handleCompanyChange}>
            {companies.map((company) => (
              <option key={company.ticker} value={company.ticker}>
                {company.name}
              </option>
            ))}
          </select>
          
          <select value={selectedStrategy} onChange={handleStrategyChange}>
            {strategies.map((strategy) => (
              <option key={strategy.class_title} value={strategy.class_title}>
                {strategy.name}
              </option>
            ))}
          </select>
          
          <p>Selected Company: {selectedCompany}</p>
          <p>Selected Strategy: {selectedStrategy}</p>
        </>
      )}
    </div>
  );
}

export default App;




