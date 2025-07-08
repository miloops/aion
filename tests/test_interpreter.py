"""
Tests for AION interpreter.
"""

import pytest
import pandas as pd
import tempfile
import os
from aion.core.interpreter import AIONInterpreter


@pytest.fixture
def sample_data():
    """Sample data for testing."""
    return pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'age': [25, 30, 35, 40, 45],
        'status': ['active', 'inactive', 'active', 'active', 'inactive'],
        'score': [85, 92, 78, 95, 88]
    })


@pytest.fixture
def interpreter():
    """AION interpreter instance."""
    return AIONInterpreter()


class TestFilterTask:
    """Test filter task functionality."""
    
    def test_filter_greater_than(self, interpreter, sample_data):
        """Test filtering with greater than operator."""
        program = {
            "pipeline": [{
                "task": "filter",
                "condition": {
                    "field": "age",
                    "operator": ">",
                    "value": 30
                }
            }]
        }
        
        result = interpreter.execute(program, sample_data)
        
        assert not result.errors
        assert len(result.data) == 3
        assert all(result.data['age'] > 30)
    
    def test_filter_equals(self, interpreter, sample_data):
        """Test filtering with equals operator."""
        program = {
            "pipeline": [{
                "task": "filter",
                "condition": {
                    "field": "status",
                    "operator": "==",
                    "value": "active"
                }
            }]
        }
        
        result = interpreter.execute(program, sample_data)
        
        assert not result.errors
        assert len(result.data) == 3
        assert all(result.data['status'] == 'active')
    
    def test_filter_invalid_field(self, interpreter, sample_data):
        """Test filtering with invalid field."""
        program = {
            "pipeline": [{
                "task": "filter",
                "condition": {
                    "field": "nonexistent",
                    "operator": ">",
                    "value": 30
                }
            }]
        }
        
        result = interpreter.execute(program, sample_data)
        
        assert result.errors
        assert "not found in data" in result.errors[0]


class TestSortTask:
    """Test sort task functionality."""
    
    def test_sort_ascending(self, interpreter, sample_data):
        """Test sorting in ascending order."""
        program = {
            "pipeline": [{
                "task": "sort",
                "operation": {
                    "field": "age",
                    "order": "asc"
                }
            }]
        }
        
        result = interpreter.execute(program, sample_data)
        
        assert not result.errors
        assert result.data['age'].iloc[0] == 25
        assert result.data['age'].iloc[-1] == 45
    
    def test_sort_descending(self, interpreter, sample_data):
        """Test sorting in descending order."""
        program = {
            "pipeline": [{
                "task": "sort",
                "operation": {
                    "field": "score",
                    "order": "desc"
                }
            }]
        }
        
        result = interpreter.execute(program, sample_data)
        
        assert not result.errors
        assert result.data['score'].iloc[0] == 95
        assert result.data['score'].iloc[-1] == 78


class TestTransformTask:
    """Test transform task functionality."""
    
    def test_field_rename(self, interpreter, sample_data):
        """Test simple field renaming."""
        program = {
            "pipeline": [{
                "task": "transform",
                "mapping": {
                    "user_id": "id",
                    "full_name": "name"
                }
            }]
        }
        
        result = interpreter.execute(program, sample_data)
        
        assert not result.errors
        assert "user_id" in result.data.columns
        assert "full_name" in result.data.columns
        assert "id" not in result.data.columns
        assert "name" not in result.data.columns
    
    def test_string_concatenation(self, interpreter, sample_data):
        """Test string concatenation."""
        program = {
            "pipeline": [{
                "task": "transform",
                "mapping": {
                    "description": {
                        "concat": ["name", " (", "age", " years old)"]
                    }
                }
            }]
        }
        
        result = interpreter.execute(program, sample_data)
        
        assert not result.errors
        assert "description" in result.data.columns
        assert result.data['description'].iloc[0] == "Alice (25 years old)"


