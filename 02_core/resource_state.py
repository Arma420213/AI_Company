"""
AI Company — Canonical Resource State Core Contract

Resource State represents the currently usable finite resource capacity
of the company environment.

This module belongs to the Core layer.

Canonical derivation:

    Hardware Capability
            +
    Hardware Observation
            +
    Resource Interpretation Rules
            +
    Resource Constraints
            |
            v
      Resource Values
            |
            v
      Resource State

This module owns the semantic boundary for Resource State.

It does not:
- observe hardware directly
- define structural hardware capability
- redefine Hardware Observation
- evaluate Tasks
- determine Task feasibility
- select Agents
- determine execution readiness
- authorize execution
- schedule work
- allocate resources to Tasks
- execute work
- depend on Runtime
- depend on Integrations
- depend on Weft
- depend on operating-system APIs
- depend on hardware-monitoring providers
- depend on external infrastructure
"""


from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from math import isfinite
from types import MappingProxyType
from typing import Mapping, Optional


class ResourceValueStatus(str, Enum):
    """
    Canonical semantic status of one Resource Value.

    These statuses belong exclusively to the Resource State domain.

    They must not be confused with Execution Readiness states.
    """

    KNOWN = "KNOWN"
    UNAVAILABLE = "UNAVAILABLE"
    UNOBSERVED = "UNOBSERVED"
    INCOMPLETE = "INCOMPLETE"
    CONSTRAINED = "CONSTRAINED"


@dataclass(frozen=True)
class ResourceValue:
    """
    Canonical interpreted value of one resource dimension.

    A Resource Value is neither raw hardware capability nor raw
    hardware observation.

    Quantity is optional because not every resource dimension has
    a canonical numeric representation.

    Absence of quantity never means zero.
    """

    dimension: str
    status: ResourceValueStatus
    quantity: Optional[float] = None
    unit: Optional[str] = None
    limitation: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.dimension.strip():
            raise ValueError(
                "Resource value dimension must not be empty."
            )

        if self.unit is not None and not self.unit.strip():
            raise ValueError(
                "Resource value unit must not be empty when provided."
            )

        if (
            self.limitation is not None
            and not self.limitation.strip()
        ):
            raise ValueError(
                "Resource value limitation must not be empty when provided."
            )

        if self.quantity is not None:
            if not isfinite(self.quantity):
                raise ValueError(
                    "Resource value quantity must be finite."
                )

            if self.quantity < 0:
                raise ValueError(
                    "Resource value quantity must not be negative."
                )

        if self.status == ResourceValueStatus.KNOWN:
            quantitative_dimensions = {
                "cpu",
                "memory",
                "gpu",
                "storage",
            }

            if (
                self.dimension in quantitative_dimensions
                and self.quantity is None
            ):
                raise ValueError(
                    "KNOWN quantitative resource values require "
                    "a quantity."
                )

        if self.status == ResourceValueStatus.UNAVAILABLE:
            if self.quantity is not None:
                raise ValueError(
                    "UNAVAILABLE resource values must not expose "
                    "a usable quantity."
                )

        if self.status == ResourceValueStatus.UNOBSERVED:
            if self.quantity is not None:
                raise ValueError(
                    "UNOBSERVED resource values must not expose "
                    "a usable quantity."
                )

        if self.status == ResourceValueStatus.INCOMPLETE:
            if self.quantity is not None:
                raise ValueError(
                    "INCOMPLETE resource values must not expose "
                    "a complete usable quantity."
                )

        if self.status == ResourceValueStatus.CONSTRAINED:
            if not self.limitation:
                raise ValueError(
                    "CONSTRAINED resource values require a limitation."
                )

            # Network is currently the canonical semantic dimension.
            # It may therefore be constrained without a quantitative
            # usable quantity. Quantitative dimensions must expose the
            # interpreted usable quantity when constrained.
            if self.dimension != "network" and self.quantity is None:
                raise ValueError(
                    "quantitative CONSTRAINED resource values require "
                    "an interpreted usable quantity."
                )


