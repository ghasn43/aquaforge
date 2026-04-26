"""
Help & Documentation Content for AquaForge
Comprehensive user guide, FAQ, glossary, and troubleshooting
"""

BRAND_NAME = "AquaForge"
BRAND_TAGLINE = "Engineer Water from Air"
BRAND_DESCRIPTION = "AquaForge is a professional R&D decision-support tool for designing green nanomaterial-based atmospheric water harvesting systems."

# ============================================================================
# HELP PAGE SECTIONS
# ============================================================================

GETTING_STARTED = """
## 🚀 Getting Started with AquaForge

### What is AquaForge?
AquaForge is an **investor-grade, research-grade R&D decision-support platform** that enables engineers, 
scientists, and entrepreneurs to design, simulate, compare, and optimize green nanomaterial-based 
atmospheric water harvesting (AWH) systems.

### The 5-Minute Quick Start

**Step 1: Load a Preset (Optional)**
- Click "📋 Load Preset" in the sidebar to start with a proven design template
- Options include: Chitosan/Silica/ZnO, Fe/Zn/Si Composite, Dual-Layer Design, Passive Collector, Solar-Assisted

**Step 2: Design Your Materials** (Tab 2)
- Select a **biomass feedstock** (peanut shell, banana peel, algae, etc.)
- Choose a **synthesis route** (green synthesis, calcination, TEOS-based, etc.)
- Adjust **synthesis parameters** (temperature, reaction time, solvent)
- View **predicted nanomaterial properties** instantly

**Step 3: Formulate Your Membrane** (Tab 3)
- Select a **polymer matrix** (chitosan, modified chitosan, silica-enhanced, etc.)
- Set **nanoparticle loading** (0-30%)
- Choose **layer configuration** (single, dual, triple layer)
- View **performance scores** for adsorption, desorption, mechanical stability

**Step 4: Design Your Device** (Tab 4)
- Specify **collector geometry** (diameter, height, cone angle)
- Choose **device class** (bench, pilot, field demonstrator)
- Set **thermal mode** (passive, low-heat, solar, lab-assisted)
- View **calculated surface areas and component lists**

**Step 5: Run Performance Simulation** (Tab 5)
- Input **atmospheric conditions** (humidity, temperature, airflow)
- Click "🎯 Run Simulation" to predict **water yield** and performance
- View **performance curves** (RH sensitivity, temperature sensitivity, cycle profile)

**Step 6: Compare Against Reference Systems** (Tab 6)
- Select industry **benchmarks** (MOF-801, MOF-303, bio-based systems)
- View **comparison tables and radar charts**
- Analyze your design's **competitive position**

**Step 7: Analyze Economics** (Tab 7)
- View **cost breakdown** (per membrane, per prototype, per liter)
- Analyze **scale-up pathways** (Lab → Pilot → Pre-commercial)
- Assess **commercial readiness** (TRL levels)

**Step 8: Generate Reports** (Tab 8)
- Create **Technical Summary** for R&D teams
- Create **Investor Summary** for stakeholder communication
- Export as **CSV or JSON** for further analysis
- Generate **Standard Operating Procedure** draft for manufacturing
"""

# ============================================================================
# FAQ SECTION
# ============================================================================

