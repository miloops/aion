#!/usr/bin/env python3
"""
Advanced AION Demo - Showcasing all capabilities.
"""

import pandas as pd
import os
from aion.core.interpreter import AIONInterpreter


def main():
    """Demonstrate advanced AION functionality."""
    print("🧬 AION Advanced Demo - AI-Native Data Processing\n")

    # Create comprehensive sample data
    data = pd.DataFrame(
        {
            "id": [1, 2, 3, 4, 5, 6, 7, 8],
            "first_name": [
                "John",
                "Jane",
                "Bob",
                "Alice",
                "Charlie",
                "Diana",
                "Eve",
                "Frank",
            ],
            "last_name": [
                "Doe",
                "Smith",
                "Johnson",
                "Brown",
                "Wilson",
                "Davis",
                "Miller",
                "Garcia",
            ],
            "age": [25, 17, 30, 22, 19, 28, 35, 26],
            "status": [
                "active",
                "inactive",
                "active",
                "active",
                "inactive",
                "active",
                "active",
                "inactive",
            ],
            "created_at": [
                "2023-01-15",
                "2023-02-20",
                "2023-01-10",
                "2023-03-05",
                "2023-02-28",
                "2023-01-25",
                "2023-03-15",
                "2023-02-10",
            ],
            "activity_score": [85, 45, 92, 78, 60, 88, 95, 52],
            "department": [
                "Engineering",
                "Marketing",
                "Engineering",
                "Sales",
                "HR",
                "Engineering",
                "Sales",
                "Marketing",
            ],
        }
    )

    print("📊 Original Data:")
    print(data)
    print(f"Shape: {data.shape}")
    print()

    interpreter = AIONInterpreter()

    # Demo 1: Basic filtering and transformation
    print("🔍 Demo 1: Basic Data Processing")
    basic_program = {
        "pipeline": [
            {
                "task": "filter",
                "condition": {"field": "age", "operator": ">=", "value": 18},
            },
            {
                "task": "transform",
                "mapping": {
                    "user_id": "id",
                    "full_name": {"concat": ["first_name", " ", "last_name"]},
                },
            },
        ]
    }

    result = interpreter.execute(basic_program, data)
    if not result.errors:
        print("✅ Basic processing completed")
        print(f"Result: {len(result.data)} rows")
        print(result.data[["user_id", "full_name", "age"]].head())
    else:
        print("❌ Errors:", result.errors)
    print()

    # Demo 2: Advanced aggregation
    print("📈 Demo 2: Data Aggregation")
    agg_program = {
        "pipeline": [
            {
                "task": "aggregate",
                "group_by": ["department", "status"],
                "aggregations": {
                    "activity_score": ["mean", "max", "min"],
                    "age": "count",
                },
            }
        ]
    }

    result = interpreter.execute(agg_program, data)
    if not result.errors:
        print("✅ Aggregation completed")
        print(result.data)
    else:
        print("❌ Errors:", result.errors)
    print()

    # Demo 3: Complex pipeline with AI integration
    print("🤖 Demo 3: AI-Enhanced Pipeline")
    ai_program = {
        "pipeline": [
            {
                "task": "filter",
                "condition": {"field": "status", "operator": "==", "value": "active"},
            },
            {"task": "sort", "operation": {"field": "activity_score", "order": "desc"}},
            {
                "task": "transform",
                "mapping": {
                    "performance_summary": {
                        "concat": ["first_name", " (", "activity_score", " points)"]
                    }
                },
            },
            {
                "task": "model_call",
                "prompt": "Analyze this user's performance level:",
                "input_field": "performance_summary",
                "output_field": "ai_analysis",
                "provider": "simulate",
            },
        ]
    }

    result = interpreter.execute(ai_program, data)
    if not result.errors:
        print("✅ AI pipeline completed")
        print(result.data[["first_name", "activity_score", "ai_analysis"]].head())
    else:
        print("❌ Errors:", result.errors)
    print()

    # Demo 4: Export functionality
    print("💾 Demo 4: Data Export")

    # Create output directory
    os.makedirs("output", exist_ok=True)

    export_program = {
        "pipeline": [
            {
                "task": "filter",
                "condition": {"field": "status", "operator": "==", "value": "active"},
            },
            {
                "task": "transform",
                "mapping": {
                    "user_id": "id",
                    "full_name": {"concat": ["first_name", " ", "last_name"]},
                },
            },
            {"task": "export", "file_path": "output/active_users.csv", "format": "csv"},
        ]
    }

    result = interpreter.execute(export_program, data)
    if not result.errors:
        print("✅ Export completed")
        print("File saved to: output/active_users.csv")
        if os.path.exists("output/active_users.csv"):
            exported_data = pd.read_csv("output/active_users.csv")
            print(f"Exported {len(exported_data)} rows")
    else:
        print("❌ Errors:", result.errors)
    print()

    # Demo 5: Program explanation
    print("📖 Demo 5: Program Explanation")
    explanation = interpreter.explain(ai_program)
    print(explanation)
    print()

    # Demo 6: Error handling
    print("⚠️ Demo 6: Error Handling")
    error_program = {
        "pipeline": [
            {
                "task": "filter",
                "condition": {
                    "field": "nonexistent_field",
                    "operator": ">",
                    "value": 10,
                },
            }
        ]
    }

    result = interpreter.execute(error_program, data)
    if result.errors:
        print("✅ Error handling works")
        print("Error:", result.errors[0])
    else:
        print("❌ Expected error not caught")
    print()

    print("🎉 Advanced AION demo completed!")
    print("\nKey Features Demonstrated:")
    print("✅ Data filtering and transformation")
    print("✅ Complex aggregations")
    print("✅ AI model integration")
    print("✅ Data export capabilities")
    print("✅ Program explanation")
    print("✅ Robust error handling")


if __name__ == "__main__":
    main()
