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
    fields_to_remove = set()

    for new_field, source in mapping.items():
        if isinstance(source, str):
            # Simple field rename
            if source in data.columns:
                result[new_field] = data[source]
                # Mark original field for removal
                fields_to_remove.add(source)
            else:
                raise ValueError(f"Source field '{source}' not found in data")

        elif isinstance(source, dict):
            # Complex transformation
            if "concat" in source:
                # Concatenate multiple fields
                fields_to_concat = source["concat"]
                if not isinstance(fields_to_concat, list):
                    raise ValueError("concat must be a list of fields")

                # Validate only actual column names exist
                for field in fields_to_concat:
                    if isinstance(field, str) and field not in data.columns:
                        # Check if it's a string literal that should be allowed
                        is_literal = (
                            field.strip() == ""
                            or len(field) <= 3
                            or field.startswith(" ")
                            or field.endswith(" ")
                            or "(" in field
                            or ")" in field
                            or "-" in field
                            or ":" in field
                        )
                        if is_literal:
                            # Allow short strings, whitespace, and common punctuation
                            continue
                        else:
                            raise ValueError(f"Field '{field}' not found in data")

                # Concatenate
                result[new_field] = ""
                for field in fields_to_concat:
                    if isinstance(field, str):
                        if field in data.columns:
                            result[new_field] += data[field].astype(str)
                        else:
                            # Treat as literal string
                            result[new_field] += field
                    else:
                        result[new_field] += str(field)

            else:
                raise ValueError(f"Unknown transformation: {source}")

        else:
            # Constant value
            result[new_field] = source

    # Remove original fields that were renamed
    for field in fields_to_remove:
        if field in result.columns:
            result = result.drop(columns=[field])

    return result
