"""
Component-Aware Device Model for AquaForge
Structured prototype architecture with explicit component definitions
Supports Concept and Prototype modes for device design
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum
import math


class OperatingMode(Enum):
    """Device operating modes"""
    CONCEPT = "Concept Mode (simplified, geometric estimates)"
    PROTOTYPE = "Prototype Mode (component-aware, detailed)"


@dataclass
class ComponentSpec:
    """Single component specification in the device"""
    name: str
    quantity: int
    material: str
    estimated_weight_g: float
    estimated_cost_usd: float
    manufacturability: float  # 0-1 (1 = easy to make)
    maintenance_complexity: float  # 0-1 (1 = complex)
    lead_time_days: int
    sourcing_notes: str = ""
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "quantity": self.quantity,
            "material": self.material,
            "weight_g": self.estimated_weight_g,
            "cost_usd": self.estimated_cost_usd,
            "manufacturability": self.manufacturability,
            "maintenance": self.maintenance_complexity,
            "lead_time_days": self.lead_time_days,
            "sourcing": self.sourcing_notes,
        }


@dataclass
class ChamberVolume:
    """Calculated volume for a specific chamber region"""
    region_name: str
    volume_cm3: float
    height_cm: float
    diameter_or_base_area_cm2: float
    description: str


@dataclass
class PrototypeGeometry:
    """Component-aware geometric model of the AWH prototype"""
    operating_mode: OperatingMode
    
    # Primary dimensions (component-driven)
    upper_chamber_height_cm: float
    upper_chamber_diameter_cm: float
    inner_cone_height_cm: float
    inner_cone_base_angle_deg: float  # Full angle at apex
    outer_cone_offset_cm: float
    lower_chamber_height_cm: float
    lower_chamber_diameter_cm: float
    funnel_throat_diameter_cm: float
    
    # Components (explicit list)
    components: List[ComponentSpec] = field(default_factory=list)
    
    # Calculated properties
    total_volume_cm3: float = 0.0
    total_weight_g: float = 0.0
    total_cost_usd: float = 0.0
    manufacturing_difficulty: float = 0.0
    
    def calculate_chamber_volumes(self) -> Dict[str, ChamberVolume]:
        """
        Calculate volumes for each chamber region using component geometry.
        
        Returns:
            Dict mapping region names to ChamberVolume objects
        """
        volumes = {}
        
        # Upper cylinder chamber
        upper_vol = math.pi * ((self.upper_chamber_diameter_cm / 2) ** 2) * self.upper_chamber_height_cm
        volumes["upper_cylinder"] = ChamberVolume(
            region_name="Upper Adsorption Chamber (Cylinder)",
            volume_cm3=upper_vol,
            height_cm=self.upper_chamber_height_cm,
            diameter_or_base_area_cm2=math.pi * (self.upper_chamber_diameter_cm / 2) ** 2,
            description="Primary adsorption zone where air contacts membrane"
        )
        
        # Inner cone frustum volume
        r1 = self.upper_chamber_diameter_cm / 2
        r2 = self.funnel_throat_diameter_cm / 2
        inner_cone_vol = (math.pi * self.inner_cone_height_cm / 3) * (r1**2 + r1*r2 + r2**2)
        volumes["inner_cone"] = ChamberVolume(
            region_name="Inner Cone (Passive Cooling & Condensation)",
            volume_cm3=inner_cone_vol,
            height_cm=self.inner_cone_height_cm,
            diameter_or_base_area_cm2=math.pi * r2**2,
            description="Thermally isolated cone for passive water condensation"
        )
        
        # Outer cone (thermal isolation layer)
        r3 = r1 + self.outer_cone_offset_cm
        outer_cone_vol = (math.pi * self.inner_cone_height_cm / 3) * (r1**2 + r1*r3 + r3**2)
        outer_cone_vol = outer_cone_vol - inner_cone_vol  # Subtract inner cone
        volumes["outer_cone"] = ChamberVolume(
            region_name="Outer Cone (Thermal Insulation)",
            volume_cm3=outer_cone_vol,
            height_cm=self.inner_cone_height_cm,
            diameter_or_base_area_cm2=math.pi * r3**2,
            description="Air gap or foam insulation for thermal isolation"
        )
        
        # Lower chamber (collection & filtration)
        lower_vol = math.pi * ((self.lower_chamber_diameter_cm / 2) ** 2) * self.lower_chamber_height_cm
        volumes["lower_chamber"] = ChamberVolume(
            region_name="Lower Collection Chamber",
            volume_cm3=lower_vol,
            height_cm=self.lower_chamber_height_cm,
            diameter_or_base_area_cm2=math.pi * (self.lower_chamber_diameter_cm / 2) ** 2,
            description="Condensed water collection and optional filtration"
        )
        
        # Funnel (collection tapering)
        funnel_vol = (math.pi * 5 / 3) * (  # Estimate: 5 cm depth
            (self.funnel_throat_diameter_cm/2)**2 + 
            (self.funnel_throat_diameter_cm/2) * (self.inner_cone_height_cm/10) + 
            (self.inner_cone_height_cm/10)**2
        )
        volumes["funnel"] = ChamberVolume(
            region_name="Funnel (Liquid Routing)",
            volume_cm3=funnel_vol,
            height_cm=5.0,
            diameter_or_base_area_cm2=math.pi * (self.funnel_throat_diameter_cm / 2) ** 2,
            description="Routes condensed water to collection chamber"
        )
        
        self.total_volume_cm3 = sum(v.volume_cm3 for v in volumes.values())
        
        return volumes
    
    def calculate_surface_areas(self) -> Dict[str, float]:
        """
        Calculate internal surface areas for membrane deposition.
        
        Returns:
            Dict mapping surface names to areas in cm²
        """
        areas = {}
        
        # Upper cylinder lateral surface (where membrane is deployed)
        areas["upper_cylinder_lateral"] = math.pi * self.upper_chamber_diameter_cm * self.upper_chamber_height_cm
        
        # Inner cone lateral surface
        cone_slant = math.sqrt(self.inner_cone_height_cm**2 + (self.upper_chamber_diameter_cm/2 - self.funnel_throat_diameter_cm/2)**2)
        areas["inner_cone_lateral"] = math.pi * ((self.upper_chamber_diameter_cm/2) + (self.funnel_throat_diameter_cm/2)) * cone_slant
        
        # Outer cone lateral surface
        outer_slant = math.sqrt(self.inner_cone_height_cm**2 + (self.upper_chamber_diameter_cm/2 + self.outer_cone_offset_cm - self.funnel_throat_diameter_cm/2)**2)
        areas["outer_cone_lateral"] = math.pi * ((self.upper_chamber_diameter_cm/2 + self.outer_cone_offset_cm) + (self.funnel_throat_diameter_cm/2)) * outer_slant
        
        # Total deployable surface area (typically upper cylinder + inner cone)
        areas["total_membrane_deployable"] = areas["upper_cylinder_lateral"] + areas["inner_cone_lateral"]
        
        return areas
    
    def update_component_list(self) -> None:
        """
        Build or update component list based on current geometry and mode.
        """
        self.components = []
        
        # Top lid
        self.components.append(ComponentSpec(
            name="Top Lid (PMMA or polycarbonate)",
            quantity=1,
            material="PMMA or polycarbonate",
            estimated_weight_g=200,
            estimated_cost_usd=15,
            manufacturability=0.8,
            maintenance_complexity=0.2,
            lead_time_days=5,
            sourcing_notes="Transparent for visual inspection"
        ))
        
        # Lower glass (observation chamber)
        self.components.append(ComponentSpec(
            name="Lower Glass Panels (borosilicate)",
            quantity=3,
            material="Borosilicate glass 5mm",
            estimated_weight_g=500,
            estimated_cost_usd=45,
            manufacturability=0.6,
            maintenance_complexity=0.5,
            lead_time_days=10,
            sourcing_notes="For viewing interior and thermal isolation"
        ))
        
        # Base
        self.components.append(ComponentSpec(
            name="Base Frame (aluminum)",
            quantity=1,
            material="Aluminum 6061-T6",
            estimated_weight_g=800,
            estimated_cost_usd=35,
            manufacturability=0.7,
            maintenance_complexity=0.3,
            lead_time_days=7,
            sourcing_notes="CNC milled or machined"
        ))
        
        # Support columns
        self.components.append(ComponentSpec(
            name="Support Columns (aluminum)",
            quantity=4,
            material="Aluminum 6061-T6",
            estimated_weight_g=150,
            estimated_cost_usd=8,
            manufacturability=0.8,
            maintenance_complexity=0.2,
            lead_time_days=5,
            sourcing_notes="Vertical supports for upper chamber"
        ))
        
        # Inner cone
        self.components.append(ComponentSpec(
            name="Inner Cone (stainless steel)",
            quantity=1,
            material="Stainless steel 304",
            estimated_weight_g=600,
            estimated_cost_usd=50,
            manufacturability=0.5,
            maintenance_complexity=0.3,
            lead_time_days=14,
            sourcing_notes="Spun/formed cone. Critical for thermal isolation."
        ))
        
        # Outer cone
        self.components.append(ComponentSpec(
            name="Outer Cone (PVC)",
            quantity=1,
            material="PVC or foam-filled",
            estimated_weight_g=300,
            estimated_cost_usd=20,
            manufacturability=0.7,
            maintenance_complexity=0.2,
            lead_time_days=7,
            sourcing_notes="Provides air gap for insulation"
        ))
        
        # Funnel
        self.components.append(ComponentSpec(
            name="Funnel (stainless steel)",
            quantity=1,
            material="Stainless steel 304",
            estimated_weight_g=200,
            estimated_cost_usd=18,
            manufacturability=0.6,
            maintenance_complexity=0.2,
            lead_time_days=10,
            sourcing_notes="Routes condensed water downward"
        ))
        
        # Union rings (seals)
        self.components.append(ComponentSpec(
            name="Union Rings & Seals (silicone gaskets)",
            quantity=6,
            material="Silicone rubber",
            estimated_weight_g=30,
            estimated_cost_usd=12,
            manufacturability=0.9,
            maintenance_complexity=0.8,
            lead_time_days=3,
            sourcing_notes="O-rings for watertight seals. Replace every 6-12 months."
        ))
        
        # Lower chamber
        self.components.append(ComponentSpec(
            name="Lower Collection Chamber (stainless steel)",
            quantity=1,
            material="Stainless steel 304",
            estimated_weight_g=1200,
            estimated_cost_usd=80,
            manufacturability=0.6,
            maintenance_complexity=0.4,
            lead_time_days=14,
            sourcing_notes="Welded construction. Must be watertight."
        ))
        
        # Outlet valve
        self.components.append(ComponentSpec(
            name="Outlet Valve (ball valve)",
            quantity=1,
            material="Stainless steel",
            estimated_weight_g=150,
            estimated_cost_usd=25,
            manufacturability=0.95,
            maintenance_complexity=0.6,
            lead_time_days=2,
            sourcing_notes="For draining collected water and maintenance"
        ))
        
        # Optional filter stage
        self.components.append(ComponentSpec(
            name="Optional Filter Cartridge (activated carbon)",
            quantity=1,
            material="Activated carbon + nylon mesh",
            estimated_weight_g=100,
            estimated_cost_usd=8,
            manufacturability=0.85,
            maintenance_complexity=0.7,
            lead_time_days=5,
            sourcing_notes="Optional. Replace every 3-6 months with use."
        ))
        
        # Update totals
        self.total_weight_g = sum(c.estimated_weight_g * c.quantity for c in self.components)
        self.total_cost_usd = sum(c.estimated_cost_usd * c.quantity for c in self.components)
        self.manufacturing_difficulty = sum(
            ((1 - c.manufacturability) * 0.05) + (c.maintenance_complexity * 0.02) 
            for c in self.components
        ) / len(self.components)
    
    def get_bom(self) -> Dict:
        """
        Get Bill of Materials as structured data.
        """
        self.update_component_list()
        
        return {
            "device_mode": self.operating_mode.value,
            "total_components": len(self.components),
            "total_weight_g": self.total_weight_g,
            "total_cost_usd": self.total_cost_usd,
            "manufacturing_difficulty_score": self.manufacturing_difficulty,
            "components": [c.to_dict() for c in self.components],
        }


class ComponentAwareDeviceDesigner:
    """
    Enhanced device designer using component-aware prototype model.
    Supports Concept and Prototype modes.
    """
    
    @staticmethod
    def create_bench_prototype(
        diameter_cm: float = 20,
        height_cm: float = 30,
        cone_angle_deg: float = 45,
    ) -> PrototypeGeometry:
        """
        Create a bench-scale prototype with specified dimensions.
        """
        geom = PrototypeGeometry(
            operating_mode=OperatingMode.PROTOTYPE,
            upper_chamber_height_cm=height_cm,
            upper_chamber_diameter_cm=diameter_cm,
            inner_cone_height_cm=height_cm * 0.8,
            inner_cone_base_angle_deg=cone_angle_deg,
            outer_cone_offset_cm=2.0,  # 2 cm air gap
            lower_chamber_height_cm=height_cm * 0.6,
            lower_chamber_diameter_cm=diameter_cm * 0.8,
            funnel_throat_diameter_cm=5.0,
        )
        geom.calculate_chamber_volumes()
        geom.update_component_list()
        return geom
    
    @staticmethod
    def create_pilot_prototype(
        diameter_cm: float = 40,
        height_cm: float = 60,
        cone_angle_deg: float = 40,
    ) -> PrototypeGeometry:
        """
        Create a pilot-scale prototype.
        """
        geom = PrototypeGeometry(
            operating_mode=OperatingMode.PROTOTYPE,
            upper_chamber_height_cm=height_cm,
            upper_chamber_diameter_cm=diameter_cm,
            inner_cone_height_cm=height_cm * 0.75,
            inner_cone_base_angle_deg=cone_angle_deg,
            outer_cone_offset_cm=3.0,  # 3 cm air gap
            lower_chamber_height_cm=height_cm * 0.5,
            lower_chamber_diameter_cm=diameter_cm * 0.75,
            funnel_throat_diameter_cm=10.0,
        )
        geom.calculate_chamber_volumes()
        geom.update_component_list()
        return geom


if __name__ == "__main__":
    # Test component-aware device
    device = ComponentAwareDeviceDesigner.create_bench_prototype(diameter_cm=25, height_cm=35)
    volumes = device.calculate_chamber_volumes()
    areas = device.calculate_surface_areas()
    bom = device.get_bom()
    
    print("Bench Prototype Geometry:")
    for region, vol in volumes.items():
        print(f"  {region}: {vol.volume_cm3:.1f} cm³")
    
    print("\nMembrane Surface Areas:")
    for surface, area in areas.items():
        print(f"  {surface}: {area:.1f} cm²")
    
    print("\nBill of Materials:")
    print(f"  Total components: {bom['total_components']}")
    print(f"  Total cost: ${bom['total_cost_usd']:.2f}")
    print(f"  Total weight: {bom['total_weight_g']:.0f} g")