FAQ = """
## ❓ Frequently Asked Questions

### General Questions

**Q: Is AquaForge a real engineering design tool?**
A: AquaForge provides design-stage **heuristic estimates** based on materials science literature and synthesis data. 
It's intended for R&D guidance and bench-scale experiment planning, NOT as a certified engineering design tool. 
Always validate results experimentally before moving to production.

**Q: What does "heuristic" mean?**
A: Heuristic calculations are rule-based estimates derived from scientific principles and empirical data. 
They're fast, transparent, and explainable—ideal for early-stage R&D decision-making.

**Q: Can I modify the preset projects?**
A: Yes! All sliders and parameters are fully adjustable. Change any value and the app recalculates instantly. 
Use "🔄 Reset to Default" to return to the original state.

**Q: How do I save my design?**
A: Click "📥 Save Project" to download your complete design as JSON. Later, click "📤 Load JSON" to reload it.

---

### Materials & Synthesis

**Q: What feedstocks are available?**
A: AquaForge includes 8 green biomass options:
- Peanut Shell, Banana Peel, Phoenix Dactylifera (date palm), Algae
- Fungal Biomass, Rice Husk, Coconut Shell, Wood Waste

Each has pre-loaded properties (carbon content, sustainability score, availability, cost).

**Q: What synthesis routes are supported?**
A: 7 routes are available:
1. Green Synthesis (aqueous, low-temp)
2. Calcination (thermal decomposition)
3. TEOS-based Silica (sol-gel)
4. Gel-based Synthesis (hydrogel precursor)
5. ZnO Green Routes (biomass-assisted)
6. Fe/Zn/Si Nanocomposites (multi-element oxides)
7. Advanced Hydrothermal (high-pressure aqueous)

**Q: How are nanomaterial properties estimated?**
A: The app combines:
- Feedstock chemistry (carbon, silica potential)
- Synthesis route characteristics (particle size range, crystallinity typical values)
- Input parameters (temperature, time, solvent)
→ Produces predicted: particle size, crystallinity, hydrophilicity, water adsorption relevance, cost

**Q: What does "hydrophilicity" mean?**
A: Hydrophilicity is the degree to which a material attracts water. Higher hydrophilicity = better water adsorption. 
The app estimates contact angle (lower angle = more hydrophilic).

---

### Membrane Design

**Q: What polymer matrices are available?**
A: 5 options with different properties:
- **Pure Chitosan**: Biodegradable, moderate hydrophilicity, cost-effective
- **Modified Chitosan**: Enhanced mechanical strength, tunable hydrophilicity
- **Silica-Enhanced Chitosan**: Higher porosity, better scalability
- **ZnO/Chitosan**: Nanocomposite, antimicrobial
- **Fe/Zn/Si/Chitosan**: Multi-element oxide composite, advanced performance

**Q: What's nanoparticle loading?**
A: The percentage by weight of nanoparticles (silica, ZnO, etc.) mixed into the polymer matrix.
- Low loading (0-5%): Better mechanical strength, lower adsorption
- Optimal loading (10-15%): Best balance of adsorption and stability
- High loading (20-30%): Maximum adsorption but risk of agglomeration and brittleness

**Q: What's a "layer configuration"?**
A: Multi-layer membranes have different functions:
- **Single Layer**: Simple, uniform adsorption
- **Dual-Layer Hydrophobic Top**: Top layer rejects water initially, drives desorption
- **Dual-Layer Hydrophilic Top**: Top layer attracts water rapidly
- **Triple Layer**: Advanced separation with selective adsorption/desorption

**Q: How is "adsorption strength" calculated?**
A: Combines:
- Polymer base hydrophilicity
- Nanoparticle type and loading (% contribution)
- Porosity (layer configuration effect)
- Quality of particle dispersion
→ Result: 0-1 score (higher = stronger adsorption)

---

### Device Design

**Q: What's the cylindrical collector geometry?**
A: AquaForge models a **passive adsorption-desorption-condensation device** with:
- **Upper chamber**: Primary adsorption zone (high surface area)
- **Cone frustum**: Passive cooling and condensation zone (thermally isolated)
- **Lower chamber**: Water collection and filtration zone
- **Support columns**: Structural frame and optional insulation

**Q: How is water yield predicted?**
A: A multi-stage heuristic model:
1. **Adsorption Stage**: RH% × Membrane Adsorption Strength × Temperature Factor → Adsorbed water amount
2. **Desorption Stage**: Solar/thermal input × Membrane desorption ease → Released water
3. **Condensation Stage**: Cooled surface area × Air humidity × Temperature gradient → Condensed water
4. **Collection Stage**: Gravity + filtration efficiency → Clean water output
5. Result: **0.1 - 0.6 L/kg/day** typical range

**Q: What's TRL (Technology Readiness Level)?**
A: A scale from 1-9 measuring development stage:
- TRL 1-2: Scientific research, conceptual
- TRL 3-4: Proof-of-concept, early prototypes
- TRL 5-6: Pilot scale, field testing
- TRL 7-8: Pre-commercial demonstration
- TRL 9: Commercial deployment

AquaForge estimates TRL based on your design maturity.

---

### Benchmarking

**Q: What reference systems are included?**
A: 6 benchmarks covering state-of-the-art AWH technology:
- **MOF-801**: Metal-organic framework (0.48 L/kg/day yield)
- **MOF-303**: Advanced MOF variant (0.52 L/kg/day yield)
- **Generic MOF**: Averaged MOF performance (0.45 L/kg/day yield)
- **Bio-based Chitosan/ZnO/Silica**: Green alternative (0.38 L/kg/day yield, 88% sustainability)
- **Fe/Zn/Si Nanocomposite**: Multi-element oxide (0.42 L/kg/day yield, 82% sustainability)
- **Activated Carbon**: Traditional sorbent (0.35 L/kg/day yield, 85% sustainability)

**Q: How is the "sustainability score" calculated?**
A: Combines:
- Material sourcing impact (renewable vs. synthetic)
- Synthesis energy requirements (green routes score higher)
- End-of-life recyclability
→ 0-1 scale (1 = most sustainable)

**Q: What's the radar chart showing?**
A: Multi-dimensional comparison of your design vs. reference systems across 5 axes:
- **Sustainability**: Green material and process footprint
- **Cost Efficiency**: $/L harvested ratio
- **Scalability**: Manufacturability at scale
- **Passive Suitability**: Performance without active heating
- **Synthesis Simplicity**: Route complexity (lower = simpler)

---

### Economic Analysis

**Q: What's the difference between CAPEX and OPEX?**
A: 
- **CAPEX** (Capital Expenditure): One-time setup costs (equipment, facility, initial batch)
- **OPEX** (Operational Expenditure): Recurring costs per batch (materials, labor, testing)

**Q: How does scale-up affect cost?**
A: As you move from Lab → Pilot → Pre-commercial:
- **Batch size multiplier**: Larger batches reduce per-unit material cost
- **Labor multiplier**: Automation reduces labor cost per unit
- **Testing multiplier**: % QC testing decreases with scale
→ Total: Cost per membrane typically drops 40-60% from Lab to Pre-commercial

**Q: What's the "commercial readiness snapshot"?**
A: AquaForge assesses 4 TRL dimensions:
- **Scientific Readiness**: Materials and synthesis proven?
- **Fabrication Readiness**: Can we make it reliably?
- **Supply-Chain Readiness**: Are materials available?
- **Field-Readiness**: Does it work in real conditions?

Each rated TRL 1-9.

**Q: How do I interpret "cost per liter harvested"?**
A: This is the **equipment cost amortized over lifetime water production**:
- $1-2/L: Competitive with alternative AWH systems
- $2-5/L: Early-stage, needs optimization
- $5+/L: Preliminary, significant work needed

Actual operating costs (water, energy, labor) are separate.

---

### Technical Terminology

**Q: What's a "drying temperature"?**
A: The temperature at which wet nanomaterial precursor is dried to remove solvent. 
Typical: 50-200°C depending on synthesis route.

**Q: What's "calcination temperature"?**
A: The high temperature (200-600°C) at which organic precursor is converted to inorganic oxide. 
Higher temp = higher crystallinity but more energy.

**Q: What's "reaction time"?**
A: Duration of chemical synthesis reaction. Longer reaction = more complete conversion, 
but higher cost and complexity.

**Q: What's "solvent system"?**
A: The liquid medium in which synthesis occurs. Water-based = greener, cheaper, safer. 
Organic = higher performance, more hazardous.

**Q: What's "RH%" (Relative Humidity)?**
A: Percentage of moisture saturation in air. 
- 20% RH: Dry conditions, low water availability
- 60% RH: Moderate conditions, typical indoor air
- 90% RH: Very humid, near condensation
- 100% RH: Saturated, active condensation

---

### Reporting & Export

**Q: What's a "Technical Summary"?**
A: A 10-section comprehensive report for R&D teams including:
- Project overview, material specifications, membrane properties, device design, 
atmospheric conditions, predicted performance, cost analysis, recommendations, notes, disclaimer

**Q: What's an "Investor Summary"?**
A: A concise 5-section report for stakeholders highlighting:
- Executive summary, key features, performance table, development stage, competitive advantages, investment requirements

**Q: What's an "SOP Draft"?**
A: Standard Operating Procedure—a draft manufacturing instruction set covering:
- Feedstock preparation, nanomaterial synthesis, membrane formulation, device assembly, operation/maintenance, data collection

**Q: What format should I export for further analysis?**
A: 
- **CSV**: For spreadsheet import (Excel, Sheets), data table format
- **JSON**: For programmatic import, preserves all structure and nesting
- Both contain complete project state and calculated parameters

---

### Troubleshooting

**Q: The app is loading slowly**
A: Streamlit runs locally and recalculates on every interaction. If you have many parameter changes:
- Try reducing the number of simultaneous adjustments
- Refresh the browser (F5)
- Restart the Streamlit server

**Q: A calculation seems wrong**
A: Check:
1. Input parameter ranges (are sliders at reasonable values?)
2. The "Heuristic Predictions" disclaimer (calculations are estimates)
3. Use the "Project Validation" section (Tab 8) to identify design inconsistencies
4. Compare against benchmarks to sanity-check your results

**Q: I can't load my saved JSON project**
A: Ensure:
1. The JSON file is valid (not corrupted)
2. You're using the same version of AquaForge (older versions may have incompatible schemas)
3. Check the browser console for error messages (F12 → Console)

**Q: The radar chart isn't displaying**
A: This is a Plotly rendering issue. Try:
1. Refresh the page (Ctrl+R or Cmd+R)
2. Clear browser cache and restart
3. Try a different browser (Chrome, Firefox, Edge)

---

### Advanced Tips

**Q: How can I explore design sensitivity?**
A: Use the sliders to systematically vary one parameter while holding others fixed:
1. Start with drying temperature: keep others constant, vary drying temp 50-200°C
2. Observe how predicted nanomaterial properties change
3. Repeat for nanoparticle loading, membrane thickness, device diameter
4. Identify which parameters have the biggest impact on final water yield

**Q: How do I optimize for sustainability?**
A: Target designs with high sustainability scores:
1. Choose green feedstocks (algae, agricultural waste) over synthetic precursors
2. Select calcination or TEOS synthesis routes (simpler, greener)
3. Use water-based solvents
4. Minimize nanoparticle loading (load efficient, not load heavy)
5. Check "Sustainability Assessment" in Reports tab

**Q: How do I optimize for cost?**
A: Target designs with low cost-per-liter:
1. Use low-cost feedstocks (peanut shell, rice husk, coconut shell)
2. Select simple synthesis routes (green synthesis, not advanced hydrothermal)
3. Minimize lab-scale overheads (CAPEX)
4. Plan for scale-up (pilot/pre-commercial designs reduce per-unit cost)
5. Reduce device complexity (passive > solar-assisted > lab-assisted)

**Q: How do I balance performance vs. sustainability?**
A: Use the radar chart to visualize tradeoffs:
- Top-performing designs often use MOFs (synthetic, lower sustainability)
- Bio-based designs sacrifice yield (~5-10%) for massive sustainability gain
- Your design should optimize YOUR priorities (performance, cost, sustainability, manufacturability)

**Q: Can I use AquaForge for grant proposals?**
A: Yes! The app generates professional reports suitable for:
- NSF/DOE grant applications (Technical Summary)
- Venture capital pitches (Investor Summary)
- Manufacturing partnerships (SOP Draft, cost analysis)
- Academic publications (reference the heuristic model)

Cite: "AquaForge v1.0 | Heuristic-based R&D decision-support tool for AWH system design"
"""

