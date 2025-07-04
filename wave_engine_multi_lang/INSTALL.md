# Universal Wave Engine - Installation Guide

🌊 **Complete installation instructions for all 7 programming languages**

## Quick Start

The Universal Wave Engine supports 7 programming languages with identical functionality. Choose your preferred language(s):

- **Python** - AI/ML integration, data science
- **JavaScript** - Web development, Node.js
- **Java** - Enterprise applications, Android
- **C++** - High-performance systems, embedded
- **Rust** - Memory-safe systems programming
- **Go** - Cloud services, microservices
- **C#** - .NET applications, Unity games

## Prerequisites by Language

### 🐍 Python
- Python 3.8 or higher
- pip package manager

### 🟨 JavaScript
- Node.js 14.0 or higher
- npm or yarn package manager

### ☕ Java
- Java 8 or higher (JDK)
- Maven or Gradle (optional)

### ⚡ C++
- C++17 compatible compiler:
  - **Windows**: Visual Studio 2019+, MinGW-w64, or Clang
  - **Linux**: GCC 7+, Clang 5+
  - **macOS**: Xcode 10+, Clang 5+

### 🦀 Rust
- Rust 1.70 or higher
- Cargo package manager
- Install from: https://rustup.rs/

### 🐹 Go
- Go 1.19 or higher
- Install from: https://golang.org/dl/

### 🔷 C#
- .NET 6.0 or higher
- Install from: https://dotnet.microsoft.com/download

## Installation Methods

### Method 1: Package Managers (Recommended)

#### Python via PyPI
```bash
pip install universal-wave-engine
```

#### JavaScript via npm
```bash
npm install universal-wave-engine
```

#### C# via NuGet
```bash
dotnet add package UniversalWaveEngine
```

#### Rust via Cargo
```bash
cargo add universal-wave-engine
```

#### Go via go mod
```bash
go mod init your-project
go get github.com/wave-engine/universal-wave-engine
```

### Method 2: Source Installation

#### Clone Repository
```bash
git clone https://github.com/wave-engine/universal-wave-engine.git
cd universal-wave-engine
```

#### Language-Specific Setup

##### Python
```bash
cd python
pip install -e .
# Or for development
pip install -e .[dev,visualization]
```

##### JavaScript
```bash
cd javascript
npm install
npm test
```

##### Java
```bash
cd java
javac WaveEngine.java
java WaveEngine  # Test compilation
```

##### C++
```bash
cd cpp
# Windows (Visual Studio)
compile.bat

# Linux/macOS
g++ -std=c++17 -O3 wave_engine.cpp -o wave_engine
./wave_engine
```

##### Rust
```bash
cd rust
cargo build --release
cargo run --release
```

##### Go
```bash
cd go
go run wave_engine.go
```

##### C#
```bash
cd csharp
dotnet build
dotnet run
```

## Verification

### Run Cross-Language Validation
```bash
# From project root
python validation/cross_language_test.py
```

Expected output:
```
🎯 Overall Success Rate: 100.0%
✅ Passed: 7
❌ Failed: 0
```

### Language-Specific Tests

#### Python
```python
from universal_wave_engine import wave_process
result = wave_process(["test", "verification"])
print("Python OK:", bool(result))
```

#### JavaScript
```javascript
import { waveProcess } from 'universal-wave-engine';
const result = waveProcess(["test", "verification"]);
console.log("JavaScript OK:", Object.keys(result).length > 0);
```

#### Java
```java
WaveEngine engine = new WaveEngine();
Map<String, Double> result = engine.process(new String[]{"test", "verification"});
System.out.println("Java OK: " + !result.isEmpty());
```

#### C++
```cpp
WaveEngine engine;
auto result = engine.process({"test", "verification"});
std::cout << "C++ OK: " << !result.empty() << std::endl;
```

#### Rust
```rust
let engine = WaveEngine::new();
let result = engine.process(&["test", "verification"]);
println!("Rust OK: {}", !result.is_empty());
```

#### Go
```go
engine := NewWaveEngine()
result := engine.Process([]string{"test", "verification"})
fmt.Printf("Go OK: %v\n", len(result) > 0)
```

#### C#
```csharp
var engine = new WaveEngine();
var result = engine.Process(new[] {"test", "verification"});
Console.WriteLine($"C# OK: {result.Count > 0}");
```

