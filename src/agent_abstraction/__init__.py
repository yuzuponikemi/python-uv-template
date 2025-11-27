"""
Coding agent abstraction layer.

This module provides a unified interface for multiple coding agents
(Claude Code, Gemini CLI, Codex, SWE-agent, Copilot, etc.).
"""

from .base_agent import AgentConfig, AgentResponse, AgentType, BaseAgent
from .claude_code import ClaudeCodeAgent
from .codex import CodexAgent
from .config import ConfigLoader
from .copilot import CopilotAgent
from .factory import AgentFactory
from .gemini import GeminiAgent
from .swe_agent import SWEAgent

__all__ = [
    "AgentConfig",
    "AgentResponse",
    "AgentType",
    "BaseAgent",
    "ClaudeCodeAgent",
    "CodexAgent",
    "CopilotAgent",
    "GeminiAgent",
    "SWEAgent",
    "AgentFactory",
    "ConfigLoader",
]
