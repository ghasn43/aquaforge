# Atmospheric Water Harvesting Suite

## Professional R&D Tool for Green Nanomaterial-Based Water Systems

**NanoBio Studio** | **Bio Catalyst Engineering**

---

## Overview

The **Atmospheric Water Harvesting Suite** is a scientific, production-grade Streamlit application designed for research teams and engineers to **design, simulate, compare, and optimize** green nanomaterial-based atmospheric water harvesting (AWH) systems.

### Key Capabilities

- 🧬 **Materials Design**: Feedstock selection + nanomaterial synthesis pathway engineering
- 🎬 **Membrane Formulation**: Layer design, nanoparticle loading, performance estimation
- ⚙️ **Device Architecture**: Cylindrical collector configuration and geometric optimization
- 💧 **Performance Simulation**: Heuristic-based water yield prediction under various climatic conditions
- 🏆 **Benchmarking**: Comparison against MOF-801, MOF-303, and alternative systems
- 💰 **Economic Analysis**: Cost estimation and scale-up pathway assessment
- 📄 **Report Generation**: Technical, investor, and SOP documentation export

---

## Technology Stack

- **Framework**: Streamlit (interactive web UI)
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly, Altair
- **Data Models**: Pydantic dataclasses
- **Language**: Python 3.9+

---

## Installation

### 1. Clone or Download the Repository

```bash
cd d:\AquaCatalyst Designer\awh_suite
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
streamlit run main.py
```

The app will open in your default browser at `http://localhost:8501`

---

## Project Structure

```
awh_suite/
├── main.py                  # Main Streamlit application (8 tabs/modules)
├── data_models.py           # Core domain classes and enums
├── materials_logic.py       # Feedstock & synthesis heuristics
├── membrane_logic.py        # Membrane formulation engine
├── device_logic.py          # Device geometry & configuration
├── simulator_logic.py       # Performance simulation engine
├── benchmarking_logic.py    # Reference system comparisons
├── costing_logic.py         # Economic & scale-up analysis
├── reports_logic.py         # Report generation & export
├── utils.py                 # Utility functions & helpers
├── __init__.py              # Package initialization
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── assets/
    ├── presets.json        # Saved preset configurations
    └── reference_data.json  # Benchmark reference data
```

---

## Module Guide

### 📊 Tab 1: Overview

- System purpose and workflow explanation
- Current project KPI summary cards
- Available materials and technologies
- Quick links to all other modules

### 🧬 Tab 2: Feedstock-to-Nanomaterial Designer

**Design feedstock source + synthesis pathway**

- Select biomass feedstock (peanut shell, algae, rice husk, etc.)
- Choose synthesis route (green synthesis, calcination, TEOS-silica, etc.)
- Adjust synthesis parameters (temperature, time, solvent)
- Auto-estimate predicted nanomaterial properties
  - Particle size, morphology, crystallinity
  - Hydrophilicity, water adsorption relevance
  - Synthesis complexity, scalability

### 🎬 Tab 3: Membrane Composer

**Design membrane formulation + layer structure**

- Select polymer matrix (chitosan, silica-chitosan, ZnO-chitosan, etc.)
- Configure nanoparticle loading and dispersion
- Choose layer configuration (single, dual-hydro, triple)
- Set physical properties (thickness, porosity, crosslink density)
- Calculate membrane performance scores
  - Contact angle, adsorption strength, desorption ease
  - Mechanical stability, moisture capture, thermal robustness
  - Manufacturability, sustainability

### ⚙️ Tab 4: Device Configurator

**Design cylindrical atmospheric water harvester prototype**

- Configure device dimensions (diameter, height, cone angle)
- Select materials and chamber type
- Add thermal assist mode (passive, solar, heated)
- Include optional filtration stage
- Calculate chamber volumes and surface areas
- Generate Bill of Materials

### 💧 Tab 5: Atmospheric Water Harvesting Simulator

**Predict performance under specified conditions**

- Input environmental conditions (RH, temperature, airflow, solar exposure)
- Run heuristic-based simulation
- View water yield predictions (L/kg/day)
- Analyze adsorption/desorption cycle
- Generate sensitivity curves (yield vs. RH, yield vs. temperature)

### 🏆 Tab 6: Benchmarking Lab

**Compare design against reference systems**

- MOF-801, MOF-303, generic MOF
- Bio-based chitosan/ZnO/silica systems
- Fe/Zn/Si nanocomposites
- Activated carbon
- View radar charts, comparison tables, rankings

