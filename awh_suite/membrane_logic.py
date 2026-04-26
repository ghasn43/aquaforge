"""
Membrane design and composition logic.
Heuristic-based calculations for membrane formulation performance.
"""

import math
from data_models import (
    MembraneFormulation, PolymerMatrix, LayerConfiguration
)


class MembraneDesigner:
    """Engineer for membrane formulation design and performance estimation."""

    # Polymer matrix base properties
    POLYMER_PROPERTIES = {
        PolymerMatrix.CHITOSAN: {
            "base_hydrophilicity": 0.85,
            "base_stability": 0.75,
            "base_mechanical_strength": 0.60,
            "manufacturability": 0.90,
            "sustainability": 0.95,
        },
        PolymerMatrix.MODIFIED_CHITOSAN: {
            "base_hydrophilicity": 0.80,
            "base_stability": 0.80,
            "base_mechanical_strength": 0.70,
            "manufacturability": 0.85,
            "sustainability": 0.90,
        },
        PolymerMatrix.SILICA_CHITOSAN: {
            "base_hydrophilicity": 0.88,
            "base_stability": 0.85,
            "base_mechanical_strength": 0.75,
            "manufacturability": 0.80,
            "sustainability": 0.85,
        },
        PolymerMatrix.ZNO_CHITOSAN: {
            "base_hydrophilicity": 0.82,
            "base_stability": 0.78,
            "base_mechanical_strength": 0.72,
            "manufacturability": 0.75,
            "sustainability": 0.80,
        },
        PolymerMatrix.FE_ZN_SI_CHITOSAN: {
            "base_hydrophilicity": 0.80,
            "base_stability": 0.82,
            "base_mechanical_strength": 0.78,
            "manufacturability": 0.70,
            "sustainability": 0.75,
        },
        PolymerMatrix.BIOPOLYMER_BLEND: {
            "base_hydrophilicity": 0.78,
            "base_stability": 0.76,
            "base_mechanical_strength": 0.68,
            "manufacturability": 0.70,
            "sustainability": 0.92,
        },
    }

    # Dispersion quality impacts
    DISPERSION_QUALITY_FACTOR = {
        "Poor": 0.6,
        "Fair": 0.75,
        "Good": 0.90,
        "Excellent": 1.0,
    }

    # Crosslink density impacts
    CROSSLINK_DENSITY_FACTOR = {
        "Low": 0.7,
        "Medium": 0.85,
        "High": 0.95,
    }

    # Layer configuration multipliers
    LAYER_CONFIG_FACTORS = {
        LayerConfiguration.SINGLE: {
            "adsorption_factor": 0.8,
            "desorption_ease": 0.75,
            "balance_score": 0.75,
        },
        LayerConfiguration.DUAL_HYDRO_PHOBIC: {
            "adsorption_factor": 0.85,
            "desorption_ease": 0.70,
            "balance_score": 0.80,
        },
        LayerConfiguration.DUAL_HYDRO_PHILIC: {
            "adsorption_factor": 0.90,
            "desorption_ease": 0.65,
            "balance_score": 0.82,
        },
        LayerConfiguration.TRIPLE: {
            "adsorption_factor": 0.92,
            "desorption_ease": 0.60,
            "balance_score": 0.80,
        },
    }

    @staticmethod
    def estimate_contact_angle(formulation: MembraneFormulation) -> float:
        """
        Estimate contact angle (degrees) based on formulation.
        Lower angle = more hydrophilic.
        """
        polymer_props = MembraneDesigner.POLYMER_PROPERTIES.get(
            formulation.polymer_matrix, {}
        )
        base_hydrophilicity = polymer_props.get("base_hydrophilicity", 0.8)

        # Nanoparticles influence
        np_effect = 0.0
        if "Silica" in formulation.nanoparticle_type:
            np_effect = 0.1 * (formulation.nanoparticle_loading_wt_pct / 100.0)
        elif "ZnO" in formulation.nanoparticle_type:
            np_effect = 0.05 * (formulation.nanoparticle_loading_wt_pct / 100.0)
        elif "Fe" in formulation.nanoparticle_type or "Zn" in formulation.nanoparticle_type:
            np_effect = 0.08 * (formulation.nanoparticle_loading_wt_pct / 100.0)

        effective_hydrophilicity = min(1.0, base_hydrophilicity + np_effect)

        # Contact angle: ~140°=hydrophobic, ~100°=moderate, ~60°=hydrophilic
        # Formula: angle ≈ 140 - (hydrophilicity * 100)
        contact_angle = 140.0 - (effective_hydrophilicity * 100.0)

        return max(20.0, min(140.0, contact_angle))

    @staticmethod
    def estimate_adsorption_strength(formulation: MembraneFormulation) -> float:
        """Estimate water adsorption capacity (0-1 score)."""
        polymer_props = MembraneDesigner.POLYMER_PROPERTIES.get(
            formulation.polymer_matrix, {}
        )
        base_hydrophilicity = polymer_props.get("base_hydrophilicity", 0.8)

        # Nanoparticle loading impact (optimal around 10-20%)
        np_loading_pct = formulation.nanoparticle_loading_wt_pct
        loading_factor = 1.0
        if np_loading_pct < 5:
            loading_factor = np_loading_pct / 5.0 * 0.8
        elif np_loading_pct < 15:
            loading_factor = 0.8 + (np_loading_pct - 5) / 10.0 * 0.2
        elif np_loading_pct < 25:
            loading_factor = 1.0
        else:
            # Overloading reduces effectiveness
            loading_factor = max(0.6, 1.0 - ((np_loading_pct - 25) / 100.0))

        # Porosity helps
        porosity_factor = 0.5 + (formulation.porosity_pct / 100.0) * 0.5

        # Dispersion quality
        disp_quality = MembraneDesigner.DISPERSION_QUALITY_FACTOR.get(
            formulation.particle_dispersion_quality, 0.8
        )

        # Layer configuration
        layer_factors = MembraneDesigner.LAYER_CONFIG_FACTORS.get(
            formulation.layer_config, {}
        )
        adsorption_factor = layer_factors.get("adsorption_factor", 0.8)

        adsorption_score = (
            base_hydrophilicity * 0.3
            + loading_factor * 0.3
            + porosity_factor * 0.2
            + disp_quality * 0.1
            + adsorption_factor * 0.1
        )

        return min(1.0, adsorption_score)

    @staticmethod
    def estimate_desorption_ease(formulation: MembraneFormulation) -> float:
        """Estimate ease of water release (0-1 score, higher = easier)."""
        # Desorption is easier with:
        # - Higher porosity
        # - Lower crosslink density
        # - Lower loading
        # - Certain layer configs

        crosslink_factor = MembraneDesigner.CROSSLINK_DENSITY_FACTOR.get(
            formulation.crosslink_density, 0.85
        )
        # Higher crosslink = harder desorption
        crosslink_factor = 1.0 - (crosslink_factor - 0.5)

        # Lower loading helps desorption
        loading_factor = 1.0 - (formulation.nanoparticle_loading_wt_pct / 100.0) * 0.3

        # Porosity helps
        porosity_factor = formulation.porosity_pct / 100.0

        # Layer configuration impact
        layer_factors = MembraneDesigner.LAYER_CONFIG_FACTORS.get(
            formulation.layer_config, {}
        )
        desorption_factor = layer_factors.get("desorption_ease", 0.75)

        ease_score = (
            crosslink_factor * 0.3
            + loading_factor * 0.2
            + porosity_factor * 0.3
            + desorption_factor * 0.2
        )

        return min(1.0, max(0.0, ease_score))

    @staticmethod
    def estimate_mechanical_stability(formulation: MembraneFormulation) -> float:
        """Estimate mechanical strength and stability (0-1 score)."""
        polymer_props = MembraneDesigner.POLYMER_PROPERTIES.get(
            formulation.polymer_matrix, {}
        )
        base_mechanical = polymer_props.get("base_mechanical_strength", 0.7)

        # Thickness improves strength (up to a point)
        thickness_factor = min(1.0, formulation.thickness_um / 200.0)

        # Crosslink density improves stability
        crosslink_factor = MembraneDesigner.CROSSLINK_DENSITY_FACTOR.get(
            formulation.crosslink_density, 0.85
        )

        # Nanoparticle loading can help or hurt
        loading_pct = formulation.nanoparticle_loading_wt_pct
        loading_factor = 1.0 if loading_pct < 15 else max(0.7, 1.0 - ((loading_pct - 15) / 50.0))

        stability = (
            base_mechanical * 0.4
            + thickness_factor * 0.2
            + crosslink_factor * 0.3
            + loading_factor * 0.1
        )

        return min(1.0, stability)

    @staticmethod
    def estimate_moisture_capture(formulation: MembraneFormulation) -> float:
        """Estimate moisture capture capability (0-1 score)."""
        adsorption = MembraneDesigner.estimate_adsorption_strength(formulation)
        porosity_factor = formulation.porosity_pct / 100.0

        # Silica/ZnO nanoparticles are good for moisture
        np_bonus = 0.0
        if "Silica" in formulation.nanoparticle_type:
            np_bonus = 0.15
        elif "ZnO" in formulation.nanoparticle_type:
            np_bonus = 0.10

        moisture_score = adsorption * 0.5 + porosity_factor * 0.3 + np_bonus * 0.2

        return min(1.0, moisture_score)

    @staticmethod
    def estimate_thermal_robustness(formulation: MembraneFormulation) -> float:
        """Estimate ability to withstand thermal cycling (0-1 score)."""
        # Thermal robustness comes from:
        # - Mechanical stability
        # - Crosslink density
        # - Particle size (smaller more robust)

        mechanical = MembraneDesigner.estimate_mechanical_stability(formulation)
        crosslink_factor = MembraneDesigner.CROSSLINK_DENSITY_FACTOR.get(
            formulation.crosslink_density, 0.85
        )

        # Smaller particles = better thermal robustness
        particle_size = formulation.particle_size_nm
        size_factor = max(0.6, 1.0 - ((particle_size - 20) / 200.0))

        robustness = mechanical * 0.4 + crosslink_factor * 0.4 + size_factor * 0.2

        return min(1.0, robustness)

    @staticmethod
    def estimate_manufacturability(formulation: MembraneFormulation) -> float:
        """Estimate ease of manufacturing (0-1 score)."""
        polymer_props = MembraneDesigner.POLYMER_PROPERTIES.get(
            formulation.polymer_matrix, {}
        )
        base_manufacturability = polymer_props.get("manufacturability", 0.8)

        # High loading reduces manufacturability
        loading_penalty = (formulation.nanoparticle_loading_wt_pct / 100.0) * 0.2

        # Complex layer configs reduce manufacturability
        layer_config = formulation.layer_config
        layer_penalty = {
            LayerConfiguration.SINGLE: 0.0,
            LayerConfiguration.DUAL_HYDRO_PHOBIC: 0.15,
            LayerConfiguration.DUAL_HYDRO_PHILIC: 0.15,
            LayerConfiguration.TRIPLE: 0.25,
        }.get(layer_config, 0.1)

        manufacturability = base_manufacturability - loading_penalty - layer_penalty

        return min(1.0, max(0.3, manufacturability))

    @staticmethod
    def estimate_sustainability(formulation: MembraneFormulation) -> float:
        """Estimate sustainability score (0-1 scale)."""
        polymer_props = MembraneDesigner.POLYMER_PROPERTIES.get(
            formulation.polymer_matrix, {}
        )
        polymer_sustainability = polymer_props.get("sustainability", 0.8)

        # Green nanoparticles boost sustainability
        np_sustainability = 0.0
        if "Silica" in formulation.nanoparticle_type or "ZnO" in formulation.nanoparticle_type:
            np_sustainability = 0.85
        elif "Fe" in formulation.nanoparticle_type or "Zn" in formulation.nanoparticle_type:
            np_sustainability = 0.75
        else:
            np_sustainability = 0.65

        # Lower loading is more sustainable (uses less material)
        loading_factor = max(0.7, 1.0 - (formulation.nanoparticle_loading_wt_pct / 100.0) * 0.4)

        sustainability = (
            polymer_sustainability * 0.4 + np_sustainability * 0.4 + loading_factor * 0.2
        )

        return min(1.0, sustainability)

    @staticmethod
    def calculate_all_properties(formulation: MembraneFormulation) -> MembraneFormulation:
        """Calculate all performance properties and return updated formulation."""
        formulation.estimated_contact_angle_deg = MembraneDesigner.estimate_contact_angle(
            formulation
        )
        formulation.estimated_adsorption_strength = (
            MembraneDesigner.estimate_adsorption_strength(formulation)
        )
        formulation.desorption_ease = MembraneDesigner.estimate_desorption_ease(formulation)
        formulation.mechanical_stability = MembraneDesigner.estimate_mechanical_stability(
            formulation
        )
        formulation.moisture_capture_score = MembraneDesigner.estimate_moisture_capture(
            formulation
        )
        formulation.thermal_robustness = MembraneDesigner.estimate_thermal_robustness(
            formulation
        )
        formulation.manufacturability_score = MembraneDesigner.estimate_manufacturability(
            formulation
        )
        formulation.sustainability_score = MembraneDesigner.estimate_sustainability(
            formulation
        )

        return formulation

    @staticmethod
    def get_risk_flags(formulation: MembraneFormulation) -> list:
        """Identify design risk flags."""
        flags = []

        if formulation.mechanical_stability < 0.5:
            flags.append("⚠️ Low mechanical stability - may degrade under stress")

        if formulation.nanoparticle_loading_wt_pct > 25:
            flags.append("⚠️ High nanoparticle loading - risk of aggregation")

        if formulation.particle_dispersion_quality == "Poor":
            flags.append("⚠️ Poor nanoparticle dispersion - performance may be compromised")

        if (
            formulation.estimated_adsorption_strength > 0.8
            and formulation.desorption_ease < 0.4
        ):
            flags.append(
                "⚠️ Strong adsorption but difficult desorption - may require heating"
            )

        if formulation.manufacturability_score < 0.5:
            flags.append("⚠️ Complex design - high manufacturing difficulty")

        return flags

    @staticmethod
    def get_polymer_options() -> dict:
        """Return available polymer matrices."""
        return {pm: pm.value for pm in PolymerMatrix}

    @staticmethod
    def get_layer_config_options() -> dict:
        """Return available layer configurations."""
        return {lc: lc.value for lc in LayerConfiguration}
