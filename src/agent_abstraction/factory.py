"""Agent factory for creating coding agents."""

import os
from typing import Any, Optional, Union

from .base_agent import AgentConfig, AgentType, BaseAgent
from .claude_code import ClaudeCodeAgent
from .codex import CodexAgent
from .copilot import CopilotAgent
from .gemini import GeminiAgent
from .swe_agent import SWEAgent


class AgentFactory:
    """Factory for creating coding agents based on configuration."""

    _agent_classes = {
        AgentType.CLAUDE_CODE: ClaudeCodeAgent,
        AgentType.GEMINI: GeminiAgent,
        AgentType.CODEX: CodexAgent,
        AgentType.SWE_AGENT: SWEAgent,
        AgentType.COPILOT: CopilotAgent,
    }

    @classmethod
    def create_agent(
        cls,
        agent_type: Union[AgentType, str],
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        **kwargs: Any,
    ) -> BaseAgent:
        """
        Create a coding agent instance.

        Args:
            agent_type: Type of agent to create
            api_key: API key for the agent (or read from environment)
            model: Model name to use
            **kwargs: Additional configuration parameters

        Returns:
            Configured agent instance

        Raises:
            ValueError: If agent type is not supported
        """
        # Convert string to AgentType if needed
        if isinstance(agent_type, str):
            try:
                agent_type = AgentType(agent_type)
            except ValueError:
                raise ValueError(
                    f"Unsupported agent type: {agent_type}. "
                    f"Supported types: {[t.value for t in AgentType]}"
                ) from None

        # Get API key from environment if not provided
        if api_key is None:
            api_key = cls._get_api_key_from_env(agent_type)

        # Create configuration
        config = AgentConfig(
            agent_type=agent_type,
            api_key=api_key,
            model=model,
            **kwargs,
        )

        # Get agent class and instantiate
        agent_class = cls._agent_classes.get(agent_type)
        if agent_class is None:
            raise ValueError(f"No implementation for agent type: {agent_type}")

        return agent_class(config)  # type: ignore[abstract]

    @classmethod
    def create_from_config(cls, config: AgentConfig) -> BaseAgent:
        """
        Create an agent from an existing configuration.

        Args:
            config: Agent configuration

        Returns:
            Configured agent instance

        Raises:
            ValueError: If agent type is not supported
        """
        agent_class = cls._agent_classes.get(config.agent_type)
        if agent_class is None:
            raise ValueError(f"No implementation for agent type: {config.agent_type}")

        return agent_class(config)  # type: ignore[abstract]

    @classmethod
    def _get_api_key_from_env(cls, agent_type: AgentType) -> Optional[str]:
        """
        Get API key from environment variables.

        Args:
            agent_type: Type of agent

        Returns:
            API key or None if not found
        """
        env_var_map = {
            AgentType.CLAUDE_CODE: "ANTHROPIC_API_KEY",
            AgentType.GEMINI: "GOOGLE_API_KEY",
            AgentType.CODEX: "OPENAI_API_KEY",
            AgentType.SWE_AGENT: "OPENAI_API_KEY",  # SWE-agent can use OpenAI
            AgentType.COPILOT: "OPENAI_API_KEY",  # Copilot uses OpenAI backend
        }

        env_var = env_var_map.get(agent_type)
        if env_var:
            return os.getenv(env_var)
        return None

    @classmethod
    def get_supported_agents(cls) -> list[str]:
        """
        Get list of supported agent types.

        Returns:
            List of agent type names
        """
        return [agent_type.value for agent_type in AgentType]

    @classmethod
    def register_agent(cls, agent_type: AgentType, agent_class: type[BaseAgent]) -> None:
        """
        Register a custom agent implementation.

        Args:
            agent_type: Agent type
            agent_class: Agent class to register

        Raises:
            ValueError: If agent_class is not a subclass of BaseAgent
        """
        if not issubclass(agent_class, BaseAgent):
            raise ValueError(f"{agent_class} must be a subclass of BaseAgent")

        cls._agent_classes[agent_type] = agent_class
