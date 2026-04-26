"""
Materials science logic for feedstock and nanomaterial synthesis.
Implements heuristic-based calculations for early-stage R&D guidance.
"""

from data_models import (
    FeedstockProfile, NanomaterialProfile, FeedstockType, SynthesisRoute
)
from typing import Dict, Tuple


class MaterialsDesigner:
    """Heuristic engine for feedstock and nanomaterial design."""

    # Feedstock properties database
    FEEDSTOCK_PROPERTIES = {
        FeedstockType.PEANUT_SHELL: {
            "carbon_content_pct": 45.0,
            "silica_potential": 0.8,
            "cellulose_pct": 28.0,
            "sustainability_multiplier": 0.85,
            "cost_baseline": 1.5,
        },
        FeedstockType.BANANA_PEEL: {
            "carbon_content_pct": 42.0,
            "silica_potential": 0.6,
            "cellulose_pct": 35.0,
            "sustainability_multiplier": 0.90,
            "cost_baseline": 1.0,
        },
        FeedstockType.PHOENIX_DATE: {
            "carbon_content_pct": 46.0,
            "silica_potential": 0.75,
            "cellulose_pct": 32.0,
            "sustainability_multiplier": 0.82,
            "cost_baseline": 3.0,
        },
        FeedstockType.ALGAE: {
            "carbon_content_pct": 50.0,
            "silica_potential": 0.9,
            "cellulose_pct": 20.0,
            "sustainability_multiplier": 0.95,
            "cost_baseline": 5.0,
        },
        FeedstockType.FUNGAL_BIOMASS: {
            "carbon_content_pct": 48.0,
            "silica_potential": 0.4,
            "cellulose_pct": 25.0,
            "sustainability_multiplier": 0.88,
            "cost_baseline": 4.5,
        },
        FeedstockType.RICE_HUSK: {
            "carbon_content_pct": 38.0,
            "silica_potential": 0.95,
            "cellulose_pct": 25.0,
            "sustainability_multiplier": 0.87,
            "cost_baseline": 1.2,
        },
        FeedstockType.COCONUT_SHELL: {
            "carbon_content_pct": 49.0,
            "silica_potential": 0.6,
            "cellulose_pct": 30.0,
            "sustainability_multiplier": 0.86,
            "cost_baseline": 2.0,
        },
    }

    # Synthesis route properties
    SYNTHESIS_ROUTE_PROPERTIES = {
        SynthesisRoute.GREEN_SYNTHESIS: {
            "complexity": 0.4,
            "scalability": 0.8,
            "sustainability": 0.95,
            "particle_size_nm_range": (20, 100),
            "hydrophilicity": "high",
            "cost_multiplier": 1.0,
        },
        SynthesisRoute.CALCINATION: {
            "complexity": 0.6,
            "scalability": 0.7,
            "sustainability": 0.7,
            "particle_size_nm_range": (50, 200),
            "hydrophilicity": "moderate",
            "cost_multiplier": 1.3,
        },
        SynthesisRoute.NO_CALCINATION: {
            "complexity": 0.3,
            "scalability": 0.85,
            "sustainability": 0.85,
            "particle_size_nm_range": (30, 150),
            "hydrophilicity": "moderate-high",
            "cost_multiplier": 0.9,
        },
        SynthesisRoute.TEOS_SILICA: {
            "complexity": 0.7,
            "scalability": 0.65,
            "sustainability": 0.6,
            "particle_size_nm_range": (40, 120),
            "hydrophilicity": "high",
            "cost_multiplier": 1.5,
        },
        SynthesisRoute.GEL_SILICA: {
            "complexity": 0.5,
            "scalability": 0.75,
            "sustainability": 0.8,
            "particle_size_nm_range": (50, 150),
            "hydrophilicity": "moderate-high",
            "cost_multiplier": 1.2,
        },
        SynthesisRoute.ZNO_GREEN: {
            "complexity": 0.5,
            "scalability": 0.8,
            "sustainability": 0.85,
            "particle_size_nm_range": (20, 80),
            "hydrophilicity": "moderate",
            "cost_multiplier": 1.4,
        },
        SynthesisRoute.FE_ZN_SI: {
            "complexity": 0.75,
            "scalability": 0.6,
            "sustainability": 0.75,
            "particle_size_nm_range": (30, 150),
            "hydrophilicity": "moderate",
            "cost_multiplier": 2.0,
        },
    }

    @staticmethod
    def estimate_nanomaterial_profile(
        feedstock: FeedstockProfile,
        synthesis_route: SynthesisRoute,
        drying_temp_c: float = 100.0,
        calcination_temp_c: float = 300.0,
        reaction_time_hours: float = 4.0,
    ) -> NanomaterialProfile:
        """
        Estimate predicted nanomaterial properties based on feedstock and synthesis route.
        All outputs are heuristic predictions for early-stage R&D guidance.
        """

        # Get base properties
        feedstock_props = MaterialsDesigner.FEEDSTOCK_PROPERTIES.get(
            feedstock.feedstock_type, {}
        )
        synthesis_props = MaterialsDesigner.SYNTHESIS_ROUTE_PROPERTIES.get(
            synthesis_route, {}
        )

        # Particle size influenced by drying and reaction time
        base_size_min, base_size_max = synthesis_props.get("particle_size_nm_range", (50, 150))
        size_modifier = 1.0 - (reaction_time_hours / 50.0)  # Longer reactions can favor size
        size_modifier = max(0.8, min(1.2, size_modifier))

        particle_size_min = base_size_min * size_modifier
        particle_size_max = base_size_max * size_modifier

        # Crystallinity improves with calcination temperature
        crystallinity = 60.0 + (calcination_temp_c / 4.0) if calcination_temp_c > 100 else 50.0

        # Hydrophilicity: higher with calcination and green synthesis
        hydro_base = synthesis_props.get("hydrophilicity", "moderate")
        hydro_dict = {"low": 0.3, "moderate": 0.5, "high": 0.8, "moderate-high": 0.65}
        hydrophilicity_score = hydro_dict.get(hydro_base, 0.5)

        if calcination_temp_c > 400:
            hydrophilicity_score = min(0.95, hydrophilicity_score + 0.15)

        # Water adsorption relevance (0-1 score)
        # High for silica-based, moderate for Fe/Zn/Si, high for ZnO
        route_name = synthesis_route.value.lower()
        if "silica" in route_name or "zno" in route_name:
            adsorption_relevance = 0.85 + (feedstock_props.get("silica_potential", 0.5) * 0.1)
        else:
            adsorption_relevance = 0.7

        adsorption_relevance = min(1.0, adsorption_relevance)

        # Sustainability score
        feedstock_sustainability = feedstock_props.get("sustainability_multiplier", 0.8)
        synthesis_sustainability = synthesis_props.get("sustainability", 0.7)
        overall_sustainability = (feedstock_sustainability * 0.4 + synthesis_sustainability * 0.6)

        # Cost estimation
        feedstock_cost = feedstock.cost_per_kg
        synthesis_cost_multiplier = synthesis_props.get("cost_multiplier", 1.0)
        est_cost_per_kg = (feedstock_cost * 2 + 100.0) * synthesis_cost_multiplier

        # Morphology and complexity
        if "silica" in route_name:
            morphology = "spherical"
        elif "zno" in route_name:
            morphology = "hexagonal/rod-like"
        else:
            morphology = "composite"

        return NanomaterialProfile(
            synthesis_route=synthesis_route,
            expected_particle_size_nm=(particle_size_min, particle_size_max),
            expected_morphology=morphology,
            expected_crystallinity_pct=min(100.0, crystallinity),
            expected_hydrophilicity="high"
            if hydrophilicity_score > 0.7
            else ("moderate" if hydrophilicity_score > 0.4 else "low"),
            water_adsorption_relevance=adsorption_relevance,
            synthesis_complexity=synthesis_props.get("complexity", 0.5),
            scalability_score=synthesis_props.get("scalability", 0.7),
            estimated_cost_per_kg=est_cost_per_kg,
            drying_temperature_c=drying_temp_c,
            calcination_temperature_c=calcination_temp_c,
            reaction_time_hours=reaction_time_hours,
            environmental_safety="Low toxicity expected for green routes, monitor for heavy metals",
        )

    @staticmethod
    def estimate_synthesis_complexity_score(
        feedstock_type: FeedstockType,
        synthesis_route: SynthesisRoute,
        includes_catalyst: bool = False,
        includes_calcination: bool = False,
    ) -> float:
        """Calculate synthesis complexity on 0-1 scale."""
        route_props = MaterialsDesigner.SYNTHESIS_ROUTE_PROPERTIES.get(synthesis_route, {})
        complexity = route_props.get("complexity", 0.5)

        if includes_catalyst:
            complexity += 0.15
        if includes_calcination:
            complexity += 0.10

        return min(1.0, complexity)

    @staticmethod
    def get_feedstock_options() -> Dict[FeedstockType, str]:
        """Return available feedstock types."""
        return {ft: ft.value for ft in FeedstockType}

    @staticmethod
    def get_synthesis_route_options() -> Dict[SynthesisRoute, str]:
        """Return available synthesis routes."""
        return {sr: sr.value for sr in SynthesisRoute}

    @staticmethod
    def recommend_synthesis_route(
        feedstock_type: FeedstockType,
        priority: str = "balanced",  # balanced, sustainability, cost, performance
    ) -> SynthesisRoute:
        """
        Recommend optimal synthesis route based on feedstock and priority.
        """
        feedstock_props = MaterialsDesigner.FEEDSTOCK_PROPERTIES.get(feedstock_type, {})
        silica_potential = feedstock_props.get("silica_potential", 0.5)

        if priority == "sustainability":
            if silica_potential > 0.8:
                return SynthesisRoute.GREEN_SYNTHESIS
            else:
                return SynthesisRoute.NO_CALCINATION
        elif priority == "cost":
            return SynthesisRoute.NO_CALCINATION
        elif priority == "performance":
            if silica_potential > 0.8:
                return SynthesisRoute.TEOS_SILICA
            else:
                return SynthesisRoute.ZNO_GREEN
        else:  # balanced
            if silica_potential > 0.7:
                return SynthesisRoute.GEL_SILICA
            else:
                return SynthesisRoute.ZNO_GREEN
