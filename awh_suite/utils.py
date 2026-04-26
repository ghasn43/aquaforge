"""
Utility functions and helpers for AWH Suite.
"""

from data_models import (
    ProjectState, FeedstockProfile, NanomaterialProfile, MembraneFormulation,
    DeviceConfiguration, AtmosphericConditions, CostModel, SimulationResult,
    FeedstockType, SynthesisRoute, PolymerMatrix, LayerConfiguration, DeviceClass, ThermalMode
)
from typing import Tuple
import json
from datetime import datetime


def create_default_project() -> ProjectState:
    """Create a default project with reasonable starting values."""
    project = ProjectState(
        project_name="AWH Design - New Project",
        project_id=datetime.now().strftime("%Y%m%d_%H%M%S"),
        created_date=datetime.now().isoformat(),
        last_modified=datetime.now().isoformat(),
        feedstock=FeedstockProfile(
            feedstock_type=FeedstockType.PEANUT_SHELL,
            cost_per_kg=2.5,
        ),
        nanomaterial=NanomaterialProfile(
            synthesis_route=SynthesisRoute.GREEN_SYNTHESIS,
        ),
        membrane=MembraneFormulation(
            name="Default Formulation",
            polymer_matrix=PolymerMatrix.CHITOSAN,
            nanoparticle_type="Green Silica",
            nanoparticle_loading_wt_pct=10.0,
        ),
        device=DeviceConfiguration(
            name="Standard Collector",
            device_class=DeviceClass.BENCH_PROTOTYPE,
            overall_diameter_cm=30.0,
            total_height_cm=60.0,
        ),
        conditions=AtmosphericConditions(
            relative_humidity_pct=60.0,
            ambient_temperature_c=25.0,
        ),
        costing=CostModel(
            scale_level="Lab",
        ),
    )
    return project


def get_preset_projects() -> dict:
    """Return predefined preset projects."""
    presets = {}

    # Preset 1: Chitosan + Green Silica + ZnO
    preset1 = create_default_project()
    preset1.project_name = "Preset: Chitosan/Green Silica/ZnO System"
    preset1.feedstock = FeedstockProfile(
        feedstock_type=FeedstockType.PEANUT_SHELL,
        cost_per_kg=2.5,
        sustainability_score=0.85,
    )
    preset1.nanomaterial = NanomaterialProfile(
        synthesis_route=SynthesisRoute.GREEN_SYNTHESIS,
        expected_particle_size_nm=(30, 80),
        expected_hydrophilicity="high",
        water_adsorption_relevance=0.85,
    )
    preset1.membrane = MembraneFormulation(
        name="Chitosan/Silica/ZnO Blend",
        polymer_matrix=PolymerMatrix.SILICA_CHITOSAN,
        nanoparticle_type="Green Silica + ZnO Mix",
        nanoparticle_loading_wt_pct=12.0,
        layer_config=LayerConfiguration.SINGLE,
        thickness_um=150.0,
        porosity_pct=40.0,
    )
    presets["Chitosan/Silica/ZnO"] = preset1

    # Preset 2: Fe/Zn/Si Nanocomposite
    preset2 = create_default_project()
    preset2.project_name = "Preset: Fe/Zn/Si Nanocomposite"
    preset2.feedstock = FeedstockProfile(
        feedstock_type=FeedstockType.RICE_HUSK,
        cost_per_kg=1.2,
        sustainability_score=0.90,
    )
    preset2.nanomaterial = NanomaterialProfile(
        synthesis_route=SynthesisRoute.FE_ZN_SI,
        expected_particle_size_nm=(40, 120),
        expected_morphology="composite oxide",
        water_adsorption_relevance=0.80,
    )
    preset2.membrane = MembraneFormulation(
        name="Chitosan/Fe-Zn-Si Composite",
        polymer_matrix=PolymerMatrix.FE_ZN_SI_CHITOSAN,
        nanoparticle_type="Fe/Zn/Si Nanocomposite",
        nanoparticle_loading_wt_pct=15.0,
        layer_config=LayerConfiguration.DUAL_HYDRO_PHOBIC,
    )
    presets["Fe/Zn/Si Composite"] = preset2

    # Preset 3: Dual-layer hydrophilic/hydrophobic
    preset3 = create_default_project()
    preset3.project_name = "Preset: Dual-Layer Hydro Design"
    preset3.membrane = MembraneFormulation(
        name="Hydrophilic Top/Hydrophobic Bottom",
        polymer_matrix=PolymerMatrix.MODIFIED_CHITOSAN,
        nanoparticle_type="Green Silica",
        nanoparticle_loading_wt_pct=8.0,
        layer_config=LayerConfiguration.DUAL_HYDRO_PHILIC,
        thickness_um=120.0,
        porosity_pct=45.0,
        crosslink_density="Medium",
    )
    preset3.device = DeviceConfiguration(
        name="Dual-Layer Optimized Collector",
        device_class=DeviceClass.BENCH_PROTOTYPE,
        overall_diameter_cm=25.0,
        total_height_cm=50.0,
        cone_angle_deg=60.0,
        filtration_stage=True,
    )
    presets["Dual-Layer Design"] = preset3

    # Preset 4: Passive Cylindrical Collector
    preset4 = create_default_project()
    preset4.project_name = "Preset: Passive Cylindrical Collector"
    preset4.device = DeviceConfiguration(
        name="Passive Cylindrical AWH Prototype",
        device_class=DeviceClass.BENCH_PROTOTYPE,
        overall_diameter_cm=35.0,
        total_height_cm=70.0,
        upper_chamber_height_cm=25.0,
        lower_chamber_height_cm=30.0,
        cone_angle_deg=60.0,
        funnel_throat_diameter_cm=10.0,
        structural_material="Polycarbonate + Aluminum",
        chamber_transparency="Polycarbonate (translucent)",
        reservoir_capacity_ml=800.0,
        support_columns_count=4,
        passive_assisted="Passive",
        thermal_mode=ThermalMode.PASSIVE,
        filtration_stage=False,
    )
    preset4.conditions = AtmosphericConditions(
        relative_humidity_pct=65.0,
        ambient_temperature_c=25.0,
        day_night_mode="24h",
        airflow_level="Natural",
    )
    presets["Passive Collector"] = preset4

    # Preset 5: Solar-Assisted System
    preset5 = create_default_project()
    preset5.project_name = "Preset: Solar-Assisted AWH System"
    preset5.device = DeviceConfiguration(
        name="Solar-Assisted Collector",
        device_class=DeviceClass.PILOT_PROTOTYPE,
        overall_diameter_cm=40.0,
        total_height_cm=80.0,
        thermal_mode=ThermalMode.SOLAR_ASSISTED,
        filtration_stage=True,
    )
    preset5.conditions = AtmosphericConditions(
        relative_humidity_pct=55.0,
        ambient_temperature_c=28.0,
        solar_exposure="High",
    )
    presets["Solar-Assisted"] = preset5

    return presets


