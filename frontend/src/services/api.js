import axiosInstance from '../Axios/Axios';

/**
 * Fetch the main dashboard data (KPIs, recent shipments, lane analytics).
 */
export const fetchDashboard = async () => {
  const { data } = await axiosInstance.get('/api/carbon/dashboard');
  return data;
};

/**
 * Calculate CO₂ emissions for a single shipment.
 * @param {number} distanceKm
 * @param {number} weightKg
 * @param {string} vehicleType
 * @param {number} loadFactor
 */
export const calculateEmission = async (distanceKm, weightKg, vehicleType, loadFactor = 0.75) => {
  const { data } = await axiosInstance.post('/api/carbon/calculate', {
    distanceKm,
    weightKg,
    vehicleType,
    loadFactor,
  });
  return data;
};

/**
 * Get optimization suggestions for a shipment route.
 * @param {number} distanceKm
 * @param {number} weightKg
 * @param {string} vehicleType
 * @param {number} loadFactor
 */
export const optimizeRoute = async (distanceKm, weightKg, vehicleType, loadFactor = 0.75) => {
  const { data } = await axiosInstance.post('/api/carbon/optimize', {
    distanceKm,
    weightKg,
    vehicleType,
    loadFactor,
  });
  return data;
};

/**
 * Health check for the backend engine.
 */
export const checkHealth = async () => {
  const { data } = await axiosInstance.get('/api/health');
  return data;
};

/**
 * Generate Lane Carbon Report
 * @param {string} origin
 * @param {string} destination
 */
export const generateLaneReport = async (origin, destination) => {
  const { data } = await axiosInstance.post('/api/carbon/report/generate', {
    origin,
    destination
  });
  return data;
};

export const getDownloadReportUrl = (fileName) => {
  // Use the API server's origin if we are connecting directly, else use relative for Vite proxy
  return `/api/carbon/report/download?file=${encodeURIComponent(fileName)}`;
};

/**
 * Generate Lane Forecast
 * @param {string} origin
 * @param {string} destination
 * @param {number} horizon format: months
 */
export const generateForecast = async (origin, destination, horizon = 6) => {
  const { data } = await axiosInstance.post('/api/carbon/forecast/generate', {
    origin,
    destination,
    horizon
  });
  return data;
};
