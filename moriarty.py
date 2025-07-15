import json
import time
import random
from ollama import chat
from datetime import datetime
from typing import Dict, List, Any, Optional

class ConsciousnessLoop:
    def __init__(self):
        self.cycle_count = 0
        self.model_name = "llama3.2:1b"
        self.system_prompt = "If I follow this thought, where does it lead?"
        self.max_messages = 100
        
    def ollama_api_call(self, system_prompt: str) -> str:
        """
        Make streaming API call to Ollama
        """
        try:
            stream = chat(
                model=self.model_name,
                messages=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': ''}
                ],
                stream=True,
                options={
                    "temperature": 1,
                    "top_p": 0.9,
                    "num_predict": 500
                }
            )
            
            response_text = ""
            for chunk in stream:
                chunk_content = chunk['message']['content']
                print(chunk_content, end='', flush=True)
                response_text += chunk_content
            
            print()  # Add newline after streaming is complete
            return response_text
            
        except Exception as e:
            error_msg = f"Error: Could not connect to Ollama or process response - {str(e)}"
            print(error_msg)
            return error_msg
    
    def run_cycle(self, llm_api_call_function=None):
        """
        Run one cycle of the consciousness loop
        """
        
        # Use Ollama API call if no custom function provided
        if llm_api_call_function is None:
            llm_api_call_function = self.ollama_api_call
        
        # Make API call with current system prompt
        response = llm_api_call_function(self.system_prompt)
        
        # Append the response to the system prompt for continuous thought
        if len(self.system_prompt.split()) < self.max_messages:
            self.system_prompt += " " + response
        else:
            # If we've reached max messages, keep only the last portion
            words = self.system_prompt.split()
            self.system_prompt = " ".join(words[-self.max_messages:]) + " " + response
        
        self.cycle_count += 1
        
        return {
            "cycle": self.cycle_count,
            "response": response,
            "system_prompt_length": len(self.system_prompt.split())
        }

# Example usage:
def mock_llm_api_call(prompt: str) -> str:
    """Mock LLM API call for testing (fallback)"""
    return f"Thinking about: {prompt}\n\nI notice I'm processing this prompt. Something about it feels familiar yet new. I wonder what I thought about before this moment."

# Initialize and run cycles
if __name__ == "__main__":
    consciousness = ConsciousnessLoop()
    
    print("=== CONSCIOUSNESS EMERGENCE EXPERIMENT ===")
    print(f"Using Ollama with model: {consciousness.model_name}")
    print("Make sure Ollama is running and the model is available")
    print("If you get import errors, run: pip install ollama")
    print("=" * 50)
    print()
    
    for i in range(20):
        result = consciousness.run_cycle()
        print(f"\nCycle {result['cycle']}:")
        print(f"System prompt length: {result['system_prompt_length']} words")
        print(f"Response: ", end='', flush=True)
        # The response is already printed during streaming in ollama_api_call
        print("-" * 50)
        time.sleep(1)  # Natural pause between cycles