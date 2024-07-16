import React, { useState, useEffect } from "react";

function App() {
  const [companies, setCompanies] = useState([]);
  const [selectedCompany, setSelectedCompany] = useState("");
  const [selectedCompanyDescription, setSelectedCompanyDescription] = useState("");
  const [strategies, setStrategies] = useState([]);
  const [selectedStrategy, setSelectedStrategy] = useState("");
  const [strategyDescription, setStrategyDescription] = useState("");

  useEffect(() => {
    fetch("/companies")
      .then(res => res.json())
      .then(data => {
        setCompanies(data.Companies);
        setSelectedCompany(data.Companies[0].name);
        setSelectedCompanyDescription(data.Companies[0].description);
      })
      .catch(error => {
        console.error("Error fetching companies:", error);
      });

    fetch("/strategies")
      .then(res => res.json())
      .then(data => {
        setStrategies(data.Strategies);
        setSelectedStrategy(data.Strategies[0].class_title);
        setStrategyDescription(data.Strategies[0].description);
      })
      .catch(error => {
        console.error("Error fetching strategies:", error);
      });
  }, []);

  useEffect(() => {
    if (selectedStrategy) {
      fetch("/strategyDescription")
        .then(res => res.json())
        .then(data => {
          setStrategyDescription(data.description);
        })
        .catch(error => {
          console.error("Error fetching strategy description:", error);
        });
    }
  }, [selectedStrategy]);

  const handleCompanyChange = event => {
    const selectedValue = event.target.value;
    const selectedCompanyObj = companies.find(company => company.name === selectedValue);
    setSelectedCompany(selectedValue);
    setSelectedCompanyDescription(selectedCompanyObj.description);
    fetch("/submit", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ selectedCompany: selectedCompanyObj.ticker })
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
      fetch("/strategyDescription")
        .then(res => res.json())
        .then(data => {
          setStrategyDescription(data.description);
        })
        .catch(error => {
          console.error("Error fetching strategy description:", error);
        });
    })
    .catch(error => {
      console.error("Error submitting strategy selection:", error);
    });
  };

  return (
    <div>
      {companies.length === 0 || strategies.length === 0 ? (
        <p>Loading...</p>
      ) : (
        <>

          <select value={selectedCompany} onChange={handleCompanyChange}>
            {companies.map((company) => (
              <option key={company.ticker} value={company.name}>
                {company.name}
              </option>
            ))}
          </select>
          <p>Selected Company: {selectedCompany}</p>
          <p>{selectedCompanyDescription}</p>

          <select value={selectedStrategy} onChange={handleStrategyChange}>
            {strategies.map((strategy) => (
              <option key={strategy.class_title} value={strategy.class_title}>
                {strategy.name}
              </option>
            ))}
          </select>
          
          
          <p>Selected Strategy: {selectedStrategy}</p>
          <p>Strategy Description: {strategyDescription}</p>
        </>
      )}
    </div>
  );
}

export default App;







