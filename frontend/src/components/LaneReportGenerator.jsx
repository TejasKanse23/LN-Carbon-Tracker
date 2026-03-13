import React, { useState } from 'react';
import { Download, FileText, CheckCircle, AlertTriangle, ArrowRight } from 'lucide-react';
import { generateLaneReport, getDownloadReportUrl } from '../services/api';

const LaneReportGenerator = () => {
    const [origin, setOrigin] = useState('');
    const [destination, setDestination] = useState('');
    const [loading, setLoading] = useState(false);
    const [report, setReport] = useState(null);
    const [error, setError] = useState(null);

    const handleGenerate = async () => {
        if (!origin || !destination) {
            setError('Please enter both origin and destination.');
            return;
        }
        
        setLoading(true);
        setError(null);
        setReport(null);
        
        try {
            const data = await generateLaneReport(origin, destination);
            setReport(data);
        } catch (err) {
            console.error(err);
            if (err.response && err.response.data && err.response.data.error) {
                setError(err.response.data.error);
            } else {
                setError('Failed to generate report. Please try again.');
            }
        } finally {
            setLoading(false);
        }
    };

    const handleDownload = () => {
        if (report && report.file_path) {
            // Extact file name from file_path
            const parts = report.file_path.split(/[\\/]/);
            const fileName = parts[parts.length - 1];
            const url = getDownloadReportUrl(fileName);
            window.location.href = url;
        }
    };

    return (
        <div className="glass-panel" style={{ marginTop: '20px' }}>
            <h2 style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '1.5rem' }}>
                <FileText color="var(--accent-purple)" />
                Lane Carbon Intelligence Report Generator
            </h2>

            <div style={{ display: 'flex', gap: '15px', alignItems: 'flex-end', marginBottom: '20px', flexWrap: 'wrap' }}>
                <div className="input-group" style={{ flex: '1', minWidth: '200px', marginBottom: '0' }}>
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
                <div className="input-group" style={{ flex: '1', minWidth: '200px', marginBottom: '0' }}>
                    <label>Destination</label>
                    <input 
                        type="text" 
                        placeholder="e.g., Delhi" 
                        value={destination}
                        onChange={(e) => setDestination(e.target.value)}
                    />
                </div>
                <div style={{ paddingBottom: '0' }}>
                    <button 
                        className="submit-btn" 
                        onClick={handleGenerate}
                        disabled={loading}
                        style={{ background: 'linear-gradient(to right, var(--accent-purple), #6b21a8)', width: 'auto', padding: '0.75rem 1.5rem' }}
                    >
                        {loading ? 'Analyzing Data...' : 'Generate Report'}
                    </button>
                </div>
            </div>

            {error && (
                <div style={{ padding: '10px', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid var(--accent-danger)', borderRadius: 'var(--radius-sm)', color: '#fca5a5', marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <AlertTriangle size={18} />
                    {error}
                </div>
            )}

            {report && (
                <div style={{ background: 'rgba(0,0,0,0.3)', padding: '20px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--glass-border)', marginTop: '20px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px', borderBottom: '1px solid var(--glass-border)', paddingBottom: '15px' }}>
                        <div>
                            <h3 style={{ fontSize: '1.5rem', marginBottom: '5px' }}>Carbon Intelligence Report</h3>
                            <p style={{ color: 'var(--text-secondary)' }}>Lane: {report.overview.lane_name}</p>
                        </div>
                        <button onClick={handleDownload} className="submit-btn" style={{ width: 'auto', padding: '0.5rem 1rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
                            <Download size={18} />
                            Download Report (Word)
                        </button>
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
                        <div>
                            <h4 style={{ color: 'var(--accent-blue)', marginBottom: '10px' }}>1. Lane Overview</h4>
                            <ul style={{ listStyle: 'none', padding: '0', color: 'var(--text-secondary)' }}>
                                <li style={{ marginBottom: '8px' }}><strong style={{color:'white'}}>Total Shipments:</strong> {report.overview.total_shipments}</li>
                                <li style={{ marginBottom: '8px' }}><strong style={{color:'white'}}>Total Distance:</strong> {report.overview.total_distance_km.toLocaleString()} km</li>
                                <li style={{ marginBottom: '8px' }}><strong style={{color:'white'}}>Total Freight:</strong> {report.overview.total_freight_tons.toLocaleString()} tons</li>
                                <li style={{ marginBottom: '8px' }}><strong style={{color:'white'}}>Avg Utilization:</strong> {report.overview.avg_utilization}%</li>
                                <li style={{ marginBottom: '8px' }}><strong style={{color:'white'}}>Avg Vehicle Age:</strong> {report.overview.avg_vehicle_age} years</li>
                                <li style={{ marginBottom: '8px' }}><strong style={{color:'white'}}>Common Vehicles:</strong> {report.overview.common_vehicle_types.join(', ')}</li>
                            </ul>
                        </div>
                        
                        <div>
                            <h4 style={{ color: 'var(--accent-green)', marginBottom: '10px' }}>2. Carbon Emission Analysis</h4>
                            <ul style={{ listStyle: 'none', padding: '0', color: 'var(--text-secondary)' }}>
                                <li style={{ marginBottom: '8px' }}><strong style={{color:'white'}}>Total CO₂:</strong> {report.emissions.total_co2_kg.toLocaleString()} kg</li>
                                <li style={{ marginBottom: '8px' }}><strong style={{color:'white'}}>Avg per Shipment:</strong> {report.emissions.avg_co2_per_shipment.toLocaleString()} kg</li>
                                <li style={{ marginBottom: '8px' }}><strong style={{color:'white'}}>Emission Intensity:</strong> {report.emissions.emission_intensity} kg/t-km</li>
                                <li style={{ marginBottom: '8px' }}><strong style={{color:'white'}}>Network Avg:</strong> {report.emissions.network_avg_co2.toLocaleString()} kg</li>
                                <li style={{ marginBottom: '8px' }}><strong style={{color:'white'}}>Status:</strong> <span style={{ color: report.emissions.status_vs_network.includes('Above') ? '#fca5a5' : '#6ee7b7' }}>{report.emissions.status_vs_network}</span></li>
                            </ul>
                        </div>
                    </div>

                    <div style={{ marginTop: '20px', paddingTop: '20px', borderTop: '1px solid var(--glass-border)' }}>
                        <h4 style={{ color: 'var(--accent-purple)', marginBottom: '10px' }}>3. Emission Drivers</h4>
                        <ul style={{ paddingLeft: '20px', color: 'var(--text-secondary)' }}>
                            {report.drivers.map((driver, i) => (
                                <li key={i} style={{ marginBottom: '8px' }}>{driver}</li>
                            ))}
                        </ul>
                    </div>

                    <div style={{ marginTop: '20px', paddingTop: '20px', borderTop: '1px solid var(--glass-border)' }}>
                        <h4 style={{ color: 'var(--accent-danger)', marginBottom: '10px' }}>4. Carbon Hotspot Detection</h4>
                        <ul style={{ paddingLeft: '20px', color: 'var(--text-secondary)' }}>
                            {report.hotspots.map((hotspot, i) => (
                                <li key={i} style={{ marginBottom: '8px' }}>{hotspot}</li>
                            ))}
                        </ul>
                    </div>

                    <div style={{ marginTop: '20px', paddingTop: '20px', borderTop: '1px solid var(--glass-border)' }}>
                        <h4 style={{ color: 'var(--accent-green)', marginBottom: '10px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                            <CheckCircle size={18} />
                            5. Sustainability Recommendations
                        </h4>
                        <ul style={{ paddingLeft: '20px', color: 'var(--text-secondary)' }}>
                            {report.recommendations.map((rec, i) => (
                                <li key={i} style={{ marginBottom: '8px', color: 'white' }}>{rec}</li>
                            ))}
                        </ul>
                    </div>

                    <div style={{ marginTop: '20px', paddingTop: '20px', borderTop: '1px dashed var(--accent-green)' }}>
                        <h4 style={{ color: 'var(--accent-blue)', marginBottom: '10px' }}>6. Reduction Opportunity Summary</h4>
                        <p style={{ color: 'var(--text-secondary)', marginBottom: '8px' }}>
                            <strong style={{color:'white'}}>Potential Potential Reduction:</strong> {report.reduction.potential_reduction_kg.toLocaleString()} kg CO₂
                        </p>
                        <p style={{ color: '#6ee7b7' }}>
                            {report.reduction.impact_summary}
                        </p>
                    </div>

                </div>
            )}
        </div>
    );
};

export default LaneReportGenerator;
