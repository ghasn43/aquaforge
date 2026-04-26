"""
Device configuration and architecture logic for atmospheric water harvesters.
Geometric and performance calculations for cylindrical collector design.
"""

import math
from data_models import DeviceConfiguration, DeviceClass, ThermalMode


class DeviceDesigner:
    """Engineer for device architecture and geometric calculations."""

    @staticmethod
    def calculate_chamber_volumes(device: DeviceConfiguration) -> DeviceConfiguration:
        """Calculate chamber volumes in liters."""
        # Upper chamber approximated as cylinder
        radius_cm = device.overall_diameter_cm / 2.0
        upper_volume_cm3 = math.pi * (radius_cm ** 2) * device.upper_chamber_height_cm
        device.upper_chamber_volume_l = upper_volume_cm3 / 1000.0

        # Lower chamber approximated as cylinder
        lower_volume_cm3 = math.pi * (radius_cm ** 2) * device.lower_chamber_height_cm
        device.lower_chamber_volume_l = lower_volume_cm3 / 1000.0

        # Cone volume (frustum approximation)
        # Cone goes from full diameter to funnel throat
        cone_radius_top = radius_cm
        cone_radius_bottom = device.funnel_throat_diameter_cm / 2.0
        cone_height = device.upper_chamber_height_cm * 0.4  # Approximate cone height
        cone_volume_cm3 = (
            (math.pi * cone_height / 3.0)
            * (cone_radius_top ** 2 + cone_radius_top * cone_radius_bottom + cone_radius_bottom ** 2)
        )
        device.cone_volume_l = cone_volume_cm3 / 1000.0

        return device

    @staticmethod
    def estimate_manufacturability(device: DeviceConfiguration) -> float:
        """Estimate manufacturing complexity (0-1, higher = harder)."""
        complexity = 0.0

        # Device class baseline
        class_complexity = {
            DeviceClass.BENCH_PROTOTYPE: 0.3,
            DeviceClass.PILOT_PROTOTYPE: 0.5,
            DeviceClass.FIELD_DEMONSTRATOR: 0.7,
        }.get(device.device_class, 0.5)

        complexity += class_complexity * 0.3

        # Support columns complexity (more = harder)
        column_complexity = min(0.3, device.support_columns_count * 0.1)
        complexity += column_complexity * 0.2

        # Filtration stage adds complexity
        if device.filtration_stage:
            complexity += 0.15

        # Thermal assist adds complexity
        if device.thermal_mode != ThermalMode.PASSIVE:
            complexity += 0.2

        # Chamber transparency and material affects difficulty
        if "Polycarbonate" in device.chamber_transparency:
            complexity += 0.1  # Slightly harder
        else:
            complexity += 0.05  # Glass is easier but more fragile

        # Size impact: larger = harder to prototype
        total_volume = device.upper_chamber_volume_l + device.lower_chamber_volume_l
        if total_volume > 50:
            complexity += 0.15
        elif total_volume < 5:
            complexity += 0.05

        return min(1.0, max(0.2, complexity))

    @staticmethod
    def estimate_maintenance_complexity(device: DeviceConfiguration) -> float:
        """Estimate maintenance difficulty (0-1, higher = harder)."""
        complexity = 0.0

        # Filtration stage requires regular cleaning
        if device.filtration_stage:
            complexity += 0.3

        # Thermal modes require more maintenance
        thermal_maintenance = {
            ThermalMode.PASSIVE: 0.0,
            ThermalMode.LOW_HEAT: 0.15,
            ThermalMode.SOLAR_ASSISTED: 0.20,
            ThermalMode.LAB_ASSISTED: 0.25,
        }.get(device.thermal_mode, 0.1)
        complexity += thermal_maintenance

        # Passive designs are easier to maintain
        if device.passive_assisted == "Passive":
            complexity += 0.1
        else:
            complexity += 0.3

        # Number of support columns affects accessibility
        if device.support_columns_count > 4:
            complexity += 0.1

        # Complex geometry increases maintenance burden
        if device.cone_angle_deg < 45 or device.cone_angle_deg > 75:
            complexity += 0.1

        return min(1.0, max(0.1, complexity))

    @staticmethod
    def estimate_prototype_complexity(device: DeviceConfiguration) -> float:
        """Estimate overall prototype build complexity (0-1, higher = harder)."""
        manufacturability = DeviceDesigner.estimate_manufacturability(device)
        maintenance = DeviceDesigner.estimate_maintenance_complexity(device)

        # Weighted average
        complexity = manufacturability * 0.6 + maintenance * 0.4

        return min(1.0, complexity)

    @staticmethod
    def estimate_surface_area_cm2(device: DeviceConfiguration) -> float:
        """Estimate internal membrane/film surface area."""
        radius = device.overall_diameter_cm / 2.0

        # Upper chamber internal surface (approximation)
        upper_lateral_area = 2 * math.pi * radius * device.upper_chamber_height_cm
        upper_bottom_area = math.pi * (radius ** 2)

        # Cone surface area (approximation)
        cone_slant_height = math.sqrt(
            (device.upper_chamber_height_cm ** 2)
            + ((radius - device.funnel_throat_diameter_cm / 2.0) ** 2)
        )
        cone_lateral = math.pi * (radius + device.funnel_throat_diameter_cm / 2.0) * cone_slant_height

        # Total active area (upper chamber + cone)
        total_area = upper_lateral_area + upper_bottom_area + cone_lateral

        return max(100.0, total_area)  # Minimum 100 cm²

    @staticmethod
    def get_device_summary(device: DeviceConfiguration) -> dict:
        """Generate summary of device configuration."""
        device = DeviceDesigner.calculate_chamber_volumes(device)

        return {
            "device_class": device.device_class.value,
            "dimensions": f"{device.overall_diameter_cm}cm Ø × {device.total_height_cm}cm H",
            "upper_volume_l": round(device.upper_chamber_volume_l, 2),
            "lower_volume_l": round(device.lower_chamber_volume_l, 2),
            "cone_volume_l": round(device.cone_volume_l, 2),
            "total_volume_l": round(
                device.upper_chamber_volume_l
                + device.lower_chamber_volume_l
                + device.cone_volume_l,
                2,
            ),
            "reservoir_capacity_ml": device.reservoir_capacity_ml,
            "thermal_mode": device.thermal_mode.value,
            "filtration": "Yes" if device.filtration_stage else "No",
            "passive_design": device.passive_assisted == "Passive",
            "estimated_surface_area_cm2": round(
                DeviceDesigner.estimate_surface_area_cm2(device), 0
            ),
        }

    @staticmethod
    def get_condensation_path_description(device: DeviceConfiguration) -> str:
        """Describe expected condensation and collection flow."""
        path = "**Atmospheric Water Capture Flow:**\n\n"
        path += "1. **Adsorption Phase**: Humid air enters upper chamber, moisture adsorbs onto membrane\n"
        path += "2. **Passive Heating**: Solar/ambient heat warms the device\n"
        path += "3. **Desorption Phase**: Temperature rise triggers water release from membrane\n"
        path += "4. **Condensation Zone**: Released vapor condenses on cool inner cone surfaces\n"
        path += f"5. **Collection**: Water droplets form and flow down {device.cone_angle_deg}° cone\n"
        path += f"6. **Funnel Stage**: Converges to {device.funnel_throat_diameter_cm}cm throat\n"

        if device.filtration_stage:
            path += "7. **Filtration**: Water passes through optional filter stage for purification\n"

        path += f"8. **Storage**: Collected water stored in {device.reservoir_capacity_ml}mL reservoir"

        return path

    @staticmethod
    def get_component_list(device: DeviceConfiguration) -> list:
        """Generate Bill of Materials style component list."""
        components = [
            f"Top Lid (material: {device.chamber_transparency})",
            f"Upper Chamber ({device.upper_chamber_height_cm}cm H, transparent)",
            f"Inner Cone ({device.cone_angle_deg}° angle)",
            f"Outer Cone (support structure)",
            f"Funnel ({device.funnel_throat_diameter_cm}cm throat)",
            f"Support Columns (qty: {device.support_columns_count})",
            f"Lower Chamber ({device.lower_chamber_height_cm}cm H)",
            f"Reservoir ({device.reservoir_capacity_ml}mL capacity)",
            "Outlet Valve (drain, maintenance access)",
        ]

        if device.filtration_stage:
            components.append("Filtration Stage (activated carbon / mesh)")

        if device.thermal_mode != ThermalMode.PASSIVE:
            if device.thermal_mode == ThermalMode.SOLAR_ASSISTED:
                components.append("Solar Heating Module")
            elif device.thermal_mode == ThermalMode.LAB_ASSISTED:
                components.append("Lab Heating Element (electric)")

        if device.passive_assisted == "Assisted":
            components.append("Air circulation pump (low-power)")

        components.extend([
            "Membrane/Film Insert (replaceable)",
            "Gaskets and Seals (silicone/PTFE)",
            "Fasteners (stainless steel)",
        ])

        return components

    @staticmethod
    def validate_device_config(device: DeviceConfiguration) -> list:
        """Check for design inconsistencies."""
        warnings = []

        if device.total_height_cm < device.upper_chamber_height_cm + device.lower_chamber_height_cm:
            warnings.append(
                "Total height may be too small for chamber heights specified"
            )

        if device.cone_angle_deg < 30 or device.cone_angle_deg > 85:
            warnings.append(
                f"Cone angle {device.cone_angle_deg}° is unusual - consider 45-70° range"
            )

        if device.funnel_throat_diameter_cm > device.overall_diameter_cm / 2.0:
            warnings.append("Funnel throat larger than practical - will not converge properly")

        if device.reservoir_capacity_ml < 100 and device.device_class == DeviceClass.FIELD_DEMONSTRATOR:
            warnings.append("Small reservoir for field demonstrator - may need frequent emptying")

        if device.support_columns_count < 2:
            warnings.append("Device may be unstable with less than 2 support columns")

        return warnings

    @staticmethod
    def get_device_class_options() -> dict:
        """Return available device classes."""
        return {dc: dc.value for dc in DeviceClass}

    @staticmethod
    def get_thermal_mode_options() -> dict:
        """Return available thermal modes."""
        return {tm: tm.value for tm in ThermalMode}
