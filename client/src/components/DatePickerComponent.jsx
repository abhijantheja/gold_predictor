import React, { useState, useEffect } from 'react';
import { useContext } from 'react';
import { MyContext } from '../Context';
function DatePickerComponent() {
  const { setValue } = useContext(MyContext);
  const [selectedDate, setSelectedDate] = useState('');
  const [loading, setLoading] = useState(false);
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState('');

  // Effect to handle changes when selectedDate is updated
  useEffect(() => {
    if (selectedDate) {
      // If you want to trigger an effect on date change, add logic here.
    }
  }, [selectedDate]);

  const handleDateChange = (e) => {
    setSelectedDate(e.target.value);
  };

  const handleSubmit = async () => {
    if (!selectedDate) return;
    setLoading(true);
    setError('');
    
    try {
      // Make the POST request to the API
      const response = await fetch('https://goldpredict.patalu.tech/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ date: selectedDate }), // Send the selected date in the body
      });

      if (!response.ok) {
        throw new Error('Failed to fetch prediction');
      }

      const data = await response.json();

      // Assuming the response contains 'prediction' as the gold price
      const predictionResult = data.prediction;
      setPrediction(predictionResult); // Store the prediction value
      setValue(data.total_data)
      setLoading(false);
    } catch (error) {
      setLoading(false);
      setError(error.message); // Set any errors
    }
  };

  return (
    <div className="flex justify-center min-h-screen bg-gradient-to-r">
      <div className="p-10 rounded-3xl shadow-xl max-w-lg w-full bg-white/10 backdrop-blur-lg border border-yellow-500">
        <h1 className="text-4xl font-bold text-center text-yellow-400 mb-8">Gold Price Prediction</h1>
        <p className="text-lg text-center text-gray-300 mb-6">Select a date to get predictions:</p>
        <div className="space-y-8">
          <div className="flex flex-col">
            <label htmlFor="date-picker" className="text-lg font-semibold text-yellow-300 mb-2">Choose a date:</label>
            <input
              id="date-picker"
              type="date"
              value={selectedDate}
              onChange={handleDateChange}
              className="p-4 border border-yellow-500 bg-gray-800 text-yellow-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-400 transition duration-300 ease-in-out"
            />
          </div>
          <div className="mt-4">
            <button
              onClick={handleSubmit}
              disabled={!selectedDate || loading}
              className="w-full py-3 bg-yellow-500 text-white font-semibold rounded-lg hover:bg-yellow-400 focus:outline-none focus:ring-2 focus:ring-yellow-400 disabled:opacity-50 transition duration-300 ease-in-out"
            >
              {loading ? 'Loading...' : 'Submit'}
            </button>
          </div>
          {selectedDate && (
            <div className="mt-8 text-center">
              <h3 className="text-2xl font-medium text-yellow-400">Selected Date: {selectedDate}</h3>
              <p className="text-lg text-gray-400 mt-2">Check back soon for your price prediction!</p>
            </div>
          )}
          {prediction !== null && (
            <div className="mt-8 text-center">
              <h3 className="text-2xl font-medium text-yellow-400">Prediction: {prediction.toFixed(2)}</h3>
              <p className="text-lg text-gray-400 mt-2">Based on the selected date.</p>
            </div>
          )}
          {error && (
            <div className="mt-4 text-center text-red-500">
              <p>Error: {error}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default DatePickerComponent;
