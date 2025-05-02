import React, { useState } from "react";
import axios from "axios";

const API_URL = process.env.REACT_APP_API_URL;

function App() {
  const [searchQuery, setSearchQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);

  const RESULTS_PER_PAGE = 25;
  const paginatedResults = results.slice(
    (currentPage - 1) * RESULTS_PER_PAGE,
    currentPage * RESULTS_PER_PAGE
  );

  const handleSearch = () => {
    if (!searchQuery.trim()) return;

    setLoading(true);
    setError(null);
    setResults([]);
    setCurrentPage(1);

    axios
      .get(`${API_URL}/search?query=${encodeURIComponent(searchQuery)}`)
      .then(res => {
        setResults(res.data.results);
      })
      .catch(err => {
        console.error("Error during search:", err);
        setError("Search failed.");
      })
      .finally(() => {
        setLoading(false);
      });
  };

  return (
    <div style={{ padding: "2rem", maxWidth: "800px", margin: "0 auto" }}>
      <h1>Resume Search</h1>

      <div style={{ marginBottom: "1rem" }}>
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="e.g. banking"
          style={{ padding: "0.5rem", width: "300px", marginRight: "0.5rem" }}
        />
        <button onClick={handleSearch}>Search</button>
      </div>

      {loading && <p>Loading...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {results.length > 0 && (
        <>
          <h2>🔍 Search Results (Showing {paginatedResults.length} of {results.length})</h2>
          {paginatedResults.map((r, i) => (
            <div key={i} className="card" style={{ marginBottom: "1rem" }}>
              <h3>{r.filename}</h3>
              <p>Score: {r.score}/10</p>
              <p><strong>Reason:</strong> {r.reason}</p>
            </div>
          ))}

          <div style={{ marginTop: "1rem" }}>
            <button
              onClick={() => setCurrentPage(p => Math.max(p - 1, 1))}
              disabled={currentPage === 1}
            >
              ⬅ Prev
            </button>
            <span style={{ margin: "0 1rem" }}>Page {currentPage}</span>
            <button
              onClick={() =>
                setCurrentPage(p =>
                  p * RESULTS_PER_PAGE < results.length ? p + 1 : p
                )
              }
              disabled={currentPage * RESULTS_PER_PAGE >= results.length}
            >
              Next ➡
            </button>
          </div>
        </>
      )}
    </div>
  );
}

export default App;
