# Quick Start

## Basic Usage

```python
from enhanced_wave_engine import EnhancedWaveEngine

# Create the engine
engine = EnhancedWaveEngine()

# Process a simple query
result = engine.process_query("What is 2 + 2?")
print(f"Answer: {result.answer}")
print(f"Confidence: {result.confidence}")
```

## Running Tests

Test the installation:

```bash
# Run basic tests
python test_conversational_wave_engine.py

# Run wave mechanics validation
python wave_mechanics_test.py

# Run performance benchmark
python fast_logicbench_benchmark.py
```

## Examples

### Logic Reasoning

```python
# Test logical reasoning
query = "If all cats are mammals, and Fluffy is a cat, is Fluffy a mammal?"
result = engine.process_query(query)
print(result.answer)  # Should be "yes"
```

### Mathematical Operations

```python
# Test mathematical reasoning
query = "What is the square root of 144?"
result = engine.process_query(query)
print(result.answer)  # Should be "12"
```

### Conversational AI

```python
# Test conversational abilities
query = "Hello, how are you today?"
result = engine.process_query(query)
print(result.answer)  # Natural language response
```

## Configuration

The Wave Engine can be configured for different use cases:

```python
# Create engine with custom settings
engine = EnhancedWaveEngine(
    max_experts=10,
    confidence_threshold=0.7,
    enable_learning=True
)
```

## Next Steps

- Explore the examples directory
- Read the architecture documentation
- Review the API reference
- Run the benchmark tests
- Check out the multi-language implementations 