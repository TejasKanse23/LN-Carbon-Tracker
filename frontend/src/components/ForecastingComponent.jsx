import React, { useState } from 'react';
import { 
  AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Legend,
  ComposedChart, Line
} from 'recharts';
import { Activity, AlertTriangle, TrendingUp, TrendingDown, Minus, ArrowRight, Compass } from 'lucide-react';
import { generateForecast } from '../services/api';

const ForecastingComponent = () => {
    const [origin, setOrigin] = useState('');
    const [destination, setDestination] = useState('');
    const [horizon, setHorizon] = useState(6);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    const handleGenerate = async () => {
        if (!origin || !destination) {
            setError('Please enter both origin and destination.');
            return;
        }
        
        setLoading(true);
        setError(null);
        setResult(null);
        
        try {
            const data = await generateForecast(origin, destination, horizon);
            
            // Format data for Recharts
            // We want to combine historical and forecast so the chart is continuous
            const combinedData = [];
            data.historical.forEach(item => {
                combinedData.push({
                    date: item.date,
                    Historical: item.value,
                    Forecast: null
                });
            });
            
            // To make the line connect perfectly between historical and forecast,
            // we attach the forecast line starting from the last historical point
            const lastHistorical = data.historical[data.historical.length - 1];
            if (lastHistorical && data.forecast.length > 0) {
                // Link point
                combinedData.push({
                    date: lastHistorical.date,
                    Historical: null,
                    Forecast: lastHistorical.value, // Start forecast area from here visually
                });
            }
            
            data.forecast.forEach(item => {
                combinedData.push({
                    date: item.date,
                    Historical: null,
                    Forecast: item.value
                });
            });
            
            setResult({ ...data, chartData: combinedData });
        } catch (err) {
            console.error(err);
            if (err.response && err.response.data && err.response.data.error) {
                setError(err.response.data.error);
            } else {
                setError('Failed to generate forecast. Please try again.');
            }
        } finally {
            setLoading(false);
        }
    };

    const getTrendIcon = (trend) => {
        if (trend === 'increasing') return <TrendingUp color="#fca5a5" />;
        if (trend === 'decreasing') return <TrendingDown color="#6ee7b7" />;
        return <Minus color="#9ca3af" />;
    };

    return (
        <div className="glass-panel" style={{ marginTop: '20px' }}>
            <h2 style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '1.5rem' }}>
                <Compass color="var(--accent-purple)" />
                AI Emission Trend Forecasting
            </h2>

            <div style={{ display: 'flex', gap: '15px', alignItems: 'flex-end', marginBottom: '20px', flexWrap: 'wrap' }}>
                <div className="input-group" style={{ flex: '1', minWidth: '150px', marginBottom: '0' }}>
                    <label>Origin</label>
                    <input 
                        type="text" 
                        placeholder="e.g., Mumbai" 
                        value={origin}
                        onChange={(e) => setOrigin(e.target.value)}
                    />
                </div>
                <div style={{ paddingBottom: '12px', color: 'var(--text-secondary)' }}>
                    <ArrowRight size={20} />
                </div>
                <div className="input-group" style={{ flex: '1', minWidth: '150px', marginBottom: '0' }}>
                    <label>Destination</label>
                    <input 
                        type="text" 
                        placeholder="e.g., Delhi" 
                        value={destination}
                        onChange={(e) => setDestination(e.target.value)}
                    />
                </div>
                <div className="input-group" style={{ width: '120px', marginBottom: '0' }}>
                    <label>Horizon</label>
                    <select value={horizon} onChange={(e) => setHorizon(Number(e.target.value))} style={{ padding: '0.8rem', borderRadius: 'var(--radius-sm)', border: '1px solid var(--glass-border)', background: 'rgba(0,0,0,0.2)', color: 'white', outline: 'none' }}>
                        <option value={3}>3 Months</option>
                        <option value={6}>6 Months</option>
                        <option value={12}>12 Months</option>
                    </select>
                </div>
                <div style={{ paddingBottom: '0' }}>
                    <button 
                        className="submit-btn" 
                        onClick={handleGenerate}
                        disabled={loading}
                        style={{ background: 'linear-gradient(to right, var(--accent-purple), #6b21a8)', width: 'auto', padding: '0.8rem 1.5rem' }}
                    >
                        {loading ? 'Analyzing Trends...' : 'Generate Forecast'}
                    </button>
                </div>
            </div>

            {error && (
                <div style={{ padding: '10px', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid var(--accent-danger)', borderRadius: 'var(--radius-sm)', color: '#fca5a5', marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <AlertTriangle size={18} />
                    {error}
                </div>
            )}

            {result && (
                <div style={{ background: 'rgba(0,0,0,0.3)', padding: '20px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--glass-border)', marginTop: '20px' }}>
                    
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px', marginBottom: '25px' }}>
                        <div className="glass-panel" style={{ padding: '15px' }}>
                            <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginBottom: '5px' }}>Lane Forecast</p>
                            <h3 style={{ fontSize: '1.2rem', color: 'white' }}>{result.lane}</h3>
                        </div>
                        <div className="glass-panel" style={{ padding: '15px' }}>
                            <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginBottom: '5px' }}>Historical Avg (Monthly)</p>
                            <h3 style={{ fontSize: '1.2rem', color: 'var(--accent-blue)' }}>{Math.round(result.summary.historical_mean).toLocaleString()} kg CO₂</h3>
                        </div>
                        <div className="glass-panel" style={{ padding: '15px' }}>
                            <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginBottom: '5px' }}>Predicted Avg (Monthly)</p>
                            <h3 style={{ fontSize: '1.2rem', color: 'var(--accent-purple)' }}>{Math.round(result.summary.forecast_mean).toLocaleString()} kg CO₂</h3>
                        </div>
                        <div className="glass-panel" style={{ padding: '15px' }}>
                            <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginBottom: '5px' }}>Growth / Decline</p>
                            <h3 style={{ fontSize: '1.2rem', display: 'flex', alignItems: 'center', gap: '8px', color: result.summary.trend === 'increasing' ? '#fca5a5' : (result.summary.trend === 'decreasing' ? '#6ee7b7' : 'white') }}>
                                {getTrendIcon(result.summary.trend)}
                                {Math.abs(result.summary.growth_pct).toFixed(1)}%
                            </h3>
                        </div>
                    </div>

                    <div style={{ marginBottom: '25px', padding: '15px', background: 'rgba(59, 130, 246, 0.05)', borderRadius: '8px', borderLeft: '4px solid var(--accent-blue)' }}>
                        <h4 style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px', color: 'var(--accent-blue)' }}>
                            <Activity size={18} /> AI Insight
                        </h4>
                        <p style={{ color: 'white', lineHeight: '1.5' }}>
                            {result.explanation}
                        </p>
                    </div>

                    {result.riskInsight && (
                        <div style={{ marginBottom: '25px', padding: '15px', background: 'rgba(239, 68, 68, 0.05)', borderRadius: '8px', borderLeft: '4px solid var(--accent-danger)' }}>
                            <h4 style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px', color: 'var(--accent-danger)' }}>
                                <AlertTriangle size={18} /> Risk Alert
                            </h4>
                            <p style={{ color: '#fca5a5', lineHeight: '1.5' }}>
                                {result.riskInsight}
                            </p>
                        </div>
                    )}

                    <h3 style={{ marginBottom: '15px', color: 'var(--text-secondary)', fontSize: '1rem' }}>Emission Projection Chart</h3>
                    <div style={{ width: '100%', height: '350px' }}>
                        <ResponsiveContainer>
                            <ComposedChart data={result.chartData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                                <defs>
                                    <linearGradient id="colorHist" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="var(--accent-blue)" stopOpacity={0.3}/>
                                        <stop offset="95%" stopColor="var(--accent-blue)" stopOpacity={0}/>
                                    </linearGradient>
                                    <linearGradient id="colorFore" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="var(--accent-purple)" stopOpacity={0.3}/>
                                        <stop offset="95%" stopColor="var(--accent-purple)" stopOpacity={0}/>
                                    </linearGradient>
                                </defs>
                                <CartesianGrid strokeDasharray="3 3" stroke="var(--glass-border)" vertical={false} />
                                <XAxis dataKey="date" stroke="var(--text-secondary)" tick={{fontSize: 12}} minTickGap={20} />
                                <YAxis stroke="var(--text-secondary)" tick={{fontSize: 12}} />
                                <Tooltip contentStyle={{ backgroundColor: 'var(--bg-dark)', borderColor: 'var(--glass-border)', color: 'white', borderRadius: '8px' }} />
                                <Legend wrapperStyle={{ paddingTop: '10px' }} />
                                
                                <Area type="monotone" dataKey="Historical" stroke="var(--accent-blue)" strokeWidth={2} fillOpacity={1} fill="url(#colorHist)" activeDot={{ r: 6 }} />
                                <Line type="dashed" dataKey="Forecast" stroke="var(--accent-purple)" strokeWidth={2} strokeDasharray="5 5" activeDot={{ r: 6 }} dot={false} />
                                <Area type="monotone" dataKey="Forecast" stroke="none" fillOpacity={1} fill="url(#colorFore)" />
                            </ComposedChart>
                        </ResponsiveContainer>
                    </div>

                </div>
            )}
        </div>
    );
};

export default ForecastingComponent;