# ============================================================================
# MODULE DESCRIPTIONS
# ============================================================================

MODULES_GUIDE = """
## 📚 AquaForge Module Guide

### Tab 1: 📊 Overview
**Purpose**: Project dashboard and quick reference
**Key Information**:
- Purpose statement and workflow diagram
- Current project KPIs (quick status)
- Available green materials (8 biomass, 7 synthesis routes)
- Core technologies (polymer matrices, layer configs, nanoparticles)
- Performance science fundamentals (mechanisms, typical ranges)
- About this module, disclaimers, next steps

**Use When**: You need a quick reference or are new to the tool

---

### Tab 2: 🧬 Feedstock-to-Nanomaterial Designer
**Purpose**: Design nanomaterial synthesis pathway
**Key Steps**:
1. Select biomass feedstock (8 options)
2. Choose synthesis route (7 options)
3. Adjust synthesis parameters (temperature, time, solvent)
4. Customize feedstock cost
5. Click "🔬 Estimate Nanomaterial Properties" button

**Outputs**: Predicted nanomaterial KPIs
- Particle size (nm range)
- Crystallinity (%)
- Hydrophilicity (low/moderate/high)
- Adsorption value (0-1 score)
- Morphology, complexity, scalability, cost/kg

**Heuristic Model**: Based on literature values for each feedstock + synthesis route combination, 
adjusted by your input parameters (temperature, time, etc.)

**Use For**: Exploring how feedstock and synthesis route affect nanomaterial properties

---

### Tab 3: 🎬 Membrane Composer
**Purpose**: Design membrane formulation with nanoparticles
**Key Steps**:
1. Select polymer matrix (5 options)
2. Choose primary nanoparticle type (silica, ZnO, multi-element oxide)
3. Set nanoparticle loading (%)
4. Select layer configuration (single, dual, triple)
5. Optionally add crosslinking and porosity adjustments
6. Click "📊 Calculate Membrane Properties" button

**Outputs**: Membrane performance scores
- Contact angle (hydrophilicity measure)
- Adsorption strength (0-1)
- Desorption ease (0-1)
- Mechanical stability (0-1)
- Manufacturability (0-1)
- Sustainability (0-1)
- Risk flags (design warnings)

**Heuristic Model**: Each score combines polymer baseline + nanoparticle loading effect + layer configuration effect

**Use For**: Optimizing membrane for your specific needs (high adsorption vs. easy desorption vs. mechanical strength)

---

### Tab 4: ⚙️ Device Configurator
**Purpose**: Design cylindrical collector device geometry
**Key Steps**:
1. Set device diameter (cm) → affects surface area
2. Set device height (cm) → affects upper chamber volume
3. Set cone angle (degrees) → affects frustum volume and passive cooling
4. Select device class (bench/pilot/field demonstrator)
5. Choose thermal mode (passive/low-heat/solar/lab-assisted)
6. Optional: Select filtration type, material selection, insulation
7. Click "🔧 Configure Device" button

**Outputs**: Device specifications
- Chamber volumes (cm³)
- Total surface area (cm²)
- Bill of materials (components, quantities)
- Manufacturability score
- Maintenance complexity
- Component list with specifications

**Heuristic Model**: Geometric calculations (cylinder volume, cone frustum volume, lateral surface areas) 
combined with engineering heuristics for complexity and feasibility

**Use For**: Designing the physical collector and understanding geometric constraints

---

### Tab 5: 💧 AWH Simulator
**Purpose**: Predict water harvesting performance under atmospheric conditions
**Key Steps**:
1. Input atmospheric conditions:
   - Relative humidity (20-100%)
   - Temperature (10-40°C)
   - Airflow (passive/low/medium/high)
   - Solar exposure (none/partial/full)
2. Click "🎯 Run Simulation" button
3. View predicted water yield, performance window, confidence level

**Outputs**: Simulation results
- Predicted water yield (L/kg/day and mL/g)
- Performance window (limited/moderate/strong/excellent)
- Confidence level (low/medium/high)
- Stage contributions (% from adsorption, desorption, condensation, collection, filtration)
- Sensitivity curves:
  - Water yield vs. RH (20-100%)
  - Water yield vs. temperature (10-40°C)
  - Adsorption-desorption cycle (30-minute profile)

**Heuristic Model**: Multi-stage calculation combining membrane properties, device geometry, and atmospheric conditions

**Use For**: Understanding performance under different environmental scenarios

---

### Tab 6: 🏆 Benchmarking Lab
**Purpose**: Compare your design against industry-leading reference systems
**Key Steps**:
1. Select one or more reference benchmarks (MOF-801, MOF-303, bio-based, composites, activated carbon)
2. View comparison table with all metrics
3. View radar charts (your design vs. reference system)
4. View ranking by water yield or other metrics

**Outputs**: Benchmark comparison
- Comparison table (rows = systems, columns = metrics)
- Radar charts showing 5-axis comparison
- Rankings by yield, sustainability, cost, scalability
- CSV export for further analysis

**Use For**: Understanding your competitive position and identifying improvement areas

---

### Tab 7: 💰 Scale-Up & Cost Analysis
**Purpose**: Economic analysis and commercialization pathway
**Key Steps**:
1. Set material costs (feedstock, polymer, nanoparticles $/kg)
2. Set device fabrication cost ($)
3. Set batch size (units)
4. Select scale level (lab/pilot/pre-commercial)
5. Adjust labor and testing multipliers
6. Set number of prototypes
7. Click "💻 Calculate Costs & Scale-Up" button

**Outputs**: Cost analysis
- Cost per membrane ($)
- Prototype cost total ($)
- Cost per liter harvested ($)
- CAPEX and OPEX breakdown
- Commercial readiness snapshot (4 TRL dimensions)
- Scale-up cost pathway (Lab → Pilot → Pre-commercial)
- Sustainability-adjusted cost score

**Heuristic Model**: Material costs + labor + testing + device overhead, adjusted by scale level multipliers

**Use For**: Understanding economics and planning commercialization timeline

---

### Tab 8: 📄 Reports & Export
**Purpose**: Generate professional reports and export project
**Key Features**:
1. Generate Technical Summary (for R&D teams)
2. Generate Investor Summary (for stakeholders)
3. Generate SOP Draft (for manufacturing)
4. Download CSV (for spreadsheet analysis)
5. Download JSON (for programmatic import)
6. Project validation (design check)
7. R&D recommendations (next experiment suggestions)
8. Sustainability assessment (green score)

**Outputs**: Multi-format reports
- Markdown text (Technical, Investor, SOP summaries)
- CSV table (flat format, all parameters)
- JSON (complete project state)
- Validation warnings
- Recommendations and sustainability badge

**Use For**: Communicating results, saving work, and planning next steps
"""

