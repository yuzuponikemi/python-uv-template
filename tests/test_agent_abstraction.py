"""Tests for agent abstraction layer."""

from pathlib import Path

import pytest
import yaml  # type: ignore[import-untyped]

from src.agent_abstraction import (
    AgentConfig,
    AgentFactory,
    AgentResponse,
    AgentType,
    ClaudeCodeAgent,
    CodexAgent,
    ConfigLoader,
    GeminiAgent,
    SWEAgent,
)


class TestAgentConfig:
    """Tests for AgentConfig dataclass."""

    def test_agent_config_creation(self) -> None:
        """Test creating an agent configuration."""
        config = AgentConfig(
            agent_type=AgentType.CLAUDE_CODE,
            api_key="test_key",
            model="claude-sonnet-4-5-20250929",
            max_tokens=2048,
            temperature=0.5,
        )

        assert config.agent_type == AgentType.CLAUDE_CODE
        assert config.api_key == "test_key"
        assert config.model == "claude-sonnet-4-5-20250929"
        assert config.max_tokens == 2048
        assert config.temperature == 0.5
        assert config.custom_settings == {}
        assert config.allowed_tools == []

    def test_agent_config_defaults(self) -> None:
        """Test default values in agent configuration."""
        config = AgentConfig(agent_type=AgentType.GEMINI)

        assert config.api_key is None
        assert config.model is None
        assert config.max_tokens == 4096
        assert config.temperature == 0.7
        assert config.custom_settings == {}
        assert config.allowed_tools == []


class TestAgentFactory:
    """Tests for AgentFactory."""

    def test_create_claude_agent(self) -> None:
        """Test creating a Claude Code agent."""
        agent = AgentFactory.create_agent(
            agent_type=AgentType.CLAUDE_CODE,
            api_key="test_key",
            model="claude-sonnet-4-5-20250929",
        )

        assert isinstance(agent, ClaudeCodeAgent)
        assert agent.config.agent_type == AgentType.CLAUDE_CODE
        assert agent.config.model == "claude-sonnet-4-5-20250929"

    def test_create_gemini_agent(self) -> None:
        """Test creating a Gemini agent."""
        agent = AgentFactory.create_agent(
            agent_type=AgentType.GEMINI,
            api_key="test_key",
            model="gemini-2.0-flash-exp",
        )

        assert isinstance(agent, GeminiAgent)
        assert agent.config.agent_type == AgentType.GEMINI

    def test_create_codex_agent(self) -> None:
        """Test creating a Codex agent."""
        agent = AgentFactory.create_agent(
            agent_type=AgentType.CODEX, api_key="test_key", model="gpt-4-turbo"
        )

        assert isinstance(agent, CodexAgent)
        assert agent.config.agent_type == AgentType.CODEX

    def test_create_swe_agent(self) -> None:
        """Test creating a SWE-agent."""
        agent = AgentFactory.create_agent(
            agent_type=AgentType.SWE_AGENT,
            api_key="test_key",
            model="gpt-4-turbo",
        )

        assert isinstance(agent, SWEAgent)
        assert agent.config.agent_type == AgentType.SWE_AGENT

    def test_create_agent_from_string(self) -> None:
        """Test creating an agent from string type."""
        agent = AgentFactory.create_agent(agent_type="claude_code", api_key="test_key")

        assert isinstance(agent, ClaudeCodeAgent)

    def test_create_agent_invalid_type(self) -> None:
        """Test creating an agent with invalid type."""
        with pytest.raises(ValueError, match="Unsupported agent type"):
            AgentFactory.create_agent(agent_type="invalid_type", api_key="test_key")

    def test_get_supported_agents(self) -> None:
        """Test getting list of supported agents."""
        supported = AgentFactory.get_supported_agents()

        assert "claude_code" in supported
        assert "gemini" in supported
        assert "codex" in supported
        assert "swe_agent" in supported


