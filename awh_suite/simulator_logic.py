"""
Atmospheric water harvesting performance simulator.
Heuristic-based predictions for system performance under various conditions.
"""

from data_models import (
    SimulationResult, MembraneFormulation, DeviceConfiguration,
    AtmosphericConditions
)


class AwhSimulator:
    """Simulator for atmospheric water harvesting performance."""

    @staticmethod
    def simulate_performance(
        membrane: MembraneFormulation,
        device: DeviceConfiguration,
        conditions: AtmosphericConditions,
    ) -> SimulationResult:
        """
        Simulate AWH performance under given conditions.
        All outputs are design-stage heuristic estimates.
        """

        result = SimulationResult()

        # ========== ADSORPTION PHASE ==========
        # Higher RH and better membrane adsorption = higher adsorption score
        rh_factor = conditions.relative_humidity_pct / 100.0
        membrane_adsorption = getattr(membrane, 'estimated_adsorption_strength', 0.75)
        base_adsorption = (rh_factor * 0.6 + membrane_adsorption * 0.4)

        # Temperature effect: cooler = better adsorption
        temp_factor = max(0.5, 1.0 - (conditions.ambient_temperature_c / 40.0) * 0.3)
        result.adsorption_score = base_adsorption * temp_factor * 0.95  # Normalize to <1.0

        # ========== DESORPTION PHASE ==========
        # Desorption efficiency depends on thermal input and membrane ease
        desorption_base = getattr(membrane, 'desorption_ease', 0.7)

        # Thermal mode boosts desorption
        thermal_boost = {
            "Passive (No Heat)": 0.0,
            "Low Heat Assist": 0.25,
            "Solar Assisted": 0.40,
            "Lab Assisted": 0.50,
        }.get(device.thermal_mode.value, 0.0)

        # Day/night affects solar heating
        if conditions.day_night_mode == "Day" and device.thermal_mode.value in [
            "Solar Assisted"
        ]:
            thermal_boost += 0.15

        result.desorption_efficiency = min(0.95, (desorption_base + thermal_boost) * 0.95)

        # ========== CONDENSATION LIKELIHOOD ==========
        # Condensation improves with:
        # - High RH (more vapor to condense)
        # - Cool device surfaces (from passive/solar thermal cycling)
        # - Device design (cone geometry helps)

        cone_geometry_factor = max(0.6, 1.0 - abs(60.0 - device.cone_angle_deg) / 100.0)
        condensation_likelihood = (
            rh_factor * 0.4 + temp_factor * 0.3 + cone_geometry_factor * 0.3
        )
        result.condensation_likelihood = min(1.0, condensation_likelihood)

        # ========== WATER YIELD CALCULATION ==========
        # Based on adsorption and desorption and device surface area
        # Reference: typical activated carbon ~0.2-0.4 g/g under ideal conditions

        # Device surface area factor
        import math
        radius = device.overall_diameter_cm / 2.0
        membrane_area_cm2 = 2 * math.pi * radius * device.upper_chamber_height_cm + math.pi * (radius ** 2)

        # Load factor: how much adsorbent is in system
        # Assume membrane thickness and area translate to ~1-5g of active material
        active_material_g = (membrane_area_cm2 / 100.0) * 2.0  # Rough estimate

        # Base water uptake per gram of adsorbent under ideal conditions
        base_uptake_g_per_g = result.adsorption_score * 0.35  # Max ~0.35 g/g

        # Environmental factor: how "ideal" are the conditions
        # RH impact, temperature window, airflow
        rh_optimal = 1.0 if conditions.relative_humidity_pct > 40 else 0.5
        airflow_factor = {
            "Low": 0.7,
            "Natural": 1.0,
            "Medium": 1.15,
            "High": 1.25,
        }.get(conditions.airflow_level, 1.0)

        # Duty cycle: 24h operation
        duty_cycle_hours = conditions.cycle_duration_hours
        cycles_per_day = 24.0 / duty_cycle_hours if duty_cycle_hours > 0 else 1.0

        # Calculate yield
        water_per_cycle_g = (
            active_material_g
            * base_uptake_g_per_g
            * result.desorption_efficiency
            * rh_optimal
            * airflow_factor
        )

        # Efficiency losses
        collection_efficiency = 0.85  # Some water lost in system
        filtration_efficiency = 0.95 if device.filtration_stage else 1.0

        result.predicted_water_yield_ml_g = water_per_cycle_g * collection_efficiency * filtration_efficiency
        result.predicted_water_yield_l_kg_day = (
            result.predicted_water_yield_ml_g * cycles_per_day * active_material_g * 1.05 / 1000.0
        )

        # Efficiency percentages
        result.collection_efficiency_pct = collection_efficiency * 100.0
        result.filtration_efficiency_pct = filtration_efficiency * 100.0

        # ========== OVERALL RELATIVE PERFORMANCE ==========
        # Score relative to baseline MOF system (~0.4-0.6 L/kg/day)
        baseline_yield = 0.5
        relative_performance = min(
            1.0,
            result.predicted_water_yield_l_kg_day / baseline_yield
        )
        result.relative_performance_score = relative_performance

        # ========== CONFIDENCE LEVEL ==========
        # Confidence depends on how "standard" the conditions are
        confidence_score = 0.0
        if 40 < conditions.relative_humidity_pct < 80:
            confidence_score += 0.3
        else:
            confidence_score += 0.1

        if 15 < conditions.ambient_temperature_c < 35:
            confidence_score += 0.3
        else:
            confidence_score += 0.1

        if conditions.airflow_level in ["Natural", "Medium"]:
            confidence_score += 0.2
        else:
            confidence_score += 0.1

        if device.device_class.value in ["Bench Prototype", "Pilot Prototype"]:
            confidence_score += 0.2
        else:
            confidence_score += 0.1

        if confidence_score < 0.3:
            result.confidence_level = "Low"
        elif confidence_score < 0.6:
            result.confidence_level = "Medium"
        else:
            result.confidence_level = "High"

        # ========== PERFORMANCE WINDOW ==========
        if result.predicted_water_yield_l_kg_day < 0.1:
            result.performance_window = "Limited - design requires optimization"
        elif result.predicted_water_yield_l_kg_day < 0.3:
            result.performance_window = "Moderate - suitable for bench/pilot phase"
        elif result.predicted_water_yield_l_kg_day < 0.6:
            result.performance_window = "Strong - viable for field testing"
        else:
            result.performance_window = "Excellent - promising commercial potential"

        # ========== STAGE CONTRIBUTIONS ==========
        result.stage_contributions = {
            "Adsorption": float(result.adsorption_score * 25),  # Normalized to 0-25%
            "Desorption": float(result.desorption_efficiency * 25),
            "Condensation": float(result.condensation_likelihood * 20),
            "Collection": float(result.collection_efficiency_pct / 5),
            "Filtration": float(result.filtration_efficiency_pct / 5),
        }

        result.notes = (
            "Design-stage heuristic estimate based on selected formulation, device, and environmental conditions. "
            "Not a certified performance claim. Recommend bench-scale validation experiments."
        )

        return result

    @staticmethod
    def get_water_yield_vs_rh(
        membrane: MembraneFormulation,
        device: DeviceConfiguration,
        base_conditions: AtmosphericConditions,
    ) -> list:
        """Generate water yield curve across RH range (20%-100%)."""
        curve_data = []

        for rh in range(20, 101, 5):
            test_conditions = AtmosphericConditions(
                relative_humidity_pct=rh,
                ambient_temperature_c=base_conditions.ambient_temperature_c,
                day_night_mode=base_conditions.day_night_mode,
                airflow_level=base_conditions.airflow_level,
            )
            result = AwhSimulator.simulate_performance(membrane, device, test_conditions)
            curve_data.append({
                "rh_pct": rh,
                "yield_l_kg_day": max(0, result.predicted_water_yield_l_kg_day),
                "adsorption_score": result.adsorption_score,
            })

        return curve_data

    @staticmethod
    def get_water_yield_vs_temperature(
        membrane: MembraneFormulation,
        device: DeviceConfiguration,
        base_conditions: AtmosphericConditions,
    ) -> list:
        """Generate water yield curve across temperature range (10°C - 40°C)."""
        curve_data = []

        for temp in range(10, 41, 2):
            test_conditions = AtmosphericConditions(
                relative_humidity_pct=base_conditions.relative_humidity_pct,
                ambient_temperature_c=temp,
                day_night_mode=base_conditions.day_night_mode,
                airflow_level=base_conditions.airflow_level,
            )
            result = AwhSimulator.simulate_performance(membrane, device, test_conditions)
            curve_data.append({
                "temp_c": temp,
                "yield_l_kg_day": max(0, result.predicted_water_yield_l_kg_day),
                "desorption_efficiency": result.desorption_efficiency,
            })

        return curve_data

    @staticmethod
    def get_adsorption_desorption_cycle(
        membrane: MembraneFormulation,
        device: DeviceConfiguration,
        conditions: AtmosphericConditions,
        cycle_duration_hours: float = 8.0,
    ) -> list:
        """Generate adsorption/desorption cycle profile."""
        cycle_data = []

        # Simulate cycle in 30-minute intervals
        intervals = int(cycle_duration_hours * 2)

        for i in range(intervals + 1):
            time_hours = (i / intervals) * cycle_duration_hours

            # Model adsorption in first half, desorption in second half
            if time_hours < cycle_duration_hours / 2.0:
                # Adsorption phase
                phase_progress = time_hours / (cycle_duration_hours / 2.0)
                adsorption_level = getattr(
                    membrane, 'estimated_adsorption_strength', 0.75
                ) * phase_progress
                desorption_level = 0.0
            else:
                # Desorption phase
                phase_progress = (time_hours - cycle_duration_hours / 2.0) / (
                    cycle_duration_hours / 2.0
                )
                adsorption_level = getattr(
                    membrane, 'estimated_adsorption_strength', 0.75
                ) * (1.0 - phase_progress)
                desorption_level = getattr(membrane, 'desorption_ease', 0.7) * phase_progress

            cycle_data.append({
                "time_hours": round(time_hours, 1),
                "adsorption_level": max(0, min(1, adsorption_level)),
                "desorption_level": max(0, min(1, desorption_level)),
                "water_accumulated_ml": (
                    adsorption_level * 10
                ),  # Arbitrary scale for visualization
            })

        return cycle_data
