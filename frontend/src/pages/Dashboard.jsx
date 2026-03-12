import React, { useState, useEffect } from 'react';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';
import { Activity, Leaf, Truck, AlertTriangle } from 'lucide-react';
import axios from 'axios';
import CarbonCalculator from '../components/CarbonCalculator';

const Dashboard = () => {
    const [data, setData] = useState(null);

    useEffect(() => {
        const fetchDashboard = async () => {
            try {
                const res = await axios.get('http://localhost:5000/api/carbon/dashboard');
                setData(res.data);
            } catch (err) {
                console.error("Failed to fetch dashboard data", err);
            }
        };
        fetchDashboard();
    }, []);

    if (!data) return <div className="app-container"><h2 style={{color: 'var(--accent-blue)'}}>Initializing AI Engine...</h2></div>;

    // Build trend chart
    const trendData = data.recentShipments.map((s, i) => ({
        name: `Ship-${i+1}`,
        CO2: s.co2Kg
    })).reverse();

    return (
        <div className="app-container">
            <header className="header">
                <h1>
                    <Leaf color="#10b981" size={36} />
                    <span className="title-glow">Carbon Intelligence Platform</span>
                </h1>
                <div style={{ display: 'flex', gap: '15px', alignItems: 'center' }}>
                    <span className="badge badge-low" style={{ fontSize: '1rem', padding: '6px 16px' }}>
                        ESG Score: {data.kpis.esgScore}
                    </span>
                </div>
            </header>

            <div className="kpi-grid">
                <div className="glass-panel kpi-card">
                    <div className="kpi-header">
                        <span>Total Emissions Today</span>
                        <Activity size={18} color="var(--accent-purple)" />
                    </div>
                    <div className="kpi-value">{data.kpis.totalCO2Today} <span style={{fontSize: '1rem', color: 'var(--text-secondary)', fontWeight: 'normal'}}>tCO₂</span></div>
                </div>
                
                <div className="glass-panel kpi-card">
                    <div className="kpi-header">
                        <span>Active Shipments</span>
                        <Truck size={18} color="var(--accent-blue)" />
                    </div>
                    <div className="kpi-value">{data.kpis.activeShipments}</div>
                </div>

                <div className="glass-panel kpi-card">
                    <div className="kpi-header">
                        <span>High Emission Lanes</span>
                        <AlertTriangle size={18} color="var(--accent-danger)" />
                    </div>
                    <div className="kpi-value">{data.kpis.highEmissionLanes}</div>
                </div>
            </div>

            <div className="main-grid">
                <div className="glass-panel chart-panel" style={{ display: 'flex', flexDirection: 'column' }}>
                    <h2 style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                        <Activity color="var(--accent-blue)" /> Activity Trend (Last 10 Shipments)
                    </h2>
                    <div className="chart-container" style={{ flexGrow: 1, marginTop: '20px' }}>
                        <ResponsiveContainer width="100%" height="100%">
                            <AreaChart data={trendData}>
                                <defs>
                                    <linearGradient id="colorCo2" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="var(--accent-blue)" stopOpacity={0.4}/>
                                        <stop offset="95%" stopColor="var(--accent-blue)" stopOpacity={0}/>
                                    </linearGradient>
                                </defs>
                                <CartesianGrid strokeDasharray="3 3" stroke="var(--glass-border)" vertical={false} />
                                <XAxis dataKey="name" stroke="var(--text-secondary)" tick={{fontSize: 12}} />
                                <YAxis stroke="var(--text-secondary)" tick={{fontSize: 12}} />
                                <Tooltip contentStyle={{ backgroundColor: 'var(--bg-dark)', borderColor: 'var(--glass-border)', color: 'white', borderRadius: '8px' }} />
                                <Area type="monotone" dataKey="CO2" stroke="var(--accent-blue)" strokeWidth={3} fillOpacity={1} fill="url(#colorCo2)" />
                            </AreaChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                <div>
                    <CarbonCalculator />
                </div>
            </div>

            <div className="main-grid">
                <div className="glass-panel">
                    <h2 style={{ marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '10px' }}>
                        <Truck color="var(--accent-green)" />
                        Recent Shipments
                    </h2>
                    <div className="list-table-container">
                        {data.recentShipments.map((shp) => (
                            <div className="list-item" key={shp.id}>
                                <div className="list-item-left">
                                    <h4>{shp.from} → {shp.to}</h4>
                                    <p>{shp.vehicle} • {Math.round(shp.distance)} km • {shp.status}</p>
                                </div>
                                <div className="list-item-right">
                                    <p style={{ color: shp.hasAnomaly ? 'var(--accent-danger)' : 'white' }}>{Math.round(shp.co2Kg)} kg CO₂</p>
                                    <span className={`badge badge-${shp.sustainabilityScore}`}>{shp.sustainabilityScore} Rate</span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="glass-panel">
                    <h2 style={{ marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '10px' }}>
                        <AlertTriangle color="var(--accent-danger)" />
                        Risky Lanes
                    </h2>
                    <div className="list-table-container">
                        {data.lanes.map((lane) => (
                            <div className="list-item" key={lane.id}>
                                <div className="list-item-left">
                                    <h4>{lane.from} - {lane.to}</h4>
                                    <p>Avg Load: {lane.avgLoadFactor}% • Dominant: {lane.dominantVehicle}</p>
                                </div>
                                <div className="list-item-right">
                                    <p>{Math.round(lane.totalCO2/1000)} t</p>
                                    <span className={`badge badge-${lane.riskLevel}`}>{lane.riskLevel.toUpperCase()}</span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
            
        </div>
    );
};

export default Dashboard;
