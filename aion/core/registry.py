"""
Task registry for mapping AION task types to their handler functions.
"""

from typing import Dict, Callable, Any, Optional
import logging

logger = logging.getLogger(__name__)


class TaskRegistry:
    """Registry for AION task handlers."""

    def __init__(self):
        self._handlers: Dict[str, Callable] = {}
        self._metadata: Dict[str, Dict[str, Any]] = {}

    def register(
        self,
        task_type: str,
        handler: Callable,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Register a task handler.

        Args:
            task_type: The type of task (e.g., 'filter', 'sort', 'transform')
            handler: Function that processes the task
            metadata: Optional metadata about the task (schema, description, etc.)
        """
        self._handlers[task_type] = handler
        self._metadata[task_type] = metadata or {}
        logger.info(f"Registered task handler for '{task_type}'")

    def get_handler(self, task_type: str) -> Optional[Callable]:
        """Get the handler for a task type."""
        return self._handlers.get(task_type)

    def get_metadata(self, task_type: str) -> Dict[str, Any]:
        """Get metadata for a task type."""
        return self._metadata.get(task_type, {})

    def list_tasks(self) -> list[str]:
        """List all registered task types."""
        return list(self._handlers.keys())

    def has_task(self, task_type: str) -> bool:
        """Check if a task type is registered."""
        return task_type in self._handlers
