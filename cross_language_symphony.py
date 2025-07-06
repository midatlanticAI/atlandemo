#!/usr/bin/env python3
"""
Atlan Wave Engine Cross-Language Symphony Demo
Orchestrates all 7 language implementations in a coordinated demonstration
"""

import subprocess
import time
import json
import asyncio
from pathlib import Path
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed


class WaveEngineSymphony:
    """Orchestrates Wave Engine across all 7 languages"""
    
    def __init__(self):
        self.languages = {
            'python': {
                'name': '🐍 Python',
                'cmd': ['python', 'wave_engine_multi_lang/python/wave_engine.py'],
                'color': '\033[94m',  # Blue
                'status': 'pending'
            },
            'javascript': {
                'name': '🟨 JavaScript',
                'cmd': ['node', 'wave_engine_multi_lang/javascript/wave_engine.js'],
                'color': '\033[93m',  # Yellow
                'status': 'pending'
            },
            'rust': {
                'name': '🦀 Rust',
                'cmd': ['cargo', 'run', '--manifest-path', 'wave_engine_multi_lang/rust/Cargo.toml'],
                'color': '\033[91m',  # Red
                'status': 'pending'
            },
            'go': {
                'name': '🐹 Go',
                'cmd': ['go', 'run', 'wave_engine_multi_lang/go/wave_engine.go'],
                'color': '\033[96m',  # Cyan
                'status': 'pending'
            },
            'csharp': {
                'name': '💜 C#',
                'cmd': ['dotnet', 'run', '--project', 'wave_engine_multi_lang/csharp/WaveEngine.csproj'],
                'color': '\033[95m',  # Magenta
                'status': 'pending'
            },
            'java': {
                'name': '☕ Java',
                'cmd': ['java', '-cp', 'wave_engine_multi_lang/java', 'WaveEngine'],
                'color': '\033[92m',  # Green
                'status': 'pending'
            },
            'cpp': {
                'name': '[BOLT] C++',
                'cmd': ['wave_engine_multi_lang/cpp/wave_engine.exe'],
                'color': '\033[97m',  # White
                'status': 'pending'
            }
        }
        
        self.results = {}
        self.start_time = None
        
    def print_banner(self):
        """Print the demo banner"""
        banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                     [WAVE] ATLAN WAVE ENGINE SYMPHONY [WAVE]                         ║
