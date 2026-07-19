"""
Chapter 1: BPE Tokenizer Demo
==============================
Demonstrates how Byte-Pair Encoding tokenization affects agent performance.
Shows why standard JSON is preferred over exotic formats for tool calls.

From: The Practitioner's Handbook of Agentic AI, Chapter 1.1.1
"""

try:
    import tiktoken
except ImportError:
    print("Install tiktoken: pip install tiktoken")
    exit(1)


def analyze_tokenization(text: str, encoding_name: str = "cl100k_base") -> dict:
    """
    Analyzes how a given text is tokenized by a specific BPE vocabulary.

    Returns token count, tokens, and compression ratio.
    """
    encoder = tiktoken.get_encoding(encoding_name)
    token_ids = encoder.encode(text)
    tokens = [encoder.decode([tid]) for tid in token_ids]

    return {
        "text": text,
        "encoding": encoding_name,
        "token_count": len(token_ids),
        "token_ids": token_ids,
        "tokens": tokens,
        "chars_per_token": len(text) / len(token_ids) if token_ids else 0,
    }


if __name__ == "__main__":
    print("=" * 70)
    print("BPE Tokenizer Demo — Why Format Choice Matters for Agents")
    print("=" * 70)

    # Standard code patterns (well-compressed)
    standard_examples = [
        'def __init__(self):',
        '{"name": "search_web", "query": "latest news"}',
        'import numpy as np',
        'self.model = AutoModelForCausalLM.from_pretrained("meta-llama")',
    ]

    # Exotic formats (poorly compressed, more tokens)
    exotic_examples = [
        '<TOOL_CALL::search_web::PARAMS::query=latest+news::END>',
        '|||FUNCTION:search_web|||ARG:query=latest news|||',
        '@@INVOKE(search_web){query:"latest news"}@@',
    ]

    print("\n📊 Standard Formats (Well-Compressed by BPE):")
    print("-" * 70)
    for text in standard_examples:
        result = analyze_tokenization(text)
        print(f"  Text: {text}")
        print(f"  Tokens: {result['token_count']} | "
              f"Ratio: {result['chars_per_token']:.1f} chars/token")
        print(f"  Breakdown: {result['tokens']}")
        print()

    print("\n⚠️  Exotic Formats (Fragmented — More Tokens, Worse Reasoning):")
    print("-" * 70)
    for text in exotic_examples:
        result = analyze_tokenization(text)
        print(f"  Text: {text}")
        print(f"  Tokens: {result['token_count']} | "
              f"Ratio: {result['chars_per_token']:.1f} chars/token")
        print(f"  Breakdown: {result['tokens']}")
        print()

    # Direct comparison
    json_format = '{"name": "search_web", "query": "latest AI news"}'
    xml_format = '<tool_call name="search_web"><param name="query">latest AI news</param></tool_call>'

    json_result = analyze_tokenization(json_format)
    xml_result = analyze_tokenization(xml_format)

    print("=" * 70)
    print("HEAD-TO-HEAD: JSON vs Custom XML for Tool Calls")
    print("=" * 70)
    print(f"  JSON: {json_result['token_count']} tokens")
    print(f"  XML:  {xml_result['token_count']} tokens")
    print(f"  Overhead: {xml_result['token_count'] - json_result['token_count']} "
          f"extra tokens ({(xml_result['token_count']/json_result['token_count'] - 1)*100:.0f}% more)")
    print(f"\n  → Stick to standard JSON for agent tool calls.")
    print(f"  → Exotic formats waste tokens AND degrade reasoning quality.")
