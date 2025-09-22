"use client";
import { useState } from "react";

export default function Home() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [answer, setAnswer] = useState(null);
  const [sources, setSources] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setAnswer(null);
    setSources([]);

    try {
      const res = await fetch("http://127.0.0.1:8000/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });

      if (!res.ok) throw new Error("Failed to fetch recommendations");

      const data = await res.json();
      setAnswer(data.answer);
      setSources(data.sources || []);
    } catch (err) {
      console.error(err);
      setAnswer("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="container">
      <h1>Anime Recommender</h1>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter your anime preference..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? "Loading..." : "Search"}
        </button>
      </form>

      {answer && (
        <div className="result">
          <h2>Recommendation:</h2>
          <pre>{answer}</pre>
        </div>
      )}

      {sources.length > 0 && (
        <div className="sources">
          <h3>Sources:</h3>
          <ul>
            {sources.map((src, i) => (
              <li key={i}>{src}</li>
            ))}
          </ul>
        </div>
      )}
    </main>
  );
}
