"""Configuration loader for coding agents."""

import os
from pathlib import Path
from typing import Any, Optional, Union

import yaml  # type: ignore[import-untyped]

from .base_agent import AgentConfig, AgentType


class ConfigLoader:
    """Load and manage agent configuration."""

    DEFAULT_CONFIG_PATH = ".agent-config.yml"

    @classmethod
    def load_from_file(cls, config_path: Optional[Union[str, Path]] = None) -> AgentConfig:
        """
        Load agent configuration from YAML file.

        Args:
            config_path: Path to configuration file
                        (defaults to .agent-config.yml in project root)

        Returns:
            AgentConfig instance

        Raises:
            FileNotFoundError: If config file doesn't exist
            ValueError: If configuration is invalid
        """
        if config_path is None:
            config_path = cls._find_config_file()

        config_path = Path(config_path)
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        with open(config_path) as f:
            config_data = yaml.safe_load(f)

        return cls._parse_config(config_data)

    @classmethod
    def load_from_env(cls) -> AgentConfig:
        """
        Load agent configuration from environment variables.

        Environment variables:
        - CODING_AGENT_TYPE: Agent type (claude_code, gemini, codex, swe_agent)
        - CODING_AGENT_MODEL: Model name
        - CODING_AGENT_MAX_TOKENS: Max tokens
        - CODING_AGENT_TEMPERATURE: Temperature

        Returns:
            AgentConfig instance

        Raises:
            ValueError: If required environment variables are missing
        """
        agent_type_str = os.getenv("CODING_AGENT_TYPE", "claude_code")
        try:
            agent_type = AgentType(agent_type_str)
        except ValueError:
            raise ValueError(f"Invalid CODING_AGENT_TYPE: {agent_type_str}") from None

        return AgentConfig(
            agent_type=agent_type,
            api_key=None,  # Will be loaded by factory
            model=os.getenv("CODING_AGENT_MODEL"),
            max_tokens=int(os.getenv("CODING_AGENT_MAX_TOKENS", "4096")),
            temperature=float(os.getenv("CODING_AGENT_TEMPERATURE", "0.7")),
            system_prompt=os.getenv("CODING_AGENT_SYSTEM_PROMPT"),
        )

    @classmethod
    def _find_config_file(cls) -> Path:
        """
        Find configuration file in current directory or parent directories.

        Returns:
            Path to configuration file

        Raises:
            FileNotFoundError: If configuration file is not found
        """
        current = Path.cwd()

        # Check current directory and parents
        for parent in [current, *current.parents]:
            config_path = parent / cls.DEFAULT_CONFIG_PATH
            if config_path.exists():
                return config_path

        raise FileNotFoundError(
            f"Configuration file '{cls.DEFAULT_CONFIG_PATH}' not found "
            f"in {current} or any parent directory"
        )

    @classmethod
    def _parse_config(cls, config_data: dict[str, Any]) -> AgentConfig:
        """
        Parse configuration data into AgentConfig.

        Args:
            config_data: Configuration dictionary from YAML

        Returns:
            AgentConfig instance

        Raises:
            ValueError: If configuration is invalid
        """
        agent_section = config_data.get("agent", {})

        # Get agent type
        agent_type_str = agent_section.get("type", "claude_code")
        try:
            agent_type = AgentType(agent_type_str)
        except ValueError:
            raise ValueError(
                f"Invalid agent type: {agent_type_str}. Supported: {[t.value for t in AgentType]}"
            ) from None

        # Get agent-specific settings
        agent_specific = config_data.get(agent_type_str, {})

        # Merge settings (agent-specific overrides general)
        model = agent_specific.get("model") or agent_section.get("model")
        max_tokens = agent_section.get("max_tokens", 4096)
        temperature = agent_section.get("temperature", 0.7)
        system_prompt = agent_section.get("system_prompt")
        allowed_tools = agent_section.get("allowed_tools")

        return AgentConfig(
            agent_type=agent_type,
            api_key=None,  # Will be loaded from environment by factory
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            system_prompt=system_prompt,
            allowed_tools=allowed_tools,
            custom_settings=agent_specific,
        )

    @classmethod
    def save_config(
        cls,
        config: AgentConfig,
        config_path: Optional[Union[str, Path]] = None,
    ) -> None:
        """
        Save agent configuration to YAML file.

        Args:
            config: Agent configuration to save
            config_path: Path to save configuration
                        (defaults to .agent-config.yml)
        """
        if config_path is None:
            config_path = Path.cwd() / cls.DEFAULT_CONFIG_PATH

        config_path = Path(config_path)

        config_data = {
            "agent": {
                "type": config.agent_type.value,
                "max_tokens": config.max_tokens,
                "temperature": config.temperature,
            }
        }

        if config.model:
            config_data["agent"]["model"] = config.model
        if config.system_prompt:
            config_data["agent"]["system_prompt"] = config.system_prompt
        if config.allowed_tools:
            config_data["agent"]["allowed_tools"] = config.allowed_tools  # type: ignore[assignment]

        # Add agent-specific settings
        if config.custom_settings:
            config_data[config.agent_type.value] = config.custom_settings

        with open(config_path, "w") as f:
            yaml.dump(config_data, f, default_flow_style=False, sort_keys=False)
