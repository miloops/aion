"""
Sort task implementation for AION.
"""

from typing import Dict, Any
import pandas as pd


def sort_task(data: pd.DataFrame, task: Dict[str, Any]) -> pd.DataFrame:
    """Sort data by specified fields.
    
    Args:
        data: Input DataFrame
        task: Task configuration with operation
        
    Returns:
        Sorted DataFrame
    """
    if data.empty:
        return data
    
    operation = task["operation"]
    field = operation["field"]
    order = operation.get("order", "asc")
    
    # Validate field exists
    if field not in data.columns:
        raise ValueError(f"Field '{field}' not found in data")
    
    # Determine sort order
    ascending = order.lower() == "asc"
    
    # Sort the data
    return data.sort_values(by=field, ascending=ascending) 