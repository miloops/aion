"""
AION - AI-Oriented Notation
An AI-native intermediate representation for structured reasoning and 
execution.
"""

__version__ = "0.1.0"
__author__ = "AION Team"

from .core.interpreter import AIONInterpreter
from .core.registry import TaskRegistry

__all__ = ["AIONInterpreter", "TaskRegistry"] 