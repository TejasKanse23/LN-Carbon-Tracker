export const EMISSION_FACTORS = {
    "HCV-Diesel": 2.68,
    "MCV-Diesel": 2.31,
    "LCV-Diesel": 1.98,
    "CNG-Truck": 1.12,
    "EV-Truck": 0.22,
    "HCV-BS6": 2.45,
};

export const calculateEmission = (distanceKm, weightKg, vehicleType, loadFactor = 0.75, anomalyMultiplier = 1.0) => {
    const ef = EMISSION_FACTORS[vehicleType] || 2.31;
    
    const baseFuelPer100km = vehicleType.includes("HCV") ? 35 : vehicleType.includes("MCV") ? 25 : vehicleType.includes("LCV") ? 15 : vehicleType.includes("CNG") ? 18 : vehicleType.includes("EV") ? 0 : 20;

    const utilPenalty = loadFactor < 0.5 ? 1.0 / loadFactor : 1.0;
    
    const fuelUsed = (distanceKm / 100) * baseFuelPer100km * (0.6 + (weightKg / 20000) * 0.4) * utilPenalty * anomalyMultiplier;
    
    const co2Kg = fuelUsed * ef;

    return {
        fuelUsed: Math.round(fuelUsed * 10) / 10,
        co2Kg: Math.round(co2Kg * 10) / 10,
        emissionFactor: ef,
        sustainabilityScore: co2Kg < 100 ? "A" : co2Kg < 300 ? "B" : co2Kg < 500 ? "C" : "D",
    };
};
