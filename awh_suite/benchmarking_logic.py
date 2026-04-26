"""
Benchmarking logic for comparing designs against reference systems.
"""

from data_models import BenchmarkProfile, SimulationResult
from typing import List, Dict


class BenchmarkingLab:
    """Reference system comparison and benchmarking."""

    # Reference benchmark profiles
    REFERENCE_BENCHMARKS = {
        "MOF-801": BenchmarkProfile(
            name="MOF-801",
            material_system="Zr-based metal-organic framework",
            estimated_water_yield=0.48,  # L/kg/day
            sustainability_score=0.45,  # Synthetic, not green
            cost_score=0.30,  # Expensive ($1000+/kg)
            scalability_score=0.50,
            passive_suitability=0.80,
            synthesis_complexity=0.85,
            contact_angle_category="hydrophilic (30-50°)",
            energy_demand_kwh_kg=2.5,
            biodegradability="Non-biodegradable",
            material_sourcing_risk="Medium (Zr availability)",
        ),
        "MOF-303": BenchmarkProfile(
            name="MOF-303",
            material_system="Al-based metal-organic framework",
            estimated_water_yield=0.52,
            sustainability_score=0.48,
            cost_score=0.35,
            scalability_score=0.55,
            passive_suitability=0.85,
            synthesis_complexity=0.80,
            contact_angle_category="hydrophilic (25-45°)",
            energy_demand_kwh_kg=2.2,
            biodegradability="Non-biodegradable",
            material_sourcing_risk="Low (Al abundance)",
        ),
        "Generic MOF": BenchmarkProfile(
            name="Generic MOF",
            material_system="Typical MOF system (average)",
            estimated_water_yield=0.45,
            sustainability_score=0.50,
            cost_score=0.32,
            scalability_score=0.52,
            passive_suitability=0.82,
            synthesis_complexity=0.82,
            contact_angle_category="hydrophilic (30-50°)",
            energy_demand_kwh_kg=2.4,
            biodegradability="Non-biodegradable",
            material_sourcing_risk="Medium",
        ),
        "Bio-based Chitosan/ZnO/Silica": BenchmarkProfile(
            name="Bio-based Chitosan/ZnO/Silica",
            material_system="Green synthesis, nanocomposite",
            estimated_water_yield=0.38,  # Slightly lower than MOF
            sustainability_score=0.88,  # Much better
            cost_score=0.75,  # Much cheaper
            scalability_score=0.82,  # Better scalability
            passive_suitability=0.78,
            synthesis_complexity=0.55,  # Easier to make
            contact_angle_category="moderately hydrophilic (50-70°)",
            energy_demand_kwh_kg=1.2,  # Much lower
            biodegradability="Biodegradable (chitosan backbone)",
            material_sourcing_risk="Very Low (agro-waste)",
        ),
        "Fe/Zn/Si Nanocomposite": BenchmarkProfile(
            name="Fe/Zn/Si Nanocomposite",
            material_system="Multi-element oxide nanocomposite",
            estimated_water_yield=0.42,
            sustainability_score=0.82,
            cost_score=0.65,
            scalability_score=0.75,
            passive_suitability=0.75,
            synthesis_complexity=0.68,
            contact_angle_category="moderate (55-75°)",
            energy_demand_kwh_kg=1.4,
            biodegradability="Partially degradable",
            material_sourcing_risk="Low (Fe, Zn, Si abundant)",
        ),
        "Activated Carbon": BenchmarkProfile(
            name="Activated Carbon",
            material_system="Porous carbon from biomass",
            estimated_water_yield=0.35,
            sustainability_score=0.85,
            cost_score=0.85,
            scalability_score=0.90,
            passive_suitability=0.70,
            synthesis_complexity=0.40,
            contact_angle_category="moderate to slightly hydrophobic (70-85°)",
            energy_demand_kwh_kg=1.0,
            biodegradability="Biodegradable",
            material_sourcing_risk="Very Low",
        ),
    }

    @staticmethod
    def get_benchmark_profiles() -> Dict[str, BenchmarkProfile]:
        """Return available benchmark profiles."""
        return BenchmarkingLab.REFERENCE_BENCHMARKS

    @staticmethod
    def get_benchmark_names() -> List[str]:
        """Return list of benchmark names."""
        return list(BenchmarkingLab.REFERENCE_BENCHMARKS.keys())

    @staticmethod
    def compare_with_benchmarks(
        user_simulation: SimulationResult,
        selected_benchmarks: List[str],
    ) -> Dict[str, Dict]:
        """
        Compare user's design simulation results with selected benchmarks.
        Returns comparison metrics.
        """
        comparison = {}

        # User design performance
        comparison["User Design"] = {
            "estimated_water_yield": user_simulation.predicted_water_yield_l_kg_day,
            "adsorption_score": user_simulation.adsorption_score,
            "desorption_efficiency": user_simulation.desorption_efficiency,
            "condensation_likelihood": user_simulation.condensation_likelihood,
            "relative_performance": user_simulation.relative_performance_score,
        }

        # Selected benchmarks
        for bench_name in selected_benchmarks:
            if bench_name in BenchmarkingLab.REFERENCE_BENCHMARKS:
                profile = BenchmarkingLab.REFERENCE_BENCHMARKS[bench_name]
                comparison[bench_name] = {
                    "estimated_water_yield": profile.estimated_water_yield,
                    "sustainability_score": profile.sustainability_score,
                    "cost_score": profile.cost_score,
                    "scalability_score": profile.scalability_score,
                    "synthesis_complexity": profile.synthesis_complexity,
                    "passive_suitability": profile.passive_suitability,
                }

        return comparison

    @staticmethod
    def rank_benchmarks(
        user_result: SimulationResult,
        metric: str = "estimated_water_yield",
    ) -> List[tuple]:
        """
        Rank all available benchmarks by specified metric.
        Returns list of (name, value) tuples sorted descending.
        """
        rankings = []

        for name, profile in BenchmarkingLab.REFERENCE_BENCHMARKS.items():
            if metric == "estimated_water_yield":
                value = profile.estimated_water_yield
            elif metric == "sustainability_score":
                value = profile.sustainability_score
            elif metric == "cost_score":
                value = profile.cost_score
            elif metric == "scalability_score":
                value = profile.scalability_score
            elif metric == "passive_suitability":
                value = profile.passive_suitability
            else:
                value = 0.0

            rankings.append((name, value))

        # Add user design
        if metric == "estimated_water_yield":
            user_value = user_result.predicted_water_yield_l_kg_day
        elif metric == "relative_performance":
            user_value = user_result.relative_performance_score
        else:
            user_value = 0.0

        rankings.append(("Your Design", user_value))

        # Sort descending
        rankings.sort(key=lambda x: x[1], reverse=True)

        return rankings

    @staticmethod
    def get_benchmark_radar_data(
        profile: BenchmarkProfile,
    ) -> Dict:
        """Extract radar chart data from benchmark profile."""
        return {
            "Sustainability": profile.sustainability_score,
            "Cost Efficiency": profile.cost_score,
            "Scalability": profile.scalability_score,
            "Passive Suitability": profile.passive_suitability,
            "Synthesis Complexity": 1.0 - profile.synthesis_complexity,  # Invert for radar
        }

    @staticmethod
    def get_benchmark_details(name: str) -> BenchmarkProfile:
        """Retrieve full details of a benchmark."""
        return BenchmarkingLab.REFERENCE_BENCHMARKS.get(
            name, BenchmarkingLab.REFERENCE_BENCHMARKS["Generic MOF"]
        )