# ============================================================================
# GLOSSARY
# ============================================================================

GLOSSARY = """
## 📖 Glossary of Terms

**Adsorption**: Physical or chemical process where gas or liquid molecules accumulate on a solid surface. 
In AWH, water vapor adsorbs onto the membrane when RH is high.

**Atmospheric Water Harvesting (AWH)**: Technology to extract drinking water directly from air moisture. 
Typically uses adsorbent materials that capture water at high RH and release it when heated.

**Biomass Feedstock**: Renewable organic material (agricultural waste, plant residue) used as starting material 
for nanomaterial synthesis. Examples: peanut shell, banana peel, rice husk.

**Calcination**: High-temperature heating (200-600°C) to decompose organic precursor into inorganic ceramic oxide. 
Used in nanomaterial synthesis to create crystalline particles.

**CAPEX**: Capital Expenditure—one-time setup costs for equipment, facility, initial inventory.

**Chitosan**: Biopolymer derived from chitin (shellfish, fungal cell walls). Used as polymer matrix in membranes 
due to biodegradability and tunable hydrophilicity.

**Condensation**: Process where water vapor cools and converts to liquid water. In AWH, occurs on cold collector surfaces.

**Contact Angle**: Measure of liquid-surface interaction. Lower angle = more hydrophilic (water-loving). 
Typical: <90° hydrophilic, >90° hydrophobic.

**Crystallinity**: Percentage of ordered crystal structure vs. amorphous. Higher crystallinity often = better mechanical strength, 
but may reduce porosity.

**Desorption**: Process of releasing adsorbed molecules from a surface, typically by heating. 
In AWH, heating the membrane releases captured water.

**Device Class**: Size/stage of prototype: Bench (100s cm³, lab scale), Pilot (liter scale, field testing), 
Field Demonstrator (1000+ liter, operational).

**Feedstock**: Starting material for synthesis. In AquaForge context: biomass sources like peanut shell, algae, etc.

**Heuristic**: Rule-based estimation approach using transparent logic and empirical data. 
Not machine learning (ML), but deterministic and explainable.

**Hydrophilicity**: Degree to which a surface attracts water. High hydrophilicity = good water adsorption. 
Opposite: hydrophobicity (water-repelling).

**Hydrothermal**: Synthesis in high-temperature, high-pressure aqueous environment. 
"Hydrothermal" = water + high temperature.

**Membrane**: Engineered polymer film (with or without nanoparticles) used as adsorbent in AWH. 
Can be single or multi-layer.

**Metal-Organic Framework (MOF)**: Crystalline material with metal ions connected by organic linkers. 
High surface area, excellent water adsorption. Examples: MOF-801, MOF-303. Typically synthetic (lower sustainability).

**Nanoparticle**: Particle between 1-100 nanometers (nm). Examples in AquaForge: silica (SiO₂), zinc oxide (ZnO).

**OPEX**: Operational Expenditure—recurring costs per batch (materials, labor, testing, energy).

**Polymer Matrix**: Base polymer material that forms the membrane structure. Examples: chitosan, cellulose, polyurethane.

**Porosity**: Percentage of void space (pores) in a material. Higher porosity = more surface area for adsorption, 
but may reduce mechanical strength.

**Relative Humidity (RH)**: Percentage of moisture saturation in air compared to saturation point at that temperature. 
100% RH = saturated (dew point).

**Scalability**: Feasibility of producing material at larger scale (from lab to pilot to commercial). 
Higher score = easier to scale up.

**Sol-Gel Synthesis**: Wet chemistry method starting with liquid precursor (sol), forming solid gel, then drying/calcining. 
Used for silica and some oxide nanomaterials.

**Solvent System**: Liquid medium in which synthesis occurs. "Water-based" = aqueous, environmentally friendly. 
"Organic" = non-aqueous, higher performance but more hazardous.

**Sustainability**: Measure of environmental impact considering renewable sourcing, energy efficiency, 
end-of-life recyclability, and toxicity. Higher = greener.

**Synthesis Route**: Chemical pathway to create nanomaterial. Examples in AquaForge: Green Synthesis, 
Calcination, TEOS-based Silica, Hydrothermal, etc.

**Thermal Mode**: Energy source for desorption: Passive (no heat, relies on cooling for condensation), 
Low-Heat (ambient + small heater), Solar (solar thermal collector), Lab-Assisted (controlled lab heating).

**Technology Readiness Level (TRL)**: Scale 1-9 measuring maturity:
- 1-2: Concept stage
- 3-4: Proof-of-concept
- 5-6: Pilot scale
- 7-8: Pre-commercial
- 9: Commercial deployment

**Water Yield**: Amount of clean water produced per unit mass of adsorbent per day. 
Typical: 0.1-0.6 L/kg/day. Also expressed as mL/g.

**Zeolite**: Microporous aluminosilicate mineral used in adsorption applications. 
Less common in modern AWH compared to MOFs and bio-based materials.
"""

