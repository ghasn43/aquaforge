"""
AQUAFORGE - ATMOSPHERIC WATER HARVESTING SUITE
Main Streamlit Application
Powered by NanoBio Studio - Bio Catalyst Engineering

Professional, investor-grade atmospheric water harvesting system designer.
Brand: AquaForge | Tagline: Engineer Water from Air
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from io import StringIO, BytesIO

# Import all modules
from data_models import (
    ProjectState, MembraneFormulation, DeviceConfiguration, AtmosphericConditions
)
from materials_logic import MaterialsDesigner
from membrane_logic import MembraneDesigner
from device_logic import DeviceDesigner
from simulator_logic import AwhSimulator
from benchmarking_logic import BenchmarkingLab
from costing_logic import CostingEngine
from reports_logic import ReportGenerator
from utils import (
    create_default_project, get_preset_projects, estimate_trl_level,
    calculate_sustainability_badge, recommend_next_experiment, validate_project_state
)
from help_content import (
    BRAND_NAME, BRAND_TAGLINE, BRAND_DESCRIPTION,
    GETTING_STARTED, FAQ, MODULES_GUIDE, GLOSSARY, TIPS_AND_TRICKS
)
from help_content import (
    BRAND_NAME, BRAND_TAGLINE, BRAND_DESCRIPTION,
    GETTING_STARTED, FAQ, MODULES_GUIDE, GLOSSARY, TIPS_AND_TRICKS
)

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="AquaForge | Atmospheric Water Harvesting Suite",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if "project" not in st.session_state:
    st.session_state.project = create_default_project()

if "simulation_result" not in st.session_state:
    st.session_state.simulation_result = None

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Overview"

# ============================================================================
# STYLING & BRANDING
# ============================================================================

st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #1e5a96;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 0.5em;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.1em;
        margin-bottom: 2em;
    }
    .module-header {
        background: linear-gradient(135deg, #1e5a96 0%, #2e7cb0 100%);
        color: white;
        padding: 1.5em;
        border-radius: 8px;
        margin-bottom: 1.5em;
    }
    .kpi-card {
        background: #f8f9fa;
        border-left: 4px solid #1e5a96;
        padding: 1em;
        border-radius: 6px;
        margin: 0.5em 0;
    }
    .metric-label {
        font-size: 0.85em;
        color: #666;
        font-weight: 600;
    }
    .metric-value {
        font-size: 1.5em;
        color: #1e5a96;
        font-weight: bold;
    }
    .warning-box {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1em;
        border-radius: 6px;
        margin: 1em 0;
    }
    .success-box {
        background: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1em;
        border-radius: 6px;
        margin: 1em 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def update_all_calculations():
    """Recalculate all derived metrics."""
    project = st.session_state.project
    
    # Calculate membrane properties
    project.membrane = MembraneDesigner.calculate_all_properties(project.membrane)
    
    # Calculate device volumes
    project.device = DeviceDesigner.calculate_chamber_volumes(project.device)
    project.device.estimated_manufacturability = DeviceDesigner.estimate_manufacturability(project.device)
    project.device.maintenance_complexity = DeviceDesigner.estimate_maintenance_complexity(project.device)
    project.device.prototype_complexity = DeviceDesigner.estimate_prototype_complexity(project.device)
    
    # Run simulation
    st.session_state.simulation_result = AwhSimulator.simulate_performance(
        project.membrane,
        project.device,
        project.conditions
    )
    project.simulation = st.session_state.simulation_result
    
    # Calculate costs
    project.costing = CostingEngine.estimate_costs(
        project.membrane,
        project.device,
        project.costing
    )

def render_kpi_card(label: str, value: str, unit: str = "", tooltip: str = ""):
    """Render a KPI metric card."""
    col = st.container()
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value} {unit}</div>
            {'<small>' + tooltip + '</small>' if tooltip else ''}
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# MAIN APP STRUCTURE
# ============================================================================

# Header
st.markdown(f'<div class="main-title">💧 {BRAND_NAME}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="subtitle">{BRAND_TAGLINE} | {BRAND_DESCRIPTION[:80]}... | NanoBio Studio</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🎛️ Project Management")
    
    # Project name
    st.session_state.project.project_name = st.text_input(
        "Project Name",
        value=st.session_state.project.project_name,
        key="project_name_input"
    )
    
    # Presets
    st.markdown("#### Quick Start")
    preset_names = list(get_preset_projects().keys())
    if st.button("📋 Load Preset"):
        selected_preset = st.selectbox("Select Preset", preset_names, key="preset_select")
        if selected_preset:
            st.session_state.project = get_preset_projects()[selected_preset]
            st.success(f"✅ Loaded preset: {selected_preset}")
            st.rerun()
    
    # Reset
    if st.button("🔄 Reset to Default"):
        st.session_state.project = create_default_project()
        st.rerun()
    
    # Import/Export
    st.markdown("#### Export & Sharing")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📥 Save Project"):
            st.info("Project auto-saved to session. Use Reports tab to download formats.")
    with col2:
        if st.button("📤 Load JSON"):
            st.info("Load JSON feature - use Reports tab")

# ============================================================================
# TAB NAVIGATION
# ============================================================================

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "📊 Overview",
    "🧬 Feedstock-to-Nanomaterial",
    "🎬 Membrane Composer",
    "⚙️ Device Configurator",
    "💧 AWH Simulator",
    "🏆 Benchmarking Lab",
    "💰 Scale-Up & Cost",
    "📄 Reports & Export",
    "❓ Help & Docs"
])

# ============================================================================
# TAB 1: OVERVIEW
# ============================================================================

with tab1:
    st.markdown('<div class="module-header"><h2>📊 Atmospheric Water Harvesting Suite Overview</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Purpose
        
        This module enables you to design, simulate, compare, and optimize **green nanomaterial-based 
        atmospheric water harvesting systems**. It integrates:
        
        - **Materials Science**: Feedstock selection, nanomaterial synthesis pathways, formulation engineering
        - **Device Engineering**: Cylindrical collector architecture, geometric optimization
        - **Performance Simulation**: Heuristic-based water yield prediction
        - **Benchmarking**: Comparison against MOF and alternative systems
        - **Economic Analysis**: Cost estimation and scale-up pathway
        
        ### Workflow
        """)
        
        # Workflow diagram
        workflow_text = """
        **BIOMASS / FEEDSTOCK**
        ↓
        **NANOMATERIAL SYNTHESIS**
        ↓
        **MEMBRANE FORMULATION**
        ↓
        **DEVICE ARCHITECTURE**
        ↓
        **ATMOSPHERIC WATER CAPTURE**
        ↓
        **FILTRATION & CLEAN WATER**
        """
        st.markdown(workflow_text)
        
    with col2:
        st.markdown("### Current Project KPIs")
        
        update_all_calculations()
        project = st.session_state.project
        
        col_a, col_b = st.columns(2)
        with col_a:
            render_kpi_card(
                "Feedstock",
                project.feedstock.feedstock_type.value[:15],
                "",
                "Selected biomass source"
            )
            render_kpi_card(
                "Nanomaterial Route",
                project.nanomaterial.synthesis_route.value[:12],
                "",
                "Synthesis pathway"
            )
            render_kpi_card(
                "Membrane Type",
                project.membrane.polymer_matrix.value[:12],
                "",
                "Polymer matrix"
            )
        
        with col_b:
            render_kpi_card(
                "Device Class",
                project.device.device_class.value[:12],
                "",
                "Prototype stage"
            )
            render_kpi_card(
                "Water Yield",
                f"{project.simulation.predicted_water_yield_l_kg_day:.3f}",
                "L/kg/day",
                "Predicted yield"
            )
            trl_num, trl_desc = estimate_trl_level(
                project.membrane.mechanical_stability,
                project.device.device_class.value
            )
            render_kpi_card(
                "Technology Readiness",
                f"TRL {trl_num}",
                "",
                trl_desc
            )
    
    st.markdown("---")
    
    # Material systems overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🌱 Green Materials Available
        
        **Biomass Feedstocks:**
        - Peanut Shell
        - Banana Peel
        - Phoenix Dactylifera
        - Algae
        - Fungal Biomass
        - Rice Husk
        - Coconut Shell
        
        **Green Synthesis Routes:**
        - Green synthesis (aqueous)
        - Calcination pathways
        - TEOS-based silica
        - Gel-based synthesis
        - ZnO green routes
        - Fe/Zn/Si nanocomposites
        """)
    
    with col2:
        st.markdown("""
        ### 🔬 Core Technologies
        
        **Polymer Matrices:**
        - Pure Chitosan
        - Modified Chitosan
        - Silica-Enhanced Chitosan
        - ZnO/Chitosan
        - Fe/Zn/Si/Chitosan
        
        **Layer Configurations:**
        - Single Layer
        - Dual-layer hydrophobic/hydrophilic
        - Triple-layer systems
        
        **Nanoparticles:**
        - Green silica
        - ZnO particles
        - Multi-element oxides
        """)
    
    with col3:
        st.markdown("""
        ### 💡 Performance Science
        
        **Mechanisms:**
        - Passive adsorption under high RH
        - Solar/thermal-driven desorption
        - Passive condensation on cooled surfaces
        - Gravity-driven collection
        - Optional filtration
        
        **Performance Range:**
        - Yield: 0.1 - 0.6 L/kg/day
        - Sustainability: 70-95%
        - TRL: 3-6 (bench to field)
        """)
    
    st.markdown("---")
    
    # System overview text
    st.markdown("""
    ### 📋 About This Module
    
    **Current Readiness Level**: Concept-to-Prototype Validation
    
    This tool provides **design-stage heuristic estimates** for R&D guidance. All calculations are based on:
    - Green synthesis literature data
    - Membrane adsorption principles
    - Device geometry simulations
    - Benchmark comparisons (MOF, activated carbon)
    
    **This is NOT:**
    - A certified engineering design tool
    - A guarantee of performance
    - A replacement for experimental validation
    
    **Recommendation**: Use results to guide bench-scale experiments, then validate against actual data.
    
    ### 🎓 Next Steps
    1. Configure feedstock and synthesis route in Tab 2
    2. Design membrane formulation in Tab 3
    3. Build device architecture in Tab 4
    4. Run performance simulation in Tab 5
    5. Compare benchmarks in Tab 6
    6. Analyze costs in Tab 7
    7. Generate reports in Tab 8
    """)

# ============================================================================
# TAB 2: FEEDSTOCK-TO-NANOMATERIAL DESIGNER
# ============================================================================

with tab2:
    st.markdown('<div class="module-header"><h2>🧬 Feedstock-to-Nanomaterial Designer</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown("### Material Selection")
        
        # Feedstock selection
        feedstock_options = MaterialsDesigner.get_feedstock_options()
        feedstock_key = st.selectbox(
            "Select Biomass Feedstock",
            options=list(feedstock_options.keys()),
            format_func=lambda x: feedstock_options[x],
            key="feedstock_select"
        )
        
        if feedstock_key != st.session_state.project.feedstock.feedstock_type:
            st.session_state.project.feedstock.feedstock_type = feedstock_key
        
        # Synthesis route
        synthesis_options = MaterialsDesigner.get_synthesis_route_options()
        synthesis_key = st.selectbox(
            "Select Synthesis Route",
            options=list(synthesis_options.keys()),
            format_func=lambda x: synthesis_options[x],
            key="synthesis_select"
        )
        
        if synthesis_key != st.session_state.project.nanomaterial.synthesis_route:
            st.session_state.project.nanomaterial.synthesis_route = synthesis_key
        
        # Process parameters
        st.markdown("#### Synthesis Parameters")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.session_state.project.nanomaterial.drying_temperature_c = st.slider(
                "Drying Temperature (°C)",
                50, 200, 100, key="drying_temp"
            )
        with col_b:
            st.session_state.project.nanomaterial.calcination_temperature_c = st.slider(
                "Calcination Temperature (°C)",
                200, 600, 300, key="calc_temp"
            )
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.session_state.project.nanomaterial.reaction_time_hours = st.slider(
                "Reaction Time (hours)",
                0.5, 12.0, 4.0, key="reaction_time"
            )
        with col_b:
            st.session_state.project.nanomaterial.solvent_system = st.selectbox(
                "Solvent System",
                ["Water-based", "Ethanol-based", "Mixed aqueous-organic"],
                key="solvent_sys"
            )
        
    with col2:
        st.markdown("### Feedstock Properties")
        
        feedstock = st.session_state.project.feedstock
        
        render_kpi_card("Feedstock Type", feedstock.feedstock_type.value)
        render_kpi_card("Sustainability", f"{feedstock.sustainability_score:.1%}")
        render_kpi_card("Cost", f"${feedstock.cost_per_kg:.2f}/kg")
        render_kpi_card("Availability", feedstock.availability)
        
        st.markdown("#### Cost Adjustment")
        st.session_state.project.feedstock.cost_per_kg = st.slider(
            "Cost per kg (USD)",
            0.5, 10.0, feedstock.cost_per_kg, key="feedstock_cost"
        )
    
    st.markdown("---")
    
    # Estimate nanomaterial properties
    if st.button("🔬 Estimate Nanomaterial Properties", key="estimate_nano"):
        designer = MaterialsDesigner()
        estimated_nano = designer.estimate_nanomaterial_profile(
            st.session_state.project.feedstock,
            st.session_state.project.nanomaterial.synthesis_route,
            st.session_state.project.nanomaterial.drying_temperature_c,
            st.session_state.project.nanomaterial.calcination_temperature_c,
            st.session_state.project.nanomaterial.reaction_time_hours,
        )
        st.session_state.project.nanomaterial = estimated_nano
        st.success("✅ Nanomaterial properties estimated!")
    
    st.markdown("### 📊 Predicted Nanomaterial Profile")
    
    nano = st.session_state.project.nanomaterial
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card("Particle Size", f"{nano.expected_particle_size_nm[0]:.0f}-{nano.expected_particle_size_nm[1]:.0f}", "nm")
    with col2:
        render_kpi_card("Crystallinity", f"{nano.expected_crystallinity_pct:.0f}", "%")
    with col3:
        render_kpi_card("Hydrophilicity", nano.expected_hydrophilicity.title())
    with col4:
        render_kpi_card("Adsorption Value", f"{nano.water_adsorption_relevance:.2f}", "/1.0")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card("Morphology", nano.expected_morphology.title())
    with col2:
        render_kpi_card("Complexity", f"{nano.synthesis_complexity:.2f}", "/1.0")
    with col3:
        render_kpi_card("Scalability", f"{nano.scalability_score:.2f}", "/1.0")
    with col4:
        render_kpi_card("Est. Cost", f"${nano.estimated_cost_per_kg:.0f}", "/kg")
    
    st.markdown("---")
    st.info(
        "**💡 Heuristic Predictions**: All values above are estimates based on synthesis route and parameters. "
        "Validate with experimental characterization (XRD, SEM, BET, particle sizing)."
    )

# ============================================================================
# TAB 3: MEMBRANE COMPOSER
# ============================================================================

with tab3:
    st.markdown('<div class="module-header"><h2>🎬 Membrane Composer & Formulation Designer</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown("### Membrane Formulation")
        
        # Polymer matrix selection
        polymer_options = MembraneDesigner.get_polymer_options()
        polymer_key = st.selectbox(
            "Select Polymer Matrix",
            options=list(polymer_options.keys()),
            format_func=lambda x: polymer_options[x],
            key="polymer_select"
        )
        st.session_state.project.membrane.polymer_matrix = polymer_key
        
        # Nanoparticle configuration
        st.session_state.project.membrane.nanoparticle_type = st.selectbox(
            "Nanoparticle Type",
            ["Green Silica", "ZnO", "Fe/Zn/Si Composite", "Mixed Silica/ZnO", "Custom"],
            key="np_type"
        )
        
        st.session_state.project.membrane.nanoparticle_loading_wt_pct = st.slider(
            "Nanoparticle Loading (wt%)",
            0.0, 30.0, 10.0, key="np_loading"
        )
        
        st.session_state.project.membrane.particle_size_nm = st.slider(
            "Average Particle Size (nm)",
            10, 200, 50, key="p_size"
        )
        
        st.session_state.project.membrane.particle_dispersion_quality = st.selectbox(
            "Dispersion Quality",
            ["Poor", "Fair", "Good", "Excellent"],
            key="disp_qual"
        )
        
        # Layer configuration
        layer_options = MembraneDesigner.get_layer_config_options()
        layer_key = st.selectbox(
            "Layer Configuration",
            options=list(layer_options.keys()),
            format_func=lambda x: layer_options[x],
            key="layer_config"
        )
        st.session_state.project.membrane.layer_config = layer_key
        
    with col2:
        st.markdown("### Physical Properties")
        
        st.session_state.project.membrane.thickness_um = st.slider(
            "Thickness (µm)",
            50.0, 300.0, 100.0, key="thickness"
        )
        
        st.session_state.project.membrane.porosity_pct = st.slider(
            "Porosity (%)",
            10.0, 70.0, 35.0, key="porosity"
        )
        
        st.session_state.project.membrane.crosslink_density = st.selectbox(
            "Crosslink Density",
            ["Low", "Medium", "High"],
            key="crosslink_dens"
        )
        
        st.session_state.project.membrane.crosslinker = st.selectbox(
            "Crosslinker",
            ["Glutaraldehyde", "EDC/NHS", "Genipin", "Epichlorohydrin", "None"],
            key="crosslinker"
        )
        
        st.session_state.project.membrane.drying_method = st.selectbox(
            "Drying Method",
            ["Air dry at 60°C", "Lyophilization", "Oven 80°C", "Room temp"],
            key="dry_method"
        )
    
    # Calculate properties
    if st.button("🧪 Calculate Membrane Properties", key="calc_membrane"):
        st.session_state.project.membrane = MembraneDesigner.calculate_all_properties(
            st.session_state.project.membrane
        )
        st.success("✅ Membrane properties calculated!")
    
    st.markdown("---")
    st.markdown("### 📈 Estimated Membrane Performance")
    
    membrane = st.session_state.project.membrane
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card("Contact Angle", f"{membrane.estimated_contact_angle_deg:.1f}", "°",
                       "Lower = more hydrophilic")
    with col2:
        render_kpi_card("Adsorption", f"{membrane.estimated_adsorption_strength:.2f}", "/1.0")
    with col3:
        render_kpi_card("Desorption Ease", f"{membrane.desorption_ease:.2f}", "/1.0",
                       "Higher = easier release")
    with col4:
        render_kpi_card("Mechanical", f"{membrane.mechanical_stability:.2f}", "/1.0")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card("Moisture Capture", f"{membrane.moisture_capture_score:.2f}", "/1.0")
    with col2:
        render_kpi_card("Thermal Robust", f"{membrane.thermal_robustness:.2f}", "/1.0")
    with col3:
        render_kpi_card("Manufacturability", f"{membrane.manufacturability_score:.2f}", "/1.0")
    with col4:
        render_kpi_card("Sustainability", f"{membrane.sustainability_score:.2f}", "/1.0")
    
    # Risk flags
    risk_flags = MembraneDesigner.get_risk_flags(membrane)
    if risk_flags:
        st.markdown("### ⚠️ Design Risk Flags")
        for flag in risk_flags:
            st.markdown(f"- {flag}")
    
    # Radar chart
    st.markdown("### 📊 Performance Radar Chart")
    
    radar_data = {
        "Adsorption": membrane.estimated_adsorption_strength,
        "Desorption": membrane.desorption_ease,
        "Mechanical": membrane.mechanical_stability,
        "Moisture": membrane.moisture_capture_score,
        "Thermal": membrane.thermal_robustness,
        "Manufacturability": membrane.manufacturability_score,
    }
    
    fig = go.Figure(data=go.Scatterpolar(
        r=list(radar_data.values()),
        theta=list(radar_data.keys()),
        fill='toself',
        name='Membrane'
    ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=False,
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# TAB 4: DEVICE CONFIGURATOR
# ============================================================================

with tab4:
    st.markdown('<div class="module-header"><h2>⚙️ Device Configurator & Architecture</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown("### Device Dimensions & Structure")
        
        device_class_options = DeviceDesigner.get_device_class_options()
        device_class_key = st.selectbox(
            "Device Class",
            options=list(device_class_options.keys()),
            format_func=lambda x: device_class_options[x],
            key="device_class"
        )
        st.session_state.project.device.device_class = device_class_key
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.session_state.project.device.overall_diameter_cm = st.slider(
                "Overall Diameter (cm)",
                15, 80, 30, key="diameter"
            )
        with col_b:
            st.session_state.project.device.total_height_cm = st.slider(
                "Total Height (cm)",
                40, 150, 60, key="height"
            )
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.session_state.project.device.upper_chamber_height_cm = st.slider(
                "Upper Chamber Height (cm)",
                10, 50, 20, key="upper_h"
            )
        with col_b:
            st.session_state.project.device.lower_chamber_height_cm = st.slider(
                "Lower Chamber Height (cm)",
                10, 50, 25, key="lower_h"
            )
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.session_state.project.device.cone_angle_deg = st.slider(
                "Cone Angle (degrees)",
                30, 85, 60, key="cone_angle"
            )
        with col_b:
            st.session_state.project.device.funnel_throat_diameter_cm = st.slider(
                "Funnel Throat (cm)",
                3, 20, 8, key="throat"
            )
        
    with col2:
        st.markdown("### Component Selection")
        
        st.session_state.project.device.structural_material = st.selectbox(
            "Structural Material",
            ["Polycarbonate + Aluminum", "Glass + Steel", "PMMA + Aluminum", "PVC + Steel"],
            key="struct_mat"
        )
        
        st.session_state.project.device.chamber_transparency = st.selectbox(
            "Chamber Type",
            ["Polycarbonate (translucent)", "Glass (clear)", "PMMA (clear)", "Frosted"],
            key="chamber_type"
        )
        
        st.session_state.project.device.reservoir_capacity_ml = st.slider(
            "Reservoir Capacity (mL)",
            100, 2000, 500, step=50, key="reservoir"
        )
        
        st.session_state.project.device.support_columns_count = st.slider(
            "Support Columns",
            1, 6, 3, key="columns"
        )
        
        st.session_state.project.device.passive_assisted = st.radio(
            "Operation Mode",
            ["Passive", "Assisted"],
            key="passive_mode"
        )
        
        thermal_options = DeviceDesigner.get_thermal_mode_options()
        thermal_key = st.selectbox(
            "Thermal Mode",
            options=list(thermal_options.keys()),
            format_func=lambda x: thermal_options[x],
            key="thermal_mode"
        )
        st.session_state.project.device.thermal_mode = thermal_key
        
        st.session_state.project.device.filtration_stage = st.checkbox(
            "Include Filtration Stage",
            value=True,
            key="filtration"
        )
    
    # Calculate device geometry
    if st.button("📐 Calculate Device Geometry", key="calc_device"):
        st.session_state.project.device = DeviceDesigner.calculate_chamber_volumes(
            st.session_state.project.device
        )
        st.session_state.project.device.estimated_manufacturability = DeviceDesigner.estimate_manufacturability(st.session_state.project.device)
        st.session_state.project.device.maintenance_complexity = DeviceDesigner.estimate_maintenance_complexity(st.session_state.project.device)
        st.success("✅ Device geometry calculated!")
    
    st.markdown("---")
    st.markdown("### 📊 Device Specifications")
    
    device = st.session_state.project.device
    device_summary = DeviceDesigner.get_device_summary(device)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card("Class", device_summary["device_class"][:12])
        render_kpi_card("Dimensions", device_summary["dimensions"])
    with col2:
        render_kpi_card("Upper Volume", f"{device_summary['upper_volume_l']:.2f}", "L")
        render_kpi_card("Lower Volume", f"{device_summary['lower_volume_l']:.2f}", "L")
    with col3:
        render_kpi_card("Cone Volume", f"{device_summary['cone_volume_l']:.2f}", "L")
        render_kpi_card("Reservoir", f"{device_summary['reservoir_capacity_ml']:.0f}", "mL")
    with col4:
        render_kpi_card("Manufacturability", f"{device.estimated_manufacturability:.2f}", "/1.0")
        render_kpi_card("Maintenance", f"{device.maintenance_complexity:.2f}", "/1.0")
    
    st.markdown("---")
    st.markdown("### 🔄 Condensation & Collection Flow")
    
    flow_desc = DeviceDesigner.get_condensation_path_description(device)
    st.markdown(flow_desc)
    
    st.markdown("---")
    st.markdown("### 📋 Bill of Materials (Concept)")
    
    components = DeviceDesigner.get_component_list(device)
    for i, component in enumerate(components, 1):
        st.markdown(f"{i}. {component}")
    
    # Validation warnings
    warnings = DeviceDesigner.validate_device_config(device)
    if warnings:
        st.markdown("### ⚠️ Design Considerations")
        for warning in warnings:
            st.warning(warning)

# ============================================================================
# TAB 5: WATER HARVESTING SIMULATOR
# ============================================================================

with tab5:
    st.markdown('<div class="module-header"><h2>💧 Atmospheric Water Harvesting Simulator</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown("### Environmental Conditions")
        
        st.session_state.project.conditions.relative_humidity_pct = st.slider(
            "Relative Humidity (%)",
            10, 100, 60, key="sim_rh"
        )
        
        st.session_state.project.conditions.ambient_temperature_c = st.slider(
            "Ambient Temperature (°C)",
            5, 40, 25, key="sim_temp"
        )
        
        st.session_state.project.conditions.day_night_mode = st.selectbox(
            "Operational Mode",
            ["Day", "Night", "24h Continuous"],
            key="day_night"
        )
        
        st.session_state.project.conditions.airflow_level = st.selectbox(
            "Air Flow Level",
            ["Low", "Natural", "Medium", "High"],
            key="airflow"
        )
        
        st.session_state.project.conditions.solar_exposure = st.selectbox(
            "Solar Exposure",
            ["None", "Low", "Moderate", "High"],
            key="solar_exp"
        )
        
        st.session_state.project.conditions.cycle_duration_hours = st.slider(
            "Cycle Duration (hours)",
            2.0, 24.0, 8.0, key="cycle_dur"
        )
        
        st.session_state.project.conditions.operation_mode = st.selectbox(
            "Operation Strategy",
            ["adsorption-focused", "Balanced", "high-release"],
            key="op_mode"
        )
    
    with col2:
        st.markdown("### Simulation Control")
        
        if st.button("▶️ Run Simulation", key="run_sim"):
            sim_result = AwhSimulator.simulate_performance(
                st.session_state.project.membrane,
                st.session_state.project.device,
                st.session_state.project.conditions
            )
            st.session_state.project.simulation = sim_result
            st.session_state.simulation_result = sim_result
            st.success("✅ Simulation complete!")
        
        st.info(
            "**Note**: All simulations are heuristic-based design estimates. "
            "Validate with bench-scale experiments."
        )
    
    if st.session_state.simulation_result:
        sim = st.session_state.simulation_result
        
        st.markdown("---")
        st.markdown("### 📊 Simulation Results")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            render_kpi_card("Water Yield", f"{sim.predicted_water_yield_l_kg_day:.3f}", "L/kg/day")
        with col2:
            render_kpi_card("Adsorption", f"{sim.adsorption_score:.2f}", "/1.0")
        with col3:
            render_kpi_card("Desorption", f"{sim.desorption_efficiency:.2f}", "/1.0")
        with col4:
            render_kpi_card("Condensation", f"{sim.condensation_likelihood:.2f}", "/1.0")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            render_kpi_card("Collection", f"{sim.collection_efficiency_pct:.1f}", "%")
        with col2:
            render_kpi_card("Filtration", f"{sim.filtration_efficiency_pct:.1f}", "%")
        with col3:
            render_kpi_card("Relative Perf", f"{sim.relative_performance_score:.2f}", "/1.0")
        with col4:
            render_kpi_card("Confidence", sim.confidence_level)
        
        # Performance assessment
        st.markdown("### 📈 Performance Assessment")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Performance Window**: {sim.performance_window}")
        with col2:
            st.markdown(f"**Confidence Level**: {sim.confidence_level}")
        
        # Stage contributions
        st.markdown("### 🔀 Stage Contributions")
        
        contrib_df = pd.DataFrame([
            {"Stage": k, "Contribution %": v} for k, v in sim.stage_contributions.items()
        ])
        
        fig = px.bar(contrib_df, x="Stage", y="Contribution %", title="System Stage Contributions")
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.markdown("### 📉 Performance Curves")
        
        # RH sensitivity
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Water Yield vs RH**")
            rh_curve = AwhSimulator.get_water_yield_vs_rh(
                st.session_state.project.membrane,
                st.session_state.project.device,
                st.session_state.project.conditions
            )
            rh_df = pd.DataFrame(rh_curve)
            
            fig = px.line(rh_df, x="rh_pct", y="yield_l_kg_day",
                         labels={"rh_pct": "RH (%)", "yield_l_kg_day": "Water Yield (L/kg/day)"},
                         title="Yield Sensitivity to Humidity")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("**Water Yield vs Temperature**")
            temp_curve = AwhSimulator.get_water_yield_vs_temperature(
                st.session_state.project.membrane,
                st.session_state.project.device,
                st.session_state.project.conditions
            )
            temp_df = pd.DataFrame(temp_curve)
            
            fig = px.line(temp_df, x="temp_c", y="yield_l_kg_day",
                         labels={"temp_c": "Temperature (°C)", "yield_l_kg_day": "Water Yield (L/kg/day)"},
                         title="Yield Sensitivity to Temperature")
            st.plotly_chart(fig, use_container_width=True)
        
        # Adsorption/desorption cycle
        st.markdown("---")
        st.markdown("**Adsorption/Desorption Cycle**")
        
        cycle_data = AwhSimulator.get_adsorption_desorption_cycle(
            st.session_state.project.membrane,
            st.session_state.project.device,
            st.session_state.project.conditions,
            st.session_state.project.conditions.cycle_duration_hours
        )
        cycle_df = pd.DataFrame(cycle_data)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=cycle_df['time_hours'], y=cycle_df['adsorption_level'],
                                name='Adsorption', mode='lines'))
        fig.add_trace(go.Scatter(x=cycle_df['time_hours'], y=cycle_df['desorption_level'],
                                name='Desorption', mode='lines'))
        
        fig.update_xaxes(title_text="Time (hours)")
        fig.update_yaxes(title_text="Activity Level (0-1)")
        fig.update_layout(title="AWH Cycle Profile", hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.info("⏳ Run simulation to see results here.")

# ============================================================================
# TAB 6: BENCHMARKING LAB
# ============================================================================

with tab6:
    st.markdown('<div class="module-header"><h2>🏆 Benchmarking Lab</h2></div>', unsafe_allow_html=True)
    
    st.markdown("### Compare Your Design Against Reference Systems")
    
    # Run simulation if needed
    if not st.session_state.simulation_result:
        if st.button("🔄 Run Simulation First", key="bench_run_sim"):
            sim_result = AwhSimulator.simulate_performance(
                st.session_state.project.membrane,
                st.session_state.project.device,
                st.session_state.project.conditions
            )
            st.session_state.simulation_result = sim_result
            st.rerun()
    
    benchmark_names = BenchmarkingLab.get_benchmark_names()
    selected_benchmarks = st.multiselect(
        "Select Benchmarks to Compare",
        benchmark_names,
        default=["MOF-801", "MOF-303", "Bio-based Chitosan/ZnO/Silica"],
        key="bench_select"
    )
    
    if st.session_state.simulation_result:
        st.markdown("---")
        st.markdown("### 📊 Comparison Table")
        
        # Create comparison table
        comparison_data = []
        
        # User design
        comparison_data.append({
            "System": "✨ Your Design",
            "Water Yield (L/kg/day)": f"{st.session_state.simulation_result.predicted_water_yield_l_kg_day:.3f}",
            "Adsorption": f"{st.session_state.simulation_result.adsorption_score:.2f}",
            "Desorption": f"{st.session_state.simulation_result.desorption_efficiency:.2f}",
        })
        
        # Benchmarks
        for bench_name in selected_benchmarks:
            profile = BenchmarkingLab.get_benchmark_details(bench_name)
            comparison_data.append({
                "System": bench_name,
                "Water Yield (L/kg/day)": f"{profile.estimated_water_yield:.3f}",
                "Sustainability": f"{profile.sustainability_score:.2f}",
                "Cost": f"{profile.cost_score:.2f}",
                "Scalability": f"{profile.scalability_score:.2f}",
            })
        
        comp_df = pd.DataFrame(comparison_data)
        st.dataframe(comp_df, use_container_width=True)
        
        st.markdown("---")
        st.markdown("### 📈 Benchmark Radar Comparison")
        
        col_rad1, col_rad2 = st.columns(2)
        
        with col_rad1:
            st.markdown("**Your Design**")
            your_radar = {
                "Sustainability": st.session_state.project.membrane.sustainability_score,
                "Cost Efficiency": 0.7,  # Placeholder
                "Scalability": st.session_state.project.device.estimated_manufacturability,
                "Passive Suitability": 0.8 if st.session_state.project.device.thermal_mode.value == "Passive (No Heat)" else 0.5,
                "Synthesis Simplicity": 1.0 - st.session_state.project.nanomaterial.synthesis_complexity,
            }
            
            fig = go.Figure(data=go.Scatterpolar(
                r=list(your_radar.values()),
                theta=list(your_radar.keys()),
                fill='toself',
                name='Your Design'
            ))
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                            showlegend=False, height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col_rad2:
            st.markdown("**Reference Benchmark**")
            if selected_benchmarks:
                bench_profile = BenchmarkingLab.get_benchmark_details(selected_benchmarks[0])
                benchmark_radar = BenchmarkingLab.get_benchmark_radar_data(bench_profile)
                
                fig = go.Figure(data=go.Scatterpolar(
                    r=list(benchmark_radar.values()),
                    theta=list(benchmark_radar.keys()),
                    fill='toself',
                    name=selected_benchmarks[0]
                ))
                fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                                showlegend=False, height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        # Rankings
        st.markdown("---")
        st.markdown("### 🏅 Benchmark Rankings by Water Yield")
        
        rankings = BenchmarkingLab.rank_benchmarks(st.session_state.simulation_result,
                                                   metric="estimated_water_yield")
        rank_df = pd.DataFrame(rankings, columns=["System", "Water Yield (L/kg/day)"])
        rank_df['Rank'] = range(1, len(rank_df) + 1)
        
        st.dataframe(rank_df[['Rank', 'System', 'Water Yield (L/kg/day)']], use_container_width=True)

# ============================================================================
# TAB 7: SCALE-UP & COST
# ============================================================================

with tab7:
    st.markdown('<div class="module-header"><h2>💰 Scale-Up & Cost Analysis</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown("### Economic Parameters")
        
        st.session_state.project.costing.feedstock_cost_per_kg = st.slider(
            "Feedstock Cost ($/kg)",
            0.5, 10.0, st.session_state.project.costing.feedstock_cost_per_kg,
            key="cost_feedstock"
        )
        
        st.session_state.project.costing.polymer_cost_per_kg = st.slider(
            "Polymer Cost ($/kg)",
            20.0, 100.0, st.session_state.project.costing.polymer_cost_per_kg,
            key="cost_polymer"
        )
        
        st.session_state.project.costing.nanoparticle_prep_cost_per_kg = st.slider(
            "Nanoparticle Prep Cost ($/kg)",
            50.0, 300.0, st.session_state.project.costing.nanoparticle_prep_cost_per_kg,
            key="cost_np"
        )
        
        st.session_state.project.costing.device_fabrication_cost_base = st.slider(
            "Base Device Fabrication Cost ($)",
            100.0, 500.0, st.session_state.project.costing.device_fabrication_cost_base,
            key="cost_device"
        )
        
        st.session_state.project.costing.batch_size_units = st.number_input(
            "Batch Size (units)",
            1, 1000, 10, key="batch_size"
        )
        
        st.session_state.project.costing.scale_level = st.selectbox(
            "Scale Level",
            ["Lab", "Pilot", "Pre-commercial"],
            key="scale_level"
        )
    
    with col2:
        st.markdown("### Multiplier Factors")
        
        st.session_state.project.costing.labor_multiplier = st.slider(
            "Labor Multiplier",
            0.5, 3.0, 1.0, key="labor_mult"
        )
        
        st.session_state.project.costing.testing_multiplier = st.slider(
            "Testing Multiplier",
            0.5, 3.0, 1.5, key="test_mult"
        )
        
        st.session_state.project.costing.prototype_count = st.number_input(
            "Number of Prototypes",
            1, 100, 1, key="proto_count"
        )
    
    # Calculate costs
    if st.button("💻 Calculate Costs & Scale-Up", key="calc_costs"):
        st.session_state.project.costing = CostingEngine.estimate_costs(
            st.session_state.project.membrane,
            st.session_state.project.device,
            st.session_state.project.costing
        )
        st.success("✅ Cost analysis complete!")
    
    st.markdown("---")
    st.markdown("### 💵 Cost Breakdown")
    
    costing = st.session_state.project.costing
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card("Cost per Membrane", f"${costing.cost_per_membrane:.2f}")
    with col2:
        render_kpi_card("Prototype Cost", f"${costing.prototype_cost_total:.2f}")
    with col3:
        render_kpi_card("Cost per Liter", f"${costing.cost_per_liter_harvested:.2f}")
    with col4:
        render_kpi_card("CAPEX", f"${costing.capex_estimate:.2f}")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card("OPEX", f"${costing.opex_estimate:.2f}")
    with col2:
        render_kpi_card("Scale-Up Burden", f"{costing.scale_up_burden*100:.1f}%")
    with col3:
        pass
    with col4:
        pass
    
    st.markdown("---")
    st.markdown("### 🚀 Commercial Readiness")
    
    readiness = CostingEngine.get_commercial_readiness_snapshot(
        st.session_state.project.membrane,
        st.session_state.project.device
    )
    
    for category, status in readiness.items():
        st.markdown(f"**{category}**: {status}")
    
    st.markdown("---")
    st.markdown("### 📊 Scale-Up Cost Path")
    
    scaling_path = CostingEngine.estimate_scaling_path(costing)
    
    scale_df = pd.DataFrame([
        {"Scale": k, "Cost per Membrane ($)": v} for k, v in scaling_path.items()
    ])
    
    fig = px.bar(scale_df, x="Scale", y="Cost per Membrane ($)",
                title="Cost Reduction with Scale-Up", color="Scale")
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.markdown(CostingEngine.get_cost_summary_text(costing))

# ============================================================================
# TAB 8: REPORTS & EXPORT
# ============================================================================

with tab8:
    st.markdown('<div class="module-header"><h2>📄 Reports & Export</h2></div>', unsafe_allow_html=True)
    
    st.markdown("### Generate & Export Project Reports")
    
    # First ensure all calculations are current
    update_all_calculations()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📋 Generate Technical Summary", key="gen_tech"):
            st.session_state.technical_report = ReportGenerator.generate_technical_summary(
                st.session_state.project
            )
            st.success("✅ Technical summary generated!")
    
    with col2:
        if st.button("💼 Generate Investor Summary", key="gen_investor"):
            st.session_state.investor_report = ReportGenerator.generate_investor_summary(
                st.session_state.project
            )
            st.success("✅ Investor summary generated!")
    
    with col3:
        if st.button("📄 Generate SOP Draft", key="gen_sop"):
            st.session_state.sop_report = ReportGenerator.generate_sop_draft(
                st.session_state.project
            )
            st.success("✅ SOP draft generated!")
    
    st.markdown("---")
    st.markdown("### 📥 Download Formats")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        csv_data = ReportGenerator.generate_csv_export(st.session_state.project)
        st.download_button(
            "📊 Download CSV",
            csv_data,
            f"awh_project_{st.session_state.project.project_id}.csv",
            "text/csv",
            key="download_csv"
        )
    
    with col2:
        json_data = ReportGenerator.generate_json_export(st.session_state.project)
        st.download_button(
            "🔐 Download JSON",
            json_data,
            f"awh_project_{st.session_state.project.project_id}.json",
            "application/json",
            key="download_json"
        )
    
    with col3:
        if hasattr(st.session_state, 'technical_report'):
            st.download_button(
                "📋 Download Technical",
                st.session_state.technical_report,
                f"awh_technical_{st.session_state.project.project_id}.txt",
                "text/plain",
                key="download_tech"
            )
    
    with col4:
        if hasattr(st.session_state, 'investor_report'):
            st.download_button(
                "💼 Download Investor",
                st.session_state.investor_report,
                f"awh_investor_{st.session_state.project.project_id}.txt",
                "text/plain",
                key="download_inv"
            )
    
    st.markdown("---")
    st.markdown("### 📰 Report Previews")
    
    tab_report1, tab_report2, tab_report3 = st.tabs([
        "Technical Summary",
        "Investor Summary",
        "SOP Draft"
    ])
    
    with tab_report1:
        if hasattr(st.session_state, 'technical_report'):
            st.text(st.session_state.technical_report)
        else:
            st.info("Click 'Generate Technical Summary' above to generate the report.")
    
    with tab_report2:
        if hasattr(st.session_state, 'investor_report'):
            st.text(st.session_state.investor_report)
        else:
            st.info("Click 'Generate Investor Summary' above to generate the report.")
    
    with tab_report3:
        if hasattr(st.session_state, 'sop_report'):
            st.text(st.session_state.sop_report)
        else:
            st.info("Click 'Generate SOP Draft' above to generate the report.")
    
    st.markdown("---")
    st.markdown("### ✅ Project Validation")
    
    issues = validate_project_state(st.session_state.project)
    
    if issues:
        st.warning("**Design Issues Detected**:")
        for issue in issues:
            st.markdown(f"- {issue}")
    else:
        st.success("✅ Design configuration looks good!")
    
    # R&D recommendations
    st.markdown("---")
    st.markdown("### 🔬 R&D Recommendations")
    
    next_exp = recommend_next_experiment(
        st.session_state.project.simulation,
        st.session_state.project.device.estimated_manufacturability
    )
    st.info(next_exp)
    
    # Sustainability assessment
    st.markdown("---")
    st.markdown("### 🌱 Sustainability Assessment")
    
    badge, desc = calculate_sustainability_badge(
        st.session_state.project.feedstock.sustainability_score,
        st.session_state.project.membrane.sustainability_score,
        st.session_state.project.device.estimated_manufacturability
    )
    
    st.markdown(f"**{badge}**")
    st.markdown(desc)

# ============================================================================
# TAB 9: HELP & DOCUMENTATION
# ============================================================================

with tab9:
    st.markdown(f'<div class="module-header"><h2>❓ Help & Documentation</h2></div>', unsafe_allow_html=True)
    
    st.markdown(f"""
    ### Welcome to {BRAND_NAME}
    **{BRAND_TAGLINE}**
    
    {BRAND_DESCRIPTION}
    """)
    
    st.divider()
    
    # Help content tabs
    help_tab1, help_tab2, help_tab3, help_tab4, help_tab5 = st.tabs([
        "🚀 Quick Start",
        "❓ FAQ",
        "📚 Module Guide",
        "📖 Glossary",
        "💡 Tips & Tricks"
    ])
    
    with help_tab1:
        st.markdown(GETTING_STARTED)
    
    with help_tab2:
        st.markdown(FAQ)
    
    with help_tab3:
        st.markdown(MODULES_GUIDE)
    
    with help_tab4:
        st.markdown(GLOSSARY)
    
    with help_tab5:
        st.markdown(TIPS_AND_TRICKS)
    
    # Brand info section
    st.divider()
    st.markdown(f"""
    ### 🏷️ About {BRAND_NAME}
    
    **Version**: 1.0  
    **Brand Name**: {BRAND_NAME}  
    **Tagline**: {BRAND_TAGLINE}  
    **Platform**: NanoBio Studio | Bio Catalyst Engineering  
    **Technology**: Streamlit + Python + Heuristic R&D Models
    
    #### Key Features:
    - ✅ 8 integrated design modules
    - ✅ Real-time performance simulation
    - ✅ Benchmarking against industry standards
    - ✅ Economic analysis and scale-up planning
    - ✅ Professional report generation
    - ✅ Multi-format export (CSV, JSON, Markdown)
    
    #### Get Started:
    1. **Load a Preset** from the sidebar to explore existing designs
    2. **Design Your Materials** (Tab 2) - Select feedstock and synthesis route
    3. **Formulate Your Membrane** (Tab 3) - Optimize polymer and nanoparticles
    4. **Configure Your Device** (Tab 4) - Set geometry and thermal mode
    5. **Run Simulation** (Tab 5) - Predict water yield under atmospheric conditions
    6. **Compare & Optimize** (Tab 6) - Benchmark against reference systems
    7. **Analyze Costs** (Tab 7) - Plan for scale-up and commercialization
    8. **Generate Reports** (Tab 8) - Export for stakeholder communication
    
    #### Need Help?
    - Read the **Quick Start** tab above for a 5-minute introduction
    - Check the **FAQ** for common questions
    - Review the **Module Guide** for detailed feature documentation
    - Look up terms in the **Glossary**
    - Explore **Tips & Tricks** for advanced usage
    
    #### Citation:
    > "AquaForge v1.0: Heuristic-based R&D Decision-Support Tool for Green Nanomaterial-Based 
    > Atmospheric Water Harvesting System Design"
    > Powered by NanoBio Studio | Bio Catalyst Engineering
    """)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #666; font-size: 0.85em;">

**{BRAND_NAME}** — {BRAND_TAGLINE} | NanoBio Studio | Bio Catalyst Engineering

This tool provides design-stage heuristic estimates for R&D guidance. All values are predictions based on 
material properties and synthesis literature. Actual performance requires bench-scale validation.

*Generated with Streamlit | Data-driven scientific engineering*

</div>
""", unsafe_allow_html=True)
