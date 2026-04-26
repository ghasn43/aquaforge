"""
Recommendation Engine for AquaForge
Provides next-best-experiment suggestions, design bottleneck analysis, and optimization pathways
"""

from dataclasses import dataclass
from typing import List, Dict, Tuple
from enum import Enum


class BottleneckType(Enum):
    """Types of design bottlenecks"""
    ADSORPTION = "Adsorption capacity too low"
    DESORPTION = "Desorption efficiency too low"
    CONDENSATION = "Condensation likelihood too low"
    COLLECTION = "Collection efficiency too low"
    COST = "Cost per liter too high"
    MANUFACTURABILITY = "Manufacturability too complex"
    SUSTAINABILITY = "Sustainability score too low"
    TRL_MATURITY = "Technology readiness level too low"


@dataclass
class Bottleneck:
    """Identified design bottleneck"""
    bottleneck_type: BottleneckType
    current_score: float  # 0-1 or unit-specific
    target_score: float
    impact_on_yield_pct: float  # -10 to -50 (how much yield is lost)
    difficulty_to_fix: float  # 0-1 (1 = very hard)
    estimated_time_to_fix_days: int


@dataclass
class NextExperiment:
    """Recommended next experiment to test/validate a design"""
    experiment_name: str
    objective: str  # What question does this answer?
    hypothesis: str  # What do we expect to find?
    procedure: str  # How to run the experiment
    expected_duration_hours: float
    required_equipment: List[str]
    success_criteria: List[str]
    confidence_gain_expected: float  # 0-1 (how much does this improve confidence?)
    cost_estimate_usd: float
    risk_level: str  # "low", "medium", "high"
    scientific_rationale: str


@dataclass
class DesignRecommendation:
    """Actionable design recommendation"""
    recommendation_text: str
    parameter_to_change: str
    suggested_value: float
    expected_impact_on_yield_pct: float
    expected_impact_on_cost_pct: float
    expected_impact_on_sustainability: float
    confidence: float  # 0-1
    scientific_basis: str


