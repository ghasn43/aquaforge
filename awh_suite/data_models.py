"""
Data models for Atmospheric Water Harvesting Suite.
Structured domain classes with validation and defaults.
"""

from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional, Tuple
from enum import Enum
import json
from datetime import datetime


class FeedstockType(Enum):
    """Biomass feedstock options."""
    PEANUT_SHELL = "Peanut Shell"
    BANANA_PEEL = "Banana Peel"
    PHOENIX_DATE = "Phoenix Dactylifera"
    ALGAE = "Algae"
    FUNGAL_BIOMASS = "Fungal Biomass"
    RICE_HUSK = "Rice Husk"
    COCONUT_SHELL = "Coconut Shell"
    OTHER = "Other Agro-waste"


class SynthesisRoute(Enum):
    """Nanomaterial synthesis pathways."""
    GREEN_SYNTHESIS = "Green Synthesis"
    CALCINATION = "Calcination"
    NO_CALCINATION = "No Calcination"
    TEOS_SILICA = "TEOS-based Silica Route"
    GEL_SILICA = "Gel-based Silica Route"
    ZNO_GREEN = "ZnO Green Route"
    FE_ZN_SI = "Fe/Zn/Si Nanocomposite Route"


class PolymerMatrix(Enum):
    """Polymer matrix options for membranes."""
    CHITOSAN = "Pure Chitosan"
    MODIFIED_CHITOSAN = "Modified Chitosan"
    SILICA_CHITOSAN = "Silica-Enhanced Chitosan"
    ZNO_CHITOSAN = "ZnO/Chitosan"
    FE_ZN_SI_CHITOSAN = "Fe/Zn/Si/Chitosan"
    BIOPOLYMER_BLEND = "Custom Biopolymer Blend"


class LayerConfiguration(Enum):
    """Membrane layer structure."""
    SINGLE = "Single Layer"
    DUAL_HYDRO_PHOBIC = "Dual-Layer (Hydrophobic Top)"
    DUAL_HYDRO_PHILIC = "Dual-Layer (Hydrophilic Top)"
    TRIPLE = "Triple Layer"


class DeviceClass(Enum):
    """Device prototype classification."""
    BENCH_PROTOTYPE = "Bench Prototype"
    PILOT_PROTOTYPE = "Pilot Prototype"
    FIELD_DEMONSTRATOR = "Field Demonstrator"


class ThermalMode(Enum):
    """Thermal support for desorption."""
    PASSIVE = "Passive (No Heat)"
    LOW_HEAT = "Low Heat Assist"
    SOLAR_ASSISTED = "Solar Assisted"
    LAB_ASSISTED = "Lab Assisted"


@dataclass
class FeedstockProfile:
    """Biomass feedstock specification."""
    feedstock_type: FeedstockType
    pretreatment_chemistry: str = "Water washing"
    ph: float = 7.0
    cost_per_kg: float = 2.5
    sustainability_score: float = 0.8  # 0-1 scale
    availability: str = "High"
    notes: str = ""

    def to_dict(self):
        return asdict(self)


@dataclass
class NanomaterialProfile:
    """Predicted nanomaterial properties from synthesis route."""
    synthesis_route: SynthesisRoute
    expected_particle_size_nm: Tuple[float, float] = (50.0, 150.0)  # min, max
    expected_morphology: str = "spherical"
    expected_crystallinity_pct: float = 75.0
    expected_hydrophilicity: str = "moderate"  # low, moderate, high
    water_adsorption_relevance: float = 0.75  # 0-1 score
    synthesis_complexity: float = 0.5  # 0-1 (0=simple, 1=complex)
    scalability_score: float = 0.7  # 0-1
    estimated_cost_per_kg: float = 150.0
    environmental_safety: str = "Low toxicity expected"
    catalyst: str = "None"
    reaction_time_hours: float = 4.0
    drying_temperature_c: float = 100.0
    calcination_temperature_c: float = 300.0
    solvent_system: str = "Water-based"
    notes: str = ""

    def to_dict(self):
        return asdict(self)


@dataclass
class MembraneFormulation:
    """Membrane/film design specification."""
    name: str = "Design 1"
    polymer_matrix: PolymerMatrix = PolymerMatrix.CHITOSAN
    nanoparticle_type: str = "Green Silica"
    nanoparticle_loading_wt_pct: float = 10.0
    particle_size_nm: float = 50.0
    particle_dispersion_quality: str = "Good"  # Poor, Fair, Good, Excellent
    layer_config: LayerConfiguration = LayerConfiguration.SINGLE
    thickness_um: float = 100.0
    porosity_pct: float = 35.0
    crosslinker: str = "Glutaraldehyde"
    crosslink_density: str = "Medium"  # Low, Medium, High
    drying_method: str = "Air dry at 60°C"
    film_casting_method: str = "Solution casting"
    
    # Computed properties
    estimated_contact_angle_deg: float = 0.0
    estimated_adsorption_strength: float = 0.0
    desorption_ease: float = 0.0
    mechanical_stability: float = 0.0
    moisture_capture_score: float = 0.0
    thermal_robustness: float = 0.0
    manufacturability_score: float = 0.0
    sustainability_score: float = 0.0

    def to_dict(self):
        d = asdict(self)
        d['polymer_matrix'] = self.polymer_matrix.value
        d['layer_config'] = self.layer_config.value
        return d