@dataclass(frozen=True)
class ResourceInterpretationRules:
    """
    Immutable semantic rules used by Resource State Authority.

    These rules are inputs to Resource State derivation.

    They are not a separate authority.
    """

    freshness_threshold: Optional[timedelta] = None
    stale_status: ResourceValueStatus = (
        ResourceValueStatus.UNAVAILABLE
    )
    unknown_status: ResourceValueStatus = (
        ResourceValueStatus.UNOBSERVED
    )
    incomplete_status: ResourceValueStatus = (
        ResourceValueStatus.INCOMPLETE
    )
    inconsistent_status: ResourceValueStatus = (
        ResourceValueStatus.UNAVAILABLE
    )

    def __post_init__(self) -> None:
        if self.freshness_threshold is not None:
            if self.freshness_threshold < timedelta(0):
                raise ValueError(
                    "Freshness threshold must not be negative."
                )

        allowed_statuses = {
            ResourceValueStatus.UNAVAILABLE,
            ResourceValueStatus.UNOBSERVED,
            ResourceValueStatus.INCOMPLETE,
        }

        if self.stale_status not in allowed_statuses:
            raise ValueError(
                "Stale observations must resolve to an uncertainty "
                "or unavailable status."
            )

        if self.unknown_status not in allowed_statuses:
            raise ValueError(
                "Unknown information must resolve to an uncertainty "
                "or unavailable status."
            )

        if self.incomplete_status not in allowed_statuses:
            raise ValueError(
                "Incomplete information must resolve to an uncertainty "
                "or unavailable status."
            )

        if self.inconsistent_status not in allowed_statuses:
            raise ValueError(
                "Inconsistent information must resolve to an uncertainty "
                "or unavailable status."
            )


@dataclass(frozen=True)
class ResourceConstraints:
    """
    Immutable canonical resource constraints.

    Constraints can reduce usable capacity.

    They cannot create physical capacity.

    These constraints are intentionally resource-domain semantics.
    They are not scheduling, allocation, authorization, or Task policy.
    """

    reserved: Mapping[str, float]
    committed: Mapping[str, float]
    contention: Mapping[str, float]
    environmental_limitations: Mapping[str, str]
    operational_restrictions: Mapping[str, str]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "reserved",
            self._freeze_quantities(
                self.reserved,
                "reserved",
            ),
        )

        object.__setattr__(
            self,
            "committed",
            self._freeze_quantities(
                self.committed,
                "committed",
            ),
        )

        object.__setattr__(
            self,
            "contention",
            self._freeze_quantities(
                self.contention,
                "contention",
            ),
        )

        object.__setattr__(
            self,
            "environmental_limitations",
            self._freeze_text_mapping(
                self.environmental_limitations,
                "environmental limitations",
            ),
        )

        object.__setattr__(
            self,
            "operational_restrictions",
            self._freeze_text_mapping(
                self.operational_restrictions,
                "operational restrictions",
            ),
        )

    @staticmethod
    def _freeze_quantities(
        values: Mapping[str, float],
        field_name: str,
    ) -> Mapping[str, float]:
        normalized: dict[str, float] = {}

        for dimension, value in values.items():
            if not dimension.strip():
                raise ValueError(
                    f"{field_name} dimension must not be empty."
                )

            if not isfinite(value):
                raise ValueError(
                    f"{field_name} values must be finite."
                )

            if value < 0:
                raise ValueError(
                    f"{field_name} values must not be negative."
                )

            normalized[dimension] = float(value)

        return MappingProxyType(normalized)

    @staticmethod
    def _freeze_text_mapping(
        values: Mapping[str, str],
        field_name: str,
    ) -> Mapping[str, str]:
        normalized: dict[str, str] = {}

        for dimension, value in values.items():
            if not dimension.strip():
                raise ValueError(
                    f"{field_name} dimension must not be empty."
                )

            if not value.strip():
                raise ValueError(
                    f"{field_name} explanations must not be empty."
                )

            normalized[dimension] = value

        return MappingProxyType(normalized)

    @classmethod
    def empty(cls) -> "ResourceConstraints":
        """
        Return an immutable constraint set with no reductions.
        """
        return cls(
            reserved={},
            committed={},
            contention={},
            environmental_limitations={},
            operational_restrictions={},
        )

    def reduction_for(
        self,
        dimension: str,
    ) -> float:
        """
        Return the total quantitative reduction for one dimension.

        Constraints are additive reductions.

        This method does not allocate capacity to any Task.
        """
        return (
            self.reserved.get(dimension, 0.0)
            + self.committed.get(dimension, 0.0)
            + self.contention.get(dimension, 0.0)
        )

    def limitation_for(
        self,
        dimension: str,
    ) -> Optional[str]:
        """
        Return a human-readable canonical limitation for a dimension.
        """
        limitations = []

        environmental = self.environmental_limitations.get(
            dimension
        )
        if environmental:
            limitations.append(
                f"environmental limitation: {environmental}"
            )

        operational = self.operational_restrictions.get(
            dimension
        )
        if operational:
            limitations.append(
                f"operational restriction: {operational}"
            )

        reduction = self.reduction_for(dimension)

        if reduction > 0:
            limitations.append(
                f"resource constraint reduction: {reduction:g}"
            )

        if not limitations:
            return None

        return "; ".join(limitations)