class TestClaudeCodeAgent:
    """Tests for ClaudeCodeAgent."""

    def test_claude_agent_creation(self) -> None:
        """Test creating a Claude Code agent."""
        config = AgentConfig(
            agent_type=AgentType.CLAUDE_CODE,
            api_key="test_key",
            model="claude-sonnet-4-5-20250929",
        )
        agent = ClaudeCodeAgent(config)

        assert agent.config.model == "claude-sonnet-4-5-20250929"

    def test_claude_agent_default_model(self) -> None:
        """Test Claude agent sets default model."""
        config = AgentConfig(agent_type=AgentType.CLAUDE_CODE, api_key="test_key")
        agent = ClaudeCodeAgent(config)

        assert agent.config.model == "claude-sonnet-4-5-20250929"

    def test_claude_agent_requires_api_key(self) -> None:
        """Test Claude agent requires API key."""
        config = AgentConfig(agent_type=AgentType.CLAUDE_CODE)

        with pytest.raises(ValueError, match="ANTHROPIC_API_KEY is required"):
            ClaudeCodeAgent(config)

    def test_claude_agent_process_task(self) -> None:
        """Test processing a task with Claude agent."""
        config = AgentConfig(agent_type=AgentType.CLAUDE_CODE, api_key="test_key")
        agent = ClaudeCodeAgent(config)

        response = agent.process_task("Implement a new feature")

        assert isinstance(response, AgentResponse)
        assert response.success is True
        assert "Task processed" in response.message

    def test_claude_agent_capabilities(self) -> None:
        """Test Claude agent capabilities."""
        config = AgentConfig(agent_type=AgentType.CLAUDE_CODE, api_key="test_key")
        agent = ClaudeCodeAgent(config)

        capabilities = agent.get_capabilities()

        assert capabilities["github_integration"] is True
        assert capabilities["auto_fix_ci"] is True
        assert capabilities["tdd_support"] is True


class TestConfigLoader:
    """Tests for ConfigLoader."""

    def test_load_from_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test loading configuration from environment variables."""
        monkeypatch.setenv("CODING_AGENT_TYPE", "gemini")
        monkeypatch.setenv("CODING_AGENT_MODEL", "gemini-2.0-flash-exp")
        monkeypatch.setenv("CODING_AGENT_MAX_TOKENS", "2048")
        monkeypatch.setenv("CODING_AGENT_TEMPERATURE", "0.5")

        config = ConfigLoader.load_from_env()

        assert config.agent_type == AgentType.GEMINI
        assert config.model == "gemini-2.0-flash-exp"
        assert config.max_tokens == 2048
        assert config.temperature == 0.5

    def test_load_from_file(self, tmp_path: Path) -> None:
        """Test loading configuration from YAML file."""
        config_file = tmp_path / ".agent-config.yml"
        config_data = {
            "agent": {
                "type": "claude_code",
                "model": "claude-sonnet-4-5-20250929",
                "max_tokens": 2048,
                "temperature": 0.5,
            }
        }

        with open(config_file, "w") as f:
            yaml.dump(config_data, f)

        config = ConfigLoader.load_from_file(config_file)

        assert config.agent_type == AgentType.CLAUDE_CODE
        assert config.model == "claude-sonnet-4-5-20250929"
        assert config.max_tokens == 2048
        assert config.temperature == 0.5

    def test_load_from_file_not_found(self) -> None:
        """Test loading from non-existent file raises error."""
        with pytest.raises(FileNotFoundError):
            ConfigLoader.load_from_file("/nonexistent/config.yml")

    def test_save_config(self, tmp_path: Path) -> None:
        """Test saving configuration to file."""
        config = AgentConfig(
            agent_type=AgentType.GEMINI,
            model="gemini-2.0-flash-exp",
            max_tokens=2048,
            temperature=0.5,
        )

        config_file = tmp_path / ".agent-config.yml"
        ConfigLoader.save_config(config, config_file)

        assert config_file.exists()

        # Load and verify
        with open(config_file) as f:
            saved_data = yaml.safe_load(f)

        assert saved_data["agent"]["type"] == "gemini"
        assert saved_data["agent"]["model"] == "gemini-2.0-flash-exp"
        assert saved_data["agent"]["max_tokens"] == 2048
        assert saved_data["agent"]["temperature"] == 0.5
