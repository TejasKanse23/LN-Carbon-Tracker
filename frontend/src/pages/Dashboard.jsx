import React from 'react';
import CarbonCalculator from '../components/CarbonCalculator';
import './Dashboard.css';

const Dashboard = () => {
    return (
        <div className="dashboard-layout">
            <header className="dashboard-header">
                <div className="container">
                    <h1>🌿 LN Carbon Tracker</h1>
                    <p>Track and estimate your transportation carbon emissions</p>
                </div>
            </header>
            <main className="dashboard-main">
                <div className="container">
                    <CarbonCalculator />
                </div>
            </main>
            <footer className="dashboard-footer">
                <p>&copy; {new Date().getFullYear()} LN Carbon Tracker - Hackathon Project</p>
            </footer>
        </div>
    );
};

export default Dashboard;
