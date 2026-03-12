import axios from '../Axios/Axios';

export const calculateCarbonEmission = async (distance, vehicleType) => {
  try {

    await new Promise(resolve => setTimeout(resolve, 800));

    const EMISSION_FACTORS = {
      "truck": 0.161,
      "van": 0.120,
      "car": 0.089
    };
    
    if (!EMISSION_FACTORS[vehicleType]) {
      throw new Error("Invalid vehicle type");
    }

    const mockEmission = Number(distance) * EMISSION_FACTORS[vehicleType];

    return {
      distance: Number(distance),
      vehicle_type: vehicleType,
      carbon_emission: mockEmission
    };
  } catch (error) {
    console.error("Failed to calculate carbon emission via axios", error);
    throw error;
  }
};
