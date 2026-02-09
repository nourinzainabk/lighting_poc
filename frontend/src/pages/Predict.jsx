import { useState } from "react";

function Predict() {
  const [file, setFile] = useState(null);
  const [userClass, setUserClass] = useState("");
  const [result, setResult] = useState(null);

  async function handlePredict(e) {
    e.preventDefault();

    const token = localStorage.getItem("token");

    const formData = new FormData();
    formData.append("file", file);
    formData.append("user_provided_class", userClass);

    const response = await fetch("http://localhost:8000/predict", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`
      },
      body: formData
    });

    const data = await response.json();
    setResult(data);
  }

  return (
    <div>
      <h2>Image Prediction</h2>

      <form onSubmit={handlePredict}>
        <input
          type="file"
          accept="image/*"
          onChange={(e) => setFile(e.target.files[0])}
          required
        />

        <input
          type="text"
          placeholder="Actual class"
          value={userClass}
          onChange={(e) => setUserClass(e.target.value)}
          required
        />

        <button type="submit">Predict</button>
      </form>

      {result && (
        <div>
          <p><b>Predicted Class:</b> {result.class}</p>
          <p><b>Confidence:</b> {result.confidence}</p>
          <p><b>Recommendation:</b> {result.recommended_placement}</p>
        </div>
      )}
    </div>
  );
}

export default Predict;
