"""
Project Versioning & Design Traceability for AquaForge
Tracks design history, provides design provenance, version control, and audit trail
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum
import json


class VersionStatus(Enum):
    """Status of a design version"""
    DRAFT = "Draft (not yet validated)"
    CONCEPT = "Concept (preliminary design)"
    OPTIMIZED = "Optimized (parameter tuning complete)"
    VALIDATED = "Validated (experimental data acquired)"
    ARCHIVED = "Archived (historical)"


@dataclass
class DesignChange:
    """Single design parameter change"""
    timestamp: str  # ISO format
    parameter_name: str
    old_value: Any
    new_value: Any
    reason: str  # Why was this changed?
    confidence_before: float  # 0-1
    confidence_after: float  # 0-1


@dataclass
class ValidationResult:
    """Experimental validation against this design"""
    validation_date: str
    validation_type: str  # "nanomaterial_characterization", "water_sorption", "device_test"
    metric_name: str
    predicted_value: float
    actual_value: float
    accuracy_pct: float  # (actual - predicted) / predicted * 100
    notes: str
    confidence_impact: float  # -1 to +1 (does this boost or reduce confidence?)


@dataclass
class ProjectVersion:
    """A complete snapshot of design at a point in time"""
    version_number: str  # e.g., "1.0.0", "1.1.0-beta"
    creation_date: str  # ISO format
    created_by: str  # User or AI agent
    status: VersionStatus
    
    # Design parameters (JSON-serializable snapshot)
    feedstock_type: str
    synthesis_route: str
    polymer_matrix: str
    nanoparticle_type: str
    nanoparticle_loading_pct: float
    device_diameter_cm: float
    device_height_cm: float
    
    # Performance predictions
    predicted_water_yield_l_kg_day: float
    predicted_sustainability_score: float
    predicted_cost_per_liter_usd: float
    predicted_trl_level: int
    
    # Provenance
    design_changes: List[DesignChange] = field(default_factory=list)
    validation_results: List[ValidationResult] = field(default_factory=list)
    design_notes: str = ""
    assumptions: List[str] = field(default_factory=list)
    
    # Metadata
    parent_version: Optional[str] = None  # Version this was derived from
    modification_reason: str = ""  # Why was this version created?
    is_published: bool = False  # Ready for stakeholder sharing?
    
    def get_summary(self) -> Dict:
        """Return structured version summary"""
        return {
            "version": self.version_number,
            "status": self.status.value,
            "created": self.creation_date,
            "created_by": self.created_by,
            "design": {
                "feedstock": self.feedstock_type,
                "synthesis": self.synthesis_route,
                "polymer": self.polymer_matrix,
                "nanoparticle": f"{self.nanoparticle_type} @ {self.nanoparticle_loading_pct}%",
                "device": f"{self.device_diameter_cm}cm ø × {self.device_height_cm}cm H",
            },
            "predictions": {
                "water_yield": f"{self.predicted_water_yield_l_kg_day:.3f} L/kg/day",
                "sustainability": f"{self.predicted_sustainability_score:.2f}/1.0",
                "cost_per_liter": f"${self.predicted_cost_per_liter_usd:.2f}",
                "trl_level": self.predicted_trl_level,
            },
            "changes_count": len(self.design_changes),
            "validations_count": len(self.validation_results),
            "is_published": self.is_published,
        }
    
    def to_json_dict(self) -> Dict:
        """Convert to JSON-serializable dictionary"""
        return {
            "version_number": self.version_number,
            "creation_date": self.creation_date,
            "created_by": self.created_by,
            "status": self.status.value,
            "feedstock_type": self.feedstock_type,
            "synthesis_route": self.synthesis_route,
            "polymer_matrix": self.polymer_matrix,
            "nanoparticle_type": self.nanoparticle_type,
            "nanoparticle_loading_pct": self.nanoparticle_loading_pct,
            "device_diameter_cm": self.device_diameter_cm,
            "device_height_cm": self.device_height_cm,
            "predicted_water_yield_l_kg_day": self.predicted_water_yield_l_kg_day,
            "predicted_sustainability_score": self.predicted_sustainability_score,
            "predicted_cost_per_liter_usd": self.predicted_cost_per_liter_usd,
            "predicted_trl_level": self.predicted_trl_level,
            "design_changes": [asdict(dc) for dc in self.design_changes],
            "validation_results": [asdict(vr) for vr in self.validation_results],
            "design_notes": self.design_notes,
            "assumptions": self.assumptions,
            "parent_version": self.parent_version,
            "modification_reason": self.modification_reason,
            "is_published": self.is_published,
        }


class ProjectVersionManager:
    """
    Manages design versions, tracks changes, and maintains design history.
    """
    
    def __init__(self):
        self.versions: List[ProjectVersion] = []
        self.current_version_idx: int = -1
    
    def create_initial_version(
        self,
        feedstock: str,
        synthesis_route: str,
        polymer: str,
        nanoparticle_type: str,
        nanoparticle_loading: float,
        device_diameter: float,
        device_height: float,
        predicted_yield: float,
        created_by: str = "User",
    ) -> ProjectVersion:
        """Create the first version of a design."""
        version = ProjectVersion(
            version_number="1.0.0",
            creation_date=datetime.now().isoformat(),
            created_by=created_by,
            status=VersionStatus.CONCEPT,
            feedstock_type=feedstock,
            synthesis_route=synthesis_route,
            polymer_matrix=polymer,
            nanoparticle_type=nanoparticle_type,
            nanoparticle_loading_pct=nanoparticle_loading,
            device_diameter_cm=device_diameter,
            device_height_cm=device_height,
            predicted_water_yield_l_kg_day=predicted_yield,
            predicted_sustainability_score=0.75,
            predicted_cost_per_liter_usd=2.50,
            predicted_trl_level=3,
            parent_version=None,
        )
        
        self.versions.append(version)
        self.current_version_idx = len(self.versions) - 1
        return version
    
    def create_derived_version(
        self,
        parent_version_idx: int,
        modification_reason: str,
        updates: Dict[str, Any],
        created_by: str = "User",
    ) -> ProjectVersion:
        """
        Create a new version derived from an existing one.
        
        Args:
            parent_version_idx: Index of parent version
            modification_reason: Why is this new version created?
            updates: Dict of parameter changes (e.g., {"nanoparticle_loading_pct": 15})
            created_by: Who created this version
        
        Returns:
            New ProjectVersion
        """
        if parent_version_idx >= len(self.versions):
            raise ValueError("Invalid parent version index")
        
        parent = self.versions[parent_version_idx]
        
        # Create new version as copy of parent
        new_version = ProjectVersion(
            version_number=self._increment_version(parent.version_number),
            creation_date=datetime.now().isoformat(),
            created_by=created_by,
            status=VersionStatus.DRAFT,
            feedstock_type=parent.feedstock_type,
            synthesis_route=parent.synthesis_route,
            polymer_matrix=parent.polymer_matrix,
            nanoparticle_type=parent.nanoparticle_type,
            nanoparticle_loading_pct=parent.nanoparticle_loading_pct,
            device_diameter_cm=parent.device_diameter_cm,
            device_height_cm=parent.device_height_cm,
            predicted_water_yield_l_kg_day=parent.predicted_water_yield_l_kg_day,
            predicted_sustainability_score=parent.predicted_sustainability_score,
            predicted_cost_per_liter_usd=parent.predicted_cost_per_liter_usd,
            predicted_trl_level=parent.predicted_trl_level,
            parent_version=parent.version_number,
            modification_reason=modification_reason,
        )
        
        # Track changes
        for param_name, new_value in updates.items():
            old_value = getattr(parent, param_name, None)
            if old_value is not None and old_value != new_value:
                change = DesignChange(
                    timestamp=datetime.now().isoformat(),
                    parameter_name=param_name,
                    old_value=old_value,
                    new_value=new_value,
                    reason=modification_reason,
                    confidence_before=0.6,
                    confidence_after=0.6,
                )
                new_version.design_changes.append(change)
            
            # Apply update
            setattr(new_version, param_name, new_value)
        
        # Copy assumptions and notes from parent
        new_version.assumptions = parent.assumptions.copy()
        new_version.design_notes = parent.design_notes
        
        self.versions.append(new_version)
        self.current_version_idx = len(self.versions) - 1
        return new_version
    
    def add_validation(
        self,
        version_idx: int,
        validation: ValidationResult,
    ) -> None:
        """Add experimental validation result to a version."""
        if version_idx < len(self.versions):
            self.versions[version_idx].validation_results.append(validation)
    
    def get_version_history(self) -> List[Dict]:
        """Get timeline of all versions"""
        return [v.get_summary() for v in self.versions]
    
    def get_current_version(self) -> Optional[ProjectVersion]:
        """Get the current active version"""
        if 0 <= self.current_version_idx < len(self.versions):
            return self.versions[self.current_version_idx]
        return None
    
    def get_change_log(self, version_idx: int) -> str:
        """Get human-readable changelog for a version"""
        if version_idx >= len(self.versions):
            return "Version not found"
        
        v = self.versions[version_idx]
        log = f"## Version {v.version_number} Changelog\n\n"
        
        if v.parent_version:
            log += f"**Derived from**: {v.parent_version}\n"
            log += f"**Reason**: {v.modification_reason}\n\n"
        
        if v.design_changes:
            log += "### Parameter Changes\n"
            for change in v.design_changes:
                log += f"- **{change.parameter_name}**: {change.old_value} → {change.new_value}\n"
                log += f"  - Reason: {change.reason}\n"
                log += f"  - Confidence: {change.confidence_before:.1%} → {change.confidence_after:.1%}\n"
        
        if v.validation_results:
            log += "\n### Experimental Validations\n"
            for vr in v.validation_results:
                log += f"- **{vr.metric_name}** ({vr.validation_type})\n"
                log += f"  - Predicted: {vr.predicted_value}, Actual: {vr.actual_value}\n"
                log += f"  - Accuracy: {vr.accuracy_pct:+.1f}%\n"
        
        return log
    
    @staticmethod
    def _increment_version(version_str: str) -> str:
        """Increment semantic version"""
        parts = version_str.split(".")
        if len(parts) >= 2:
            parts[1] = str(int(parts[1]) + 1)
            return ".".join(parts)
        return version_str


if __name__ == "__main__":
    # Test version manager
    vm = ProjectVersionManager()
    
    v1 = vm.create_initial_version(
        feedstock="peanut_shell",
        synthesis_route="green_synthesis",
        polymer="pure_chitosan",
        nanoparticle_type="silica",
        nanoparticle_loading=10,
        device_diameter=20,
        device_height=30,
        predicted_yield=0.35,
    )
    
    print("Initial Version:")
    print(json.dumps(v1.get_summary(), indent=2))
    
    v2 = vm.create_derived_version(
        parent_version_idx=0,
        modification_reason="Increased nanoparticle loading to boost adsorption",
        updates={"nanoparticle_loading_pct": 15},
    )
    
    print("\nVersion History:")
    for summary in vm.get_version_history():
        print(f"  {summary['version']}: {summary['status']}")
