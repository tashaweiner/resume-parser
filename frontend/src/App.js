import React, { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [allResumes, setAllResumes] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch all parsed resumes on mount
  useEffect(() => {
    axios.get("http://localhost:8000/resumes")
      .then(res => setAllResumes(res.data))
      .catch(err => {
        console.error("Error fetching resumes:", err);
        setError("Failed to load resumes");
      });
  }, []);

  const handleSearch = () => {
    if (!searchQuery.trim()) return;

    setLoading(true);
    setError(null);
    setResults([]);

    axios.get(`http://localhost:8000/search?query=${searchQuery}`)
      .then(res => setResults(res.data.results))
      .catch(err => {
        console.error("Error searching:", err);
        setError("Search failed.");
      })
      .finally(() => setLoading(false));
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
          <h2>🔍 Search Results</h2>
          {results.map((r, i) => (
            <div key={i} className="card">
              <h3>{r.filename}</h3>
              <p>Score: {r.score}/10</p>
              <p><strong>Reason:</strong> {r.reason}</p>
            </div>
          ))}
        </>
      )}

      <h2>📂 All Parsed Resumes</h2>
      {allResumes.map((resume, i) => (
        <div key={i} className="card">
          <h3>{resume.filename}</h3>
          <p><strong>Name:</strong> {resume.content?.name}</p>
          <p><strong>Email:</strong> {resume.content?.email}</p>
          <p><strong>Phone:</strong> {resume.content?.phone}</p>
        </div>
      ))}
    </div>
  );
}

export default App;
