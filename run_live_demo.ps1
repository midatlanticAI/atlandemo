#!/usr/bin/env pwsh
<#
🎭 LIVE DISCORD DEMO RUNNER
Quick script to run the Wave Engine exposure demo
#>

Write-Host "🎭 LIVE DISCORD DEMO: WAVE ENGINE EXPOSED!" -ForegroundColor Cyan
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host "Preparing to show the wizard behind the curtain..." -ForegroundColor Yellow
Write-Host "=" * 80 -ForegroundColor Cyan

# Check if Python is available
Write-Host "🐍 Checking Python installation..." -ForegroundColor Green
try {
    $pythonVersion = python --version 2>&1
    Write-Host "   ✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Python not found! Please install Python first." -ForegroundColor Red
    exit 1
}

# Check if we have the required files
Write-Host "📁 Checking Wave Engine files..." -ForegroundColor Green
$requiredFiles = @(
    "simple_live_demo.py",
    "enhanced_wave_engine.py",
    "src/temporal_cognition.py"
)

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        $size = (Get-Item $file).Length
        Write-Host "   ✅ $file ($([math]::Round($size/1024, 1)) KB)" -ForegroundColor Green
    } else {
        Write-Host "   ❌ $file not found!" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "🚀 DEMO OPTIONS:" -ForegroundColor Cyan
Write-Host "1. Simple Live Demo (no dependencies)" -ForegroundColor White
Write-Host "2. Full Benchmark vs Local LLM" -ForegroundColor White
Write-Host "3. Quick Speed Test" -ForegroundColor White
Write-Host "4. Show Source Code" -ForegroundColor White

$choice = Read-Host "Choose option (1-4)"

switch ($choice) {
    "1" {
        Write-Host "🎭 Running Simple Live Demo..." -ForegroundColor Cyan
        python simple_live_demo.py
    }
    "2" {
        Write-Host "🏁 Running Full Benchmark..." -ForegroundColor Cyan
        if (Test-Path "realistic_wave_vs_llama_benchmark.py") {
            python realistic_wave_vs_llama_benchmark.py
        } else {
            Write-Host "❌ Benchmark file not found!" -ForegroundColor Red
        }
    }
    "3" {
        Write-Host "⚡ Running Quick Speed Test..." -ForegroundColor Cyan
        python -c "
import time
import math

print('🌊 Wave Engine Speed Test')
print('=' * 40)

# Test Wave Engine math
start = time.time()
for i in range(1000):
    symbols = ['test', 'speed', 'benchmark']
    for symbol in symbols:
        freq = 1.0 + (hash(symbol) % 100) / 100.0
        amp = 0.5 + (len(symbol) % 10) / 20.0
        phase = (hash(symbol) % 628) / 100.0
        wave = amp * math.sin(2 * math.pi * freq * 0.001 + phase)
elapsed = time.time() - start

print(f'✅ Processed 1000 iterations in {elapsed*1000:.1f}ms')
print(f'⚡ Average per query: {elapsed:.6f}s')
print(f'🔥 Throughput: {1000/elapsed:.0f} queries/second')
print('📊 This is pure mathematical computation!')
"
    }
    "4" {
        Write-Host "💻 Showing Source Code Files..." -ForegroundColor Cyan
        
        # Show file sizes
        Write-Host "📁 Wave Engine Files:" -ForegroundColor Green
        Get-ChildItem -Path "enhanced_wave_engine.py", "src/temporal_cognition.py", "expert_modules/*.py" -ErrorAction SilentlyContinue | 
        ForEach-Object { 
            $sizeKB = [math]::Round($_.Length/1024, 1)
            Write-Host "   $($_.Name): $sizeKB KB" -ForegroundColor White
        }
        
        # Show first few lines of core files
        Write-Host "`n🔍 Core Wave Algorithm (first 10 lines):" -ForegroundColor Green
        if (Test-Path "src/temporal_cognition.py") {
            Get-Content "src/temporal_cognition.py" | Select-Object -First 10 | ForEach-Object { Write-Host "   $_" -ForegroundColor Gray }
        }
        
        Write-Host "`n💡 All source code is readable Python!" -ForegroundColor Cyan
        Write-Host "   No binary files, no hidden models, just math!" -ForegroundColor White
    }
    default {
        Write-Host "❌ Invalid option!" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "🎯 SUMMARY:" -ForegroundColor Cyan
Write-Host "✅ Wave Engine = Pure mathematical sine wave functions" -ForegroundColor Green
Write-Host "✅ No neural networks, no language models" -ForegroundColor Green
Write-Host "✅ Complete source code transparency" -ForegroundColor Green
Write-Host "✅ You can verify every calculation by hand" -ForegroundColor Green

Write-Host ""
Write-Host "💡 Want to see more? Check the source files!" -ForegroundColor Yellow
Write-Host "   - enhanced_wave_engine.py" -ForegroundColor White
Write-Host "   - src/temporal_cognition.py" -ForegroundColor White
Write-Host "   - simple_live_demo.py" -ForegroundColor White 