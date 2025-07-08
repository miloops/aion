"""
AION interpreter for executing AION programs.
"""

from typing import Dict, Any, List, Optional
import logging
import pandas as pd
from dataclasses import dataclass

from .registry import TaskRegistry
from .validators import AIONValidator, ValidationError

logger = logging.getLogger(__name__)


@dataclass
class ExecutionResult:
    """Result of executing an AION program."""
    data: Any
    logs: List[str]
    errors: List[str]
    execution_plan: List[Dict[str, Any]]


class AIONInterpreter:
    """Interpreter for AION programs."""
    
    def __init__(self):
        self.registry = TaskRegistry()
        self.validator = AIONValidator()
        self._register_default_tasks()
    
    def _register_default_tasks(self):
        """Register the default task handlers."""
        from ..tasks import (
            filter_task, sort_task, transform_task, model_call_task,
            aggregate_task, export_task
        )
        
        self.registry.register("filter", filter_task)
        self.registry.register("sort", sort_task)
        self.registry.register("transform", transform_task)
        self.registry.register("model_call", model_call_task)
        self.registry.register("aggregate", aggregate_task)
        self.registry.register("export", export_task)
    
    def execute(self, program: Dict[str, Any], 
                input_data: Optional[Any] = None) -> ExecutionResult:
        """Execute an AION program.
        
        Args:
            program: The AION program to execute
            input_data: Input data (defaults to empty DataFrame)
            
        Returns:
            ExecutionResult with data, logs, errors, and execution plan
        """
        logs = []
        errors = []
        execution_plan = []
        
        # Validate the program
        validation_errors = self.validator.validate_program(program)
        if validation_errors:
            errors.extend([f"{e.path}: {e.message}" for e in validation_errors])
            return ExecutionResult(
                data=None, logs=logs, errors=errors, execution_plan=[]
            )
        
        # Initialize data
        if input_data is None:
            data = pd.DataFrame()
        else:
            data = input_data
        
        logs.append("Program validation passed")
        
        # Execute pipeline
        pipeline = program["pipeline"]
        for i, task in enumerate(pipeline):
            task_type = task["task"]
            logs.append(f"Executing task {i+1}/{len(pipeline)}: {task_type}")
            
            try:
                # Get task handler
                handler = self.registry.get_handler(task_type)
                if handler is None:
                    error_msg = f"No handler registered for task type: {task_type}"
                    errors.append(error_msg)
                    logs.append(f"ERROR: {error_msg}")
                    break
                
                # Execute task
                result = handler(data, task)
                data = result
                
                # Record execution
                execution_plan.append({
                    "task_index": i,
                    "task_type": task_type,
                    "task_config": task,
                    "success": True
                })
                
                logs.append(f"Task {task_type} completed successfully")
                
            except Exception as e:
                error_msg = f"Task {task_type} failed: {str(e)}"
                errors.append(error_msg)
                logs.append(f"ERROR: {error_msg}")
                
                execution_plan.append({
                    "task_index": i,
                    "task_type": task_type,
                    "task_config": task,
                    "success": False,
                    "error": str(e)
                })
                break
        
        return ExecutionResult(
            data=data,
            logs=logs,
            errors=errors,
            execution_plan=execution_plan
        )
    
    def explain(self, program: Dict[str, Any]) -> str:
        """Generate a human-readable explanation of an AION program.
        
        Args:
            program: The AION program to explain
            
        Returns:
            Natural language explanation
        """
        if "pipeline" not in program:
            return "Invalid program: missing pipeline"
        
        pipeline = program["pipeline"]
        explanation = f"This AION program contains {len(pipeline)} tasks:\n\n"
        
        for i, task in enumerate(pipeline):
            task_type = task["task"]
            explanation += f"{i+1}. **{task_type.upper()}** task\n"
            
            if task_type == "filter":
                condition = task.get("condition", {})
                field = condition.get("field", "unknown")
                operator = condition.get("operator", "unknown")
                value = condition.get("value", "unknown")
                explanation += f"   - Filters data where {field} {operator} {value}\n"
            
            elif task_type == "sort":
                operation = task.get("operation", {})
                field = operation.get("field", "unknown")
                order = operation.get("order", "asc")
                explanation += f"   - Sorts data by {field} in {order}ending order\n"
            
            elif task_type == "transform":
                mapping = task.get("mapping", {})
                explanation += f"   - Transforms fields: {list(mapping.keys())}\n"
            
            elif task_type == "model_call":
                prompt = task.get("prompt", "unknown")
                explanation += f"   - Calls AI model with prompt: {prompt[:50]}...\n"
            
            explanation += "\n"
        
        return explanation 