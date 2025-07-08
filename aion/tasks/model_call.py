"""
Model call task implementation for AION.
"""

from typing import Dict, Any, Optional
import pandas as pd
import os
import logging

logger = logging.getLogger(__name__)


class ModelCallHandler:
    """Handles AI model calls with different providers."""
    
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    
    def call_openai(self, prompt: str, input_text: str, model: str = "gpt-3.5-turbo") -> str:
        """Call OpenAI API."""
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        try:
            import openai
            client = openai.OpenAI(api_key=self.openai_api_key)
            
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": input_text}
                ],
                max_tokens=150,
                temperature=0.1
            )
            return response.choices[0].message.content.strip()
        except ImportError:
            raise ImportError("OpenAI package not installed. Run: pip install openai")
        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
            return f"[AI Error: {str(e)}]"
    
    def call_anthropic(self, prompt: str, input_text: str, model: str = "claude-3-sonnet-20240229") -> str:
        """Call Anthropic API."""
        if not self.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=self.anthropic_api_key)
            
            response = client.messages.create(
                model=model,
                max_tokens=150,
                messages=[
                    {"role": "user", "content": f"{prompt}\n\nInput: {input_text}"}
                ]
            )
            return response.content[0].text.strip()
        except ImportError:
            raise ImportError("Anthropic package not installed. Run: pip install anthropic")
        except Exception as e:
            logger.error(f"Anthropic API call failed: {e}")
            return f"[AI Error: {str(e)}]"
    
    def simulate_call(self, prompt: str, input_text: str) -> str:
        """Simulate AI model call for testing."""
        return f"[AI: {prompt}] {input_text}"


def model_call_task(data: pd.DataFrame, task: Dict[str, Any]) -> pd.DataFrame:
    """Call an AI model to process data.
    
    Args:
        data: Input DataFrame
        task: Task configuration with prompt and fields
        
    Returns:
        DataFrame with model outputs
    """
    if data.empty:
        return data
    
    prompt = task["prompt"]
    input_field = task.get("input_field")
    output_field = task.get("output_field", "model_output")
    provider = task.get("provider", "simulate")  # openai, anthropic, simulate
    model = task.get("model", "gpt-3.5-turbo")
    
    result = data.copy()
    handler = ModelCallHandler()
    
    # Process each row
    if input_field and input_field in data.columns:
        outputs = []
        for idx, row in data.iterrows():
            input_text = str(row[input_field])
            
            try:
                if provider == "openai":
                    output = handler.call_openai(prompt, input_text, model)
                elif provider == "anthropic":
                    output = handler.call_anthropic(prompt, input_text, model)
                else:
                    output = handler.simulate_call(prompt, input_text)
                
                outputs.append(output)
                
            except Exception as e:
                logger.error(f"Model call failed for row {idx}: {e}")
                outputs.append(f"[Error: {str(e)}]")
        
        result[output_field] = outputs
    else:
        # No input field specified, just add the prompt as context
        result[output_field] = f"[AI: {prompt}]"
    
    return result 