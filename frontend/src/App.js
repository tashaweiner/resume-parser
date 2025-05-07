import React, { useState, useEffect } from "react";
import axios from "axios";

const API_URL = process.env.REACT_APP_API_URL;

function App() {
  const [searchQuery, setSearchQuery] = useState("");
  const [owner, setOwner] = useState("all");
  const [ownerOptions, setOwnerOptions] = useState([]);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);

  const RESULTS_PER_PAGE = 25;

  useEffect(() => {
    axios
      .get(`${API_URL}/owners`)
      .then((res) => {
        setOwnerOptions(res.data.owners || []);
      })
      .catch((err) => {
        console.error("Failed to fetch owners:", err);
      });
  }, []);

  const handleSearch = () => {
    if (!searchQuery.trim()) return;

    setLoading(true);
    setError(null);
    setResults([]);
    setCurrentPage(1);

    axios
      .post(`${API_URL}/search/full`, {
        prompt: searchQuery,
        top_k: 25,
        owner: owner !== "all" ? owner : null,
      })
      .then((res) => {
        setResults(res.data.results);
      })
      .catch((err) => {
        console.error("Error during search:", err);
        setError("Search failed.");
      })
      .finally(() => {
        setLoading(false);
      });
  };

  const paginatedResults = results.slice(
    (currentPage - 1) * RESULTS_PER_PAGE,
    currentPage * RESULTS_PER_PAGE
  );

  return (
    <div style={{ padding: "2rem", maxWidth: "800px", margin: "0 auto" }}>
      <h1>Resume Search</h1>

      <div style={{ marginBottom: "1rem", display: "flex", gap: "1rem", alignItems: "flex-end" }}>
        <div style={{ display: "flex", flexDirection: "column" }}>
          <label style={{ color: "#888", fontSize: "0.9rem", marginBottom: "0.2rem" }}>Search Prompt</label>
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="e.g. banking"
            style={{ padding: "0.5rem", width: "300px" }}
          />
        </div>

        <div style={{ display: "flex", flexDirection: "column" }}>
          <label style={{ color: "#888", fontSize: "0.9rem", marginBottom: "0.2rem" }}>Owner</label>
          <select
            value={owner}
            onChange={(e) => setOwner(e.target.value)}
            style={{ padding: "0.5rem", width: "150px" }}
          >
            <option value="all">All Candidates</option>
            {ownerOptions.map((opt) => (
              <option key={opt} value={opt}>
                {opt}
              </option>
            ))}
          </select>
        </div>

        <button style={{ padding: "0.5rem 1rem", height: "fit-content" }} onClick={handleSearch}>
          Search
        </button>
      </div>

      {loading && <p>Loading...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {results.length > 0 && (
        <>
          <h2>
            🔍 Search Results (Showing {paginatedResults.length} of {results.length})
          </h2>
          {paginatedResults.map((r, i) => (
            <div
              key={i}
              className="card"
              style={{
                marginBottom: "1rem",
                padding: "1rem",
                border: "1px solid #ddd",
                borderRadius: "8px",
              }}
            >
              <h3>{r.name || "Unnamed Candidate"}</h3>
              <p><strong>Filename:</strong> {r.filename}</p>
              <p><strong>Score:</strong> {r.score !== null && r.score !== undefined ? `${r.score}/10` : "Not scored"}</p>
              <p><strong>Reason:</strong> {r.reason || "N/A"}</p>
            </div>
          ))}

          <div style={{ marginTop: "1rem" }}>
            <button
              onClick={() => setCurrentPage((p) => Math.max(p - 1, 1))}
              disabled={currentPage === 1}
            >
              ⬅ Prev
            </button>
            <span style={{ margin: "0 1rem" }}>Page {currentPage}</span>
            <button
              onClick={() =>
                setCurrentPage((p) =>
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
