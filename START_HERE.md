# START_HERE.md – Wave Engine in 60 Seconds 🚀

Welcome! This repo is the full research dump — successes, failures, experiments. If you just want to *see it work*, follow the steps below.

---
## TL;DR
```
# 1. Clone
git clone https://github.com/midatlanticAI/atlandemo.git
cd atlandemo

# 2. 30-second demo (logic reasoning)
python simple_wave_showcase.py

# 3. Chat with it (CLI chatbot)
python wave_interactive_chatbot.py

# 4. Reproduce speed benchmark
python quick_logicbench_test.py      # results → wave_vs_ollama_results.json
```
No extra dependencies, no GPU, runs on a toaster.

---
## What *is* Wave Engine?
• A 102 KB wave-interference reasoning core (file: `enhanced_wave_engine.py`).  
• Uses pure sin/cos math — **zero** neural networks or attention layers.  
• Deterministic, explainable, ~5 000× faster than transformer LLMs in LogicBench tests.

## What it *is not* (yet)
• It does **not** load or fine-tune existing LLM weights.  
• It is **not** a production-ready ChatGPT replacement.  
• UX is CLI-only for now — contributions welcome!

---
## License & Patent
MIT for **personal/research** use. For any commercial or embedded use, licensing is required under U.S. Provisional Patent **63/839,719**.

Contact: john@midatlantic.ai  |  +1-540-604-3368

Have fun, break things, and please open issues/pull requests with your findings! 🚀 