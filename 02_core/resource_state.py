"""
AI Company — Canonical Resource State Core Contract

Resource State represents the currently usable computational and
operational resource capacity of the company environment.

This module belongs to the Core layer.

Resource State is distinct from:

- Hardware Capability
- Hardware Observation
- Task Evaluation
- Agent Selection
- Execution Readiness
- Execution Authorization
- Execution Attempt

Hardware Capability describes what hardware can structurally provide.

Hardware Observation describes what is observed in the physical
environment.

Resource State represents what capacity is currently considered
usable within the canonical resource model.

This module does not:

- observe hardware directly
- define structural hardware capability
- evaluate Tasks
- determine Task feasibility
- select Agents
- authorize execution
- execute work
- own Hardware Capability
- own Hardware Observation
- own Task Evaluation
- own Execution Readiness
- own Execution Authorization
- depend on Runtime
- depend on Integrations
- depend on Weft
- depend on operating-system APIs
- depend on hardware monitoring providers
- depend on external infrastructure

Interpretation of resource conditions belongs to the Resource State
authority, but Task-specific suitability remains the responsibility
of Task Evaluation.
"""

from dataclasses import dataclass
from datetime import datetime
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True)
class ResourceStateProvenance:
    """
    Provenance describing the origin of a Resource State.
    """

    source: str
    timestamp: datetime
    authority: str

    def __post_init__(self) -> None:
        if not self.source.strip():
            raise ValueError(
                "Resource state provenance source must not be empty."
            )

        if not self.authority.strip():
            raise ValueError(
                "Resource state provenance authority must not be empty."
            )

        if self.timestamp.tzinfo is None:
            raise ValueError(
                "Resource state provenance timestamp must be timezone-aware."
            )


@dataclass(frozen=True)
class ResourceState:
    """
    Canonical immutable representation of currently usable resources.

    The state describes resource conditions and usable capacity.

    It does not determine whether a specific Task is feasible.
    """

    resource_state_id: str
    hardware_id: str
    evaluated_at: datetime

    cpu_state: Mapping[str, str]
    memory_state: Mapping[str, str]
    gpu_state: Mapping[str, str]
    storage_state: Mapping[str, str]
    network_state: Mapping[str, str]
    other_resource_state: Mapping[str, str]

    provenance: ResourceStateProvenance

    def __post_init__(self) -> None:
        if not self.resource_state_id.strip():
            raise ValueError(
                "Resource state ID must not be empty."
            )

        if not self.hardware_id.strip():
            raise ValueError(
                "Hardware ID must not be empty."
            )

        if self.evaluated_at.tzinfo is None:
            raise ValueError(
                "Resource state evaluation timestamp must be timezone-aware."
            )

        object.__setattr__(
            self,
            "cpu_state",
            MappingProxyType(dict(self.cpu_state)),
        )

        object.__setattr__(
            self,
            "memory_state",
            MappingProxyType(dict(self.memory_state)),
        )

        object.__setattr__(
            self,
            "gpu_state",
            MappingProxyType(dict(self.gpu_state)),
        )

        object.__setattr__(
            self,
            "storage_state",
            MappingProxyType(dict(self.storage_state)),
        )

        object.__setattr__(
            self,
            "network_state",
            MappingProxyType(dict(self.network_state)),
        )

        object.__setattr__(
            self,
            "other_resource_state",
            MappingProxyType(dict(self.other_resource_state)),
        )


class ResourceStateAuthority:
    """
    Sole canonical authority for Resource State.

    The authority owns Resource State records.

    It does not:

    - evaluate Tasks
    - select Agents
    - determine execution readiness
    - authorize execution
    - execute work
    - allocate resources to a specific Task
    """

    def __init__(self) -> None:
        self._states: dict[str, ResourceState] = {}

    def record_state(
        self,
        state: ResourceState,
    ) -> ResourceState:
        """
        Record a canonical Resource State.

        Resource State identity must be unique.
        """
        if state.resource_state_id in self._states:
            raise ValueError(
                "Resource state already exists: "
                f"{state.resource_state_id}"
            )

        self._states[state.resource_state_id] = state

        return state

    def get_state(
        self,
        resource_state_id: str,
    ) -> ResourceState:
        """
        Return a Resource State by canonical identity.
        """
        try:
            return self._states[resource_state_id]
        except KeyError as exc:
            raise KeyError(
                f"Unknown resource state: {resource_state_id}"
            ) from exc

    def states_for(
        self,
        hardware_id: str,
    ) -> tuple[ResourceState, ...]:
        """
        Return Resource States associated with one hardware identity.

        The returned collection is immutable.
        """
        return tuple(
            state
            for state in self._states.values()
            if state.hardware_id == hardware_id
        )

    def all_states(
        self,
    ) -> Mapping[str, ResourceState]:
        """
        Return a read-only view of all canonical Resource States.
        """
        return MappingProxyType(dict(self._states))
