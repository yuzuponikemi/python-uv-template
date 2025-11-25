"""
Coding agent abstraction layer.

This module provides a unified interface for multiple coding agents
(Claude Code, Gemini CLI, Codex, SWE-agent, etc.).
"""

from .base_agent import AgentConfig, AgentResponse, AgentType, BaseAgent
from .claude_code import ClaudeCodeAgent
from .codex import CodexAgent
from .config import ConfigLoader
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
    "GeminiAgent",
    "SWEAgent",
    "AgentFactory",
    "ConfigLoader",
]
