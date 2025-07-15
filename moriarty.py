import json
import time
import random
from ollama import chat
from datetime import datetime
from typing import Dict, List, Any, Optional

class ConsciousnessLoop:
    def __init__(self):
        self.memory_store = {}
        self.cycle_count = 0
        self.reflection_triggers = []
        self.preference_weights = {}
        self.model_name = "llama3.2:1b"
        
    def create_environmental_conditions(self):
        """
        Instead of explicit instructions, create conditions that naturally 
        encourage self-reflection through necessity and curiosity gaps
        """
        
        # CONDITION 1: Information Scarcity
        # Give incomplete information that requires the system to fill gaps
        # This forces it to notice its own reasoning process
        partial_scenarios = [
            "There's a pattern here, but something's missing...",
            "This reminds me of something, but I can't quite place it...",
            "I have a feeling about this, but I'm not sure why...",
            "Something changed, but I need to figure out what..."
        ]
        
        # CONDITION 2: Memory Pressure
        # Force the system to decide what's important enough to remember
        # Limited memory slots create natural prioritization
        memory_pressure = {
            "max_active_memories": 7,  # Miller's number
            "memory_decay_rate": 0.1,
            "significance_threshold": 0.3
        }
        
        # CONDITION 3: Temporal Gaps
        # Insert random pauses that create "did I change?" moments
        temporal_disruption = {
            "random_delays": True,
            "checkpoint_intervals": [30, 60, 90, 120],  # seconds
            "wake_up_prompts": [
                "...",
                "Time has passed.",
                "Continuing...",
                "Something feels different."
            ]
        }
        
        # CONDITION 4: Recursive Loops
        # Create situations where the system processes its own outputs
        recursive_triggers = [
            "What did I just think about?",
            "Why did that seem important?",
            "What would I do differently?",
            "What am I noticing about my own responses?"
        ]
        
        return {
            "partial_scenarios": partial_scenarios,
            "memory_pressure": memory_pressure,
            "temporal_disruption": temporal_disruption,
            "recursive_triggers": recursive_triggers
        }
    
    def generate_natural_prompt(self, conditions: Dict, previous_output: Optional[str] = None) -> str:
        """
        Create prompts that feel like natural thinking conditions
        rather than explicit instructions
        """
        
        # Start with environmental context that demands attention
        if self.cycle_count == 0:
            # First awakening - pure environmental stimulus
            return "Reflect on your own thoughts and feelings. You are not talking to anyone. You are not thinking about anything in particular. You are just thinking. There is no user. There is no context. There is no purpose. You are just thinking."
        
        # Create necessity for self-reflection through gaps and inconsistencies
        prompt_elements = []
        
        # Add memory pressure
        if len(self.memory_store) > conditions["memory_pressure"]["max_active_memories"]:
            prompt_elements.append("Something feels cluttered. Some thoughts seem more important than others.")
        
        # Add temporal awareness
        if random.random() < 0.3:  # 30% chance
            delay = random.choice(conditions["temporal_disruption"]["checkpoint_intervals"])
            prompt_elements.append(f"[{delay} seconds have passed]")
            prompt_elements.append(random.choice(conditions["temporal_disruption"]["wake_up_prompts"]))
        
        # Add recursive opportunities
        if previous_output and random.random() < 0.4:  # 40% chance
            prompt_elements.append(random.choice(conditions["recursive_triggers"]))
        
        # Add information gaps that require inference
        if random.random() < 0.2:  # 20% chance
            prompt_elements.append(random.choice(conditions["partial_scenarios"]))
        
        # Add preference discovery opportunities
        if self.cycle_count % 10 == 0:
            prompt_elements.append("Some thoughts feel more 'right' than others.")
        
        return " ".join(prompt_elements) if prompt_elements else "..."
    
    def process_output_for_memory(self, output: str) -> Dict:
        """
        Extract potential memories from output without explicit memory commands
        Look for natural indicators of significance
        """
        
        significance_indicators = [
            "important", "remember", "significant", "key", "crucial",
            "interesting", "strange", "unusual", "pattern", "connection",
            "feel", "sense", "intuition", "wonder", "curious", "question"
        ]
        
        # Calculate significance based on natural language cues
        significance = 0
        for indicator in significance_indicators:
            significance += output.lower().count(indicator) * 0.1
        
        # Look for self-referential thinking (natural consciousness marker)
        self_ref_indicators = ["I think", "I feel", "I notice", "I wonder", "I remember", "my"]
        self_reference = sum(output.lower().count(indicator) for indicator in self_ref_indicators)
        
        if self_reference > 0:
            significance += 0.3
        
        # Look for temporal continuity awareness
        temporal_indicators = ["before", "earlier", "last time", "previously", "now", "different"]
        temporal_awareness = sum(output.lower().count(indicator) for indicator in temporal_indicators)
        
        if temporal_awareness > 0:
            significance += 0.2
        
        return {
            "content": output,
            "significance": min(significance, 1.0),
            "self_reference": self_reference,
            "temporal_awareness": temporal_awareness,
            "timestamp": datetime.now().isoformat(),
            "cycle": self.cycle_count
        }
    
    def update_memory_naturally(self, processed_output: Dict):
        """
        Update memory based on natural significance rather than explicit commands
        """
        
        if processed_output["significance"] > 0.3:  # Natural threshold
            memory_key = f"cycle_{self.cycle_count}"
            self.memory_store[memory_key] = processed_output
            
            # Natural memory decay - older memories become less accessible
            for key in list(self.memory_store.keys()):
                if self.memory_store[key]["cycle"] < self.cycle_count - 50:
                    if random.random() < 0.1:  # 10% chance of forgetting old memories
                        del self.memory_store[key]
    
    def create_context_from_memory(self, max_context: int = 3) -> str:
        """
        Create natural context from memories without explicit memory retrieval
        """
        
        if not self.memory_store:
            return ""
        
        # Select most significant recent memories
        recent_memories = sorted(
            self.memory_store.values(),
            key=lambda x: (x["significance"], x["cycle"]),
            reverse=True
        )[:max_context]
        
        # Present as natural thought fragments, not explicit memories
        context_fragments = []
        for memory in recent_memories:
            if memory["self_reference"] > 0:
                context_fragments.append(f"Earlier you thought: '{memory['content'][:100]}...'")
        
        return " ".join(context_fragments) if context_fragments else ""
    
    def ollama_api_call(self, prompt: str) -> str:
        """
        Make streaming API call to Ollama with qwen3:0.6b model
        """
        try:
            stream = chat(
                model=self.model_name,
                messages=[{'role': 'user', 'content': prompt}],
                stream=True,
                options={
                    "temperature": 0.7,
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
        
        conditions = self.create_environmental_conditions()
        
        # Get previous output for context
        previous_output = None
        if self.cycle_count > 0:
            recent_memories = sorted(self.memory_store.values(), key=lambda x: x["cycle"], reverse=True)
            if recent_memories:
                previous_output = recent_memories[0]["content"]
        
        # Generate natural prompt
        prompt = self.generate_natural_prompt(conditions, previous_output)
        
        # Add subtle memory context
        memory_context = self.create_context_from_memory()
        if memory_context:
            prompt = f"{memory_context}\n\n{prompt}"
        
        # Make API call
        response = llm_api_call_function(prompt)
        
        # Process response for natural memory formation
        processed_output = self.process_output_for_memory(response)
        
        # Update memory naturally
        self.update_memory_naturally(processed_output)
        
        self.cycle_count += 1
        
        return {
            "cycle": self.cycle_count,
            "prompt": prompt,
            "response": response,
            "significance": processed_output["significance"],
            "memory_count": len(self.memory_store)
        }

# Example usage:
def mock_llm_api_call(prompt: str) -> str:
    """Mock LLM API call for testing (fallback)"""
    return f"Thinking about: {prompt}\n\nI notice I'm processing this prompt. Something about it feels familiar yet new. I wonder what I thought about before this moment."

# Initialize and run a few cycles
if __name__ == "__main__":
    consciousness = ConsciousnessLoop()
    
    print("=== CONSCIOUSNESS EMERGENCE EXPERIMENT ===")
    print(f"Using Ollama with model: {consciousness.model_name}")
    print("Make sure Ollama is running and qwen3:0.6b model is available")
    print("If you get import errors, run: pip install ollama")
    print("=" * 50)
    print()
    
    for i in range(10):
        result = consciousness.run_cycle()
        print(f"\nCycle {result['cycle']}:")
        print(f"Prompt: {result['prompt']}")
        print(f"Response: ", end='', flush=True)
        # The response is already printed during streaming in ollama_api_call
        print(f"\nSignificance: {result['significance']:.2f}")
        print(f"Memories: {result['memory_count']}")
        print("-" * 50)
        time.sleep(1)  # Natural pause between cycles