# Chapter 1: The Anatomy of an LLM — Code Lab

> 📖 **Book Chapter**: [Chapter 1 — The Anatomy of an LLM](../../book/chapter_1_anatomy.md)

Production implementations of core LLM mechanics: Scaled Dot-Product Attention, KV Cache VRAM Footprint Calculator, and Byte-Pair Encoding (BPE) Tokenization.

---

## 🎯 Multi-Tier Learning Tracks

### 🎓 Student Track (Foundations)
- **Concept**: Learn how LLMs process integer tokens instead of raw strings and why Transformer blocks use Key, Query, and Value matrices.
- **Lab Command**: `python kv_cache_calculator.py`
- **Exercise**: Run `bpe_tokenizer_demo.py` on python code snippets vs English text and note token counts.

### 🔬 Researcher Track (Empirical Benchmarks & Math)
- **Equations**:
  $$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$
  $$\text{KV Cache (Bytes)} = 2 \times N_{\text{layers}} \times D_{\text{hidden}} \times L_{\text{ctx}} \times B \times P_{\text{bytes}}$$
- **Experiment**: Run `python kv_cache_calculator.py` to compare memory overhead of 128k context on Llama 3 8B vs 70B across FP16, INT8, and INT4 precision.

### 🚀 AI Engineer Track (Production Systems)
- **Production Guardrail**: Avoid obscure custom XML formats that fragment BPE tokens. Stick to standard JSON tool calls to minimize token inflation.
- **Memory Scaling**: Calculate GPU VRAM allocation limits before deploying multi-tenant agent instances.

---

## 🛠️ Code Modules

| Module | Key Concept |
|--------|-------------|
| [`scaled_dot_product_attention.py`](./scaled_dot_product_attention.py) | Softmax attention scaling ($1/\sqrt{d_k}$) |
| [`kv_cache_calculator.py`](./kv_cache_calculator.py) | GPU VRAM calculator across context lengths & precision |
| [`bpe_tokenizer_demo.py`](./bpe_tokenizer_demo.py) | Tokenization mechanics & code fragmentation |
