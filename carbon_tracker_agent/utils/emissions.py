def calculate_emissions(distance_km: float, weight_ton: float, vehicle_type: str, utilization_percent: float = 100.0) -> float:
    factors = {
        "Heavy Truck": 0.08,
        "Medium Truck": 0.12,
        "Light Truck": 0.18,
    }
    base_factor = factors.get(vehicle_type, 0.12)
    
    # Utilization penalty
    util_penalty = 1.0
    if utilization_percent < 50:
        util_penalty = 1.2
    elif utilization_percent < 80:
        util_penalty = 1.05
        
    return distance_km * weight_ton * base_factor * util_penalty