@dataclass(frozen=True)
class ResourceStateProvenance:
    """
    Provenance describing the derivation of a Resource State.
    """

    source: str
    timestamp: datetime
    authority: str
    observation_timestamp: Optional[datetime] = None
    observation_source: Optional[str] = None
    interpretation_rules: str = "ResourceInterpretationRules"
    constraints_source: str = "ResourceConstraints"

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

        if (
            self.observation_timestamp is not None
            and self.observation_timestamp.tzinfo is None
        ):
            raise ValueError(
                "Observation provenance timestamp must be timezone-aware."
            )

        if not self.interpretation_rules.strip():
            raise ValueError(
                "Interpretation rules provenance must not be empty."
            )

        if not self.constraints_source.strip():
            raise ValueError(
                "Constraints provenance must not be empty."
            )


@dataclass(frozen=True)
class ResourceState:
    """
    Canonical immutable snapshot of currently usable resources.

    Every resource dimension is represented as a Resource Value.

    Resource State itself does not answer whether a specific Task can run.
    """

    resource_state_id: str
    hardware_id: str
    evaluated_at: datetime

    cpu: ResourceValue
    memory: ResourceValue
    gpu: ResourceValue
    storage: ResourceValue
    network: ResourceValue
    other_resources: Mapping[str, ResourceValue]

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
                "Resource state evaluation timestamp must be "
                "timezone-aware."
            )

        expected_dimensions = {
            "cpu": self.cpu,
            "memory": self.memory,
            "gpu": self.gpu,
            "storage": self.storage,
            "network": self.network,
        }

        for field_name, value in expected_dimensions.items():
            if value.dimension != field_name:
                raise ValueError(
                    f"{field_name} Resource Value has incorrect "
                    f"dimension: {value.dimension}"
                )

        normalized_other: dict[str, ResourceValue] = {}

        for dimension, value in self.other_resources.items():
            if not dimension.strip():
                raise ValueError(
                    "Other resource dimension must not be empty."
                )

            if value.dimension != dimension:
                raise ValueError(
                    f"Other resource key '{dimension}' does not "
                    f"match Resource Value dimension "
                    f"'{value.dimension}'."
                )

            normalized_other[dimension] = value

        object.__setattr__(
            self,
            "other_resources",
            MappingProxyType(normalized_other),
        )

    def values(self) -> Mapping[str, ResourceValue]:
        """
        Return all canonical Resource Values as a read-only mapping.
        """
        values = {
            "cpu": self.cpu,
            "memory": self.memory,
            "gpu": self.gpu,
            "storage": self.storage,
            "network": self.network,
        }

        values.update(self.other_resources)

        return MappingProxyType(values)

    def value_for(
        self,
        dimension: str,
    ) -> ResourceValue:
        """
        Return the Resource Value for one canonical dimension.
        """
        try:
            return self.values()[dimension]
        except KeyError as exc:
            raise KeyError(
                f"Unknown resource dimension: {dimension}"
            ) from exc