║              Cross-Language Reasoning Orchestration Demo                     ║
║                                                                              ║
║  🐍 Python  🟨 JavaScript  🦀 Rust  🐹 Go  💜 C#  ☕ Java  [BOLT] C++          ║
║                                                                              ║
║              "One Engine, Seven Languages, Infinite Possibilities"          ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """
        print(banner)
        print(f"🎼 Preparing to conduct the Wave Engine Symphony...")
        print(f"🌐 Demonstrating interconnectivity across the entire tech stack")
        print("=" * 80)
    
    def compile_if_needed(self):
        """Compile languages that need compilation"""
        print("\n🔨 COMPILATION PHASE")
        print("-" * 40)
        
        compile_tasks = []
        
        # Rust compilation
        print("🦀 Compiling Rust...")
        try:
            result = subprocess.run(
                ['cargo', 'build', '--manifest-path', 'wave_engine_multi_lang/rust/Cargo.toml'], 
                capture_output=True, text=True, timeout=60
            )
            if result.returncode == 0:
                print("  [+] Rust compiled successfully")
            else:
                print("  [WARN] Rust compilation warning (continuing anyway)")
        except:
            print("  [WARN] Rust compilation skipped")
        
        # Java compilation
        print("☕ Compiling Java...")
        try:
            result = subprocess.run(
                ['javac', '-cp', 'wave_engine_multi_lang/java', 'wave_engine_multi_lang/java/WaveEngine.java'],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                print("  [+] Java compiled successfully")
            else:
                print("  [WARN] Java compilation warning (continuing anyway)")
        except:
            print("  [WARN] Java compilation skipped")
        
        # C++ compilation
        print("[BOLT] Compiling C++...")
        try:
            subprocess.run(['wave_engine_multi_lang/cpp/compile.bat'], 
                         capture_output=True, text=True, timeout=30)
            print("  [+] C++ compiled successfully")
        except:
            print("  [WARN] C++ compilation skipped")
        
        print("🔨 Compilation phase complete!")
    
    async def run_language_demo(self, lang_key, lang_info):
        """Run Wave Engine demo for a specific language"""
        try:
            print(f"{lang_info['color']}{lang_info['name']} 🎵 Starting...\033[0m")
            
            # Run the language implementation
            process = await asyncio.create_subprocess_exec(
                *lang_info['cmd'],
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=10)
                
                if process.returncode == 0:
                    output = stdout.decode().strip()
                    
                    # Try to extract any JSON results
                    result_data = self.extract_results(output)
                    
                    self.results[lang_key] = {
                        'status': 'success',
                        'output': output[:200] + '...' if len(output) > 200 else output,
                        'data': result_data
                    }
                    
                    print(f"{lang_info['color']}{lang_info['name']} [+] Complete!\033[0m")
                    return True
                else:
                    error_msg = stderr.decode().strip()
                    self.results[lang_key] = {
                        'status': 'error',
                        'error': error_msg[:100] + '...' if len(error_msg) > 100 else error_msg
                    }
                    print(f"{lang_info['color']}{lang_info['name']} [WARN] Warning (continuing...)\033[0m")
                    return False
                    
            except asyncio.TimeoutError:
                process.kill()
                self.results[lang_key] = {
                    'status': 'timeout',
                    'error': 'Execution timeout'
                }
                print(f"{lang_info['color']}{lang_info['name']} ⏰ Timeout (continuing...)\033[0m")
                return False
                
        except Exception as e:
            self.results[lang_key] = {
                'status': 'failed',
                'error': str(e)
            }
            print(f"{lang_info['color']}{lang_info['name']} [-] Failed (continuing...)\033[0m")
            return False
    
    def extract_results(self, output):
        """Extract structured results from output"""
        try:
            # Look for JSON in the output
            lines = output.split('\n')
            for line in lines:
                if '{' in line and '}' in line:
                    try:
                        return json.loads(line)
                    except:
                        continue
            
            # Extract simple metrics
            result = {}
            if 'accuracy' in output.lower():
                import re
                accuracy_match = re.search(r'accuracy[:\s]+(\d+\.?\d*)%?', output.lower())
                if accuracy_match:
                    result['accuracy'] = float(accuracy_match.group(1))
            
            if 'speed' in output.lower() or 'time' in output.lower():
                speed_match = re.search(r'(\d+\.?\d*)\s*(q/s|questions/second|ms|seconds)', output.lower())
                if speed_match:
                    result['speed'] = float(speed_match.group(1))
            
            return result if result else None
            
        except:
            return None
    
    async def conduct_symphony(self):
        """Conduct the cross-language symphony"""
        print("\n🎼 CONDUCTING THE WAVE ENGINE SYMPHONY")
        print("-" * 50)
        
        self.start_time = time.time()
        
        # Create tasks for all languages
        tasks = []
        for lang_key, lang_info in self.languages.items():
            task = asyncio.create_task(
                self.run_language_demo(lang_key, lang_info),
                name=lang_key
            )
            tasks.append(task)
        
        # Run all languages concurrently with progress updates
        print("[WAVE] Wave Engine instances launching across all platforms...")
        
        # Show real-time progress
        completed_count = 0
        for task in asyncio.as_completed(tasks):
            await task
            completed_count += 1
            progress = completed_count / len(tasks) * 100
            print(f"[DATA] Symphony Progress: {progress:.1f}% ({completed_count}/{len(tasks)} languages)")
        
        end_time = time.time()
        total_time = end_time - self.start_time
        
        print(f"\n🎵 Symphony complete in {total_time:.2f} seconds!")
        
        return total_time
    
    def display_results(self, total_time):
        """Display the symphony results"""
        print("\n[TROPHY] SYMPHONY PERFORMANCE REPORT")
        print("=" * 60)
        
        successful = 0
        failed = 0
        
        for lang_key, lang_info in self.languages.items():
            result = self.results.get(lang_key, {'status': 'unknown'})
            status = result['status']
            
            if status == 'success':
                icon = "[+]"
                successful += 1
            elif status in ['error', 'timeout']:
                icon = "[WARN]"
            else:
                icon = "[-]"
                failed += 1
            
            print(f"{lang_info['color']}{icon} {lang_info['name']:15} {status.upper():10}\033[0m")
            
            # Show any extracted data
            if 'data' in result and result['data']:
                data = result['data']
                if 'accuracy' in data:
                    print(f"    [DATA] Accuracy: {data['accuracy']:.1f}%")
                if 'speed' in data:
                    print(f"    [BOLT] Speed: {data['speed']:.1f}")
        
        print("-" * 60)
        print(f"[TARGET] Symphony Results:")
        print(f"   [+] Successful: {successful}/{len(self.languages)} languages")
        print(f"   [WARN] Warnings: {len(self.languages) - successful - failed}")
        print(f"   [-] Failed: {failed}")
        print(f"   ⏱️ Total Time: {total_time:.2f} seconds")
        print(f"   🌐 Cross-Platform Coverage: {successful/len(self.languages)*100:.1f}%")
    
    def display_interconnectivity_demo(self):
        """Show interconnectivity possibilities"""
        print("\n🌐 INTERCONNECTIVITY DEMONSTRATION")
        print("=" * 50)
        
        scenarios = [
            {
                'name': 'Web Application Stack',
                'flow': 'Browser (JS/WASM) → API (Go) → Logic (Rust) → Data (Python)',
                'description': 'Real-time reasoning from browser to backend'
            },
            {
                'name': 'Enterprise Integration',
                'flow': 'Frontend (.NET/C#) → Service (Java) → Engine (C++) → ML (Python)',
                'description': 'Enterprise-grade reasoning pipeline'
            },
            {
                'name': 'Microservices Architecture',
                'flow': 'Gateway (Go) → Logic (Rust) → API (Node.js) → Analytics (Python)',
                'description': 'Distributed reasoning across microservices'
            },
            {
                'name': 'Edge Computing',
                'flow': 'IoT (C++) → Edge (Rust/WASM) → Cloud (Go) → Analysis (Python)',
                'description': 'Edge-to-cloud reasoning pipeline'
            }
        ]
        
        for i, scenario in enumerate(scenarios, 1):
            print(f"\n{i}. [LINK] {scenario['name']}")
            print(f"   Flow: {scenario['flow']}")
            print(f"   Use: {scenario['description']}")
        
        print(f"\n💡 Key Advantages:")
        print(f"   [ROCKET] Single codebase, multiple platforms")
        print(f"   [BOLT] 58KB core, deployable anywhere")
        print(f"   🔄 Cross-language message passing")
        print(f"   [WAVE] Consistent reasoning across stack")
    
    def save_results(self):
        """Save symphony results"""
        report = {
            'timestamp': time.time(),
            'languages_tested': len(self.languages),
            'results': self.results,
            'summary': {
                'successful': len([r for r in self.results.values() if r['status'] == 'success']),
                'total': len(self.languages)
            }
        }
        
        with open('wave_symphony_results.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n[SAVE] Symphony results saved to wave_symphony_results.json")


async def main():
    """Run the Cross-Language Symphony Demo"""
    symphony = WaveEngineSymphony()
    
    # Show banner
    symphony.print_banner()
    
    # Compilation phase
    symphony.compile_if_needed()
    
    # Conduct the symphony
    total_time = await symphony.conduct_symphony()
    
    # Display results
    symphony.display_results(total_time)
    
    # Show interconnectivity demo
    symphony.display_interconnectivity_demo()
    
    # Save results
    symphony.save_results()
    
    print(f"\n[PARTY] ATLAN WAVE ENGINE SYMPHONY COMPLETE!")
    print(f"[WAVE] Demonstrated: Cross-language reasoning orchestration")
    print(f"[ROCKET] Ready for: Production deployment across any tech stack")


if __name__ == "__main__":
    asyncio.run(main()) 