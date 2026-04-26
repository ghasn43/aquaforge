"""
Bio Catalyst Logic for AquaForge
Explicit scientific modeling of biomass pretreatment, catalyst selection, 
synthesis pathway effects, morphology control, and surface chemistry influence.
Powered by Bio Catalyst Engineering expertise.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Tuple


class BiomassPretreatmentMethod(Enum):
    """Biomass pretreatment methods affecting synthesis outcomes"""
    NONE = "None (raw material)"
    DRYING = "Thermal drying"
    GRINDING = "Mechanical grinding"
    ACID_WASH = "Acid wash (removes inorganics)"
    ALKALINE_WASH = "Alkaline wash (removes lignin)"
    COMBINED = "Acid + alkaline wash (comprehensive)"


class CatalystType(Enum):
    """Catalyst families for green synthesis"""
    ACID = "Acid catalyst (HCl, H₂SO₄, citric acid)"
    BASE = "Base catalyst (NaOH, NH₃)"
    SALT = "Salt-based (FeCl₃, ZnCl₂, CaCl₂)"
    ENZYME = "Enzymatic (peroxidase, amylase)"
    METAL_SALT = "Metal salt precursor (Fe/Zn/Ce salts)"
    NONE = "None (self-catalyzing)"


class MorphologyControl(Enum):
    """Morphology control techniques"""
    TEMPLATE_FREE = "Template-free (random)"
    SURFACTANT_TEMPLATED = "Surfactant-templated (spheres, rods)"
    STRUCTURE_DIRECTING = "Structure-directing agent (hierarchical)"
    SEEDED_GROWTH = "Seeded growth (size control)"


@dataclass
class BiomassPretreatmentProfile:
    """Pretreatment specifications and their effects"""
    feedstock_type: str
    pretreatment_method: BiomassPretreatmentMethod
    pretreatment_temperature_c: float
    pretreatment_time_hours: float
    
    # Effects
    impurity_removal_pct: float  # 0-100% of inorganic/lignin removal
    carbon_concentration_increase_pct: float  # % increase in reactive carbon
    cost_multiplier: float  # 1.0 = no cost increase
    sustainability_adjustment: float  # -1 to +1 (negative if energy-intensive)
    
    def get_description(self) -> str:
        """Human-readable description of pretreatment"""
        desc = f"Pretreatment: {self.pretreatment_method.value}\n"
        desc += f"  Temperature: {self.pretreatment_temperature_c}°C\n"
        desc += f"  Time: {self.pretreatment_time_hours} hours\n"
        desc += f"  Expected impurity removal: {self.impurity_removal_pct}%\n"
        desc += f"  Carbon concentration increase: +{self.carbon_concentration_increase_pct}%\n"
        return desc


@dataclass
class CatalystProfile:
    """Catalyst specifications for synthesis"""
    catalyst_type: CatalystType
    catalyst_name: str
    concentration_mol_per_l: float
    reaction_ph: float
    synergy_with_morphology: float  # 0-1 (how well it supports morphology control)
    green_score: float  # 0-1 (greener = lower toxicity, renewable, etc.)
    cost_per_kg: float
    
    def get_description(self) -> str:
        """Human-readable catalyst description"""
        return (
            f"Catalyst: {self.catalyst_name}\n"
            f"  Type: {self.catalyst_type.value}\n"
            f"  Concentration: {self.concentration_mol_per_l:.2f} M\n"
            f"  Reaction pH: {self.reaction_ph:.1f}\n"
            f"  Green Score: {self.green_score:.2f}/1.0\n"
            f"  Cost: ${self.cost_per_kg:.2f}/kg"
        )


class BioCatalystEngine:
    """
    Central engine for green synthesis pathway design using Bio Catalyst Engineering principles.
    Provides scientific modeling of biomass pretreatment, catalyst selection, and synthesis effects.
    """
    
    # Biomass pretreatment profiles
    PRETREATMENT_PROFILES: Dict[str, Dict[BiomassPretreatmentMethod, BiomassPretreatmentProfile]] = {
        "peanut_shell": {
            BiomassPretreatmentMethod.NONE: BiomassPretreatmentProfile(
                feedstock_type="Peanut Shell",
                pretreatment_method=BiomassPretreatmentMethod.NONE,
                pretreatment_temperature_c=0,
                pretreatment_time_hours=0,
                impurity_removal_pct=0,
                carbon_concentration_increase_pct=0,
                cost_multiplier=1.0,
                sustainability_adjustment=0.0,
            ),
            BiomassPretreatmentMethod.ACID_WASH: BiomassPretreatmentProfile(
                feedstock_type="Peanut Shell",
                pretreatment_method=BiomassPretreatmentMethod.ACID_WASH,
                pretreatment_temperature_c=80,
                pretreatment_time_hours=2,
                impurity_removal_pct=45,
                carbon_concentration_increase_pct=12,
                cost_multiplier=1.2,
                sustainability_adjustment=-0.1,
            ),
            BiomassPretreatmentMethod.COMBINED: BiomassPretreatmentProfile(
                feedstock_type="Peanut Shell",
                pretreatment_method=BiomassPretreatmentMethod.COMBINED,
                pretreatment_temperature_c=90,
                pretreatment_time_hours=4,
                impurity_removal_pct=75,
                carbon_concentration_increase_pct=25,
                cost_multiplier=1.5,
                sustainability_adjustment=-0.15,
            ),
        }
    }
    
    # Catalyst profiles for different synthesis routes
    CATALYST_PROFILES: Dict[str, CatalystProfile] = {
        "green_synth_no_cat": CatalystProfile(
            catalyst_type=CatalystType.NONE,
            catalyst_name="Self-catalyzing (pH-driven)",
            concentration_mol_per_l=0.0,
            reaction_ph=7.0,
            synergy_with_morphology=0.3,
            green_score=1.0,
            cost_per_kg=0.0,
        ),
        "green_synth_acid": CatalystProfile(
            catalyst_type=CatalystType.ACID,
            catalyst_name="Citric acid (green catalyst)",
            concentration_mol_per_l=0.1,
            reaction_ph=3.5,
            synergy_with_morphology=0.6,
            green_score=0.95,
            cost_per_kg=2.5,
        ),
        "teos_silica": CatalystProfile(
            catalyst_type=CatalystType.ACID,
            catalyst_name="HCl (sol-gel catalyst)",
            concentration_mol_per_l=0.01,
            reaction_ph=2.0,
            synergy_with_morphology=0.7,
            green_score=0.60,
            cost_per_kg=1.5,
        ),
        "zno_green": CatalystProfile(
            catalyst_type=CatalystType.BASE,
            catalyst_name="NaOH (ZnO precipitation)",
            concentration_mol_per_l=0.5,
            reaction_ph=10.0,
            synergy_with_morphology=0.8,
            green_score=0.85,
            cost_per_kg=1.2,
        ),
        "fe_zn_composite": CatalystProfile(
            catalyst_type=CatalystType.METAL_SALT,
            catalyst_name="FeCl₃/ZnCl₂ co-precursor",
            concentration_mol_per_l=0.2,
            reaction_ph=5.0,
            synergy_with_morphology=0.65,
            green_score=0.50,
            cost_per_kg=8.0,
        ),
    }
    
    @staticmethod
    def estimate_morphology_effect(
        morphology_control: MorphologyControl,
        catalyst_synergy: float,
        synthesis_complexity: float,
    ) -> Tuple[float, str, List[str]]:
        """
        Estimate morphology control success and particle uniformity.
        
        Args:
            morphology_control: Control method
            catalyst_synergy: 0-1 (how well catalyst supports morphology)
            synthesis_complexity: 0-1 (ease of achieving target morphology)
        
        Returns:
            (uniformity_score: 0-1, description: str, recommendations: [str])
        """
        base_scores = {
            MorphologyControl.TEMPLATE_FREE: 0.4,
            MorphologyControl.SURFACTANT_TEMPLATED: 0.7,
            MorphologyControl.STRUCTURE_DIRECTING: 0.85,
            MorphologyControl.SEEDED_GROWTH: 0.75,
        }
        
        uniformity = base_scores.get(morphology_control, 0.5)
        uniformity *= catalyst_synergy
        uniformity *= (1.0 - synthesis_complexity * 0.2)  # Complexity penalty
        uniformity = max(0.0, min(1.0, uniformity))
        
        descriptions = {
            MorphologyControl.TEMPLATE_FREE: "Random morphology, broad size distribution",
            MorphologyControl.SURFACTANT_TEMPLATED: "Spheroidal shapes, moderate uniformity",
            MorphologyControl.STRUCTURE_DIRECTING: "Hierarchical/controlled structures, excellent uniformity",
            MorphologyControl.SEEDED_GROWTH: "Fine size control, good uniformity",
        }
        
        recommendations = []
        if uniformity < 0.5:
            recommendations.append("⚠️ Low uniformity - expect broad particle size distribution")
        if catalyst_synergy < 0.6:
            recommendations.append("💡 Consider catalyst adjustment to improve morphology control")
        if synthesis_complexity > 0.6:
            recommendations.append("🔬 High complexity - recommend bench-scale optimization first")
        
        return uniformity, descriptions.get(morphology_control, "Unknown"), recommendations
    
    @staticmethod
    def estimate_surface_chemistry(
        nanoparticle_type: str,
        synthesis_route: str,
        morphology: MorphologyControl,
        post_treatment: str = "none",
    ) -> Dict:
        """
        Estimate surface chemistry and its implications for adsorption.
        
        Args:
            nanoparticle_type: "silica", "zno", "composite"
            synthesis_route: "green_synthesis", "calcination", etc.
            morphology: MorphologyControl enum
            post_treatment: "none", "silanized", "aminosilane", "sulfhydryl"
        
        Returns:
            Dict with surface chemistry assessment
        """
        surface_oh_groups = {
            "silica": {"green_synthesis": 0.8, "calcination": 0.6, "teos": 0.75},
            "zno": {"green_synthesis": 0.7, "calcination": 0.5, "hydrothermal": 0.75},
            "composite": {"green_synthesis": 0.75, "calcination": 0.6},
        }
        
        oh_baseline = surface_oh_groups.get(nanoparticle_type, {}).get(synthesis_route, 0.5)
        
        # Morphology effect on surface OH
        morphology_boost = {
            MorphologyControl.STRUCTURE_DIRECTING: 0.1,
            MorphologyControl.SEEDED_GROWTH: 0.05,
            MorphologyControl.SURFACTANT_TEMPLATED: 0.02,
            MorphologyControl.TEMPLATE_FREE: 0.0,
        }
        oh_baseline += morphology_boost.get(morphology, 0.0)
        
        # Post-treatment effects
        post_treatment_effects = {
            "none": {"oh_groups": 0.0, "hydrophilicity_change": 0.0},
            "silanized": {"oh_groups": -0.4, "hydrophilicity_change": -0.3},
            "aminosilane": {"oh_groups": -0.2, "hydrophilicity_change": 0.2},
            "sulfhydryl": {"oh_groups": -0.1, "hydrophilicity_change": 0.1},
        }
        effects = post_treatment_effects.get(post_treatment.lower(), {})
        
        final_oh = max(0.0, min(1.0, oh_baseline + effects.get("oh_groups", 0.0)))
        
        return {
            "nanoparticle_type": nanoparticle_type,
            "synthesis_route": synthesis_route,
            "baseline_oh_groups_score": oh_baseline,
            "final_oh_groups_score": final_oh,
            "post_treatment": post_treatment,
            "hydrophilicity_implication": "High OH groups → strong water affinity → good adsorption",
            "recommendations": [
                "Surface characterization: FTIR (OH stretching ~3300-3500 cm⁻¹), TGA (hydroxyl content)",
                "Contact angle measurement: Validate hydrophilicity predictions",
                "BET/BJH: Confirm surface area and pore structure",
            ]
        }
    
    @staticmethod
    def recommend_synthesis_pathway(
        feedstock: str,
        target_yield_l_kg_day: float = 0.4,
        priority: str = "balanced",  # "green", "performance", "cost", "balanced"
    ) -> Dict:
        """
        Recommend optimized synthesis pathway combining pretreatment, catalyst, and morphology.
        
        Args:
            feedstock: e.g., "peanut_shell", "rice_husk"
            target_yield_l_kg_day: Desired water yield goal
            priority: Optimization criterion
        
        Returns:
            Dict with recommended pathway and rationale
        """
        recommendations = {
            "feedstock": feedstock,
            "target_yield": target_yield_l_kg_day,
            "priority": priority,
            "recommended_pretreatment": None,
            "recommended_catalyst": None,
            "recommended_morphology": None,
            "expected_performance": {},
            "rationale": "",
            "next_steps": [],
        }
        
        if priority == "green":
            recommendations["recommended_pretreatment"] = BiomassPretreatmentMethod.ACID_WASH
            recommendations["recommended_catalyst"] = "green_synth_acid"
            recommendations["recommended_morphology"] = MorphologyControl.TEMPLATE_FREE
            recommendations["rationale"] = (
                "Prioritizing sustainability: minimal pretreatment, citric acid catalyst, "
                "no surfactants or toxic chemicals. Yield trade-off expected."
            )
        elif priority == "performance":
            recommendations["recommended_pretreatment"] = BiomassPretreatmentMethod.COMBINED
            recommendations["recommended_catalyst"] = "zno_green"
            recommendations["recommended_morphology"] = MorphologyControl.STRUCTURE_DIRECTING
            recommendations["rationale"] = (
                "Prioritizing water yield: comprehensive pretreatment removes impurities, "
                "ZnO catalyst excellent for hydrophilicity, structure-directing for uniformity."
            )
        elif priority == "cost":
            recommendations["recommended_pretreatment"] = BiomassPretreatmentMethod.NONE
            recommendations["recommended_catalyst"] = "green_synth_no_cat"
            recommendations["recommended_morphology"] = MorphologyControl.TEMPLATE_FREE
            recommendations["rationale"] = (
                "Minimizing cost: no pretreatment, self-catalyzing, minimal additives. "
                "Lower yield and uniformity, but lowest production cost."
            )
        else:  # balanced
            recommendations["recommended_pretreatment"] = BiomassPretreatmentMethod.ACID_WASH
            recommendations["recommended_catalyst"] = "teos_silica"
            recommendations["recommended_morphology"] = MorphologyControl.SURFACTANT_TEMPLATED
            recommendations["rationale"] = (
                "Balanced approach: moderate pretreatment, well-established TEOS/silica pathway, "
                "surfactant-templated for good particle control. Good compromise across metrics."
            )
        
        recommendations["next_steps"] = [
            "1. Perform bench-scale synthesis with recommended pathway",
            "2. Characterize nanomaterial (SEM, XRD, BET, contact angle)",
            "3. Prepare membrane formulation (Tab 3) with synthesized nanoparticles",
            "4. Run water sorption tests at various RH levels",
            "5. Compare experimental yield against AquaForge simulation",
            "6. Iterate design based on validation data",
        ]
        
        return recommendations


if __name__ == "__main__":
    # Test Bio Catalyst Engine
    rec = BioCatalystEngine.recommend_synthesis_pathway(
        feedstock="peanut_shell",
        target_yield_l_kg_day=0.4,
        priority="green",
    )
    print("Recommended Synthesis Pathway:")
    for key, value in rec.items():
        print(f"  {key}: {value}")
