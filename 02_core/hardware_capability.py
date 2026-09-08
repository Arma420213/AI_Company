"""
AI Company — Canonical Hardware Capability Core Contract

Hardware Capability represents the structural physical capabilities
of hardware available to AI Company.

This module belongs to the Core layer.

It does not:
- observe current hardware conditions
- measure current utilization
- represent current resource availability
- allocate resources
- evaluate Tasks
- select Agents
- authorize execution
- execute Tasks
- own Hardware Observation
- own Resource State
- depend on Runtime
- depend on Integrations
- depend on operating-system APIs
- depend on hardware monitoring providers

Hardware Capability describes what hardware structurally provides.

Current physical conditions belong to Hardware Observation.
Usable capacity belongs to Resource State.
"""

from dataclasses import dataclass
from datetime import datetime
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True)
class HardwareCapabilityProvenance:
    """
    Provenance describing where the hardware capability information
    originated.
    """

    source: str
    timestamp: datetime
    authority: str

    def __post_init__(self) -> None:
        if not self.source.strip():
            raise ValueError(
                "Hardware capability provenance source must not be empty."
            )

        if not self.authority.strip():
            raise ValueError(
                "Hardware capability provenance authority must not be empty."
            )

        if self.timestamp.tzinfo is None:
            raise ValueError(
                "Hardware capability provenance timestamp must be timezone-aware."
            )


@dataclass(frozen=True)
class HardwareCapability:
    """
    Canonical structural description of a hardware capability profile.

    This object describes physical capability, not current physical state.

    Examples of capability:
    - CPU architecture and core/thread capacity
    - installed RAM capacity
    - GPU presence and structural characteristics
    - storage capacity
    - other structural hardware characteristics

    Runtime utilization, current availability, allocation, and execution
    suitability do not belong to this contract.
    """

    hardware_id: str
    cpu_capability: Mapping[str, str]
    memory_capability: Mapping[str, str]
    gpu_capability: Mapping[str, str]
    storage_capability: Mapping[str, str]
    other_capabilities: Mapping[str, str]
    provenance: HardwareCapabilityProvenance

    def __post_init__(self) -> None:
        if not self.hardware_id.strip():
            raise ValueError(
                "Hardware ID must not be empty."
            )

        object.__setattr__(
            self,
            "cpu_capability",
            MappingProxyType(dict(self.cpu_capability)),
        )

        object.__setattr__(
            self,
            "memory_capability",
            MappingProxyType(dict(self.memory_capability)),
        )

        object.__setattr__(
            self,
            "gpu_capability",
            MappingProxyType(dict(self.gpu_capability)),
        )

        object.__setattr__(
            self,
            "storage_capability",
            MappingProxyType(dict(self.storage_capability)),
        )

        object.__setattr__(
            self,
            "other_capabilities",
            MappingProxyType(dict(self.other_capabilities)),
        )


class HardwareCapabilityAuthority:
    """
    Sole canonical authority for Hardware Capability profiles.

    Individual HardwareCapability objects remain immutable.

    This authority does not:
    - observe hardware
    - measure utilization
    - own Resource State
    - allocate resources
    - evaluate Tasks
    - select Agents
    - authorize execution
    - execute work
    """

    def __init__(self) -> None:
        self._hardware_capabilities: dict[
            str,
            HardwareCapability,
        ] = {}

    def get_capability(
        self,
        hardware_id: str,
    ) -> HardwareCapability:
        """
        Return the canonical Hardware Capability profile identified by
        hardware_id.
        """
        try:
            return self._hardware_capabilities[hardware_id]
        except KeyError as exc:
            raise KeyError(
                f"Unknown hardware capability: {hardware_id}"
            ) from exc

    def set_capability(
        self,
        capability: HardwareCapability,
    ) -> HardwareCapability:
        """
        Register or replace a canonical Hardware Capability profile.

        Hardware Capability represents descriptive structural information,
        so controlled replacement of an existing profile is permitted.
        """
        self._hardware_capabilities[
            capability.hardware_id
        ] = capability

        return capability

    def update_capability(
        self,
        capability: HardwareCapability,
    ) -> HardwareCapability:
        """
        Replace an existing Hardware Capability profile.

        The profile must already exist.
        """
        if capability.hardware_id not in self._hardware_capabilities:
            raise KeyError(
                f"Unknown hardware capability: "
                f"{capability.hardware_id}"
            )

        self._hardware_capabilities[
            capability.hardware_id
        ] = capability

        return capability

    def all_capabilities(
        self,
    ) -> Mapping[str, HardwareCapability]:
        """
        Return a read-only view of canonical Hardware Capability profiles.
        """
        return MappingProxyType(
            self._hardware_capabilities
        )
