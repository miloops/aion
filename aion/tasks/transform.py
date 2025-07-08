"""
Transform task implementation for AION.
"""

from typing import Dict, Any
import pandas as pd


def transform_task(data: pd.DataFrame, task: Dict[str, Any]) -> pd.DataFrame:
    """Transform data fields based on mapping.
    
    Args:
        data: Input DataFrame
        task: Task configuration with mapping
        
    Returns:
        Transformed DataFrame
    """
    if data.empty:
        return data
    
    mapping = task["mapping"]
    result = data.copy()
    
    for new_field, source in mapping.items():
        if isinstance(source, str):
            # Simple field rename
            if source in data.columns:
                result[new_field] = data[source]
            else:
                raise ValueError(f"Source field '{source}' not found in data")
        
        elif isinstance(source, dict):
            # Complex transformation
            if "concat" in source:
                # Concatenate multiple fields
                fields_to_concat = source["concat"]
                if not isinstance(fields_to_concat, list):
                    raise ValueError("concat must be a list of fields")
                
                # Validate all fields exist
                for field in fields_to_concat:
                    if isinstance(field, str) and field not in data.columns:
                        raise ValueError(f"Field '{field}' not found in data")
                
                # Concatenate
                result[new_field] = ""
                for field in fields_to_concat:
                    if isinstance(field, str):
                        result[new_field] += data[field].astype(str)
                    else:
                        result[new_field] += str(field)
            
            else:
                raise ValueError(f"Unknown transformation: {source}")
        
        else:
            # Constant value
            result[new_field] = source
    
    return result 