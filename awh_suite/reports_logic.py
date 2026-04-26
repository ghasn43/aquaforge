"""
Report generation and export functionality.
"""

from data_models import ProjectState, SimulationResult
from typing import Dict
import json
from datetime import datetime


class ReportGenerator:
    """Generate technical reports and export summaries."""

    @staticmethod
    def generate_technical_summary(project: ProjectState) -> str:
        """
        Generate comprehensive technical summary report.
        """
        report = f"""
# Atmospheric Water Harvesting Design Summary

**Project**: {project.project_name}
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 1. Project Overview

{project.notes if project.notes else 'No project notes provided.'}

---

## 2. Selected Materials

### Feedstock
- **Type**: {project.feedstock.feedstock_type.value}
- **Pretreatment**: {project.feedstock.pretreatment_chemistry}
- **pH**: {project.feedstock.ph}
- **Cost per kg**: ${project.feedstock.cost_per_kg:.2f}
- **Sustainability Score**: {project.feedstock.sustainability_score:.2f}/1.0

### Nanomaterial System
- **Synthesis Route**: {project.nanomaterial.synthesis_route.value}
- **Expected Particle Size**: {project.nanomaterial.expected_particle_size_nm[0]:.0f}-{project.nanomaterial.expected_particle_size_nm[1]:.0f} nm
- **Expected Morphology**: {project.nanomaterial.expected_morphology}
- **Crystallinity**: {project.nanomaterial.expected_crystallinity_pct:.1f}%
- **Water Adsorption Relevance**: {project.nanomaterial.water_adsorption_relevance:.2f}/1.0
- **Synthesis Complexity**: {project.nanomaterial.synthesis_complexity:.2f}/1.0
- **Estimated Cost per kg**: ${project.nanomaterial.estimated_cost_per_kg:.2f}

---

## 3. Membrane Configuration

- **Matrix Polymer**: {project.membrane.polymer_matrix.value}
- **Nanoparticle Type**: {project.membrane.nanoparticle_type}
- **Nanoparticle Loading**: {project.membrane.nanoparticle_loading_wt_pct:.1f} wt%
- **Particle Size**: {project.membrane.particle_size_nm:.1f} nm
- **Dispersion Quality**: {project.membrane.particle_dispersion_quality}
- **Layer Configuration**: {project.membrane.layer_config.value}
- **Thickness**: {project.membrane.thickness_um:.1f} µm
- **Porosity**: {project.membrane.porosity_pct:.1f}%
- **Crosslinker**: {project.membrane.crosslinker}
- **Crosslink Density**: {project.membrane.crosslink_density}

### Estimated Membrane Performance
- **Contact Angle**: {project.membrane.estimated_contact_angle_deg:.1f}° {'(Hydrophilic)' if project.membrane.estimated_contact_angle_deg < 70 else '(Hydrophobic)'}
- **Adsorption Strength**: {project.membrane.estimated_adsorption_strength:.2f}/1.0
- **Desorption Ease**: {project.membrane.desorption_ease:.2f}/1.0
- **Mechanical Stability**: {project.membrane.mechanical_stability:.2f}/1.0
- **Moisture Capture**: {project.membrane.moisture_capture_score:.2f}/1.0
- **Thermal Robustness**: {project.membrane.thermal_robustness:.2f}/1.0
- **Manufacturability**: {project.membrane.manufacturability_score:.2f}/1.0
- **Sustainability Score**: {project.membrane.sustainability_score:.2f}/1.0

---

## 4. Device Configuration

- **Device Class**: {project.device.device_class.value}
- **Overall Diameter**: {project.device.overall_diameter_cm:.1f} cm
- **Total Height**: {project.device.total_height_cm:.1f} cm
- **Upper Chamber Height**: {project.device.upper_chamber_height_cm:.1f} cm
- **Lower Chamber Height**: {project.device.lower_chamber_height_cm:.1f} cm
- **Cone Angle**: {project.device.cone_angle_deg:.1f}°
- **Funnel Throat Diameter**: {project.device.funnel_throat_diameter_cm:.1f} cm
- **Structural Material**: {project.device.structural_material}
- **Chamber Transparency**: {project.device.chamber_transparency}
- **Reservoir Capacity**: {project.device.reservoir_capacity_ml:.0f} mL
- **Support Columns**: {project.device.support_columns_count}
- **Thermal Mode**: {project.device.thermal_mode.value}
- **Filtration Stage**: {'Yes' if project.device.filtration_stage else 'No'}

### Estimated Device Volumes
- **Upper Chamber**: {project.device.upper_chamber_volume_l:.2f} L
- **Lower Chamber**: {project.device.lower_chamber_volume_l:.2f} L
- **Cone Volume**: {project.device.cone_volume_l:.2f} L
- **Estimated Manufacturability**: {project.device.estimated_manufacturability:.2f}/1.0
- **Maintenance Complexity**: {project.device.maintenance_complexity:.2f}/1.0

---

## 5. Operating Conditions

- **Relative Humidity**: {project.conditions.relative_humidity_pct:.1f}%
- **Ambient Temperature**: {project.conditions.ambient_temperature_c:.1f}°C
- **Day/Night Mode**: {project.conditions.day_night_mode}
- **Airflow Level**: {project.conditions.airflow_level}
- **Solar Exposure**: {project.conditions.solar_exposure}
- **Cycle Duration**: {project.conditions.cycle_duration_hours:.1f} hours
- **Operation Mode**: {project.conditions.operation_mode}

---

## 6. Predicted Performance

### Water Yield
- **Estimated Yield**: {project.simulation.predicted_water_yield_l_kg_day:.3f} L/kg/day
- **Yield per gram adsorbent**: {project.simulation.predicted_water_yield_ml_g:.2f} mL/g

### Efficiency Metrics
- **Adsorption Score**: {project.simulation.adsorption_score:.2f}/1.0
- **Desorption Efficiency**: {project.simulation.desorption_efficiency:.2f}/1.0
- **Condensation Likelihood**: {project.simulation.condensation_likelihood:.2f}/1.0
- **Collection Efficiency**: {project.simulation.collection_efficiency_pct:.1f}%
- **Filtration Efficiency**: {project.simulation.filtration_efficiency_pct:.1f}%
- **Relative Performance Score**: {project.simulation.relative_performance_score:.2f}/1.0

### Performance Assessment
- **Performance Window**: {project.simulation.performance_window}
- **Confidence Level**: {project.simulation.confidence_level}

### Stage Contributions
"""
        for stage, contribution in project.simulation.stage_contributions.items():
            report += f"- **{stage}**: {contribution:.1f}%\n"

        report += f"""
---

## 7. Cost & Scale-Up Analysis

- **Feedstock Cost**: ${project.costing.feedstock_cost_per_kg:.2f}/kg
- **Polymer Cost**: ${project.costing.polymer_cost_per_kg:.2f}/kg
- **Nanoparticle Prep Cost**: ${project.costing.nanoparticle_prep_cost_per_kg:.2f}/kg
- **Base Device Cost**: ${project.costing.device_fabrication_cost_base:.2f}

### Estimated Economics
- **Cost per Membrane**: ${project.costing.cost_per_membrane:.2f}
- **Total Prototype Cost**: ${project.costing.prototype_cost_total:.2f}
- **Cost per Liter Harvested**: ${project.costing.cost_per_liter_harvested:.2f}
- **CAPEX (Equipment)**: ${project.costing.capex_estimate:.2f}
- **OPEX (Per Batch)**: ${project.costing.opex_estimate:.2f}

### Scale Level
- **Current Scale**: {project.costing.scale_level}
- **Scale-Up Burden**: {project.costing.scale_up_burden * 100:.1f}%
- **Sustainability-Adjusted Cost**: {project.costing.sustainability_adjusted_cost:.2f}/1.0

---

## 8. R&D Recommendations

This design represents a **design-phase heuristic model** for R&D decision support.

### Next Steps
1. Conduct feedstock characterization and green synthesis trials
2. Validate membrane formulation through adsorption isotherms and contact angle measurements
3. Prototype device and conduct bench-scale atmospheric water collection experiments
4. Compare actual performance against predicted heuristic values
5. Iterate design based on experimental validation

### Important Notes
- All performance predictions are based on heuristic rules, not certified experimental data
- Material costs are indicative; validate with suppliers
- Water yield estimates assume ideal conditions; field conditions will vary
- Recommend TRL validation before commercial commitment

---

**Report Disclaimer**: This report is generated by the Atmospheric Water Harvesting Suite as a design-stage decision support tool. It is not a certified engineering analysis or business plan. Use for R&D guidance only.
"""

        return report

    @staticmethod
    def generate_investor_summary(project: ProjectState) -> str:
        """Generate concise investor-friendly summary."""
        summary = f"""
# {project.project_name}

## Executive Summary

This atmospheric water harvesting system design combines green nanomaterial engineering 
with passive device architecture for sustainable fresh water generation.

## Key Design Features

**Materials Science**
- Feedstock: {project.feedstock.feedstock_type.value}
- Synthesis: {project.nanomaterial.synthesis_route.value}
- Matrix: {project.membrane.polymer_matrix.value}
- Nanoparticles: {project.membrane.nanoparticle_type}

**Device Architecture**
- Class: {project.device.device_class.value}
- Passive Design: {'Yes' if project.device.passive_assisted == 'Passive' else 'No (Assisted)'}
- Estimated Size: {project.device.overall_diameter_cm:.0f}cm × {project.device.total_height_cm:.0f}cm

## Performance Indicators

| Metric | Value |
|--------|-------|
| Estimated Water Yield | {project.simulation.predicted_water_yield_l_kg_day:.3f} L/kg/day |
| Adsorption Score | {project.simulation.adsorption_score:.1%} |
| Relative Performance | {project.simulation.relative_performance_score:.1%} |
| Sustainability | {project.membrane.sustainability_score:.1%} |
| Cost per Liter | ${project.costing.cost_per_liter_harvested:.2f} |

## Development Stage

- **Scientific Readiness**: TRL 3-4
- **Fabrication Status**: Early prototype development
- **Market Timeline**: 3-5 years to pilot deployment

## Competitive Advantages

- **Green Materials**: Agro-waste derived, biodegradable, sustainable supply chain
- **Passive Operation**: Lower energy demand than MOF alternatives
- **Scalability**: Simpler synthesis pathway vs. complex MOF production
- **Cost**: Projected 40-60% lower material costs than MOF systems
- **IP Potential**: Novel nanocomposite formulations and device design

## Investment Requirements

- R&D Phase: Concept validation and material optimization
- Estimated Cost: Membrane research + device prototyping
- Timeline: 18-24 months to pilot-scale demonstration

---

*This summary is based on design-stage heuristic modeling. Recommend technical due diligence before investment decisions.*
"""
        return summary

    @staticmethod
    def generate_csv_export(project: ProjectState) -> str:
        """Generate CSV format for spreadsheet import."""
        csv_lines = [
            "Parameter,Value,Unit",
            "",
            "# FEEDSTOCK",
            f"Feedstock Type,{project.feedstock.feedstock_type.value},",
            f"Cost per kg,{project.feedstock.cost_per_kg:.2f},USD/kg",
            "",
            "# NANOMATERIAL",
            f"Synthesis Route,{project.nanomaterial.synthesis_route.value},",
            f"Particle Size Min,{project.nanomaterial.expected_particle_size_nm[0]:.0f},nm",
            f"Particle Size Max,{project.nanomaterial.expected_particle_size_nm[1]:.0f},nm",
            f"Crystallinity,{project.nanomaterial.expected_crystallinity_pct:.1f},%",
            "",
            "# MEMBRANE",
            f"Polymer Matrix,{project.membrane.polymer_matrix.value},",
            f"Nanoparticle Loading,{project.membrane.nanoparticle_loading_wt_pct:.1f},%",
            f"Thickness,{project.membrane.thickness_um:.1f},micrometers",
            f"Porosity,{project.membrane.porosity_pct:.1f},%",
            f"Estimated Contact Angle,{project.membrane.estimated_contact_angle_deg:.1f},degrees",
            f"Adsorption Strength,{project.membrane.estimated_adsorption_strength:.2f},0-1",
            "",
            "# DEVICE",
            f"Device Class,{project.device.device_class.value},",
            f"Diameter,{project.device.overall_diameter_cm:.1f},cm",
            f"Height,{project.device.total_height_cm:.1f},cm",
            f"Cone Angle,{project.device.cone_angle_deg:.1f},degrees",
            f"Reservoir Capacity,{project.device.reservoir_capacity_ml:.0f},mL",
            "",
            "# SIMULATION RESULTS",
            f"Water Yield,{project.simulation.predicted_water_yield_l_kg_day:.4f},L/kg/day",
            f"Adsorption Score,{project.simulation.adsorption_score:.2f},0-1",
            f"Desorption Efficiency,{project.simulation.desorption_efficiency:.2f},0-1",
            f"Collection Efficiency,{project.simulation.collection_efficiency_pct:.1f},%",
            f"Relative Performance,{project.simulation.relative_performance_score:.2f},0-1",
            "",
            "# COST & SCALING",
            f"Cost per Membrane,{project.costing.cost_per_membrane:.2f},USD",
            f"Prototype Cost Total,{project.costing.prototype_cost_total:.2f},USD",
            f"Cost per Liter,{project.costing.cost_per_liter_harvested:.2f},USD/L",
        ]
        return "\n".join(csv_lines)

    @staticmethod
    def generate_json_export(project: ProjectState) -> str:
        """Generate full project as JSON for saving/loading."""
        data = project.to_dict()
        # Make it JSON serializable
        data['created_date'] = datetime.now().isoformat()
        data['last_modified'] = datetime.now().isoformat()
        return json.dumps(data, indent=2, default=str)

    @staticmethod
    def generate_sop_draft(project: ProjectState) -> str:
        """Generate Standard Operating Procedure draft."""
        sop = f"""
# Standard Operating Procedure (SOP) - DRAFT
# Membrane Synthesis and Device Assembly
# Based on Design: {project.project_name}

## 1. FEEDSTOCK PREPARATION

### Materials
- {project.feedstock.feedstock_type.value}: [QUANTITY]
- {project.feedstock.pretreatment_chemistry}

### Procedure
1. Source and verify feedstock (agro-industrial waste)
2. Wash feedstock with deionized water (3× cycles)
3. Adjust pH to {project.feedstock.ph} using standard acid/base
4. Dry at [TEMP]°C for 24 hours
5. Store in sealed containers, desiccant pack

---

## 2. NANOMATERIAL SYNTHESIS

### Route: {project.nanomaterial.synthesis_route.value}

### Expected Outcome
- Particle Size: {project.nanomaterial.expected_particle_size_nm[0]:.0f}-{project.nanomaterial.expected_particle_size_nm[1]:.0f} nm
- Morphology: {project.nanomaterial.expected_morphology}
- Crystallinity: ~{project.nanomaterial.expected_crystallinity_pct:.0f}%

### Key Parameters
- Reaction Time: {project.nanomaterial.reaction_time_hours:.1f} hours
- Drying Temperature: {project.nanomaterial.drying_temperature_c:.0f}°C
- Calcination Temperature: {project.nanomaterial.calcination_temperature_c:.0f}°C (if applicable)
- Solvent: {project.nanomaterial.solvent_system}

### Safety Note
{project.nanomaterial.environmental_safety}

---

## 3. MEMBRANE FORMULATION

### Composition
- Polymer Matrix: {project.membrane.polymer_matrix.value}
- Nanoparticles: {project.membrane.nanoparticle_type}
- Loading: {project.membrane.nanoparticle_loading_wt_pct:.1f} wt%
- Crosslinker: {project.membrane.crosslinker}

### Procedure
1. Dissolve {project.membrane.polymer_matrix.value} in [SOLVENT]
2. Disperse nanoparticles (sonication, {project.membrane.particle_dispersion_quality} quality target)
3. Add crosslinker ({project.membrane.crosslink_density} density)
4. Cast film on [SUBSTRATE] using {project.membrane.film_casting_method}
5. Air dry [AMBIENT] or {project.membrane.drying_method}
6. Target thickness: {project.membrane.thickness_um:.0f} µm

### Quality Control
- Measure contact angle (target: {project.membrane.estimated_contact_angle_deg:.0f}°)
- Measure thickness with micrometer
- Inspect for defects, aggregation
- Test mechanical properties (tear, tensile)

---

## 4. DEVICE ASSEMBLY

### Components
Assemble cylindrical collector:
- Outer diameter: {project.device.overall_diameter_cm:.0f} cm
- Height: {project.device.total_height_cm:.0f} cm
- Cone angle: {project.device.cone_angle_deg:.0f}°
- Materials: {project.device.structural_material}

### Assembly Steps
1. Install bottom chamber (reservoir support)
2. Mount support columns ({project.device.support_columns_count} qty)
3. Insert membrane into upper chamber
4. Assemble cone structure ({project.device.cone_angle_deg}° angle)
5. Connect funnel and drainage system
6. Install outlet valve
{'7. Mount filtration stage (activated carbon)' if project.device.filtration_stage else ''}
{'7. Install thermal heating element' if project.device.thermal_mode.value != 'Passive (No Heat)' else ''}
8. Seal all joints with silicone gaskets
9. Pressure test (~1 PSI) for leaks

### Safety
- Ensure proper drainage
- Check membrane integrity before operation
- Verify material compatibility

---

## 5. OPERATION & MAINTENANCE

### Setup
- Place in well-ventilated location
- Maintain {project.conditions.relative_humidity_pct:.0f}% RH for testing
- Ambient temperature: {project.conditions.ambient_temperature_c:.0f}°C

### Daily
- Monitor reservoir water level
- Note temperature and RH
- Record collected water volume

### Weekly
- Inspect membrane for fouling
- Clean outer surfaces if needed
- Check for leaks

### Monthly
- Replace filtration cartridge (if installed)
- Deep clean with deionized water
- Replace membrane if degraded

---

## 6. DATA COLLECTION

Log for each experiment:
- Date, Time, Duration
- Temperature (°C), Relative Humidity (%)
- Water Collected (mL), Purity (if tested)
- Observations, Issues

Target Performance: {project.simulation.predicted_water_yield_l_kg_day:.3f} L/kg/day under standard conditions

---

**Document Status**: DRAFT - For R&D use only
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        return sop

    @staticmethod
    def export_all_formats(project: ProjectState) -> Dict[str, str]:
        """Generate all export formats."""
        return {
            "technical_summary": ReportGenerator.generate_technical_summary(project),
            "investor_summary": ReportGenerator.generate_investor_summary(project),
            "csv_data": ReportGenerator.generate_csv_export(project),
            "json_data": ReportGenerator.generate_json_export(project),
            "sop_draft": ReportGenerator.generate_sop_draft(project),
        }
