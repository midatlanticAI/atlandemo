# Simple one-command runner for Wave LogicBench benchmark
# Usage:  powershell -ExecutionPolicy Bypass -File run.ps1

$ErrorActionPreference = 'Stop'

Write-Host "[RUN] Setting up environment..."

if (-Not (Test-Path .venv)) {
    py -3 -m venv .venv
}

# Activate virtual env in current session
& .venv\Scripts\Activate.ps1

Write-Host "[RUN] Installing requirements..."
python -m pip install --upgrade pip > $null
python -m pip install -r requirements.txt > $null

Write-Host "[RUN] Executing full LogicBench benchmark..."
python wave_logicbench_full_benchmark.py

Write-Host "[DONE] Benchmark complete. Results saved to wave_logicbench_full_results.json" 