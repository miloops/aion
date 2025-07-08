"""
Aggregate task implementation for AION.
"""

from typing import Dict, Any, List
import pandas as pd


def aggregate_task(data: pd.DataFrame, task: Dict[str, Any]) -> pd.DataFrame:
    """Aggregate data using groupby operations.

    Args:
        data: Input DataFrame
        task: Task configuration with group_by and aggregations

    Returns:
        Aggregated DataFrame
    """
    if data.empty:
        return data

    group_by = task.get("group_by", [])
    aggregations = task.get("aggregations", {})

    if not group_by:
        raise ValueError("Aggregate task must specify 'group_by' fields")

    if not aggregations:
        raise ValueError("Aggregate task must specify 'aggregations'")

    # Validate group_by fields exist
    for field in group_by:
        if field not in data.columns:
            raise ValueError(f"Group by field '{field}' not found in data")

    # Validate aggregation fields exist
    for field in aggregations.keys():
        if field not in data.columns:
            raise ValueError(f"Aggregation field '{field}' not found in data")

    # Perform aggregation
    grouped = data.groupby(group_by)

    # Apply aggregations
    result = grouped.agg(aggregations).reset_index()

    return result
