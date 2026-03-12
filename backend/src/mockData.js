import { calculateEmission } from './engine.js';

const LANES = [
    { id: "MUM-DEL", from: "Mumbai", to: "Delhi", distance: 1421, baseLoad: 0.78 },
    { id: "DEL-BLR", from: "Delhi", to: "Bangalore", distance: 2147, baseLoad: 0.65 },
    { id: "MUM-CHN", from: "Mumbai", to: "Chennai", distance: 1338, baseLoad: 0.82 },
    { id: "BLR-HYD", from: "Bangalore", to: "Hyderabad", distance: 569, baseLoad: 0.71 }
];

const VEHICLE_TYPES = ["HCV-Diesel", "MCV-Diesel", "LCV-Diesel", "CNG-Truck", "EV-Truck", "HCV-BS6"];
const STATUSES = ["In Transit", "Delayed", "Delivered", "Loading", "Idle"];

export const generateShipments = (count = 20) => {
    return Array.from({ length: count }, (_, i) => {
        const lane = LANES[Math.floor(Math.random() * LANES.length)];
        const vehicle = VEHICLE_TYPES[Math.floor(Math.random() * VEHICLE_TYPES.length)];
        const weightKg = 2000 + Math.random() * 18000; 
        const loadFactor = 0.4 + Math.random() * 0.6;
        const anomaly = Math.random() > 0.85 ? 1.3 : 1.0;
        
        const emission = calculateEmission(lane.distance, weightKg, vehicle, loadFactor, anomaly);
        
        return {
            id: `SHP${String(100000 + Math.floor(Math.random() * 90000)).slice(0, 8)}`,
            laneId: lane.id,
            from: lane.from,
            to: lane.to,
            distance: lane.distance,
            weightKg: Math.round(weightKg),
            vehicle,
            loadFactor: Math.round(loadFactor * 100),
            hasAnomaly: anomaly > 1.0,
            status: STATUSES[Math.floor(Math.random() * STATUSES.length)],
            timestamp: new Date(Date.now() - Math.random() * 86400000).toISOString(),
            ...emission
        };
    });
};

export const generateLaneAnalytics = () => {
    return LANES.map((lane) => {
        const shipmentCount = 10 + Math.floor(Math.random() * 40);
        const avgLoad = lane.baseLoad + (Math.random() - 0.5) * 0.15;
        const dominantVehicle = VEHICLE_TYPES[Math.floor(Math.random() * VEHICLE_TYPES.length)];
        const mockWeight = 12000;
        const emission = calculateEmission(lane.distance, mockWeight, dominantVehicle, avgLoad);
        const totalCO2 = emission.co2Kg * shipmentCount;
        
        return {
            ...lane,
            shipmentCount,
            avgLoadFactor: Math.round(avgLoad * 100),
            avgCO2PerShipment: emission.co2Kg,
            totalCO2: Math.round(totalCO2),
            riskLevel: totalCO2 > 20000 ? "critical" : totalCO2 > 10000 ? "high" : "low",
            dominantVehicle
        };
    });
};
