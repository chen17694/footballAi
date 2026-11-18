# -*- coding: utf-8 -*-
"""
测试第三方代理是否透传 thinking / reasoning 块。
分别用三个模型各发一条简单请求，打印完整响应结构。

运行：  python test_thinking.py
"""
import sys, os, json, pprint
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import openai

API_KEY  = "sk-yFOTmuKp5mZee1kP6ZrS3FiCZqy63wvckE0fiAq0JLgu4fuZ"
BASE_URL = "https://globalai.vip/v1"

MODELS = [
    ("A - claude-fable-5-1",  "claude-fable-5-1"),
    ("B - gpt-6.2-astra",   "gpt-6.2-astra"),
    ("C - gpt-6-astra",       "gpt-6-astra"),
]

PROMPT = "1+1等于几？请先思考再回答。"

client = openai.OpenAI(api_key=API_KEY, base_url=BASE_URL)


def probe(label: str, model: str):
    print(f"\n{'='*60}")
    print(f"模型：{label}")
    print('='*60)

    # ── 1. 普通非流式，看 response 对象有哪些字段 ──────────────
    print("\n[1] 普通非流式调用 → 完整 response 结构：")
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": PROMPT}],
            max_tokens=512,
        )
        # 打印原始字典（含所有额外字段）
        raw = resp.model_dump()
        pprint.pprint(raw, width=100)

        # 检查常见 thinking 字段
        thinking_fields = []
        for choice in raw.get("choices", []):
            msg = choice.get("message", {})
            for key in msg:
                if key not in ("role", "content", "function_call", "tool_calls", "refusal", "annotations"):
                    thinking_fields.append((key, msg[key]))
        if thinking_fields:
            print(f"\n  ✅ 发现额外字段：{thinking_fields}")
        else:
            print("\n  ❌ message 里没有额外字段（无 thinking）")
    except Exception as e:
        print(f"  ❌ 报错：{e}")

    # ── 2. 流式调用，看 delta 有哪些额外字段 ──────────────────
    print("\n[2] 流式调用 → delta 结构（前 5 个 chunk）：")
    try:
        stream = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": PROMPT}],
            max_tokens=512,
            stream=True,
        )
        chunks_shown = 0
        for chunk in stream:
            if chunks_shown >= 5:
                break
            raw_chunk = chunk.model_dump()
            for choice in raw_chunk.get("choices", []):
                delta = choice.get("delta", {})
                # 只打印有内容的 delta
                non_empty = {k: v for k, v in delta.items() if v not in (None, "", [])}
                if non_empty:
                    print(f"  chunk {chunks_shown}: {non_empty}")
                    chunks_shown += 1
        if chunks_shown == 0:
            print("  （所有 chunk 的 delta 均为空）")
    except Exception as e:
        print(f"  ❌ 报错：{e}")

    # ── 3. 带 thinking 参数显式请求（看代理是否接受）──────────
    print("\n[3] 显式传 thinking 参数（budget_tokens=1024）：")
    try:
        resp2 = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": PROMPT}],
            max_tokens=1024,
            extra_body={"thinking": {"type": "enabled", "budget_tokens": 1024}},
        )
        raw2 = resp2.model_dump()
        for choice in raw2.get("choices", []):
            msg = choice.get("message", {})
            extras = {k: v for k, v in msg.items()
                      if k not in ("role", "content", "function_call", "tool_calls", "refusal", "annotations")}
            if extras:
                print(f"  ✅ 有额外字段：{extras}")
            else:
                print(f"  ❌ 无额外字段，content = {str(msg.get('content',''))[:200]}")
    except Exception as e:
        print(f"  ❌ 报错（代理拒绝或不支持）：{e}")


if __name__ == "__main__":
    for label, model in MODELS:
        probe(label, model)
    print(f"\n{'='*60}\n测试完毕\n")
