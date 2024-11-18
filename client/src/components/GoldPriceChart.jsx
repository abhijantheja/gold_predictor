import React, { useContext } from 'react';
import { MyContext } from '../Context';
import {
  ComposedChart,
  Line,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend
} from 'recharts';

// Dummy data for the chart
const data = [
  { name: '2024-08-21', value: 232.15, barValue: 232.65 },
  { name: '2024-08-22', value: 229.37, barValue: 229.87 },
  { name: '2024-08-23', value: 232.02, barValue: 232.92 },
  { name: '2024-08-26', value: 232.76, barValue: 232.96 },
  { name: '2024-08-28', value: 233.39, barValue:  233.59 },
  { name: '2024-08-29', value: 231.75, barValue:  231.05 },
  { name: '2024-08-30', value: 232.95, barValue: 232.95 },
  { name: '2024-09-03', value: 231.29, barValue: 231.89 },
  { name: '2024-09-04', value: 230.29, barValue: 230.79},
  { name: '2024-09-05', value: 230.43, barValue: 230.03},
  { name: '2024-09-06', value: 232.35, barValue: 232.35 }
];

const GoldPredictionChart = () => {
  const {value}= useContext(MyContext)
  let transformedData = [];
  try {
    if (value) {
      const parsedData = JSON.parse(value);
      transformedData = Object.entries(parsedData).map(([name, value]) => ({
        name,
        value: parseFloat(value),
        barValue: parseFloat(value),
      }));
    } else {
      transformedData = data;
    }
  } catch (error) {
    console.error("Error parsing JSON:", error);
    transformedData = data; // Fallback to default data
  }
   console.log(transformedData)
  return (
    <div style={{
      opacity:0.8
    }}>
      <ResponsiveContainer width="100%" height={400}>
        <ComposedChart
          data={transformedData.length >0 ? transformedData: data}
          margin={{ top: 20, right: 30, left: 30, bottom: 20 }}
        >
          {/* Gradient for the line */}
          <defs>
            <linearGradient id="gold-gradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#f9d342" stopOpacity={0.8} />
              <stop offset="95%" stopColor="#d4af37" stopOpacity={0.5} />
            </linearGradient>
          </defs>

          {/* Background grid with a soft, muted golden tint */}
          <CartesianGrid strokeDasharray="3 3" stroke="#524d4a" opacity={0.1} />

          {/* X-Axis and Y-Axis with premium gold styling */}
          <XAxis
            dataKey="name"
            tick={{ fill: '#e0b968', fontSize: 14, fontWeight: 'bold' }}
            axisLine={{ stroke: '#e0b968' }}
            tickLine={false}
          />
          <YAxis
            tick={{ fill: '#e0b968', fontSize: 14, fontWeight: 'bold' }}
            axisLine={{ stroke: '#e0b968' }}
            tickLine={false}
            domain={[0, 250]} // Set the Y-axis range from 0 to 250
            ticks={[0, 50, 100, 150, 200, 250]} // Specify the fixed tick values

          />

          {/* Tooltip styling for crosshair with dark background */}
          <Tooltip
            contentStyle={{
              backgroundColor: '#1a1a1a',
              borderColor: '#d4af37',
              borderRadius: '10px',
              boxShadow: '0px 4px 8px rgba(0, 0, 0, 0.4)',
              color: '#f9d342',
            }}
            itemStyle={{ color: '#f9d342' }}
            cursor={{ stroke: '#e0b968', strokeWidth: 2 }}
          />

          {/* Bar Chart with premium golden styling */}
          <Bar
            dataKey="barValue"
            fill="#d4af37"
            barSize={20}
            radius={[10, 10, 0, 0]}
            opacity={0.7}
          />

          {/* Premium gold-themed Line with gradient */}
          <Line
            type="monotone"
            dataKey="value"
            stroke="url(#gold-gradient)"
            strokeWidth={4}
            dot={{ fill: '#f9d342', r: 6 }}
            activeDot={{ fill: '#d4af37', r: 10 }}
          />

          {/* Add a legend */}
          <Legend />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  );
};

export default GoldPredictionChart;