## Docker Installation

### Multi-Language Container
```dockerfile
FROM ubuntu:22.04

# Install all language runtimes
RUN apt-get update && apt-get install -y \
    python3 python3-pip \
    nodejs npm \
    openjdk-17-jdk \
    build-essential \
    curl \
    && curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y \
    && curl -OL https://golang.org/dl/go1.21.0.linux-amd64.tar.gz \
    && tar -C /usr/local -xvf go1.21.0.linux-amd64.tar.gz

# Install .NET
RUN curl -sSL https://dot.net/v1/dotnet-install.sh | bash /dev/stdin --channel LTS

# Copy and build Wave Engine
COPY . /wave-engine
WORKDIR /wave-engine

# Install all implementations
RUN pip3 install -e python/ \
    && npm install \
    && cd rust && cargo build --release \
    && cd ../csharp && dotnet build

# Verify installation
RUN python3 validation/cross_language_test.py
```

### Build and Run
```bash
docker build -t universal-wave-engine .
docker run --rm universal-wave-engine
```

## IDE Setup

### Visual Studio Code
Install recommended extensions:
- Python
- JavaScript/TypeScript
- Java Extension Pack
- C/C++
- Rust Analyzer
- Go
- C# Dev Kit

### IntelliJ IDEA
- Python plugin
- JavaScript/TypeScript
- Java (built-in)
- Rust plugin
- Go plugin

### Visual Studio
- Python Tools
- Node.js Tools
- C++ (built-in)
- Rust Tools
- Go Tools

## Performance Optimization

### Compilation Flags

#### C++
```bash
# Maximum performance
g++ -std=c++17 -O3 -march=native -flto wave_engine.cpp -o wave_engine

# Debug build
g++ -std=c++17 -g -DDEBUG wave_engine.cpp -o wave_engine_debug
```

#### Rust
```bash
# Release build (default optimization)
cargo build --release

# Maximum optimization
RUSTFLAGS="-C target-cpu=native" cargo build --release
```

#### Go
```bash
# Optimized build
go build -ldflags="-s -w" -o wave_engine wave_engine.go
```

### Runtime Optimization

#### Python
```bash
# Use PyPy for ~5x speed improvement
pypy3 -m pip install universal-wave-engine
pypy3 your_wave_script.py
```

#### JavaScript
```bash
# Use Node.js with V8 optimizations
node --max-old-space-size=4096 --optimize-for-size your_wave_script.js
```

## Troubleshooting

### Common Issues

#### Import Errors
```bash
# Python: Module not found
pip install --upgrade universal-wave-engine

# JavaScript: Cannot resolve module
npm install --save universal-wave-engine

# C++: Header not found
# Ensure wave_engine.hpp is in include path
```

#### Compilation Errors
```bash
# C++: M_PI not defined (Windows)
# Add #define _USE_MATH_DEFINES before includes

# Rust: Cargo not found
# Install Rust: curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# C#: .NET not found
# Install .NET SDK from https://dotnet.microsoft.com/download
```

#### Performance Issues
- Ensure you're using release/optimized builds
- Check system resources (RAM, CPU)
- Verify compiler optimization flags
- Use appropriate data sizes (avoid excessive symbol lists)

### Platform-Specific Notes

#### Windows
- Use PowerShell or cmd.exe
- Install Visual Studio Build Tools for C++
- Use winget for package management: `winget install Microsoft.DotNet.SDK.8`

#### macOS
- Install Xcode command line tools: `xcode-select --install`
- Use Homebrew for dependencies: `brew install python3 node go rust`

#### Linux
- Install build essentials: `sudo apt-get install build-essential`
- Use system package manager for dependencies
- Consider using snap packages: `snap install go --classic`

## Getting Help

- **Documentation**: https://wave-engine.ai/docs
- **GitHub Issues**: https://github.com/wave-engine/universal-wave-engine/issues
- **Community**: https://discord.gg/wave-engine
- **Stack Overflow**: Tag your questions with `universal-wave-engine`

## Next Steps

After installation:
1. Run the validation suite to ensure everything works
2. Try the API demos: `python api/wave_api.py`
3. Explore the examples in each language directory
4. Read the performance optimization guide
5. Check out the integration tutorials

🌊 **Welcome to the Universal Wave Engine ecosystem!** 🌊 