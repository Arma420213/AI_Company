"""
AI Company — Canonical Hardware Observation Core Contract

Hardware Observation represents observed physical conditions
of the hardware environment.

This module belongs to the Core layer.

It does not:
- define structural hardware capability
- determine usable resource capacity
- allocate resources
- evaluate Tasks
- select Agents
- authorize execution
- execute Tasks
- own Hardware Capability
- own Resource State
- depend on Runtime
- depend on Integrations
- depend on operating-system APIs
- depend on hardware monitoring providers

Hardware Observation is descriptive.

It records what was observed.

Interpretation into Resource State belongs to the Resource State
authority.
"""

from dataclasses import dataclass
from datetime import datetime
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True)
class HardwareObservationProvenance:
    """
    Provenance describing where an observation originated.
    """

    source: str
    timestamp: datetime
    authority: str

    def __post_init__(self) -> None:
        if not self.source.strip():
            raise ValueError(
                "Hardware observation provenance source must not be empty."
            )

        if not self.authority.strip():
            raise ValueError(
                "Hardware observation provenance authority must not be empty."
            )

        if self.timestamp.tzinfo is None:
            raise ValueError(
                "Hardware observation provenance timestamp must be timezone-aware."
            )


@dataclass(frozen=True)
class HardwareObservation:
    """
    Canonical descriptive record of observed hardware conditions.

    This object represents measurements or observations.

    It does not interpret those observations into resource capacity,
    execution feasibility, Task suitability, Agent selection,
    authorization, or allocation.
    """

    hardware_id: str
    observed_at: datetime
    cpu_observation: Mapping[str, str]
    memory_observation: Mapping[str, str]
    gpu_observation: Mapping[str, str]
    storage_observation: Mapping[str, str]
    other_observations: Mapping[str, str]
    provenance: HardwareObservationProvenance

    def __post_init__(self) -> None:
        if not self.hardware_id.strip():
            raise ValueError(
                "Hardware ID must not be empty."
            )

        if self.observed_at.tzinfo is None:
            raise ValueError(
                "Hardware observation timestamp must be timezone-aware."
            )

        object.__setattr__(
            self,
            "cpu_observation",
            MappingProxyType(dict(self.cpu_observation)),
        )

        object.__setattr__(
            self,
            "memory_observation",
            MappingProxyType(dict(self.memory_observation)),
        )

        object.__setattr__(
            self,
            "gpu_observation",
            MappingProxyType(dict(self.gpu_observation)),
        )

        object.__setattr__(
            self,
            "storage_observation",
            MappingProxyType(dict(self.storage_observation)),
        )

        object.__setattr__(
            self,
            "other_observations",
            MappingProxyType(dict(self.other_observations)),
        )


class HardwareObserver:
    """
    Sole canonical authority for Hardware Observation records.

    The observer records descriptive observations.

    It does not:
    - interpret observations into Resource State
    - evaluate Tasks
    - select Agents
    - authorize execution
    - allocate resources
    - execute work
    """

    def __init__(self) -> None:
        self._observations: dict[
            str,
            list[HardwareObservation],
        ] = {}

    def record_observation(
        self,
        observation: HardwareObservation,
    ) -> HardwareObservation:
        """
        Record a new canonical Hardware Observation.
        """
        self._observations.setdefault(
            observation.hardware_id,
            [],
        ).append(observation)

        return observation

    def get_observation(
        self,
        hardware_id: str,
        observed_at: datetime,
    ) -> HardwareObservation:
        """
        Return the observation identified by hardware ID and timestamp.
        """
        for observation in self._observations.get(hardware_id, []):
            if observation.observed_at == observed_at:
                return observation

        raise KeyError(
            "Unknown hardware observation: "
            f"{hardware_id} @ {observed_at.isoformat()}"
        )

    def observations_for(
        self,
        hardware_id: str,
    ) -> tuple[HardwareObservation, ...]:
        """
        Return observations for one hardware identity.

        The returned collection is immutable.
        """
        return tuple(
            self._observations.get(hardware_id, [])
        )

    def all_observations(
        self,
    ) -> Mapping[str, tuple[HardwareObservation, ...]]:
        """
        Return a read-only view of all canonical observations.
        """
        return MappingProxyType(
            {
                hardware_id: tuple(observations)
                for hardware_id, observations
                in self._observations.items()
            }
        )
