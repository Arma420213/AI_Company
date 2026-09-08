"""
AI Company — Canonical Agent Core Contract

Agent represents an organizational execution participant.

This module belongs to the Core layer.

It does not:
- execute Tasks
- schedule Tasks
- select Agents
- evaluate Tasks
- authorize execution
- make strategic decisions
- own Capability semantics
- own Experience semantics
- own Trust semantics
- depend on Runtime
- depend on Integrations
- depend on external providers

The canonical Agent model owns organizational Agent identity and
organizational properties without becoming an execution engine or a
second authority for Capability, Experience, Trust, or execution.
"""

from dataclasses import dataclass
from datetime import datetime
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True)
class AgentProvenance:
    """
    Provenance describing where the Agent information came from.
    """

    source: str
    timestamp: datetime
    authority: str

    def __post_init__(self) -> None:
        if not self.source.strip():
            raise ValueError(
                "Agent provenance source must not be empty."
            )

        if not self.authority.strip():
            raise ValueError(
                "Agent provenance authority must not be empty."
            )

        if self.timestamp.tzinfo is None:
            raise ValueError(
                "Agent provenance timestamp must be timezone-aware."
            )


@dataclass(frozen=True)
class Agent:
    """
    Canonical representation of an organizational execution participant.

    Agent identity is deliberately separated from:
    - Capability semantics
    - Task semantics
    - execution implementation
    - Execution Result
    - Experience authority
    - Trust authority
    """

    agent_id: str
    name: str
    description: str
    role: str
    agent_type: str
    capability_ids: tuple[str, ...]
    availability_state: str
    requirements: Mapping[str, str]
    execution_characteristics: Mapping[str, str]
    provenance: AgentProvenance

    def __post_init__(self) -> None:
        if not self.agent_id.strip():
            raise ValueError(
                "Agent ID must not be empty."
            )

        if not self.name.strip():
            raise ValueError(
                "Agent name must not be empty."
            )

        if not self.description.strip():
            raise ValueError(
                "Agent description must not be empty."
            )

        if not self.role.strip():
            raise ValueError(
                "Agent role must not be empty."
            )

        if not self.agent_type.strip():
            raise ValueError(
                "Agent type must not be empty."
            )

        if not self.availability_state.strip():
            raise ValueError(
                "Agent availability state must not be empty."
            )

        normalized_capability_ids = tuple(
            capability_id.strip()
            for capability_id in self.capability_ids
        )

        if any(
            not capability_id
            for capability_id in normalized_capability_ids
        ):
            raise ValueError(
                "Agent capability IDs must not be empty."
            )

        if len(normalized_capability_ids) != len(
            set(normalized_capability_ids)
        ):
            raise ValueError(
                "Agent capability IDs must be unique."
            )

        object.__setattr__(
            self,
            "capability_ids",
            normalized_capability_ids,
        )

        object.__setattr__(
            self,
            "requirements",
            MappingProxyType(dict(self.requirements)),
        )

        object.__setattr__(
            self,
            "execution_characteristics",
            MappingProxyType(
                dict(self.execution_characteristics)
            ),
        )


class AgentAuthority:
    """
    Sole canonical authority for Agent identity and organizational
    Agent state.

    Individual Agent objects remain immutable.

    AgentAuthority does not:
    - execute work
    - schedule work
    - evaluate Tasks
    - select Agents
    - authorize execution
    - make strategic decisions
    - own Capability semantics
    - own Experience semantics
    - own Trust semantics
    """

    def __init__(self) -> None:
        self._agents: dict[str, Agent] = {}

    def get_agent(self, agent_id: str) -> Agent:
        """
        Return the canonical Agent identified by agent_id.
        """
        try:
            return self._agents[agent_id]
        except KeyError as exc:
            raise KeyError(
                f"Unknown agent: {agent_id}"
            ) from exc

    def set_agent(self, agent: Agent) -> Agent:
        """
        Register a new canonical Agent.

        Agent identity is unique. Attempting to register an existing
        agent_id is rejected rather than silently replacing identity.
        """
        if agent.agent_id in self._agents:
            raise ValueError(
                f"Agent ID already exists: {agent.agent_id}"
            )

        self._agents[agent.agent_id] = agent
        return agent

    def update_agent(self, agent: Agent) -> Agent:
        """
        Replace an existing Agent definition while preserving identity
        ownership within AgentAuthority.
        """
        if agent.agent_id not in self._agents:
            raise KeyError(
                f"Unknown agent: {agent.agent_id}"
            )

        self._agents[agent.agent_id] = agent
        return agent

    def set_availability(
        self,
        agent_id: str,
        availability_state: str,
    ) -> Agent:
        """
        Update canonical Agent availability.

        A new immutable Agent state is created. Agent identity and the
        other canonical Agent properties remain unchanged.
        """
        if not availability_state.strip():
            raise ValueError(
                "Agent availability state must not be empty."
            )

        current = self.get_agent(agent_id)

        updated = Agent(
            agent_id=current.agent_id,
            name=current.name,
            description=current.description,
            role=current.role,
            agent_type=current.agent_type,
            capability_ids=current.capability_ids,
            availability_state=availability_state,
            requirements=current.requirements,
            execution_characteristics=current.execution_characteristics,
            provenance=AgentProvenance(
                source="agent_authority",
                timestamp=datetime.now().astimezone(),
                authority="AgentAuthority",
            ),
        )

        self._agents[agent_id] = updated
        return updated

    def all_agents(self) -> Mapping[str, Agent]:
        """
        Return a read-only view of canonical Agents.
        """
        return MappingProxyType(self._agents)