### 💰 Tab 7: Scale-Up & Cost Analysis

**Economic assessment and commercialization pathway**

- Input material costs (feedstock, polymer, nanoparticles, device)
- Adjust labor and testing multipliers
- Select scale level (Lab, Pilot, Pre-commercial)
- View cost breakdown and scaling path
- Commercial readiness assessment (TRL, scientific/fabrication/field readiness)

### 📄 Tab 8: Reports & Export

**Generate and download project documentation**

- Technical summary (full design specification)
- Investor summary (executive-friendly overview)
- SOP draft (Standard Operating Procedure template)
- Export formats:
  - CSV (spreadsheet import)
  - JSON (save/load project state)
  - TXT (readable reports)
- Design validation and R&D recommendations

---

## Core Concepts

### Heuristic-Based Estimation

All calculations use **rule-based heuristics** informed by literature data:

- **Feedstock Properties**: Carbon content, silica potential, sustainability profiles
- **Synthesis Routes**: Particle size ranges, hydrophilicity, complexity factors
- **Membrane Performance**: Adsorption/desorption based on formulation chemistry
- **Device Efficiency**: Geometric factors, thermal cycling, collection losses
- **Water Yield**: Adsorption capacity × desorption efficiency × environmental factors

### Design-Stage vs. Certified Performance

⚠️ **Important**: This tool generates **design-stage estimates** for R&D guidance ONLY.

- **NOT** a certified engineering analysis
- **NOT** a guarantee of actual performance
- **Requires** bench-scale experimental validation

### Sustainability & Green Materials

The system prioritizes:
- Agro-waste feedstocks (renewable, low-cost)
- Green synthesis routes (aqueous, low-toxicity)
- Biodegradable polymers (chitosan)
- Non-toxic nanoparticles (silica, ZnO, iron/zinc oxides)
- Scalable manufacturing processes

---

## Data Models

All design parameters are encapsulated in structured dataclasses:

```python
# Core domain classes
FeedstockProfile           # Biomass source + properties
NanomaterialProfile        # Predicted synthesis output
MembraneFormulation        # Polymer + nanoparticles
DeviceConfiguration        # Device geometry + components
AtmosphericConditions      # Environmental parameters
SimulationResult           # Performance predictions
CostModel                  # Economic parameters
ProjectState               # Complete project snapshot
```

---

## Presets & Quick-Start

The app includes 5 pre-configured presets:

1. **Chitosan/Silica/ZnO**: Classic green nanocomposite
2. **Fe/Zn/Si Composite**: Multi-element oxide system
3. **Dual-Layer Design**: Hydrophilic/hydrophobic optimization
4. **Passive Collector**: Pure passive operation
5. **Solar-Assisted**: Thermal-enhanced system

Load via: Sidebar → "Load Preset"

---

## Key Calculations

### Water Yield Estimation

```
Yield = Adsorption_Score × Desorption_Efficiency × Device_Area
        × Environmental_Factor × Duty_Cycle × Collection_Efficiency
```

Where:
- Adsorption_Score = f(membrane hydrophilicity, RH, temperature)
- Desorption_Efficiency = f(thermal mode, crosslink density)
- Device_Area = calculated from geometry
- Environmental_Factor = f(RH, airflow, thermal cycling)
- Collection_Efficiency = 0.85 (system losses)

### Sustainability Score

```
Sustainability = 0.4×Feedstock_Green + 0.5×Membrane_Green + 0.1×Device_Impact
```

### Manufacturing Complexity

```
Complexity = Device_Class_Base + Layer_Config_Penalty + Thermal_Penalty
             + Size_Factor + Component_Count
```

---

## Usage Workflow

### Typical Design Session

1. **Start** → Overview tab (understand system)
2. **Design** → Tab 2: Choose feedstock + synthesis route
3. **Formulate** → Tab 3: Design membrane composition
4. **Build** → Tab 4: Configure device architecture
5. **Simulate** → Tab 5: Predict performance
6. **Benchmark** → Tab 6: Compare vs. reference systems
7. **Analyze** → Tab 7: Assess costs and scale-up
8. **Export** → Tab 8: Generate reports and save project

### Iterative Optimization

- Adjust parameters in any tab
- Click "Calculate" or "Run Simulation"
- View updated results
- Export intermediate versions
- Compare design variants via CSV export

---

## Extending the Module

### Adding Custom Feedstocks

