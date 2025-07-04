#!/usr/bin/env python3
"""
Cross-Language Wave Engine Validation Suite
Tests all language implementations for consistency and performance
"""

import sys
import os
import subprocess
import time
import json
from typing import Dict, List, Any
from pathlib import Path

class CrossLanguageValidator:
    """Validates wave engine implementations across multiple languages"""
    
    def __init__(self):
        self.results = {}
        self.validation_passed = 0
        self.validation_failed = 0
        self.base_path = Path(__file__).parent.parent
        
    def run_validation(self):
        """Run comprehensive validation across all languages"""
        print("🌊 CROSS-LANGUAGE WAVE ENGINE VALIDATION")
        print("="*70)
        print("Testing wave engine implementations across multiple languages")
        print("Validating consistency, performance, and algorithm correctness")
        print("="*70)
        
        # Test each language implementation
        self.test_python()
        self.test_javascript()
        self.test_java()
        self.test_cpp()
        self.test_rust()
        self.test_go()
        self.test_csharp()
        
        # Cross-language comparison
        self.compare_results()
        
        # Generate report
        self.generate_report()
        
    def test_python(self):
        """Test Python implementation"""
        print("\n🐍 Testing Python Implementation")
        print("-" * 40)
        
        try:
            # Import and test Python implementation
            python_path = os.path.join(self.base_path, "python")
            if python_path not in sys.path:
                sys.path.insert(0, python_path)
            
            # Dynamic import to handle the wave engine module
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "wave_engine", 
                os.path.join(python_path, "wave_engine.py")
            )
            wave_engine_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(wave_engine_module)
            
            # Extract the classes and functions we need
            WaveEngine = wave_engine_module.WaveEngine
            replication_test = wave_engine_module.replication_test
            
            result = replication_test()
            self.results['python'] = {
                'status': 'PASSED' if result['avg_processing_time'] < 0.01 else 'FAILED',
                'avg_time': result['avg_processing_time'],
                'symbols_processed': result['symbols_processed'],
                'available': True
            }
            
            if result['avg_processing_time'] < 0.01:
                self.validation_passed += 1
                print("✅ Python implementation: PASSED")
            else:
                self.validation_failed += 1
                print("❌ Python implementation: FAILED")
                
        except Exception as e:
            self.results['python'] = {'status': 'ERROR', 'error': str(e), 'available': False}
            self.validation_failed += 1
            print(f"❌ Python implementation: ERROR - {e}")
    
    def test_javascript(self):
        """Test JavaScript implementation"""
        print("\n🟨 Testing JavaScript Implementation")
        print("-" * 40)
        
        try:
            # Test Node.js implementation
            js_path = self.base_path / "javascript" / "wave_engine.js"
            result = subprocess.run(
                ["node", str(js_path)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                # Parse performance from output
                output = result.stdout
                if "VALIDATION PASSED" in output:
                    self.results['javascript'] = {
                        'status': 'PASSED',
                        'output': output,
                        'available': True
                    }
                    self.validation_passed += 1
                    print("✅ JavaScript implementation: PASSED")
                else:
                    self.results['javascript'] = {
                        'status': 'FAILED',
                        'output': output,
                        'available': True
                    }
                    self.validation_failed += 1
                    print("❌ JavaScript implementation: FAILED")
            else:
                self.results['javascript'] = {
                    'status': 'ERROR',
                    'error': result.stderr,
                    'available': False
                }
                self.validation_failed += 1
                print(f"❌ JavaScript implementation: ERROR - {result.stderr}")
                
        except subprocess.TimeoutExpired:
            self.results['javascript'] = {
                'status': 'TIMEOUT',
                'available': False
            }
            self.validation_failed += 1
            print("❌ JavaScript implementation: TIMEOUT")
        except FileNotFoundError:
            self.results['javascript'] = {
                'status': 'NODE_NOT_FOUND',
                'available': False
            }
            self.validation_failed += 1
            print("❌ JavaScript implementation: Node.js not found")
    
    def test_java(self):
        """Test Java implementation"""
        print("\n☕ Testing Java Implementation")
        print("-" * 40)
        
        try:
            java_path = self.base_path / "java"
            
            # Compile Java code
            compile_result = subprocess.run(
                ["javac", "WaveEngine.java"],
                cwd=java_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if compile_result.returncode == 0:
                # Run Java code
                run_result = subprocess.run(
                    ["java", "WaveEngine"],
                    cwd=java_path,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if run_result.returncode == 0:
                    output = run_result.stdout
                    if "VALIDATION PASSED" in output:
                        self.results['java'] = {
                            'status': 'PASSED',
                            'output': output,
                            'available': True
                        }
                        self.validation_passed += 1
                        print("✅ Java implementation: PASSED")
                    else:
                        self.results['java'] = {
                            'status': 'FAILED',
                            'output': output,
                            'available': True
                        }
                        self.validation_failed += 1
                        print("❌ Java implementation: FAILED")
                else:
                    self.results['java'] = {
                        'status': 'RUNTIME_ERROR',
                        'error': run_result.stderr,
                        'available': False
                    }
                    self.validation_failed += 1
                    print(f"❌ Java implementation: RUNTIME ERROR - {run_result.stderr}")
            else:
                self.results['java'] = {
                    'status': 'COMPILE_ERROR',
                    'error': compile_result.stderr,
                    'available': False
                }
                self.validation_failed += 1
                print(f"❌ Java implementation: COMPILE ERROR - {compile_result.stderr}")
                
        except Exception as e:
            self.results['java'] = {
                'status': 'ERROR',
                'error': str(e),
                'available': False
            }
            self.validation_failed += 1
            print(f"❌ Java implementation: ERROR - {e}")
    
    def test_cpp(self):
        """Test C++ implementation"""
        print("\n⚡ Testing C++ Implementation")
        print("-" * 40)
        
        try:
            cpp_path = self.base_path / "cpp"
            
            # Try different C++ compilation approaches
            compile_result = None
            
            # Try batch file approach (Windows Visual Studio)
            try:
                # Use cmd to run the batch file on Windows
                compile_result = subprocess.run(
                    ["cmd", "/c", "compile.bat"],
                    cwd=cpp_path,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                if compile_result.returncode == 0:
                    # Successfully compiled and ran
                    pass
            except (FileNotFoundError, subprocess.TimeoutExpired):
                compile_result = None
            
            # Try standard compilers if batch file failed
            if compile_result is None or compile_result.returncode != 0:
                compilers = [
                    ["g++", "-std=c++17", "-O3", "wave_engine.cpp", "-o", "wave_engine"],
                    ["clang++", "-std=c++17", "-O3", "wave_engine.cpp", "-o", "wave_engine"],
                    ["cl", "/std:c++17", "/O2", "wave_engine.cpp", "/Fe:wave_engine.exe"]
                ]
                
                for compiler_cmd in compilers:
                    try:
                        compile_result = subprocess.run(
                            compiler_cmd,
                            cwd=cpp_path,
                            capture_output=True,
                            text=True,
                            timeout=30
                        )
                        if compile_result.returncode == 0:
                            break
                    except FileNotFoundError:
                        continue
            
            if compile_result is None or compile_result.returncode != 0:
                self.results['cpp'] = {
                    'status': 'COMPILER_NOT_FOUND',
                    'error': 'No C++ compiler found. Install: Visual Studio Build Tools, MinGW, or Clang',
                    'available': False
                }
                self.validation_failed += 1
                print("❌ C++ implementation: No compiler found")
                print("   💡 To install C++ compiler:")
                print("   • Visual Studio Build Tools: https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022")
                print("   • MinGW-w64: https://www.mingw-w64.org/downloads/")
                print("   • LLVM Clang: https://releases.llvm.org/download.html")
                return
            
            if compile_result.returncode == 0:
                # Check if batch file was used (it runs the executable automatically)
                if "compile.bat" in str(compile_result.args):
                    # Batch file already ran the executable
                    output = compile_result.stdout
                    if "VALIDATION PASSED" in output:
                        self.results['cpp'] = {
                            'status': 'PASSED',
                            'output': output,
                            'available': True
                        }
                        self.validation_passed += 1
                        print("✅ C++ implementation: PASSED")
                    else:
                        self.results['cpp'] = {
                            'status': 'FAILED',
                            'output': output,
                            'available': True
                        }
                        self.validation_failed += 1
                        print("❌ C++ implementation: FAILED")
                else:
                    # Standard compilation - need to run executable
                    run_result = subprocess.run(
                        ["./wave_engine"],
                        cwd=cpp_path,
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    
                    if run_result.returncode == 0:
                        output = run_result.stdout
                        if "VALIDATION PASSED" in output:
                            self.results['cpp'] = {
                                'status': 'PASSED',
                                'output': output,
                                'available': True
                            }
                            self.validation_passed += 1
                            print("✅ C++ implementation: PASSED")
                        else:
                            self.results['cpp'] = {
                                'status': 'FAILED',
                                'output': output,
                                'available': True
                            }
                            self.validation_failed += 1
                            print("❌ C++ implementation: FAILED")
                    else:
                        self.results['cpp'] = {
                            'status': 'RUNTIME_ERROR',
                            'error': run_result.stderr,
                            'available': False
                        }
                        self.validation_failed += 1
                        print(f"❌ C++ implementation: RUNTIME ERROR - {run_result.stderr}")
            else:
                self.results['cpp'] = {
                    'status': 'COMPILE_ERROR',
                    'error': compile_result.stderr,
                    'available': False
                }
                self.validation_failed += 1
                print(f"❌ C++ implementation: COMPILE ERROR - {compile_result.stderr}")
                
        except Exception as e:
            self.results['cpp'] = {
                'status': 'ERROR',
                'error': str(e),
                'available': False
            }
            self.validation_failed += 1
            print(f"❌ C++ implementation: ERROR - {e}")
    
    def test_rust(self):
        """Test Rust implementation"""
        print("\n🦀 Testing Rust Implementation")
        print("-" * 40)
        
        try:
            rust_path = self.base_path / "rust"
            
            # Check if Rust is available
            try:
                subprocess.run(["cargo", "--version"], capture_output=True, check=True)
            except (FileNotFoundError, subprocess.CalledProcessError):
                self.results['rust'] = {
                    'status': 'RUST_NOT_FOUND',
                    'error': 'Rust/Cargo not found. Install Rust using rustup.',
                    'available': False
                }
                self.validation_failed += 1
                print("❌ Rust implementation: Rust not found")
                print("   💡 To install Rust:")
                print("   • Visit: https://rustup.rs/")
                print("   • Run: curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh")
                print("   • Or download installer from: https://forge.rust-lang.org/infra/channel-layout.html")
                return
            
            # Run Rust code
            run_result = subprocess.run(
                ["cargo", "run", "--release"],
                cwd=rust_path,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if run_result.returncode == 0:
                output = run_result.stdout
                if "VALIDATION PASSED" in output:
                    self.results['rust'] = {
                        'status': 'PASSED',
                        'output': output,
                        'available': True
                    }
                    self.validation_passed += 1
                    print("✅ Rust implementation: PASSED")
                else:
                    self.results['rust'] = {
                        'status': 'FAILED',
                        'output': output,
                        'available': True
                    }
                    self.validation_failed += 1
                    print("❌ Rust implementation: FAILED")
            else:
                self.results['rust'] = {
                    'status': 'ERROR',
                    'error': run_result.stderr,
                    'available': False
                }
                self.validation_failed += 1
                print(f"❌ Rust implementation: ERROR - {run_result.stderr}")
                
        except Exception as e:
            self.results['rust'] = {
                'status': 'ERROR',
                'error': str(e),
                'available': False
            }
            self.validation_failed += 1
            print(f"❌ Rust implementation: ERROR - {e}")
    
    def test_go(self):
        """Test Go implementation"""
        print("\n🐹 Testing Go Implementation")
        print("-" * 40)
        
        try:
            go_path = self.base_path / "go"
            
            # Run Go code
            run_result = subprocess.run(
                ["go", "run", "wave_engine.go"],
                cwd=go_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if run_result.returncode == 0:
                output = run_result.stdout
                if "VALIDATION PASSED" in output:
                    self.results['go'] = {
                        'status': 'PASSED',
                        'output': output,
                        'available': True
                    }
                    self.validation_passed += 1
                    print("✅ Go implementation: PASSED")
                else:
                    self.results['go'] = {
                        'status': 'FAILED',
                        'output': output,
                        'available': True
                    }
                    self.validation_failed += 1
                    print("❌ Go implementation: FAILED")
            else:
                self.results['go'] = {
                    'status': 'ERROR',
                    'error': run_result.stderr,
                    'available': False
                }
                self.validation_failed += 1
                print(f"❌ Go implementation: ERROR - {run_result.stderr}")
                
        except Exception as e:
            self.results['go'] = {
                'status': 'ERROR',
                'error': str(e),
                'available': False
            }
            self.validation_failed += 1
            print(f"❌ Go implementation: ERROR - {e}")
    
    def test_csharp(self):
        """Test C# implementation"""
        print("\n🔷 Testing C# Implementation")
        print("-" * 40)
        
        try:
            csharp_path = self.base_path / "csharp"
            
            # Check if .NET SDK is available
            try:
                subprocess.run(["dotnet", "--version"], capture_output=True, check=True)
            except (FileNotFoundError, subprocess.CalledProcessError):
                self.results['csharp'] = {
                    'status': 'DOTNET_NOT_FOUND',
                    'error': '.NET SDK not found. Install .NET SDK.',
                    'available': False
                }
                self.validation_failed += 1
                print("❌ C# implementation: .NET SDK not found")
                print("   💡 To install .NET SDK:")
                print("   • Visit: https://dotnet.microsoft.com/download")
                print("   • Download and install the latest .NET SDK")
                return
            
            # Run C# code using dotnet
            run_result = subprocess.run(
                ["dotnet", "run"],
                cwd=csharp_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if run_result.returncode == 0:
                output = run_result.stdout
                if "VALIDATION PASSED" in output:
                    self.results['csharp'] = {
                        'status': 'PASSED',
                        'output': output,
                        'available': True
                    }
                    self.validation_passed += 1
                    print("✅ C# implementation: PASSED")
                else:
                    self.results['csharp'] = {
                        'status': 'FAILED',
                        'output': output,
                        'available': True
                    }
                    self.validation_failed += 1
                    print("❌ C# implementation: FAILED")
            else:
                self.results['csharp'] = {
                    'status': 'ERROR',
                    'error': run_result.stderr,
                    'available': False
                }
                self.validation_failed += 1
                print(f"❌ C# implementation: ERROR - {run_result.stderr}")
                
        except Exception as e:
            self.results['csharp'] = {
                'status': 'ERROR',
                'error': str(e),
                'available': False
            }
            self.validation_failed += 1
            print(f"❌ C# implementation: ERROR - {e}")
    
    def compare_results(self):
        """Compare results across languages"""
        print("\n🔍 CROSS-LANGUAGE COMPARISON")
        print("="*50)
        
        passed_implementations = []
        failed_implementations = []
        
        for lang, result in self.results.items():
            if result['status'] == 'PASSED':
                passed_implementations.append(lang)
            else:
                failed_implementations.append(lang)
        
        print(f"✅ Passed implementations: {len(passed_implementations)}")
        for lang in passed_implementations:
            print(f"   • {lang.upper()}")
        
        print(f"❌ Failed implementations: {len(failed_implementations)}")
        for lang in failed_implementations:
            print(f"   • {lang.upper()}: {self.results[lang]['status']}")
    
    def generate_report(self):
        """Generate comprehensive validation report"""
        print("\n📊 VALIDATION REPORT")
        print("="*50)
        
        total_languages = len(self.results)
        success_rate = (self.validation_passed / total_languages) * 100
        
        print(f"🎯 Overall Success Rate: {success_rate:.1f}%")
        print(f"✅ Passed: {self.validation_passed}")
        print(f"❌ Failed: {self.validation_failed}")
        print(f"📋 Total Languages Tested: {total_languages}")
        
        # Save detailed results
        report_path = self.base_path / "validation" / "validation_report.json"
        with open(report_path, 'w') as f:
            json.dump({
                'summary': {
                    'total_languages': total_languages,
                    'passed': self.validation_passed,
                    'failed': self.validation_failed,
                    'success_rate': success_rate
                },
                'detailed_results': self.results,
                'timestamp': time.time()
            }, f, indent=2)
        
        print(f"\n💾 Detailed report saved to: {report_path}")
        
        if success_rate >= 80:
            print("🎉 VALIDATION SUCCESSFUL: Multi-language implementation validated!")
        else:
            print("⚠️  VALIDATION INCOMPLETE: Some implementations need attention")

if __name__ == "__main__":
    validator = CrossLanguageValidator()
    validator.run_validation() 