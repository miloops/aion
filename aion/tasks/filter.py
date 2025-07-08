"""
Filter task implementation for AION.
"""

from typing import Dict, Any
import pandas as pd
import operator


def filter_task(data: pd.DataFrame, task: Dict[str, Any]) -> pd.DataFrame:
    """Filter data based on a condition.
    
    Args:
        data: Input DataFrame
        task: Task configuration with condition
        
    Returns:
        Filtered DataFrame
    """
    if data.empty:
        return data
    
    condition = task["condition"]
    field = condition["field"]
    op_str = condition["operator"]
    value = condition["value"]
    
    # Map operator strings to functions
    op_map = {
        "==": operator.eq,
        "!=": operator.ne,
        ">": operator.gt,
        ">=": operator.ge,
        "<": operator.lt,
        "<=": operator.le,
        "in": lambda x, y: x.isin(y),
        "not in": lambda x, y: ~x.isin(y),
        "contains": lambda x, y: x.str.contains(y, na=False),
        "startswith": lambda x, y: x.str.startswith(y, na=False),
        "endswith": lambda x, y: x.str.endswith(y, na=False),
    }
    
    if op_str not in op_map:
        raise ValueError(f"Unsupported operator: {op_str}")
    
    op_func = op_map[op_str]
    
    # Apply filter
    if field not in data.columns:
        raise ValueError(f"Field '{field}' not found in data")
    
    mask = op_func(data[field], value)
    return data[mask] 