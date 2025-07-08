"""
Command-line interface for AION.
"""

import argparse
import json
import sys
from pathlib import Path
import pandas as pd

from .core.interpreter import AIONInterpreter


def load_program(file_path: str) -> dict:
    """Load an AION program from a JSON file."""
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in '{file_path}': {e}")
        sys.exit(1)


def load_data(file_path: str) -> pd.DataFrame:
    """Load input data from a file."""
    path = Path(file_path)

    if path.suffix.lower() == ".csv":
        return pd.read_csv(file_path)
    elif path.suffix.lower() in [".json", ".jsonl"]:
        return pd.read_json(file_path)
    else:
        print(f"Error: Unsupported file format: {path.suffix}")
        sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="AION - AI-Oriented Notation Interpreter"
    )
    parser.add_argument("program_file", help="Path to AION program JSON file")
    parser.add_argument("--input", "-i", help="Path to input data file (CSV, JSON)")
    parser.add_argument("--output", "-o", help="Path to output file (CSV, JSON)")
    parser.add_argument(
        "--explain",
        "-e",
        action="store_true",
        help="Explain the program without executing it",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Show detailed execution logs"
    )

    args = parser.parse_args()

    # Load program
    program = load_program(args.program_file)

    # Explain mode
    if args.explain:
        interpreter = AIONInterpreter()
        explanation = interpreter.explain(program)
        print(explanation)
        return

    # Load input data
    input_data = None
    if args.input:
        input_data = load_data(args.input)

    # Execute program
    interpreter = AIONInterpreter()
    result = interpreter.execute(program, input_data)

    # Handle errors
    if result.errors:
        print("Execution failed with errors:")
        for error in result.errors:
            print(f"  - {error}")
        sys.exit(1)

    # Show logs if verbose
    if args.verbose:
        print("Execution logs:")
        for log in result.logs:
            print(f"  {log}")
        print()

    # Show results
    if isinstance(result.data, pd.DataFrame):
        if result.data.empty:
            print("Result: Empty dataset")
        else:
            print(
                f"Result: {len(result.data)} rows, {len(result.data.columns)} columns"
            )
            print(result.data.head())

            # Save output if specified
            if args.output:
                output_path = Path(args.output)
                if output_path.suffix.lower() == ".csv":
                    result.data.to_csv(args.output, index=False)
                elif output_path.suffix.lower() == ".json":
                    result.data.to_json(args.output, orient="records", indent=2)
                else:
                    print(f"Warning: Unknown output format: {output_path.suffix}")
                print(f"Results saved to: {args.output}")
    else:
        print(f"Result: {result.data}")


if __name__ == "__main__":
    main()
