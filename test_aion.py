#!/usr/bin/env python3
"""
Test script to demonstrate AION functionality.
"""

import json
import pandas as pd
from aion.core.interpreter import AIONInterpreter

def main():
    """Demonstrate AION functionality."""
    print("🧬 AION - AI-Oriented Notation Demo\n")
    
    # Create sample data
    data = pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'first_name': ['John', 'Jane', 'Bob', 'Alice', 'Charlie'],
        'last_name': ['Doe', 'Smith', 'Johnson', 'Brown', 'Wilson'],
        'age': [25, 17, 30, 22, 19],
        'status': ['active', 'inactive', 'active', 'active', 'inactive'],
        'created_at': ['2023-01-15', '2023-02-20', '2023-01-10', '2023-03-05', '2023-02-28'],
        'activity_score': [85, 45, 92, 78, 60]
    })
    
    print("📊 Original Data:")
    print(data)
    print()
    
    # Example 1: Simple filter
    print("🔍 Example 1: Filter users over 18")
    filter_program = {
        "pipeline": [
            {
                "task": "filter",
                "condition": {
                    "field": "age",
                    "operator": ">",
                    "value": 18
                }
            }
        ]
    }
    
    interpreter = AIONInterpreter()
    result = interpreter.execute(filter_program, data)
    
    if result.errors:
        print("❌ Errors:", result.errors)
    else:
        print("✅ Result:")
        print(result.data)
    print()
    
    # Example 2: Complex pipeline
    print("🔄 Example 2: Full data pipeline")
    pipeline_program = {
        "pipeline": [
            {
                "task": "filter",
                "condition": {
                    "field": "status",
                    "operator": "==",
                    "value": "active"
                }
            },
            {
                "task": "sort",
                "operation": {
                    "field": "created_at",
                    "order": "desc"
                }
            },
            {
                "task": "transform",
                "mapping": {
                    "user_id": "id",
                    "signup_date": "created_at",
                    "full_name": {
                        "concat": ["first_name", " ", "last_name"]
                    }
                }
            }
        ]
    }
    
    result = interpreter.execute(pipeline_program, data)
    
    if result.errors:
        print("❌ Errors:", result.errors)
    else:
        print("✅ Result:")
        print(result.data)
    print()
    
    # Example 3: Explain functionality
    print("📖 Example 3: Program explanation")
    explanation = interpreter.explain(pipeline_program)
    print(explanation)
    print()
    
    # Example 4: Model call (simulated)
    print("🤖 Example 4: AI model integration")
    model_program = {
        "pipeline": [
            {
                "task": "model_call",
                "prompt": "Analyze user activity level:",
                "input_field": "activity_score",
                "output_field": "ai_analysis"
            }
        ]
    }
    
    result = interpreter.execute(model_program, data)
    
    if result.errors:
        print("❌ Errors:", result.errors)
    else:
        print("✅ Result:")
        print(result.data[['first_name', 'activity_score', 'ai_analysis']])
    print()
    
    print("🎉 AION demo completed!")

if __name__ == "__main__":
    main() 