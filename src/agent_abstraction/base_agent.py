"""Base agent interface for coding agents."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional


class AgentType(Enum):
    """Supported coding agent types."""

    CLAUDE_CODE = "claude_code"
    GEMINI = "gemini"
    CODEX = "codex"
    SWE_AGENT = "swe_agent"
    COPILOT = "copilot"


@dataclass
class AgentConfig:
    """Configuration for a coding agent."""

    agent_type: AgentType
    api_key: Optional[str] = None
    model: Optional[str] = None
    max_tokens: int = 4096
    temperature: float = 0.7
    system_prompt: Optional[str] = None
    allowed_tools: Optional[list[str]] = None
    custom_settings: Optional[dict[str, Any]] = None

    def __post_init__(self) -> None:
        """Validate configuration after initialization."""
        if self.custom_settings is None:
            self.custom_settings = {}
        if self.allowed_tools is None:
            self.allowed_tools = []


@dataclass
class AgentResponse:
    """Response from a coding agent."""

    success: bool
    message: str
    changes: Optional[list[str]] = None
    error: Optional[str] = None
    metadata: Optional[dict[str, Any]] = None

    def __post_init__(self) -> None:
        """Initialize default values."""
        if self.changes is None:
            self.changes = []
        if self.metadata is None:
            self.metadata = {}


class BaseAgent(ABC):
    """Base class for all coding agents."""

    def __init__(self, config: AgentConfig) -> None:
        """
        Initialize the agent with configuration.

        Args:
            config: Agent configuration
        """
        self.config = config
        self._validate_config()

    @abstractmethod
    def _validate_config(self) -> None:
        """
        Validate agent-specific configuration.

        Raises:
            ValueError: If configuration is invalid
        """
        pass

    @abstractmethod
    def process_task(self, task: str, context: Optional[dict[str, Any]] = None) -> AgentResponse:
        """
        Process a coding task.

        Args:
            task: Task description or prompt
            context: Additional context (issue number, PR number, etc.)

        Returns:
            AgentResponse with results

        Raises:
            RuntimeError: If task processing fails
        """
        pass

    @abstractmethod
    def fix_ci_errors(self, error_logs: dict[str, str], branch: str) -> AgentResponse:
        """
        Automatically fix CI errors.

        Args:
            error_logs: Dictionary mapping error types to log content
                       (e.g., {"pytest": "...", "mypy": "..."})
            branch: Git branch name

        Returns:
            AgentResponse with fix results

        Raises:
            RuntimeError: If fix fails
        """
        pass

    @abstractmethod
    def review_code(self, diff: str, context: Optional[dict[str, Any]] = None) -> AgentResponse:
        """
        Review code changes.

        Args:
            diff: Git diff or code changes
            context: Additional context (PR number, etc.)

        Returns:
            AgentResponse with review comments

        Raises:
            RuntimeError: If review fails
        """
        pass

    def get_capabilities(self) -> dict[str, bool]:
        """
        Get agent capabilities.

        Returns:
            Dictionary of capability names to availability
        """
        return {
            "task_processing": True,
            "ci_fix": True,
            "code_review": True,
            "test_generation": True,
            "documentation": True,
        }

    def __str__(self) -> str:
        """String representation of the agent."""
        return f"{self.__class__.__name__}(type={self.config.agent_type.value})"

    def __repr__(self) -> str:
        """Detailed representation of the agent."""
        return (
            f"{self.__class__.__name__}("
            f"type={self.config.agent_type.value}, "
            f"model={self.config.model})"
        )
