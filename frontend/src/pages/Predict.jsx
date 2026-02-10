import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

function Predict() {
  const [file, setFile] = useState(null);
  const [userClass, setUserClass] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  // Protect route
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) navigate("/");
  }, []);

  async function handlePredict(e) {
    e.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const token = localStorage.getItem("token");

      const formData = new FormData();
      formData.append("file", file);
      formData.append("user_provided_class", userClass);

      const response = await fetch("http://localhost:8000/predict", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        setResult(data);
      } else {
        setError(data.detail || "Prediction failed");
      }
    } catch (err) {
      console.error(err);
      setError("Network error");
    } finally {
      setLoading(false);
    }
  }

  function handleLogout() {
    localStorage.removeItem("token");
    navigate("/");
  }

  return (
    <div className="card">
      <button className="logout-btn" onClick={handleLogout}>
        Logout
      </button>

      <h2>Lighting Prediction</h2>

      {error && <p className="error">{error}</p>}

      <form onSubmit={handlePredict}>
        <input
          type="file"
          accept="image/*"
          onChange={(e) => setFile(e.target.files[0])}
          required
        />

        {file && <p>{file.name}</p>}

        <select
          value={userClass}
          onChange={(e) => setUserClass(e.target.value)}
          required
        >
          <option value="">Select expected lighting type</option>
          <option value="wallwash lighting">Wallwash Lighting</option>
          <option value="spot lighting">Spot Lighting</option>
          <option value="path lighting">Path Lighting</option>
          <option value="deck lighting">Deck Lighting</option>
        </select>

        <button type="submit" disabled={loading}>
          {loading ? "Predicting..." : "Predict"}
        </button>
      </form>

      {result && (
        <div className="result-box">
          <p><b>Predicted Class:</b> {result.class}</p>
          <p><b>Confidence:</b> {result.confidence.toFixed(2)}%</p>
          <progress value={result.confidence} max="100" />
          <p><b>Recommendation:</b> {result.recommended_placement}</p>
        </div>
      )}
    </div>
  );
}

export default Predict;
