import express from "express";
import { calculateEmission } from "./engine.js";
import { generateShipments, generateLaneAnalytics } from "./mockData.js";
import { exec } from "child_process";
import path from "path";
import fs from "fs";
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const router = express.Router();

// Get Dashboard Data
router.get("/dashboard", (req, res) => {
    const shipments = generateShipments(35);
    const lanes = generateLaneAnalytics();
    
    const totalCO2Today = shipments.reduce((acc, s) => acc + s.co2Kg, 0);
    const highEmissionLanes = lanes.filter(l => l.riskLevel === "critical" || l.riskLevel === "high").length;
    
    res.json({
        kpis: {
            totalCO2Today: Math.round(totalCO2Today / 1000 * 10) / 10, // in Metric Tons
            activeShipments: shipments.length,
            highEmissionLanes,
            esgScore: Math.round(75 + Math.random() * 15)
        },
        recentShipments: shipments.slice(0, 10),
        lanes
    });
});

// Single Shipment calculation API
router.post("/calculate", (req, res) => {
    const { distanceKm, weightKg, vehicleType, loadFactor } = req.body;
    
    if (!distanceKm || !weightKg || !vehicleType) {
        return res.status(400).json({ error: "Missing required fields" });
    }
    
    const result = calculateEmission(
        parseFloat(distanceKm),
        parseFloat(weightKg),
        vehicleType,
        parseFloat(loadFactor) || 0.75
    );
    
    res.json(result);
});

// Route Optimization / Insights
router.post("/optimize", (req, res) => {
    const { distanceKm, weightKg, vehicleType, loadFactor } = req.body;
    
    const current = calculateEmission(distanceKm, weightKg, vehicleType, loadFactor);
    
    // Optimization logic: suggest an EV or BS6 alternative with better load consolidation
    const altVehicle = vehicleType === 'EV-Truck' ? 'EV-Truck' : (vehicleType.includes('HCV') ? 'HCV-BS6' : 'EV-Truck');
    const betterLoad = Math.min((loadFactor || 0.75) + 0.15, 1.0);
    
    const optimized = calculateEmission(
        distanceKm * 0.95, // Assume 5% route distance reduction
        weightKg,
        altVehicle,
        betterLoad
    );
    
    const savings = current.co2Kg - optimized.co2Kg;
    const savingPercent = ((savings / current.co2Kg) * 100).toFixed(1);

    res.json({
        current,
        optimized: {
            ...optimized,
            vehicle: altVehicle,
            loadFactor: betterLoad,
            distance: distanceKm * 0.95
        },
        savedCO2: Math.round(savings * 10) / 10,
        savingPercent,
        insight: savings > 0 
            ? `By switching to ${altVehicle} and consolidating loads to ${(betterLoad*100).toFixed(0)}%, you can save ${savingPercent}% emissions.`
            : "Current route is heavily optimized already."
    });
});

// Generate Lane Carbon Report
router.post("/report/generate", (req, res) => {
    const { origin, destination } = req.body;
    if (!origin || !destination) {
        return res.status(400).json({ error: "Missing origin or destination" });
    }

    const scriptPath = path.join(__dirname, "..", "generate_report.py");
    const command = `python "${scriptPath}" --origin "${origin}" --dest "${destination}"`;

    exec(command, (error, stdout, stderr) => {
        if (error) {
            console.error("Error executing Python script:", error);
            console.error(stderr);
            return res.status(500).json({ error: "Failed to generate report" });
        }

        try {
            const reportData = JSON.parse(stdout.trim());
            if (reportData.error) {
                return res.status(404).json({ error: reportData.error });
            }
            res.json(reportData);
        } catch (parseError) {
            console.error("Failed to parse Python output:", parseError);
            console.error("Output was:", stdout);
            res.status(500).json({ error: "Failed to parse report generation output" });
        }
    });
});

// Download Generated Word Document
router.get("/report/download", (req, res) => {
    const { file } = req.query;
    if (!file) {
        return res.status(400).send("No file specified");
    }
    
    // Ensure the file exists and is within the reports directory
    const repoReportPath = path.join(__dirname, "..", "reports");
    const parsedPath = path.parse(file);
    const absolutePath = path.join(repoReportPath, parsedPath.base); // Secure against path traversal

    if (!fs.existsSync(absolutePath)) {
        return res.status(404).send("File not found");
    }

    // Attempt to download the file
    res.download(absolutePath, parsedPath.base, (err) => {
        if (err) {
            console.error("Error downloading file:", err);
            // Error header sent check
            if (!res.headersSent) {
                res.status(500).send("Error downloading file");
            }
        }
    });
});

// Generate Lane Forecast
router.post("/forecast/generate", (req, res) => {
    const { origin, destination, horizon } = req.body;
    if (!origin || !destination) {
        return res.status(400).json({ error: "Missing origin or destination" });
    }

    const scriptPath = path.join(__dirname, "..", "generate_forecast.py");
    const hrz = horizon || 6;
    const command = `python "${scriptPath}" --origin "${origin}" --dest "${destination}" --horizon ${hrz}`;

    exec(command, (error, stdout, stderr) => {
        if (error) {
            console.error("Error executing Python script:", error);
            console.error(stderr);
            return res.status(500).json({ error: "Failed to generate forecast" });
        }

        try {
            const reportData = JSON.parse(stdout.trim());
            if (reportData.error) {
                return res.status(404).json({ error: reportData.error });
            }
            res.json(reportData);
        } catch (parseError) {
            console.error("Failed to parse Python output:", parseError);
            console.error("Output was:", stdout);
            res.status(500).json({ error: "Failed to parse forecast generation output" });
        }
    });
});


export default router;
