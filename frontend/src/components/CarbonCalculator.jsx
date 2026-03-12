import React, { useState } from 'react';
import { Calculator } from 'lucide-react';
import axios from 'axios';

const CarbonCalculator = () => {
    const [distance, setDistance] = useState('');
    const [weight, setWeight] = useState('');
    const [vehicle, setVehicle] = useState('HCV-Diesel');
    const [loadFactor, setLoadFactor] = useState(0.8);
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleCalculate = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            const { data } = await axios.post('http://localhost:5000/api/carbon/calculate', {
                distanceKm: distance,
                weightKg: weight,
                vehicleType: vehicle,
                loadFactor: loadFactor
            });
            setResult(data);
        } catch (error) {
            console.error("Calculation failed", error);
        }
        setLoading(false);
    };

    return (
        <div className="glass-panel">
            <h2 style={{ marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Calculator size={20} className="title-glow" /> 
                Emission Estimator
            </h2>
            <form onSubmit={handleCalculate}>
                <div className="input-group">
                    <label>Distance (km)</label>
                    <input type="number" required min="1" value={distance} onChange={e => setDistance(e.target.value)} placeholder="e.g. 1500" />
                </div>
                <div className="input-group">
                    <label>Weight (kg)</label>
                    <input type="number" required min="1" value={weight} onChange={e => setWeight(e.target.value)} placeholder="e.g. 12000" />
                </div>
                <div className="input-group">
                    <label>Vehicle Type</label>
                    <select value={vehicle} onChange={e => setVehicle(e.target.value)}>
                        <option value="HCV-Diesel">HCV - Diesel</option>
                        <option value="HCV-BS6">HCV - BS6 Diesel</option>
                        <option value="MCV-Diesel">MCV - Diesel</option>
                        <option value="LCV-Diesel">LCV - Diesel</option>
                        <option value="CNG-Truck">CNG Truck</option>
                        <option value="EV-Truck">EV Truck</option>
                    </select>
                </div>
                <div className="input-group">
                    <label>Load Utilization ({Math.round(loadFactor * 100)}%)</label>
                    <input 
                        type="range" 
                        min="0.1" max="1.0" step="0.05" 
                        value={loadFactor} 
                        onChange={e => setLoadFactor(parseFloat(e.target.value))} 
                    />
                </div>
                <button type="submit" className="submit-btn" disabled={loading}>
                    {loading ? 'Calculating...' : 'Estimate Emissions'}
                </button>
            </form>

            {result && (
                <div className="calc-result">
                    <h3 style={{ color: 'var(--accent-green)' }}>{result.co2Kg} kg CO₂</h3>
                    <p style={{ fontSize: '0.85rem' }}>Est. Fuel/Energy: {result.fuelUsed} L</p>
                    <span className={`badge badge-${result.sustainabilityScore}`} style={{ marginTop: '0.5rem', display: 'inline-block' }}>
                        Score: {result.sustainabilityScore}
                    </span>
                </div>
            )}
        </div>
    );
};

export default CarbonCalculator;
