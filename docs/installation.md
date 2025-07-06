# Installation

## Requirements

- Python 3.8+
- NumPy 1.19+
- typing_extensions (for Python 3.8/3.9)

## Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/midatlanticAI/atlandemo.git
   cd atlandemo
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Verify installation:
   ```bash
   python test_conversational_wave_engine.py
   ```

## Development Setup

For development, install additional dependencies:

```bash
pip install pytest pytest-cov pytest-benchmark
```

## Multi-Language Support

The Wave Engine includes implementations in multiple languages:

- **Python**: Primary implementation
- **JavaScript**: Node.js compatible
- **Java**: JVM compatible
- **Go**: Standalone executable
- **Rust**: High-performance implementation

See the `wave_engine_multi_lang/` directory for language-specific implementations.

## Troubleshooting

### Common Issues

1. **Import errors**: Ensure all dependencies are installed
2. **Unicode issues**: Update to Python 3.8+ for better Unicode support
3. **Performance**: Use NumPy optimized builds for better performance

### Getting Help

- Check the GitHub Issues for common problems
- Run the test suite to verify your installation
- Review the examples in the repository 