def estimate_trl_level(
    membrane_quality: float,
    device_class: str,
    cost_validated: bool = False,
) -> Tuple[int, str]:
    """
    Estimate Technology Readiness Level (TRL).
    Returns (TRL_number, TRL_description)
    """
    if device_class == "Bench Prototype":
        base_trl = 3
    elif device_class == "Pilot Prototype":
        base_trl = 5
    else:
        base_trl = 6

    if membrane_quality < 0.5:
        base_trl = max(2, base_trl - 2)
    elif membrane_quality < 0.7:
        base_trl = max(3, base_trl - 1)

    if cost_validated:
        base_trl = min(7, base_trl + 1)

    descriptions = {
        1: "TRL 1: Basic research",
        2: "TRL 2: Concept formulation",
        3: "TRL 3: Proof-of-concept",
        4: "TRL 4: Technology validation",
        5: "TRL 5: Pilot demonstration",
        6: "TRL 6: Technology demonstration",
        7: "TRL 7: System prototype demonstration",
        8: "TRL 8: System complete and qualified",
        9: "TRL 9: Actual system proven in operational environment",
    }

    return base_trl, descriptions.get(base_trl, "Unknown TRL")


def calculate_sustainability_badge(
    feedstock_sustainability: float,
    membrane_sustainability: float,
    device_manufacturability: float,
) -> Tuple[str, str]:
    """
    Calculate overall sustainability score and badge.
    Returns (badge_emoji, description)
    """
    overall_score = (
        feedstock_sustainability * 0.3
        + membrane_sustainability * 0.5
        + device_manufacturability * 0.2
    )

    if overall_score > 0.85:
        return "🌿 Excellent", "Highly sustainable, minimal environmental footprint"
    elif overall_score > 0.70:
        return "💚 Good", "Good sustainability profile"
    elif overall_score > 0.55:
        return "⚠️ Moderate", "Adequate sustainability, room for improvement"
    else:
        return "⛔ Low", "Low sustainability score - consider design revision"


def recommend_next_experiment(
    simulation: SimulationResult,
    membrane_manufacturability: float,
) -> str:
    """Generate recommendation for next R&D experiment."""
    if simulation.adsorption_score < 0.6:
        return "🔬 **Next Experiment**: Enhance membrane hydrophilicity. Try increased nanoparticle loading or dual-layer design."

    if simulation.desorption_efficiency < 0.5:
        return "🔥 **Next Experiment**: Improve desorption. Test lower crosslink density or thermal assist mode."

    if membrane_manufacturability < 0.5:
        return "⚙️ **Next Experiment**: Simplify formulation. Reduce nanoparticle loading or use single-layer design."

    if simulation.collection_efficiency_pct < 80:
        return "💧 **Next Experiment**: Optimize collection geometry. Consider different cone angle or funnel design."

    return "✅ **Next Experiment**: Design appears well-balanced. Recommend bench-scale validation experiments."


def format_performance_metric(value: float, metric_type: str) -> str:
    """Format performance metrics for display."""
    if metric_type == "percentage":
        return f"{value:.1f}%"
    elif metric_type == "yield":
        return f"{value:.3f} L/kg/day"
    elif metric_type == "score":
        return f"{value:.2f}/1.0"
    elif metric_type == "temperature":
        return f"{value:.1f}°C"
    elif metric_type == "rh":
        return f"{value:.1f}%"
    elif metric_type == "cost":
        return f"${value:.2f}"
    else:
        return f"{value:.2f}"


def validate_project_state(project: ProjectState) -> list:
    """Check for potential issues in project configuration."""
    issues = []

    if project.membrane.estimated_adsorption_strength > 0.85 and project.membrane.desorption_ease < 0.4:
        issues.append("⚠️ Strong adsorption with difficult release - may require excessive heating")

    if project.device.overall_diameter_cm < 15:
        issues.append("⚠️ Small device diameter - may have limited collection area")

    if project.conditions.relative_humidity_pct < 30:
        issues.append("⚠️ Low humidity conditions - water yield will be minimal")

    if project.costing.cost_per_liter_harvested > 50:
        issues.append("⚠️ High cost per liter - may not be economically competitive")

    return issues


def save_project_to_json(project: ProjectState, filename: str = None) -> str:
    """Serialize project to JSON string."""
    if filename is None:
        filename = f"awh_project_{project.project_id}.json"

    return project.to_json()


def load_project_from_json(json_str: str) -> ProjectState:
    """Deserialize project from JSON string."""
    return ProjectState.from_json(json_str)
