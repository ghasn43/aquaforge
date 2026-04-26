"""
Transparency Engine for AquaForge
Provides baseline-factor-confidence model for all heuristic predictions
Shows calculation rationale, adjustment factors, confidence levels, and warning flags
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
from enum import Enum


class ConfidenceLevel(Enum):
    """Confidence rating scale for predictions"""
    LOW = ("Low", 0.3, "Extrapolated far from data, high uncertainty")
    MEDIUM = ("Medium", 0.6, "Within typical range, moderate uncertainty")
    HIGH = ("High", 0.9, "Well-supported by data, low uncertainty")


@dataclass
class AdjustmentFactor:
    """Single adjustment factor applied to a baseline value"""
    name: str
    multiplier: float  # 0.5 = 50% reduction, 1.5 = 50% increase
    rationale: str
    evidence: str  # Reference or scientific basis
    
    def apply(self, value: float) -> float:
        return value * self.multiplier


@dataclass
class PredictionModel:
    """Transparent prediction with baseline, factors, confidence, and rationale"""
    metric_name: str
    baseline_value: float
    baseline_source: str
    adjustment_factors: List[AdjustmentFactor] = field(default_factory=list)
    predicted_value: float = 0.0
    confidence_level: ConfidenceLevel = ConfidenceLevel.MEDIUM
    confidence_rationale: str = ""
    warning_flags: List[str] = field(default_factory=list)
    scientific_rationale: str = ""
    caveats: List[str] = field(default_factory=list)
    
    def calculate(self) -> float:
        """Apply all factors to baseline and return predicted value"""
        value = self.baseline_value
        for factor in self.adjustment_factors:
            value = factor.apply(value)
        self.predicted_value = value
        return value
    
    def get_summary(self) -> Dict:
        """Return structured summary of prediction"""
        return {
            "metric": self.metric_name,
            "baseline": self.baseline_value,
            "baseline_source": self.baseline_source,
            "factors": [
                {
                    "name": f.name,
                    "multiplier": f"{f.multiplier:.2f}x",
                    "rationale": f.rationale,
                    "evidence": f.evidence,
                }
                for f in self.adjustment_factors
            ],
            "predicted_value": f"{self.predicted_value:.4f}",
            "confidence": self.confidence_level.value[0],
            "confidence_reason": self.confidence_rationale,
            "warnings": self.warning_flags,
            "scientific_rationale": self.scientific_rationale,
            "caveats": self.caveats,
        }
    
    def get_markdown_summary(self) -> str:
        """Generate markdown-formatted explanation"""
        md = f"## {self.metric_name}\n\n"
        md += f"**Predicted Value**: {self.predicted_value:.4f}\n"
        md += f"**Confidence**: {self.confidence_level.value[0]} ({self.confidence_rationale})\n\n"
        
        md += f"### Calculation\n"
        md += f"**Baseline**: {self.baseline_value:.4f} ({self.baseline_source})\n\n"
        
        if self.adjustment_factors:
            md += f"**Adjustment Factors**:\n"
            for factor in self.adjustment_factors:
                md += f"- {factor.name}: ×{factor.multiplier:.2f}\n"
                md += f"  - Rationale: {factor.rationale}\n"
                md += f"  - Evidence: {factor.evidence}\n"
            md += "\n"
        
        if self.scientific_rationale:
            md += f"### Scientific Rationale\n{self.scientific_rationale}\n\n"
        
        if self.warning_flags:
            md += f"### ⚠️ Warnings\n"
            for warning in self.warning_flags:
                md += f"- {warning}\n"
            md += "\n"
        
        if self.caveats:
            md += f"### Caveats\n"
            for caveat in self.caveats:
                md += f"- {caveat}\n"
        
        return md


class TransparencyEngine:
    """
    Central engine for creating transparent, explainable heuristic predictions.
    Every prediction includes baseline, factors, confidence, and rationale.
    """
    
    @staticmethod
    def create_adsorption_strength_model(
        polymer_hydrophilicity: float,
        nanoparticle_loading_pct: float,
        nanoparticle_type: str,
        porosity: float,
        dispersion_quality: str,
        layer_config: str,
    ) -> PredictionModel:
        """
        Transparent model for membrane adsorption strength prediction.
        
        Args:
            polymer_hydrophilicity: 0-1 scale (higher = more hydrophilic)
            nanoparticle_loading_pct: 0-30% by weight
            nanoparticle_type: "silica", "zno", "composite"
            porosity: 0-1 scale (higher = more porous)
            dispersion_quality: "poor", "fair", "good", "excellent"
            layer_config: "single", "dual", "triple"
        
        Returns:
            PredictionModel with transparent calculation
        """
        model = PredictionModel(
            metric_name="Membrane Adsorption Strength",
            baseline_value=polymer_hydrophilicity,  # Baseline from polymer alone
            baseline_source="Polymer matrix hydrophilicity score (0-1 scale from literature)",
        )
        
        # Factor 1: Nanoparticle loading contribution
        loading_factor = 1.0 + (nanoparticle_loading_pct / 100.0) * 0.35  # Max 35% boost
        
        # Nanoparticle type modifier
        nanoparticle_modifier = {
            "silica": 0.90,      # Good but hydrophilic, not as good as ZnO
            "zno": 1.10,         # Excellent hydrophilicity
            "composite": 1.05,   # Good balance
        }.get(nanoparticle_type.lower(), 1.0)
        
        model.adjustment_factors.append(AdjustmentFactor(
            name=f"Nanoparticle Loading ({nanoparticle_loading_pct:.1f}%) + Type ({nanoparticle_type})",
            multiplier=loading_factor * nanoparticle_modifier,
            rationale="Nanoparticles increase surface area and active sites. ZnO better than silica.",
            evidence="Literature: ZnO hydrophilicity > Silica > unloaded polymer. Optimal loading 10-15%.",
        ))
        
        # Factor 2: Porosity enhancement
        porosity_factor = 1.0 + (porosity * 0.25)  # Up to 25% boost from high porosity
        model.adjustment_factors.append(AdjustmentFactor(
            name=f"Porosity Effect ({porosity:.2f})",
            multiplier=porosity_factor,
            rationale="Higher porosity increases accessible surface area for adsorption.",
            evidence="BET theory: Surface area ∝ porosity × pore volume",
        ))
        
        # Factor 3: Dispersion quality penalty
        dispersion_factors = {
            "poor": 0.70,
            "fair": 0.85,
            "good": 0.95,
            "excellent": 1.05,
        }
        dispersion_factor = dispersion_factors.get(dispersion_quality.lower(), 0.85)
        model.adjustment_factors.append(AdjustmentFactor(
            name=f"Dispersion Quality ({dispersion_quality})",
            multiplier=dispersion_factor,
            rationale="Poor dispersion = agglomeration = reduced active surface.",
            evidence="SEM/XRD characterization: Agglomeration reduces BET surface area by 10-40%",
        ))
        
        # Factor 4: Layer configuration
        layer_factors = {
            "single": 1.0,
            "dual": 1.15,
            "triple": 1.25,
        }
        layer_factor = layer_factors.get(layer_config.lower(), 1.0)
        model.adjustment_factors.append(AdjustmentFactor(
            name=f"Layer Configuration ({layer_config})",
            multiplier=layer_factor,
            rationale="Multi-layer design increases total surface area and adsorption capacity.",
            evidence="Design principle: N layers ≈ N× effective adsorption sites",
        ))
        
        # Calculate predicted value
        model.calculate()
        
        # Clamp to 0-1
        model.predicted_value = max(0.0, min(1.0, model.predicted_value))
        
        # Set confidence based on input validity
        if 10 <= nanoparticle_loading_pct <= 15 and dispersion_quality == "good":
            model.confidence_level = ConfidenceLevel.HIGH
            model.confidence_rationale = "Inputs within optimal synthesis range"
        elif 0 <= nanoparticle_loading_pct <= 25 and dispersion_quality in ["good", "fair"]:
            model.confidence_level = ConfidenceLevel.MEDIUM
            model.confidence_rationale = "Reasonable parameter range, typical experimental conditions"
        else:
            model.confidence_level = ConfidenceLevel.LOW
            model.confidence_rationale = "Extrapolated beyond typical conditions"
        
        # Add warnings
        if nanoparticle_loading_pct > 20:
            model.warning_flags.append("⚠️ High loading (>20%) - risk of agglomeration and brittleness")
        if nanoparticle_loading_pct < 5:
            model.warning_flags.append("⚠️ Low loading (<5%) - limited nanoparticle benefit")
        if dispersion_quality == "poor":
            model.warning_flags.append("⚠️ Poor dispersion - significant performance loss expected")
        
        model.scientific_rationale = (
            "Adsorption strength combines polymer base hydrophilicity with nanoparticle loading effects. "
            "Heuristic model weights porosity and dispersion quality as limiting factors. "
            "Multi-layer configuration increases total active surface area."
        )
        
        model.caveats = [
            "Actual performance requires experimental validation (BET, dynamic water sorption testing)",
            "Assumes uniform dispersion; real nanoparticles may agglomerate",
            "Does not account for crosslinking effects or chemical modifications",
        ]
        
        return model
    
    @staticmethod
    def create_water_yield_model(
        adsorption_score: float,
        desorption_efficiency: float,
        condensation_likelihood: float,
        collection_efficiency: float,
        filtration_efficiency: float,
        atmospheric_rh: float,
        temperature_c: float,
    ) -> PredictionModel:
        """
        Transparent model for water yield prediction (L/kg/day)
        
        Shows contribution of each stage and how atmospheric conditions modulate yield.
        """
        # Baseline from literature typical range (0.3-0.5 L/kg/day for well-optimized systems)
        baseline = 0.40  # L/kg/day
        
        model = PredictionModel(
            metric_name="Water Yield (L/kg/day)",
            baseline_value=baseline,
            baseline_source="Literature average for optimized chitosan/nanoparticle systems at 70% RH, 25°C",
        )
        
        # Stage 1: Adsorption modulation by RH
        rh_normalized = max(0.0, min(1.0, (atmospheric_rh - 20) / 80))  # 20% RH = 0, 100% RH = 1
        rh_factor = 0.5 + (rh_normalized * 1.0)  # Range: 0.5x to 1.5x
        
        model.adjustment_factors.append(AdjustmentFactor(
            name=f"Adsorption Stage (RH={atmospheric_rh}%, Score={adsorption_score:.2f})",
            multiplier=rh_factor * adsorption_score,
            rationale="Higher RH increases vapor pressure gradient, driving adsorption",
            evidence="Clausius-Clapeyron relation: Adsorption ∝ (RH_sat - RH_actual)",
        ))
        
        # Stage 2: Desorption efficiency
        model.adjustment_factors.append(AdjustmentFactor(
            name=f"Desorption Efficiency ({desorption_efficiency:.2f})",
            multiplier=desorption_efficiency,
            rationale="Not all adsorbed water can be desorbed; efficiency depends on heat availability",
            evidence="Thermal analysis: Typical desorption 40-90% depending on heating mode",
        ))
        
        # Stage 3: Condensation
        temp_factor = 1.0 - ((temperature_c - 20) / 40)  # Lower T = better condensation
        temp_factor = max(0.4, min(1.2, temp_factor))
        
        model.adjustment_factors.append(AdjustmentFactor(
            name=f"Condensation Stage (T={temperature_c}°C, Score={condensation_likelihood:.2f})",
            multiplier=temp_factor * condensation_likelihood,
            rationale="Lower temperature increases condensation. Passive cooling most effective in cool climates.",
            evidence="Dew point physics: ΔT = (T_surface - T_air) drives condensation rate",
        ))
        
        # Stage 4: Collection & Filtration
        model.adjustment_factors.append(AdjustmentFactor(
            name=f"Collection & Filtration ({collection_efficiency:.2f} × {filtration_efficiency:.2f})",
            multiplier=collection_efficiency * filtration_efficiency,
            rationale="Gravity-driven collection + optional filtration stage",
            evidence="System design: Recovery losses typically 10-20%, filtration 5-15%",
        ))
        
        model.calculate()
        
        # Set confidence
        if 40 <= atmospheric_rh <= 90 and 15 <= temperature_c <= 35:
            model.confidence_level = ConfidenceLevel.HIGH
        elif 20 <= atmospheric_rh <= 100 and 10 <= temperature_c <= 40:
            model.confidence_level = ConfidenceLevel.MEDIUM
        else:
            model.confidence_level = ConfidenceLevel.LOW
        
        model.confidence_rationale = f"RH={atmospheric_rh}% {'(good range)' if 40<=atmospheric_rh<=90 else '(extrapolated)'}, T={temperature_c}°C {'(typical)' if 15<=temperature_c<=35 else '(edge case)'}"
        
        if atmospheric_rh < 30:
            model.warning_flags.append("⚠️ Very low RH (<30%) - yields will be severely limited")
        if temperature_c > 40:
            model.warning_flags.append("⚠️ High temperature (>40°C) - reduces condensation efficiency")
        
        model.scientific_rationale = (
            "Water yield is a multiplicative cascade of efficiency stages: Adsorption → Desorption → Condensation → Collection → Filtration. "
            "Each stage acts as a bottleneck. RH and temperature are the dominant climate drivers."
        )
        
        return model


if __name__ == "__main__":
    # Test the transparency engine
    model = TransparencyEngine.create_adsorption_strength_model(
        polymer_hydrophilicity=0.7,
        nanoparticle_loading_pct=12,
        nanoparticle_type="zno",
        porosity=0.6,
        dispersion_quality="good",
        layer_config="dual",
    )
    print(model.get_markdown_summary())