class ResourceStateAuthority:
    """
    Sole canonical authority for Resource State.

    Responsibilities:
    - interpret canonical Hardware Capability
    - interpret canonical Hardware Observation
    - apply Resource Interpretation Rules
    - apply Resource Constraints
    - derive Resource Values
    - derive Resource State
    - own Resource State history

    This authority does not:
    - evaluate Tasks
    - select Agents
    - determine execution readiness
    - authorize execution
    - schedule work
    - allocate resources to Tasks
    - execute work
    """

    def __init__(self) -> None:
        self._states: dict[str, ResourceState] = {}

    def derive_state(
        self,
        capability,
        observation,
        rules: ResourceInterpretationRules,
        constraints: ResourceConstraints,
        *,
        resource_state_id: str,
        evaluated_at: Optional[datetime] = None,
    ) -> ResourceState:
        """
        Derive one canonical Resource State.

        The input objects are expected to be the canonical
        HardwareCapability and HardwareObservation Core contracts.

        No Task, Agent, Runtime, Integration, or provider-specific
        object participates in this derivation.
        """
        self._validate_input_identity(
            capability,
            observation,
        )

        evaluation_time = evaluated_at or datetime.now(timezone.utc)

        if evaluation_time.tzinfo is None:
            raise ValueError(
                "Resource state evaluation timestamp must be "
                "timezone-aware."
            )

        if evaluation_time < observation.observed_at:
            raise ValueError(
                "Resource state evaluation timestamp cannot precede "
                "the hardware observation timestamp."
            )

        cpu = self._derive_quantitative_value(
            dimension="cpu",
            capability=capability.cpu_capability,
            observation=observation.cpu_observation,
            evaluated_at=evaluation_time,
            observed_at=observation.observed_at,
            rules=rules,
            constraints=constraints,
        )

        memory = self._derive_quantitative_value(
            dimension="memory",
            capability=capability.memory_capability,
            observation=observation.memory_observation,
            evaluated_at=evaluation_time,
            observed_at=observation.observed_at,
            rules=rules,
            constraints=constraints,
        )

        gpu = self._derive_gpu_value(
            capability=capability.gpu_capability,
            observation=observation.gpu_observation,
            evaluated_at=evaluation_time,
            observed_at=observation.observed_at,
            rules=rules,
            constraints=constraints,
        )

        storage = self._derive_quantitative_value(
            dimension="storage",
            capability=capability.storage_capability,
            observation=observation.storage_observation,
            evaluated_at=evaluation_time,
            observed_at=observation.observed_at,
            rules=rules,
            constraints=constraints,
        )

        network = self._derive_network_value(
            observation=observation.other_observations,
            evaluated_at=evaluation_time,
            observed_at=observation.observed_at,
            rules=rules,
            constraints=constraints,
        )

        other_resources = self._derive_other_resources(
            observation=observation.other_observations,
            evaluated_at=evaluation_time,
            observed_at=observation.observed_at,
            rules=rules,
            constraints=constraints,
        )

        provenance = ResourceStateProvenance(
            source="ResourceStateAuthority",
            timestamp=evaluation_time,
            authority="ResourceStateAuthority",
            observation_timestamp=observation.observed_at,
            observation_source=observation.provenance.source,
            interpretation_rules="ResourceInterpretationRules",
            constraints_source="ResourceConstraints",
        )

        state = ResourceState(
            resource_state_id=resource_state_id,
            hardware_id=capability.hardware_id,
            evaluated_at=evaluation_time,
            cpu=cpu,
            memory=memory,
            gpu=gpu,
            storage=storage,
            network=network,
            other_resources=other_resources,
            provenance=provenance,
        )

        return self.record_state(state)

    def record_state(
        self,
        state: ResourceState,
    ) -> ResourceState:
        """
        Record a Resource State that has already passed canonical
        derivation.

        This method does not interpret arbitrary mappings into
        Resource Values and therefore cannot create canonical
        semantics by wrapping caller-provided raw values.
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
        Return immutable Resource State history for one hardware identity.
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

    @staticmethod
    def _validate_input_identity(
        capability,
        observation,
    ) -> None:
        if capability.hardware_id != observation.hardware_id:
            raise ValueError(
                "Hardware Capability and Hardware Observation "
                "must describe the same hardware identity."
            )

    @staticmethod
    def _observation_is_stale(
        evaluated_at: datetime,
        observed_at: datetime,
        rules: ResourceInterpretationRules,
    ) -> bool:
        if rules.freshness_threshold is None:
            return False

        age = evaluated_at - observed_at

        return age > rules.freshness_threshold

    @classmethod
    def _derive_quantitative_value(
        cls,
        *,
        dimension: str,
        capability: Mapping[str, str],
        observation: Mapping[str, str],
        evaluated_at: datetime,
        observed_at: datetime,
        rules: ResourceInterpretationRules,
        constraints: ResourceConstraints,
    ) -> ResourceValue:
        if cls._observation_is_stale(
            evaluated_at,
            observed_at,
            rules,
        ):
            return ResourceValue(
                dimension=dimension,
                status=rules.stale_status,
                limitation="hardware observation is stale",
            )

        capability_quantity = cls._extract_quantity(
            capability,
            (
                "capacity",
                "total",
                "usable_capacity",
                "cores",
                "threads",
                "gb",
                "capacity_gb",
            ),
        )

        observation_quantity = cls._extract_quantity(
            observation,
            (
                "usable",
                "available",
                "capacity",
                "usable_capacity",
                "available_gb",
                "usable_gb",
                "cores",
                "threads",
                "gb",
                "capacity_gb",
            ),
        )

        if observation_quantity is None:
            if not observation:
                return ResourceValue(
                    dimension=dimension,
                    status=rules.unknown_status,
                    limitation="resource observation unavailable",
                )

            return ResourceValue(
                dimension=dimension,
                status=rules.incomplete_status,
                limitation="resource observation is incomplete",
            )

        if observation_quantity < 0:
            return ResourceValue(
                dimension=dimension,
                status=rules.inconsistent_status,
                limitation="negative resource observation",
            )

        unconstrained = observation_quantity

        if (
            capability_quantity is not None
            and unconstrained > capability_quantity
        ):
            return ResourceValue(
                dimension=dimension,
                status=rules.inconsistent_status,
                limitation=(
                    "observed usable capacity exceeds structural "
                    "hardware capability"
                ),
            )

        reduction = constraints.reduction_for(dimension)

        if reduction > unconstrained:
            return ResourceValue(
                dimension=dimension,
                status=ResourceValueStatus.CONSTRAINED,
                quantity=0.0,
                limitation=(
                    "resource constraints reduce usable capacity "
                    "below the unconstrained observed capacity"
                ),
            )

        usable = unconstrained - reduction

        if (
            capability_quantity is not None
            and usable > capability_quantity
        ):
            raise ValueError(
                "Derived usable capacity exceeds structural capability."
            )

        limitation = constraints.limitation_for(dimension)

        if limitation:
            return ResourceValue(
                dimension=dimension,
                status=ResourceValueStatus.CONSTRAINED,
                quantity=usable,
                limitation=limitation,
            )

        return ResourceValue(
            dimension=dimension,
            status=ResourceValueStatus.KNOWN,
            quantity=usable,
        )

    @classmethod
    def _derive_gpu_value(
        cls,
        *,
        capability: Mapping[str, str],
        observation: Mapping[str, str],
        evaluated_at: datetime,
        observed_at: datetime,
        rules: ResourceInterpretationRules,
        constraints: ResourceConstraints,
    ) -> ResourceValue:
        if cls._observation_is_stale(
            evaluated_at,
            observed_at,
            rules,
        ):
            return ResourceValue(
                dimension="gpu",
                status=rules.stale_status,
                limitation="GPU observation is stale",
            )

        capability_present = cls._parse_bool(
            capability.get("present")
        )

        observation_present = cls._parse_bool(
            observation.get("present")
        )

        usable_flag = cls._parse_bool(
            observation.get("usable")
        )

        if (
            capability_present is False
            and observation_present is not True
        ):
            return ResourceValue(
                dimension="gpu",
                status=ResourceValueStatus.UNAVAILABLE,
                limitation="GPU is absent from structural capability",
            )

        if not observation:
            return ResourceValue(
                dimension="gpu",
                status=rules.unknown_status,
                limitation="GPU observation unavailable",
            )

        if usable_flag is False:
            return ResourceValue(
                dimension="gpu",
                status=ResourceValueStatus.UNAVAILABLE,
                limitation="GPU is currently unusable",
            )

        quantity = cls._extract_quantity(
            observation,
            (
                "usable",
                "available",
                "capacity",
                "gb",
                "memory_gb",
                "capacity_gb",
            ),
        )

        if quantity is None:
            if usable_flag is True:
                return ResourceValue(
                    dimension="gpu",
                    status=rules.incomplete_status,
                    limitation=(
                        "GPU usability is known but quantitative "
                        "capacity is unobserved"
                    ),
                )

            return ResourceValue(
                dimension="gpu",
                status=rules.incomplete_status,
                limitation="GPU evidence is incomplete",
            )

        capability_quantity = cls._extract_quantity(
            capability,
            (
                "capacity",
                "memory_gb",
                "capacity_gb",
            ),
        )

        if (
            capability_quantity is not None
            and quantity > capability_quantity
        ):
            return ResourceValue(
                dimension="gpu",
                status=rules.inconsistent_status,
                limitation=(
                    "GPU usable capacity exceeds structural capability"
                ),
            )

        reduction = constraints.reduction_for("gpu")

        if reduction > quantity:
            return ResourceValue(
                dimension="gpu",
                status=ResourceValueStatus.CONSTRAINED,
                quantity=0.0,
                limitation="GPU constraints consume usable capacity",
            )

        usable = quantity - reduction
        limitation = constraints.limitation_for("gpu")

        if limitation:
            return ResourceValue(
                dimension="gpu",
                status=ResourceValueStatus.CONSTRAINED,
                quantity=usable,
                unit="capacity",
                limitation=limitation,
            )

        return ResourceValue(
            dimension="gpu",
            status=ResourceValueStatus.KNOWN,
            quantity=usable,
            unit="capacity",
        )

    @classmethod
    def _derive_network_value(
        cls,
        *,
        observation: Mapping[str, str],
        evaluated_at: datetime,
        observed_at: datetime,
        rules: ResourceInterpretationRules,
        constraints: ResourceConstraints,
    ) -> ResourceValue:
        if cls._observation_is_stale(
            evaluated_at,
            observed_at,
            rules,
        ):
            return ResourceValue(
                dimension="network",
                status=rules.stale_status,
                limitation="network evidence is stale",
            )

        available = cls._parse_bool(
            observation.get("network_available")
        )

        if available is None:
            available = cls._parse_bool(
                observation.get("available")
            )

        if available is None:
            return ResourceValue(
                dimension="network",
                status=rules.unknown_status,
                limitation="network availability was not observed",
            )

        if not available:
            return ResourceValue(
                dimension="network",
                status=ResourceValueStatus.UNAVAILABLE,
                limitation="network is not currently available",
            )

        limitation = constraints.limitation_for("network")

        if limitation:
            return ResourceValue(
                dimension="network",
                status=ResourceValueStatus.CONSTRAINED,
                limitation=limitation,
            )

        return ResourceValue(
            dimension="network",
            status=ResourceValueStatus.KNOWN,
        )

    @classmethod
    def _derive_other_resources(
        cls,
        *,
        observation: Mapping[str, str],
        evaluated_at: datetime,
        observed_at: datetime,
        rules: ResourceInterpretationRules,
        constraints: ResourceConstraints,
    ) -> Mapping[str, ResourceValue]:
        """
        Do not infer canonical resource dimensions from arbitrary
        observation metadata.

        Additional resource dimensions require an explicit canonical
        semantic definition before they become Resource Values.
        """
        return MappingProxyType({})

    @staticmethod
    def _extract_quantity(
        values: Mapping[str, str],
        keys: tuple[str, ...],
    ) -> Optional[float]:
        for key in keys:
            raw = values.get(key)

            if raw is None:
                continue

            try:
                value = float(raw)
            except (TypeError, ValueError):
                continue

            if not isfinite(value):
                raise ValueError(
                    f"Non-finite resource quantity for key '{key}'."
                )

            return value

        return None

    @staticmethod
    def _parse_bool(
        value: Optional[str],
    ) -> Optional[bool]:
        if value is None:
            return None

        normalized = value.strip().lower()

        if normalized in {
            "true",
            "1",
            "yes",
            "available",
            "present",
            "usable",
        }:
            return True

        if normalized in {
            "false",
            "0",
            "no",
            "unavailable",
            "absent",
            "unusable",
        }:
            return False

        return None