# ============================================================================
# TIPS & TRICKS
# ============================================================================

TIPS_AND_TRICKS = """
## 💡 Tips & Tricks for Advanced Use

### Design Optimization Strategy

**1. Start with Presets**
- Load a preset project from the sidebar
- Examine the parameter values
- Understand why those choices were made
- Use as a starting point for your variations

**2. One-at-a-Time Parameter Exploration**
- Fix all parameters except one
- Vary that one parameter across its range
- Observe how outputs change
- This reveals sensitivity and dominant factors
- Example: Keep all constant, vary nanoparticle loading 0-30%, observe yield

**3. Constraint Identification**
- Look for parameters where output plateaus (diminishing returns)
- Example: Above 15% loading, adsorption doesn't improve much (dispersion limitation)
- These reveal physical limits of your design

**4. Multi-Objective Optimization**
- Your design must balance multiple objectives:
  - Performance (high yield)
  - Sustainability (green materials)
  - Cost (low $/L)
  - Manufacturability (simple process)
- Use the Benchmarking tab radar chart to see tradeoff space
- No single design dominates all metrics; choose your priority

---

### Material Selection Deep Dive

**Green Feedstocks Ranked by Sustainability**:
1. **Algae**: Renewable, fast-growing, high nitrogen content, excellent sustainability → TRY THIS FIRST
2. **Agricultural Waste** (peanut shell, banana peel, rice husk): Free/cheap, already available, high sustainability
3. **Fungal Biomass**: Emerging option, compostable, moderate sustainability
4. **Coconut Shell**: Hard, abundant, good sustainability
5. **Wood Waste**: Common but less targeted sustainability score

**Synthesis Routes Ranked by Green-ness**:
1. **Green Synthesis**: Aqueous, room-temp or low-heat, no solvents or water-based only → GREENEST
2. **TEOS-based Silica (Sol-Gel)**: Aqueous hydrolysis, moderate energy → GOOD
3. **ZnO Green Routes**: Biomass-assisted precipitation, aqueous → GOOD
4. **Calcination**: Requires heating (200-600°C), but simple → MODERATE
5. **Gel-based Synthesis**: Aqueous, moderate energy → MODERATE
6. **Fe/Zn/Si Nanocomposites**: Multi-step, higher energy → LESS GREEN
7. **Advanced Hydrothermal**: High-pressure equipment, energy-intensive → LEAST GREEN

**Performance-Oriented Selections**:
- Aim for particle size 50-100 nm (good balance of surface area vs. diffusion)
- Maximize crystallinity (75%+ preferred) for mechanical stability
- Ensure hydrophilicity is "high" for strong adsorption
- Choose dual or triple-layer configuration for better desorption

**Cost-Optimized Selections**:
- Use low-cost feedstocks ($2-3/kg)
- Choose simple synthesis routes (green synthesis, calcination)
- Minimize nanoparticle loading (just enough for performance gain, ~10-12%)
- Use single-layer membrane (simplest to manufacture)
- Select bench prototype (smallest device complexity)

---

### Membrane Design Tricks

**Maximizing Adsorption Strength**:
1. Select high-hydrophilicity polymer (Modified Chitosan > Pure Chitosan)
2. Add silica or ZnO nanoparticles (optimal 12-15% loading)
3. Use dual or triple-layer configuration (increases effective surface area)
4. Lower crosslink density (more porous, but weaker)

**Balancing Adsorption vs. Desorption**:
- High adsorption = hard desorption (they're inversely related)
- Solution: Use multi-layer with hydrophobic bottom (blocks desorption) + hydrophilic top (strong adsorption)
- Thermal mode: Solar/lab-assisted can overcome desorption barriers

**Fast Manufacturing**:
- Single layer only (skip dual/triple complexity)
- Pure Chitosan (simpler to source than modified)
- No crosslinking or minimal crosslinking (fewer chemistry steps)
- Water-based solvent (no organic solvent safety protocols)
- Expected result: 10-20% yield reduction vs. optimized membrane, but 50%+ faster production

---

### Device Design Optimization

**Maximizing Water Yield**:
- Larger diameter cylinder (more surface area for adsorption)
- Taller height (bigger upper chamber = more water vapor contact)
- Sharper cone angle (faster condensation, gravity drainage)
- Solar thermal mode (boosts desorption efficiency)

**Minimizing Cost**:
- Smaller device (less material, less assembly)
- Bench prototype (simpler support structure)
- Passive mode (no heating equipment)
- Simple filtration (gravity or passive filter only)

**Field Robustness**:
- Medium diameter (balance size vs. portability)
- Pilot prototype (field-tested design class)
- Solar-assisted thermal mode (works in variable climates)
- Robust filtration (handles dusty/dirty air intake)
- Good insulation (thermal isolation from ambient, passive condensation)

---

### Performance Simulation Tips

**Interpreting Water Yield**:
- 0.3-0.4 L/kg/day: Conservative, achievable with green materials
- 0.4-0.5 L/kg/day: Strong performance, well-optimized design
- 0.5-0.6 L/kg/day: Excellent, likely needs active heating or MOF-quality materials
- >0.6 L/kg/day: Exceptional, usually synthetic MOF-based

**Sensitivity Analysis**:
- Look at RH curve: steep slope? = Design highly sensitive to humidity (good for humid climates, risky for dry)
- Look at temperature curve: steep slope? = Design sensitive to temperature (solar mode needed)
- Flat curve? = Robust design, works across conditions

**Confidence Level Interpretation**:
- **High confidence**: Atmospheric conditions are close to typical synthesis/testing conditions
- **Medium confidence**: Some deviation from typical conditions
- **Low confidence**: Extreme conditions; results are extrapolated, use with caution

---

### Benchmarking for Competitive Analysis

**When to Use Benchmarks**:
1. You want to know: "Am I competitive?"
2. You're pitching to investors: "How do I compare?"
3. You're planning R&D: "Where should I focus improvement?"

**Interpreting Radar Charts**:
- 5 dimensions: Sustainability, Cost Efficiency, Scalability, Passive Suitability, Synthesis Simplicity
- Large area = well-rounded, good at everything
- Spike in one axis = specialized (e.g., MOF has low cost but low sustainability)
- Your shape vs. reference shape = strategic differences

**Typical Patterns**:
- **MOF designs**: High yield, lower sustainability, high cost
- **Bio-based designs**: Lower yield (-10%), high sustainability, competitive cost
- **Composite designs**: Medium yield, medium sustainability, moderate cost
- **Your green design**: Target: Bio-based performance + unique sustainable edge

---

### Cost & Scale-Up Strategy

**Lab Scale → Commercial**: Expect 2-3 year timeline, multiple investment rounds
1. **Lab (Year 1)**: Validate concept, batch size ~100 units, cost high (~$10/membrane)
2. **Pilot (Year 2-3)**: Scale to 10K units/year, cost drops to ~$3-5/membrane
3. **Pre-commercial (Year 3+)**: Scale to 100K+ units/year, cost reaches ~$1-2/membrane

**Cost Reduction Levers**:
- Feedstock: Bulk purchase and preprocessing contracts
- Synthesis: Continuous-flow reactors vs. batch (50% energy reduction)
- Membrane: Automated coating/lamination (labor down 70%)
- Device: Injection molding for case (one-time mold cost)
- Assembly: Robotic assembly (labor down 80%)

**Funding Strategy**:
- Pre-seed/Seed: Validate concept, get first proof-of-concept (6-12 months, ~$50-200K)
- Series A: Scale to pilot (12-24 months, ~$1-2M)
- Series B: Build manufacturing facility, reach pre-commercial (24-36 months, ~$5-10M)

---

### Reporting for Different Audiences

**For R&D Team**:
- Use Technical Summary
- Include all parameters and heuristic logic
- Highlight assumptions and confidence levels
- Recommend next bench-scale experiments
- Focus on technical validation

**For Investors/Business**:
- Use Investor Summary
- Lead with sustainability angle and market opportunity
- Focus on cost trajectory and commercialization timeline
- Compare against MOF benchmarks (they know MOF)
- Highlight risk mitigation (using proven bio materials)

**For Manufacturing Partner**:
- Use SOP Draft + cost breakdown
- Focus on simplicity and scalability
- Include Bill of Materials with part numbers
- Highlight safety protocols (especially if using organic solvents)
- Provide exact parameter tolerances

**For Academic Publication**:
- Cite "AquaForge v1.0 | Heuristic-based R&D decision-support tool"
- Explain the model assumptions and data sources
- Compare results against published experimental data
- Use as preliminary screening tool (propose experimental validation)

---

### Common Mistakes to Avoid

1. **Over-optimizing for single metric**: Don't max yield without considering cost/sustainability tradeoff
2. **Ignoring manufacturability**: A design that works in simulation but is impossible to make at scale is worthless
3. **Neglecting thermal constraints**: Passive desorption has hard limits; acknowledge them
4. **Using lab costs at commercial scale**: Remember cost multipliers; don't quote lab cost for commercial product
5. **Assuming linear scale-up**: Doubling batch size doesn't halve cost (non-linear dynamics)
6. **Validating against only one climate condition**: Your design should work across RH 40-90%, temp 10-35°C
7. **Ignoring material availability**: A perfect design using rare materials is commercially dead
8. **Not planning for scale-up from day one**: Design for manufacturability early, not after proof-of-concept

"""

# ============================================================================
# EXPORT HELPER FUNCTION
# ============================================================================

def get_help_section(section_name: str) -> str:
    """
    Retrieve a specific help section by name.
    
    Args:
        section_name: One of 'getting_started', 'faq', 'modules', 'glossary', 'tips'
    
    Returns:
        Markdown text of the requested section
    """
    sections = {
        'getting_started': GETTING_STARTED,
        'faq': FAQ,
        'modules': MODULES_GUIDE,
        'glossary': GLOSSARY,
        'tips': TIPS_AND_TRICKS,
    }
    return sections.get(section_name.lower(), "Section not found. Available: getting_started, faq, modules, glossary, tips")


if __name__ == "__main__":
    # Test: print brand info
    print(f"Brand: {BRAND_NAME}")
    print(f"Tagline: {BRAND_TAGLINE}")
    print(f"Description: {BRAND_DESCRIPTION}")