@dataclass
class DeviceConfiguration:
    """Atmospheric water harvester device architecture."""
    name: str = "Collector 1"
    device_class: DeviceClass = DeviceClass.BENCH_PROTOTYPE
    overall_diameter_cm: float = 30.0
    total_height_cm: float = 60.0
    upper_chamber_height_cm: float = 20.0
    lower_chamber_height_cm: float = 25.0
    cone_angle_deg: float = 60.0
    funnel_throat_diameter_cm: float = 8.0
    structural_material: str = "Polycarbonate + Aluminum Frame"
    chamber_transparency: str = "Polycarbonate (translucent)"
    reservoir_capacity_ml: float = 500.0
    support_columns_count: int = 3
    passive_assisted: str = "Passive"  # Passive, Assisted
    thermal_mode: ThermalMode = ThermalMode.PASSIVE
    filtration_stage: bool = True
    
    # Computed properties
    upper_chamber_volume_l: float = 0.0
    lower_chamber_volume_l: float = 0.0
    cone_volume_l: float = 0.0
    estimated_manufacturability: float = 0.0
    maintenance_complexity: float = 0.0
    prototype_complexity: float = 0.0

    def to_dict(self):
        d = asdict(self)
        d['device_class'] = self.device_class.value
        d['thermal_mode'] = self.thermal_mode.value
        return d


@dataclass
class AtmosphericConditions:
    """Environmental operating conditions."""
    relative_humidity_pct: float = 60.0
    ambient_temperature_c: float = 25.0
    day_night_mode: str = "Day"  # Day, Night, 24h
    airflow_level: str = "Natural"  # Low, Natural, Medium, High
    solar_exposure: str = "Moderate"  # None, Low, Moderate, High
    passive_heating_c: float = 0.0
    condensation_support: bool = False
    cycle_duration_hours: float = 8.0
    operation_mode: str = "Balanced"  # adsorption-focused, Balanced, high-release


@dataclass
class SimulationResult:
    """Results from performance simulation."""
    adsorption_score: float = 0.0  # 0-1
    desorption_efficiency: float = 0.0  # 0-1
    condensation_likelihood: float = 0.0  # 0-1
    predicted_water_yield_ml_g: float = 0.0
    predicted_water_yield_l_kg_day: float = 0.0
    collection_efficiency_pct: float = 0.0
    filtration_efficiency_pct: float = 0.0
    relative_performance_score: float = 0.0  # 0-1
    confidence_level: str = "Medium"  # Low, Medium, High
    performance_window: str = "Moderate"
    stage_contributions: Dict[str, float] = field(default_factory=dict)
    notes: str = "Design-stage heuristic estimate for R&D guidance only."


@dataclass
class BenchmarkProfile:
    """Reference system for comparison."""
    name: str
    material_system: str
    estimated_water_yield: float
    sustainability_score: float
    cost_score: float
    scalability_score: float
    passive_suitability: float
    synthesis_complexity: float
    contact_angle_category: str
    energy_demand_kwh_kg: float
    biodegradability: str
    material_sourcing_risk: str


@dataclass
class CostModel:
    """Economic and scale-up analysis."""
    feedstock_cost_per_kg: float = 2.5
    polymer_cost_per_kg: float = 45.0
    nanoparticle_prep_cost_per_kg: float = 150.0
    device_fabrication_cost_base: float = 200.0
    batch_size_units: int = 10
    membrane_area_cm2: float = 500.0
    prototype_count: int = 1
    labor_multiplier: float = 1.0
    testing_multiplier: float = 1.5
    scale_level: str = "Lab"  # Lab, Pilot, Pre-commercial
    
    # Computed outputs
    cost_per_membrane: float = 0.0
    prototype_cost_total: float = 0.0
    cost_per_liter_harvested: float = 0.0
    scale_up_burden: float = 0.0
    capex_estimate: float = 0.0
    opex_estimate: float = 0.0
    sustainability_adjusted_cost: float = 0.0


@dataclass
class ProjectState:
    """Complete project state for save/load."""
    project_name: str = "AWH Project"
    project_id: str = ""
    created_date: str = ""
    last_modified: str = ""
    feedstock: FeedstockProfile = field(default_factory=lambda: FeedstockProfile(FeedstockType.PEANUT_SHELL))
    nanomaterial: NanomaterialProfile = field(default_factory=lambda: NanomaterialProfile(SynthesisRoute.GREEN_SYNTHESIS))
    membrane: MembraneFormulation = field(default_factory=MembraneFormulation)
    device: DeviceConfiguration = field(default_factory=DeviceConfiguration)
    conditions: AtmosphericConditions = field(default_factory=AtmosphericConditions)
    simulation: SimulationResult = field(default_factory=SimulationResult)
    costing: CostModel = field(default_factory=CostModel)
    notes: str = ""

    def to_dict(self):
        return asdict(self)

    def to_json(self) -> str:
        """Serialize to JSON string."""
        data = self.to_dict()
        # Convert enums to strings
        data['feedstock']['feedstock_type'] = data['feedstock']['feedstock_type'].value
        data['nanomaterial']['synthesis_route'] = data['nanomaterial']['synthesis_route'].value
        data['membrane']['polymer_matrix'] = data['membrane']['polymer_matrix'].value
        data['membrane']['layer_config'] = data['membrane']['layer_config'].value
        data['device']['device_class'] = data['device']['device_class'].value
        data['device']['thermal_mode'] = data['device']['thermal_mode'].value
        return json.dumps(data, indent=2)

    @classmethod
    def from_json(cls, json_str: str):
        """Deserialize from JSON string."""
        data = json.loads(json_str)
        # Convert strings back to enums - simplified for now
        return cls(**data)