Edit `materials_logic.py`:

```python
FEEDSTOCK_PROPERTIES = {
    FeedstockType.MY_FEEDSTOCK: {
        "carbon_content_pct": 45.0,
        "silica_potential": 0.75,
        "cellulose_pct": 28.0,
        "sustainability_multiplier": 0.85,
        "cost_baseline": 2.5,
    },
}
```

### Adding Benchmark Systems

Edit `benchmarking_logic.py`:

```python
REFERENCE_BENCHMARKS = {
    "My Benchmark": BenchmarkProfile(
        name="My Benchmark",
        material_system="Description",
        estimated_water_yield=0.45,
        # ... more fields
    ),
}
```

### Custom Heuristics

Modify calculation functions in individual logic modules to refine accuracy based on experimental validation.

---

## Limitations & Assumptions

### Design-Stage Tool Limitations

- **No experimental validation**: Uses literature heuristics
- **Simplified geometry**: Cylindrical approximations
- **Idealized adsorption**: Assumes Langmuir-type kinetics
- **Static conditions**: Single-point environmental scenarios
- **No fouling/degradation**: Assumes clean operation
- **Passive systems focus**: Limited active HVAC modeling

### Key Assumptions

- Membrane remains intact over design life
- Nanoparticles well-dispersed and stable
- No phase separation or aggregation
- Collection efficiency ~85% (gravity-driven)
- Filtration efficiency ~95% (if enabled)
- Linear scaling relationships

---

## Scientific References

The tool incorporates principles from:

- Green synthesis of silica, ZnO, iron oxides
- Chitosan-based membrane adsorption science
- Atmospheric water harvesting literature (MOF, sorbent materials)
- Adsorption kinetics and thermodynamics
- Device engineering for passive cooling/condensation

**Recommended Reading**:
- Metal-organic frameworks for AWH (Kalmutzki et al., 2021)
- Biosorption and chitosan applications (Kumar et al., 2020)
- Atmospheric water harvesting overview (Ghosh et al., 2022)

---

## Troubleshooting

### App Won't Start

```bash
# Check Python version
python --version  # Should be 3.9+

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Clear Streamlit cache
streamlit cache clear
```

### Calculations Give Strange Results

- Check membrane mechanical stability < 0.5 (instability flags)
- Verify nanoparticle loading < 25% (overloading penalty)
- Ensure RH is 30-80% (optimal range)
- Confirm device diameter > 15 cm (collection area constraint)

### Performance Too Low

- Increase nanoparticle loading (up to 15%)
- Use hydrophilic membranes (chitosan + silica)
- Enable thermal assist for desorption
- Increase device surface area (larger diameter/height)
- Simulate at higher RH (60-80%)

---

## Citation & Attribution

**Atmospheric Water Harvesting Suite**
- Developed for NanoBio Studio
- Bio Catalyst Engineering
- 2026

If using this tool in research, please cite as:

```
"Atmospheric Water Harvesting Suite" (2026). 
NanoBio Studio - Bio Catalyst Engineering.
https://[repository]
```

---

## License

[Specify your license - MIT, Apache 2.0, etc.]

---

## Support & Contributions

For issues, feature requests, or contributions:

1. Document the issue clearly
2. Include reproduction steps
3. Provide screenshot/terminal output
4. Reference relevant module/tab

Contributions welcome! Areas for enhancement:

- [ ] Multi-point environmental scenarios (hourly profiles)
- [ ] Experimental data import & validation
- [ ] Machine learning calibration
- [ ] Device 3D visualization
- [ ] Cost sensitivity analysis
- [ ] Supply chain modeling
- [ ] Patent landscape mapping

---

## Future Roadmap

### Version 1.1
- [ ] Enhanced device visualization (3D renderings)
- [ ] Bulk material property database
- [ ] Experimental data integration module

### Version 2.0
- [ ] Machine learning performance predictor
- [ ] Multi-scenario optimization
- [ ] IP prior art analyzer
- [ ] Pilot plant economic models

### Version 3.0
- [ ] Cloud-based collaboration
- [ ] IoT sensor integration
- [ ] Real-time field performance tracking
- [ ] Automatic report generation for investors/regulators

---

## Contact

**NanoBio Studio**  
Bio Catalyst Engineering  
2026

*Advancing sustainable nanomaterials for critical challenges*

---

**Last Updated**: April 25, 2026  
**Status**: Production Ready (v1.0.0)