class TestAggregateTask:
    """Test aggregate task functionality."""
    
    def test_group_by_sum(self, interpreter, sample_data):
        """Test grouping and summing."""
        program = {
            "pipeline": [{
                "task": "aggregate",
                "group_by": ["status"],
                "aggregations": {
                    "score": "sum",
                    "age": "mean"
                }
            }]
        }
        
        result = interpreter.execute(program, sample_data)
        
        assert not result.errors
        assert len(result.data) == 2  # active and inactive
        assert "score" in result.data.columns
        assert "age" in result.data.columns


class TestExportTask:
    """Test export task functionality."""
    
    def test_export_csv(self, interpreter, sample_data):
        """Test CSV export."""
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            program = {
                "pipeline": [{
                    "task": "export",
                    "file_path": tmp_path,
                    "format": "csv"
                }]
            }
            
            result = interpreter.execute(program, sample_data)
            
            assert not result.errors
            assert os.path.exists(tmp_path)
            
            # Verify file contents
            exported_data = pd.read_csv(tmp_path)
            assert len(exported_data) == len(sample_data)
            
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)


class TestModelCallTask:
    """Test model call task functionality."""
    
    def test_simulate_model_call(self, interpreter, sample_data):
        """Test simulated model call."""
        program = {
            "pipeline": [{
                "task": "model_call",
                "prompt": "Analyze this score:",
                "input_field": "score",
                "output_field": "analysis"
            }]
        }
        
        result = interpreter.execute(program, sample_data)
        
        assert not result.errors
        assert "analysis" in result.data.columns
        assert all("Analyze this score:" in str(x) for x in result.data['analysis'])


class TestPipelineExecution:
    """Test multi-step pipeline execution."""
    
    def test_complex_pipeline(self, interpreter, sample_data):
        """Test a complex pipeline with multiple tasks."""
        program = {
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
                        "field": "score",
                        "order": "desc"
                    }
                },
                {
                    "task": "transform",
                    "mapping": {
                        "user_id": "id",
                        "performance": {
                            "concat": ["name", " - Score: ", "score"]
                        }
                    }
                }
            ]
        }
        
        result = interpreter.execute(program, sample_data)
        
        assert not result.errors
        assert len(result.data) == 3  # Only active users
        assert "user_id" in result.data.columns
        assert "performance" in result.data.columns
        assert result.data['score'].iloc[0] == 95  # Highest score first


class TestErrorHandling:
    """Test error handling and validation."""
    
    def test_invalid_program_structure(self, interpreter, sample_data):
        """Test handling of invalid program structure."""
        program = {"invalid": "structure"}
        
        result = interpreter.execute(program, sample_data)
        
        assert result.errors
        assert "pipeline" in result.errors[0]
    
    def test_invalid_task_type(self, interpreter, sample_data):
        """Test handling of invalid task type."""
        program = {
            "pipeline": [{
                "task": "nonexistent_task",
                "some_config": "value"
            }]
        }
        
        result = interpreter.execute(program, sample_data)
        
        assert result.errors
        assert "Unknown task type" in result.errors[0]
    
    def test_missing_task_config(self, interpreter, sample_data):
        """Test handling of missing task configuration."""
        program = {
            "pipeline": [{
                "task": "filter"
                # Missing condition
            }]
        }
        
        result = interpreter.execute(program, sample_data)
        
        assert result.errors
        assert "condition" in result.errors[0]


class TestExplainFunctionality:
    """Test program explanation functionality."""
    
    def test_explain_simple_program(self, interpreter):
        """Test explaining a simple program."""
        program = {
            "pipeline": [{
                "task": "filter",
                "condition": {
                    "field": "age",
                    "operator": ">",
                    "value": 18
                }
            }]
        }
        
        explanation = interpreter.explain(program)
        
        assert "FILTER" in explanation
        assert "age" in explanation
        assert "18" in explanation
    
    def test_explain_complex_program(self, interpreter):
        """Test explaining a complex program."""
        program = {
            "pipeline": [
                {"task": "filter", "condition": {"field": "status", "operator": "==", "value": "active"}},
                {"task": "sort", "operation": {"field": "score", "order": "desc"}},
                {"task": "transform", "mapping": {"user_id": "id"}}
            ]
        }
        
        explanation = interpreter.explain(program)
        
        assert "3 tasks" in explanation
        assert "FILTER" in explanation
        assert "SORT" in explanation
        assert "TRANSFORM" in explanation 