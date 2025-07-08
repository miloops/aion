"""
Schema validation for AION programs.
"""

from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class ValidationError:
    """Represents a validation error."""
    path: str
    message: str
    value: Any = None


class AIONValidator:
    """Validates AION program schemas."""
    
    def __init__(self):
        self.required_task_fields = {"task"}
        self.valid_task_types = {"filter", "sort", "transform", "model_call"}
    
    def validate_program(self, program: Dict[str, Any]) -> List[ValidationError]:
        """Validate a complete AION program.
        
        Args:
            program: The AION program to validate
            
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        # Check for required top-level fields
        if "pipeline" not in program:
            errors.append(ValidationError(
                path="root", 
                message="Program must contain a 'pipeline' field"
            ))
            return errors
        
        # Validate pipeline
        pipeline = program["pipeline"]
        if not isinstance(pipeline, list):
            errors.append(ValidationError(
                path="pipeline",
                message="Pipeline must be a list of tasks"
            ))
            return errors
        
        # Validate each task
        for i, task in enumerate(pipeline):
            task_errors = self._validate_task(task, f"pipeline[{i}]")
            errors.extend(task_errors)
        
        return errors
    
    def _validate_task(self, task: Dict[str, Any], path: str) -> List[ValidationError]:
        """Validate a single task."""
        errors = []
        
        # Check required fields
        if not isinstance(task, dict):
            errors.append(ValidationError(
                path=path,
                message="Task must be a dictionary"
            ))
            return errors
        
        if "task" not in task:
            errors.append(ValidationError(
                path=f"{path}.task",
                message="Task must have a 'task' field"
            ))
            return errors
        
        task_type = task["task"]
        if not isinstance(task_type, str):
            errors.append(ValidationError(
                path=f"{path}.task",
                message="Task type must be a string"
            ))
            return errors
        
        if task_type not in self.valid_task_types:
            errors.append(ValidationError(
                path=f"{path}.task",
                message=f"Unknown task type: {task_type}. "
                        f"Valid types: {self.valid_task_types}"
            ))
        
        # Validate task-specific fields
        if task_type == "filter":
            errors.extend(self._validate_filter_task(task, path))
        elif task_type == "sort":
            errors.extend(self._validate_sort_task(task, path))
        elif task_type == "transform":
            errors.extend(self._validate_transform_task(task, path))
        elif task_type == "model_call":
            errors.extend(self._validate_model_call_task(task, path))
        
        return errors
    
    def _validate_filter_task(self, task: Dict[str, Any], 
                             path: str) -> List[ValidationError]:
        """Validate a filter task."""
        errors = []
        
        if "condition" not in task:
            errors.append(ValidationError(
                path=f"{path}.condition",
                message="Filter task must have a 'condition' field"
            ))
            return errors
        
        condition = task["condition"]
        if not isinstance(condition, dict):
            errors.append(ValidationError(
                path=f"{path}.condition",
                message="Condition must be a dictionary"
            ))
            return errors
        
        required_fields = {"field", "operator", "value"}
        for field in required_fields:
            if field not in condition:
                errors.append(ValidationError(
                    path=f"{path}.condition.{field}",
                    message=f"Condition must have '{field}' field"
                ))
        
        return errors
    
    def _validate_sort_task(self, task: Dict[str, Any], 
                           path: str) -> List[ValidationError]:
        """Validate a sort task."""
        errors = []
        
        if "operation" not in task:
            errors.append(ValidationError(
                path=f"{path}.operation",
                message="Sort task must have an 'operation' field"
            ))
            return errors
        
        operation = task["operation"]
        if not isinstance(operation, dict):
            errors.append(ValidationError(
                path=f"{path}.operation",
                message="Operation must be a dictionary"
            ))
            return errors
        
        if "field" not in operation:
            errors.append(ValidationError(
                path=f"{path}.operation.field",
                message="Sort operation must have a 'field'"
            ))
        
        if "order" in operation:
            order = operation["order"]
            if order not in ["asc", "desc"]:
                errors.append(ValidationError(
                    path=f"{path}.operation.order",
                    message="Sort order must be 'asc' or 'desc'"
                ))
        
        return errors
    
    def _validate_transform_task(self, task: Dict[str, Any], 
                                path: str) -> List[ValidationError]:
        """Validate a transform task."""
        errors = []
        
        if "mapping" not in task:
            errors.append(ValidationError(
                path=f"{path}.mapping",
                message="Transform task must have a 'mapping' field"
            ))
            return errors
        
        mapping = task["mapping"]
        if not isinstance(mapping, dict):
            errors.append(ValidationError(
                path=f"{path}.mapping",
                message="Mapping must be a dictionary"
            ))
        
        return errors
    
    def _validate_model_call_task(self, task: Dict[str, Any], 
                                 path: str) -> List[ValidationError]:
        """Validate a model_call task."""
        errors = []
        
        required_fields = {"prompt"}
        for field in required_fields:
            if field not in task:
                errors.append(ValidationError(
                    path=f"{path}.{field}",
                    message=f"Model call task must have '{field}' field"
                ))
        
        return errors 