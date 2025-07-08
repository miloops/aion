"""
Export task implementation for AION.
"""

from typing import Dict, Any
import pandas as pd
import os


def export_task(data: pd.DataFrame, task: Dict[str, Any]) -> pd.DataFrame:
    """Export data to various file formats.

    Args:
        data: Input DataFrame
        task: Task configuration with file path and format

    Returns:
        DataFrame (unchanged, export is side effect)
    """
    if data.empty:
        return data

    file_path = task.get("file_path")
    file_format = task.get("format", "csv")

    if not file_path:
        raise ValueError("Export task must specify 'file_path'")

    # Ensure directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Export based on format
    if file_format.lower() == "csv":
        data.to_csv(file_path, index=False)
    elif file_format.lower() == "json":
        data.to_json(file_path, orient="records", indent=2)
    elif file_format.lower() == "excel":
        data.to_excel(file_path, index=False)
    elif file_format.lower() == "parquet":
        data.to_parquet(file_path, index=False)
    else:
        raise ValueError(f"Unsupported export format: {file_format}")

    return data
