"""
AquaForge - Atmospheric Water Harvesting Suite
Main module initialization
Brand: Engineer Water from Air
"""

__version__ = "1.0.0"
__author__ = "NanoBio Studio - Bio Catalyst Engineering"
__brand__ = "AquaForge"
__tagline__ = "Engineer Water from Air"
__description__ = "Professional R&D tool for green nanomaterial-based atmospheric water harvesting system design"

from data_models import *
from materials_logic import MaterialsDesigner
from membrane_logic import MembraneDesigner
from device_logic import DeviceDesigner
from simulator_logic import AwhSimulator
from benchmarking_logic import BenchmarkingLab
from costing_logic import CostingEngine
from reports_logic import ReportGenerator
from utils import *
from help_content import BRAND_NAME, BRAND_TAGLINE, BRAND_DESCRIPTION

__all__ = [
    "MaterialsDesigner",
    "MembraneDesigner",
    "DeviceDesigner",
    "AwhSimulator",
    "BenchmarkingLab",
    "CostingEngine",
    "ReportGenerator",
    "create_default_project",
    "get_preset_projects",
    "BRAND_NAME",
    "BRAND_TAGLINE",
    "BRAND_DESCRIPTION",
]
