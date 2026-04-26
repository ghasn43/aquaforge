"""
Cost and scale-up analysis for atmospheric water harvesting systems.
"""

from data_models import CostModel, MembraneFormulation, DeviceConfiguration
from typing import Dict


class CostingEngine:
    """Economic analysis and scale-up modeling."""

    # Cost reference data (estimated 2026 values)
    COST_DATABASE = {
        "feedstock": {
            "peanut_shell": 1.5,
            "banana_peel": 1.0,
            "phoenix_date": 3.0,
            "algae": 5.0,
            "fungal_biomass": 4.5,
            "rice_husk": 1.2,
        },
        "polymers": {
            "chitosan": 45.0,  # USD per kg
            "modified_chitosan": 55.0,
            "silica_based": 65.0,
            "generic_biopolymer": 40.0,
        },
        "nanoparticles": {
            "green_silica": 150.0,
            "zno": 180.0,
            "fe_zn_si": 220.0,
            "generic": 100.0,
        },
    }

    # Scale-up cost multipliers
    SCALE_LEVEL_MULTIPLIERS = {
        "Lab": {
            "fixed_overhead": 200.0,
            "batch_size_factor": 1.0,
            "labor_factor": 1.5,
            "testing_factor": 2.0,
        },
        "Pilot": {
            "fixed_overhead": 500.0,
            "batch_size_factor": 0.8,
            "labor_factor": 1.2,
            "testing_factor": 1.5,
        },
        "Pre-commercial": {
            "fixed_overhead": 2000.0,
            "batch_size_factor": 0.6,
            "labor_factor": 1.0,
            "testing_factor": 1.2,
        },
    }

    @staticmethod
    def calculate_membrane_cost(
        membrane: MembraneFormulation,
        feedstock_cost_kg: float = 2.5,
        polymer_cost_kg: float = 45.0,
        nanoparticle_cost_kg: float = 150.0,
    ) -> float:
        """Calculate cost to produce one membrane."""
        # Estimate material quantities
        # Assume membrane: ~5g polymer + 1g nanoparticles (for typical loading)

        polymer_needed_g = 5.0
        np_needed_g = (membrane.nanoparticle_loading_wt_pct / 100.0) * polymer_needed_g

        polymer_cost = (polymer_needed_g / 1000.0) * polymer_cost_kg
        np_cost = (np_needed_g / 1000.0) * nanoparticle_cost_kg

        # Labor and overhead
        labor_overhead = 5.0  # USD per membrane

        total_cost = polymer_cost + np_cost + labor_overhead

        return total_cost

    @staticmethod
    def calculate_device_cost(
        device: DeviceConfiguration,
        base_device_cost: float = 200.0,
        material_complexity_factor: float = 1.0,
    ) -> float:
        """Calculate cost to fabricate one device."""
        complexity = 1.0

        # Size complexity
        total_volume = device.upper_chamber_volume_l + device.lower_chamber_volume_l
        complexity += (total_volume / 50.0) * 0.3

        # Thermal/assistance complexity
        if device.thermal_mode.value != "Passive (No Heat)":
            complexity += 0.3

        # Filtration adds cost
        if device.filtration_stage:
            complexity += 0.2

        # Material selection
        if "Polycarbonate" in device.chamber_transparency:
            material_cost = 80.0
        else:
            material_cost = 100.0  # Glass

        device_cost = base_device_cost * complexity + material_cost

        return device_cost

    @staticmethod
    def estimate_costs(
        membrane: MembraneFormulation,
        device: DeviceConfiguration,
        cost_model: CostModel,
    ) -> CostModel:
        """Estimate all costs for given configuration."""

        # Per-unit costs
        membrane_cost = CostingEngine.calculate_membrane_cost(
            membrane,
            feedstock_cost_kg=cost_model.feedstock_cost_per_kg,
            polymer_cost_kg=cost_model.polymer_cost_per_kg,
            nanoparticle_cost_kg=cost_model.nanoparticle_prep_cost_per_kg,
        )
        cost_model.cost_per_membrane = membrane_cost

        device_cost = CostingEngine.calculate_device_cost(
            device,
            base_device_cost=cost_model.device_fabrication_cost_base,
        )

        # Total prototype cost
        cost_model.prototype_cost_total = (
            (membrane_cost * 2) + device_cost  # 2 membranes (spare/backup)
        ) * cost_model.prototype_count

        # Get scale multipliers
        scale_mults = CostingEngine.SCALE_LEVEL_MULTIPLIERS.get(
            cost_model.scale_level, {}
        )

        # CAPEX (equipment, setup, molds)
        capex_base = 5000.0 if cost_model.scale_level == "Lab" else (
            15000.0 if cost_model.scale_level == "Pilot" else 50000.0
        )
        cost_model.capex_estimate = capex_base

        # OPEX (per batch)
        opex_per_batch = (
            (cost_model.cost_per_membrane * cost_model.batch_size_units)
            * (scale_mults.get("labor_factor", 1.0) * cost_model.labor_multiplier)
            * (scale_mults.get("testing_factor", 1.0) * cost_model.testing_multiplier)
        )
        cost_model.opex_estimate = opex_per_batch

        # Cost per liter harvested
        # Assume 10-year device life, 200 L harvested over device life (conservative)
        estimated_water_liters = 200.0
        cost_model.cost_per_liter_harvested = cost_model.prototype_cost_total / estimated_water_liters

        # Scale-up burden (cost increase per unit as volume increases)
        scale_burden = (
            1.0
            * (
                (cost_model.scale_level == "Pilot") * 0.15
                + (cost_model.scale_level == "Pre-commercial") * 0.25
            )
        )
        cost_model.scale_up_burden = scale_burden

        return cost_model

    @staticmethod
    def get_commercial_readiness_snapshot(
        membrane: MembraneFormulation,
        device: DeviceConfiguration,
    ) -> Dict[str, str]:
        """Generate readiness assessment."""
        snapshot = {}

        # Scientific readiness: membrane + device performance
        membrane_stability = getattr(membrane, 'mechanical_stability', 0.7)
        snapshot["Scientific Readiness"] = (
            "TRL 3-4: Proof-of-concept demonstrated"
            if membrane_stability > 0.7
            else "TRL 2-3: Conceptual, early experiments"
        )

        # Fabrication readiness
        manufacturability = getattr(membrane, 'manufacturability_score', 0.7)
        snapshot["Fabrication Readiness"] = (
            "TRL 4-5: Scalable production process"
            if manufacturability > 0.75
            else (
                "TRL 3-4: Small-batch capable"
                if manufacturability > 0.6
                else "TRL 2-3: Requires process development"
            )
        )

        # Supply chain readiness
        snapshot["Supply-Chain Readiness"] = (
            "TRL 4-5: Materials readily available"
        )

        # Field readiness
        device_class = device.device_class.value
        snapshot["Field-Readiness"] = (
            "TRL 6-7: Pilot field testing ready"
            if "Pilot" in device_class or "Demonstrator" in device_class
            else "TRL 4-5: Bench prototype phase"
        )

        return snapshot

    @staticmethod
    def estimate_scaling_path(
        cost_model: CostModel,
    ) -> Dict[str, float]:
        """Estimate cost progression as scale increases."""
        path = {}

        for scale in ["Lab", "Pilot", "Pre-commercial"]:
            scale_factor = {
                "Lab": 1.0,
                "Pilot": 0.8,
                "Pre-commercial": 0.6,
            }.get(scale, 1.0)

            path[scale] = cost_model.cost_per_membrane * scale_factor

        return path

    @staticmethod
    def get_cost_summary_text(cost_model: CostModel) -> str:
        """Generate human-readable cost summary."""
        summary = f"""
**Cost & Scale-Up Summary ({cost_model.scale_level} Scale)**

- **Cost per Membrane**: ${cost_model.cost_per_membrane:.2f}
- **Total Prototype Cost**: ${cost_model.prototype_cost_total:.2f}
- **Cost per Liter Harvested**: ${cost_model.cost_per_liter_harvested:.2f}

**Capital/Operating Breakdown:**
- CAPEX (Equipment Setup): ${cost_model.capex_estimate:.2f}
- OPEX (Per Batch): ${cost_model.opex_estimate:.2f}
- Scale-Up Burden: {cost_model.scale_up_burden * 100:.1f}%

**Sustainability-Adjusted Cost Score**: {(1.0 - cost_model.scale_up_burden) * 0.8:.2f} / 1.0

*Note: Costs are estimates based on material assumptions and current market data.*
"""
        return summary.strip()
