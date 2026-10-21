"""The model arm: ask a local model (Ollama) SAME / DIFFERENT for each pair.

Usage: python local_model.py pairs.json [model]
Needs Ollama on 127.0.0.1:11434. The eval used qwen3:30b-a3b-instruct-2507-q4_K_M.
"""
import json
import sys
import time
import urllib.request

SYSTEM = ("You decide if two US street addresses refer to the SAME physical property. "
          "Abbreviation and formatting differences (St/Street, Pkwy/Pky, W/West, punctuation) do NOT matter. "
          "A different house number, a different street name, or a CONFLICTING directional quadrant "
          "(NE vs SE) means they are different properties. "
          "Answer with exactly one word: SAME or DIFFERENT.")


def ask(model, a1, a2):
    body = json.dumps({"model": model, "stream": False,
                       "options": {"temperature": 0, "num_predict": 4},
                       "messages": [{"role": "system", "content": SYSTEM},
                                    {"role": "user", "content": f"A: {a1}\nB: {a2}"}]}).encode()
    req = urllib.request.Request("http://127.0.0.1:11434/api/chat", data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        out = json.load(resp)["message"]["content"].strip().upper()
    return 1 if out.startswith("SAME") else 0 if out.startswith("DIFF") else None


if __name__ == '__main__':
    pairs = json.load(open(sys.argv[1]))
    model = sys.argv[2] if len(sys.argv) > 2 else "qwen3:30b-a3b-instruct-2507-q4_K_M"
    t0 = time.time()
    right = sum(ask(model, p['a1'], p['a2']) == p['label'] for p in pairs)
    print(f"{right}/{len(pairs)} correct in {time.time() - t0:.0f}s")
