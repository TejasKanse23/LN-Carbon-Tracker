import React, { useState } from 'react';
import { calculateCarbonEmission } from '../services/api';
import './CarbonCalculator.css';

const CarbonCalculator = () => {
    const [distance, setDistance] = useState('');
    const [vehicleType, setVehicleType] = useState('car');
    const [result, setResult] = useState(null);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setResult(null);

        if (!distance || isNaN(distance) || Number(distance) <= 0) {
            setError('Please enter a valid positive distance.');
            return;
        }

        setLoading(true);
        try {
            const data = await calculateCarbonEmission(distance, vehicleType);
            setResult(data);
        } catch (err) {
            setError('Failed to calculate emissions. Please ensure the backend is running.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="calculator-container">
            <h2>Calculate Your Carbon Footprint</h2>
            <form onSubmit={handleSubmit} className="calculator-form">
                <div className="form-group">
                    <label htmlFor="distance">Distance (km)</label>
                    <input
                        type="number"
                        id="distance"
                        value={distance}
                        onChange={(e) => setDistance(e.target.value)}
                        placeholder="e.g. 120"
                        min="1"
                        step="any"
                    />
                </div>
                
                <div className="form-group">
                    <label htmlFor="vehicleType">Vehicle Type</label>
                    <select
                        id="vehicleType"
                        value={vehicleType}
                        onChange={(e) => setVehicleType(e.target.value)}
                    >
                        <option value="car">Car (0.089 kg CO2/km)</option>
                        <option value="van">Van (0.120 kg CO2/km)</option>
                        <option value="truck">Truck (0.161 kg CO2/km)</option>
                    </select>
                </div>

                <button type="submit" disabled={loading} className="submit-btn">
                    {loading ? 'Calculating...' : 'Calculate Emission'}
                </button>
            </form>

            {error && <div className="error-message">{error}</div>}

            {result && (
                <div className="result-card">
                    <h3>Result</h3>
                    <p>Distance: <strong>{result.distance} km</strong></p>
                    <p>Vehicle: <strong>{result.vehicle_type}</strong></p>
                    <div className="emission-highlight">
                        <h4>Carbon Emission:</h4>
                        <span className="emission-value">{result.carbon_emission.toFixed(2)}</span>
                        <span className="emission-unit">kg CO₂</span>
                    </div>
                </div>
            )}
        </div>
    );
};

export default CarbonCalculator;
