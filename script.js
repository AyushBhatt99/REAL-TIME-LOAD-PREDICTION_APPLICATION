document.getElementById("cityForm").addEventListener("submit", async function(e) { 
  e.preventDefault();

  const city = document.getElementById("city").value;

  // Ensure that city is not empty before making the request
  if (!city) {
      alert("Please enter a city name!");
      return;
  }

  try {
      // Make a POST request to the Flask API
      const response = await fetch('/predict', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({ city: city }),
      });
      console.log("dmd");
      // Parse the JSON response
      const data = await response.json();

      // Check if the response is successful
      if (response.ok) {
          // Update the UI with the predicted load
          document.getElementById("predictedLoad").textContent = `Predicted Load: ${data.predicted_load.toFixed(2)} MW`;
      } else {
          // Show the error if there is an issue
          document.getElementById("predictedLoad").textContent = `Error: ${data.error}`;
      }
  } catch (error) {
      // Catch any network errors and display a message
      document.getElementById("predictedLoad").textContent = `Error: Failed to fetch prediction`;
      console.error('Error:', error);
  }
});
