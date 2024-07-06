import React, { useState, useEffect } from "react";

function App() {
  const [companies, setCompanies] = useState(null);
  const [selectedCompany, setSelectedCompany] = useState("");

  useEffect(() => {
    fetch("/companies")
      .then(res => res.json())
      .then(data => {
        console.log(data); // Log the data to verify the structure
        setCompanies(data.Companies); // Update state with the companies data
      });
  }, []);

  const handleChange = event => {
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
    });
  }

  return (
    <div>
      {companies === null ? (
        <p>Loading...</p>
      ) : (
        <>
          <h1>Select an Option</h1>
          <select value={selectedCompany} onChange={handleChange}>
            <option value="">Select a company</option>
            {companies.map((company) => (
              <option key={company.ticker} value={company.ticker}>
                {company.name}
              </option>
            ))}
          </select>
        </>
      )}
    </div>
  );
}

export default App;


