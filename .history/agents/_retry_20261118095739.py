# -*- coding: utf-8 -*-
"""LLM 调用的报错重试助手。A/B/C/D 共用。"""
import time
import random
import logging

log = logging.getLogger(__name__)

# 这些错误属于"配置/凭证"问题，重试也是浪费，直接抛出
_NON_RETRYABLE_HINTS = (
    "authentication", "invalid api key", "invalid_api_key",
    "unauthorized", "permission denied", "401",
    "invalid x-api-key", "incorrect api key",
)


def call_with_retry(invoke_fn, messages, max_retries: int = 4, base_delay: float = 2.0):
    """带退避重试的 LLM 调用。

    invoke_fn: 接收 messages 列表的可调用对象（llm.invoke 或 structured_llm.invoke）。
    遇到瞬时错误（超时/连接/限流/5xx 等）指数退避后重试；
    遇到认证类错误立即抛出，不重试。
    """
    last_err = None
    for attempt in range(1, max_retries + 1):
        try:
            return invoke_fn(messages)
        except Exception as e:  # noqa: BLE001
            last_err = e
            err_text = repr(e).lower()

            # 认证/凭证类错误：重试无意义，直接抛出
            if any(h in err_text for h in _NON_RETRYABLE_HINTS):
                raise

            if attempt < max_retries:
                # 指数退避 + 抖动，避免雪崩
                delay = base_delay * (2 ** (attempt - 1)) + random.uniform(0, 1)
                log.warning(
                    "LLM 调用失败（第 %d/%d 次），%.1fs 后重试：%s",
                    attempt, max_retries, delay, repr(e)[:200],
                )
                time.sleep(delay)
            else:
                log.error("LLM 调用失败，已达最大重试次数 %d：%s", max_retries, repr(e)[:300])

    # 全部重试都失败，抛出最后一个错误
    raise last_err
