import React from 'react';
import CrosshairLineChart from './components/GoldPriceChart';
import DatePickerComponent from './components/DatePickerComponent';
import { MyProvider } from './Context.jsx';
const App = () => {
  return (
    <MyProvider>
    <div className="text-gray-900 p-4">
      <h1 className="text-4xl font-bold text-blue-600 mb-4">Gold Predictor</h1>
      <p className="text-blue-500 mb-6">Shaping Tomorrow's Trends Today.</p>

      {/* Grid layout for side by side display */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="mb-6">
          <DatePickerComponent />
        </div>

        <div className="">
          <CrosshairLineChart />
        </div>
      </div>
    </div>
    </MyProvider>
  );
};

export default App;
