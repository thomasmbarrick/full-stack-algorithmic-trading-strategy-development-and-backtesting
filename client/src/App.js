import React, { useState, useEffect } from "react";

function App() {
  const [companies, setCompanies] = useState([]);
  const [selectedCompany, setSelectedCompany] = useState("");
  const [selectedCompanyDescription, setSelectedCompanyDescription] = useState("");
  const [strategies, setStrategies] = useState([]);
  const [selectedStrategy, setSelectedStrategy] = useState("");
  const [strategyDescription, setStrategyDescription] = useState("");
  const [stake, setStake] = useState(500);
  const [brokerCash, setBrokerCash] = useState(1000000);

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
        setSelectedStrategy(data.Strategies[0].name);
        setStrategyDescription(data.Strategies[0].description);
      })
      .catch(error => {
        console.error("Error fetching strategies:", error);
      });
  }, []);

  useEffect(() => {
    if (selectedStrategy) {
      const selectedStrategyObj = strategies.find(strategy => strategy.name === selectedStrategy);
      setStrategyDescription(selectedStrategyObj.description);
    }
  }, [selectedStrategy, strategies]);

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
    const selectedStrategyObj = strategies.find(strategy => strategy.name === selectedValue);
    fetch("/submitStrategy", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ selectedStrategy: selectedStrategyObj.class_title })
    })
    .then(res => res.json())
    .then(data => {
      console.log(data);
      setStrategyDescription(selectedStrategyObj.description);
    })
    .catch(error => {
      console.error("Error submitting strategy selection:", error);
    });
  };

  const handleParameterChange = () => {
    fetch("/setParameters", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ stake: parseInt(stake, 10), brokerCash: parseFloat(brokerCash) })
    })
    .then(res => res.json())
    .then(data => {
      console.log(data);
    })
    .catch(error => {
      console.error("Error setting parameters:", error);
    });
  };

  const handleTrade = () => {
    fetch("/trade")
      .then(res => res.json())
      .then(data => {
        console.log(data);
      })
      .catch(error => {
        console.error("Error making trade:", error);
      });
  };

  return (
    <div>
      {companies.length === 0 || strategies.length === 0 ? (
        <p>Loading...</p>
      ) : (
        <>
          <h1>Select an Option</h1>
          <select value={selectedCompany} onChange={handleCompanyChange}>
            {companies.map((company) => (
              <option key={company.ticker} value={company.name}>
                {company.name}
              </option>
            ))}
          </select>

          <p>{selectedCompanyDescription}</p>

          <select value={selectedStrategy} onChange={handleStrategyChange}>
            {strategies.map((strategy) => (
              <option key={strategy.class_title} value={strategy.name}>
                {strategy.name}
              </option>
            ))}
          </select>

          <p>Selected Company: {selectedCompany}</p>
          <p>Selected Strategy: {selectedStrategy}</p>
          <p>Strategy Description: {strategyDescription}</p>

          <div>
            <label>
              Stake:
              <input
                type="number"
                value={stake}
                onChange={(e) => setStake(e.target.value)}
              />
            </label>
          </div>
          <div>
            <label>
              Broker Cash:
              <input
                type="number"
                value={brokerCash}
                onChange={(e) => setBrokerCash(e.target.value)}
              />
            </label>
          </div>
          <button onClick={handleParameterChange}>Set Parameters</button>
          <button onClick={handleTrade}>Make Trade</button>
        </>
      )}
    </div>
  );
}

export default App;