class RecommendationEngine:
    """
    Provides intelligent recommendations for design improvements and next experiments.
    """
    
    @staticmethod
    def identify_bottlenecks(
        adsorption_score: float,
        desorption_efficiency: float,
        condensation_likelihood: float,
        collection_efficiency: float,
        cost_per_liter_usd: float,
        manufacturability: float,
        sustainability: float,
        trl_level: int,
        target_yield_l_kg_day: float = 0.4,
    ) -> List[Bottleneck]:
        """
        Identify which metrics are limiting design performance.
        
        Returns:
            List of Bottleneck objects, ranked by impact
        """
        bottlenecks = []
        
        # Adsorption bottleneck
        if adsorption_score < 0.7:
            bottlenecks.append(Bottleneck(
                bottleneck_type=BottleneckType.ADSORPTION,
                current_score=adsorption_score,
                target_score=0.8,
                impact_on_yield_pct=-20 * (1 - adsorption_score),
                difficulty_to_fix=0.6,
                estimated_time_to_fix_days=21,
            ))
        
        # Desorption bottleneck
        if desorption_efficiency < 0.6:
            bottlenecks.append(Bottleneck(
                bottleneck_type=BottleneckType.DESORPTION,
                current_score=desorption_efficiency,
                target_score=0.75,
                impact_on_yield_pct=-15 * (1 - desorption_efficiency),
                difficulty_to_fix=0.7,
                estimated_time_to_fix_days=28,
            ))
        
        # Condensation bottleneck
        if condensation_likelihood < 0.5:
            bottlenecks.append(Bottleneck(
                bottleneck_type=BottleneckType.CONDENSATION,
                current_score=condensation_likelihood,
                target_score=0.7,
                impact_on_yield_pct=-15 * (1 - condensation_likelihood),
                difficulty_to_fix=0.8,
                estimated_time_to_fix_days=35,
            ))
        
        # Collection bottleneck
        if collection_efficiency < 0.85:
            bottlenecks.append(Bottleneck(
                bottleneck_type=BottleneckType.COLLECTION,
                current_score=collection_efficiency,
                target_score=0.95,
                impact_on_yield_pct=-10 * (1 - collection_efficiency),
                difficulty_to_fix=0.4,
                estimated_time_to_fix_days=7,
            ))
        
        # Cost bottleneck
        if cost_per_liter_usd > 3.0:
            bottlenecks.append(Bottleneck(
                bottleneck_type=BottleneckType.COST,
                current_score=1.0 / (1 + cost_per_liter_usd / 2),  # Inverse score
                target_score=1.0 / (1 + 2.0 / 2),
                impact_on_yield_pct=0,  # Direct cost concern, not yield
                difficulty_to_fix=0.5,
                estimated_time_to_fix_days=14,
            ))
        
        # Manufacturability bottleneck
        if manufacturability > 0.7:  # Higher = more difficult
            bottlenecks.append(Bottleneck(
                bottleneck_type=BottleneckType.MANUFACTURABILITY,
                current_score=1 - manufacturability,  # Invert
                target_score=0.8,
                impact_on_yield_pct=0,  # Doesn't affect yield directly
                difficulty_to_fix=0.6,
                estimated_time_to_fix_days=21,
            ))
        
        # Sustainability bottleneck
        if sustainability < 0.7:
            bottlenecks.append(Bottleneck(
                bottleneck_type=BottleneckType.SUSTAINABILITY,
                current_score=sustainability,
                target_score=0.85,
                impact_on_yield_pct=0,
                difficulty_to_fix=0.4,
                estimated_time_to_fix_days=14,
            ))
        
        # TRL bottleneck
        if trl_level < 4:
            bottlenecks.append(Bottleneck(
                bottleneck_type=BottleneckType.TRL_MATURITY,
                current_score=trl_level / 9,
                target_score=0.6,  # TRL 5-6
                impact_on_yield_pct=0,
                difficulty_to_fix=0.8,
                estimated_time_to_fix_days=60,
            ))
        
        # Sort by impact (descending)
        bottlenecks.sort(key=lambda b: b.impact_on_yield_pct, reverse=True)
        return bottlenecks
    
    @staticmethod
    def recommend_next_experiments(
        primary_bottleneck: Bottleneck,
        secondary_bottlenecks: List[Bottleneck],
        current_trl: int,
    ) -> List[NextExperiment]:
        """
        Recommend experiments to address identified bottlenecks.
        
        Args:
            primary_bottleneck: Most critical bottleneck
            secondary_bottlenecks: Secondary issues
            current_trl: Current technology readiness level
        
        Returns:
            List of recommended experiments, prioritized
        """
        experiments = []
        
        # Primary bottleneck experiment
        if primary_bottleneck.bottleneck_type == BottleneckType.ADSORPTION:
            experiments.append(NextExperiment(
                experiment_name="Water Sorption Isotherm Test",
                objective="Measure membrane adsorption capacity across RH range",
                hypothesis="Membrane will show adsorption capacity >0.5 g_water/g_membrane at 80% RH",
                procedure="""
                1. Prepare membrane sample (~100 mg)
                2. Condition at 50% RH, 25°C for 24h baseline
                3. Expose to serial RH: 30%, 50%, 70%, 90% at 25°C
                4. Measure mass at each point (record equilibrium time)
                5. Calculate mass uptake = (final_mass - baseline_mass) / baseline_mass
                6. Plot adsorption isotherm (RH vs. uptake)
                """,
                expected_duration_hours=40,
                required_equipment=[
                    "Dynamic Vapor Sorption (DVS) analyzer (or manual chamber)",
                    "Precision balance (±0.1 mg)",
                    "Humidity-controlled chamber",
                    "Temperature controller",
                ],
                success_criteria=[
                    "Clear S-shaped isotherm curve",
                    "Adsorption capacity >0.4 g/g at 80% RH",
                    "Reversible desorption (±5% hysteresis)",
                ],
                confidence_gain_expected=0.4,
                cost_estimate_usd=800,
                risk_level="low",
                scientific_rationale="DVS is gold-standard for AWH adsorbent testing. Provides kinetic + equilibrium data."
            ))
        
        elif primary_bottleneck.bottleneck_type == BottleneckType.DESORPTION:
            experiments.append(NextExperiment(
                experiment_name="Thermal Desorption Profile",
                objective="Measure water release rate and efficiency vs. heating method",
                hypothesis="Solar heating (55-60°C) will release >70% of adsorbed water in <2 hours",
                procedure="""
                1. Pre-saturate membrane at 80% RH to max adsorption
                2. Apply heating: Passive (convection) vs. Solar (simulated, 1000 W/m²) vs. Electric (60°C bath)
                3. Monitor water loss via: mass change, thermal camera (Tsurf), humidity (outlet air)
                4. Record: Time to 50% release, Time to 90% release, Final residual moisture
                5. Calculate desorption efficiency % and recovery time
                """,
                expected_duration_hours=30,
                required_equipment=[
                    "Programmable heating stage or solar simulator",
                    "Precision balance with live feed",
                    "IR thermal camera",
                    "Humidity/temperature sensors (inlet, outlet air)",
                    "Flow meter",
                ],
                success_criteria=[
                    "Desorption efficiency ≥70% within 2 hours",
                    "Energy cost <0.5 kWh per kg water",
                    "Repeatable over 5 cycles (no degradation)",
                ],
                confidence_gain_expected=0.35,
                cost_estimate_usd=2000,
                risk_level="medium",
                scientific_rationale="Desorption is 2nd bottleneck in AWH. Solar heating most realistic for field deployment."
            ))
        
        elif primary_bottleneck.bottleneck_type == BottleneckType.COST:
            experiments.append(NextExperiment(
                experiment_name="Scale-Up Feasibility & Cost Reduction",
                objective="Validate cost reduction pathway from lab to pilot scale",
                hypothesis="Doubling batch size will reduce cost per unit by 35-45%",
                procedure="""
                1. Synthesize current formulation at 2× batch size (lab optimization)
                2. Prepare 10 membrane samples (instead of 5) in single batch
                3. Track: material waste %, labor time, energy consumption, QC time
                4. Calculate cost per unit for 1× vs. 2× batch
                5. Identify non-scaling costs (overhead, equipment amortization)
                6. Project cost at pilot scale (100× batch)
                """,
                expected_duration_hours=60,
                required_equipment=[
                    "Current synthesis equipment",
                    "Time tracking tools",
                    "Energy meter",
                    "Material scales",
                ],
                success_criteria=[
                    "Cost per membrane reduced by >25%",
                    "Quality metrics maintained (characterization identical)",
                    "Clear cost model for further scale-up",
                ],
                confidence_gain_expected=0.3,
                cost_estimate_usd=500,
                risk_level="low",
                scientific_rationale="Cost scaling is critical for commercial viability. Direct experimental validation vs. projection."
            ))
        
        else:  # Generic fallback
            experiments.append(NextExperiment(
                experiment_name="Controlled Parametric Study",
                objective=f"Address: {primary_bottleneck.bottleneck_type.value}",
                hypothesis="Systematic variation will identify optimization path",
                procedure="Design factorial experiment; vary key parameters; measure response",
                expected_duration_hours=50,
                required_equipment=["Standard lab equipment"],
                success_criteria=["Clear performance trend identified", "Optimized parameter set found"],
                confidence_gain_expected=0.25,
                cost_estimate_usd=1000,
                risk_level="medium",
                scientific_rationale="Systematic approach reduces guesswork; provides design guidance."
            ))
        
        # Add secondary experiments if resources permit
        if len(secondary_bottlenecks) > 0 and current_trl >= 4:
            sb = secondary_bottlenecks[0]
            if sb.bottleneck_type == BottleneckType.SUSTAINABILITY:
                experiments.append(NextExperiment(
                    experiment_name="Life Cycle Assessment (LCA) Validation",
                    objective="Quantify sustainability claims",
                    hypothesis="Green synthesis pathway shows 30% lower carbon footprint vs. MOF",
                    procedure="""
                    1. Collect data: feedstock sourcing, synthesis energy, transport, end-of-life
                    2. Use standardized LCA methodology (ISO 14040/44)
                    3. Calculate: GWP, water use, toxicity scores
                    4. Compare vs. MOF-801 published data
                    """,
                    expected_duration_hours=80,
                    required_equipment=["LCA software (openLCA, SimaPro)", "Literature databases"],
                    success_criteria=["Published LCA results", "Verified sustainability claims"],
                    confidence_gain_expected=0.3,
                    cost_estimate_usd=3000,
                    risk_level="medium",
                    scientific_rationale="Sustainability validation critical for investor & grant narratives."
                ))
        
        return experiments
    
    @staticmethod
    def recommend_design_improvements(
        adsorption_score: float,
        nanoparticle_loading_pct: float,
        polymer_type: str,
        cost_per_liter: float,
        sustainability: float,
    ) -> List[DesignRecommendation]:
        """
        Generate actionable design improvement recommendations.
        """
        recommendations = []
        
        # Adsorption improvement
        if adsorption_score < 0.75 and nanoparticle_loading_pct < 18:
            recommendations.append(DesignRecommendation(
                recommendation_text="Increase nanoparticle loading to boost adsorption capacity",
                parameter_to_change="nanoparticle_loading_pct",
                suggested_value=min(18, nanoparticle_loading_pct + 5),
                expected_impact_on_yield_pct=12,
                expected_impact_on_cost_pct=8,
                expected_impact_on_sustainability=-2,
                confidence=0.8,
                scientific_basis="Optimal loading 10-15%. Diminishing returns above 20% (agglomeration risk)."
            ))
        
        # Polymer improvement
        if adsorption_score < 0.7 and polymer_type == "pure_chitosan":
            recommendations.append(DesignRecommendation(
                recommendation_text="Consider modified chitosan or ZnO/chitosan composite for better hydrophilicity",
                parameter_to_change="polymer_matrix",
                suggested_value=None,  # Categorical choice
                expected_impact_on_yield_pct=18,
                expected_impact_on_cost_pct=15,
                expected_impact_on_sustainability=-5,
                confidence=0.75,
                scientific_basis="ZnO/chitosan shows 15-20% yield improvement but higher complexity."
            ))
        
        # Cost optimization
        if cost_per_liter > 2.5:
            recommendations.append(DesignRecommendation(
                recommendation_text="Plan scale-up to pilot level to reduce per-unit costs",
                parameter_to_change="manufacturing_scale",
                suggested_value=None,  # Pilot scale
                expected_impact_on_yield_pct=0,
                expected_impact_on_cost_pct=-35,
                expected_impact_on_sustainability=2,
                confidence=0.85,
                scientific_basis="Batch scaling reduces overhead & labor. Standard manufacturing economics."
            ))
        
        # Sustainability improvement
        if sustainability < 0.75:
            recommendations.append(DesignRecommendation(
                recommendation_text="Shift to water-based solvents and biomass pretreatment",
                parameter_to_change="solvent_system",
                suggested_value=None,  # Water-based
                expected_impact_on_yield_pct=-3,
                expected_impact_on_cost_pct=-5,
                expected_impact_on_sustainability=15,
                confidence=0.9,
                scientific_basis="Water-based synthesis proven green pathway with minimal yield penalty."
            ))
        
        return recommendations


if __name__ == "__main__":
    # Test recommendation engine
    bottlenecks = RecommendationEngine.identify_bottlenecks(
        adsorption_score=0.65,
        desorption_efficiency=0.55,
        condensation_likelihood=0.60,
        collection_efficiency=0.90,
        cost_per_liter_usd=2.80,
        manufacturability=0.65,
        sustainability=0.72,
        trl_level=3,
    )
    
    print("Identified Bottlenecks:")
    for i, b in enumerate(bottlenecks, 1):
        print(f"{i}. {b.bottleneck_type.value}")
        print(f"   Current: {b.current_score:.2f}, Target: {b.target_score:.2f}")
        print(f"   Impact: {b.impact_on_yield_pct:.0f}% on yield")
