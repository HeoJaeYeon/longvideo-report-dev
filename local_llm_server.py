#!/usr/bin/env python3
"""
 Qwen3-VL-8B를 OpenAI 호환 API로 제공. 요청은 잠금으로 한 번에 하나씩 처리. 요청 길이를 상한으로 자름(:120). 토큰 계산은 잠금 안(I28). 
Local OpenAI-compatible chat server (transformers backend) for the report framework.

Exposes POST /v1/chat/completions backed by WorldMM's Qwen3VLModel
(Qwen/Qwen3-VL-8B-Instruct, bf16, flash-attn, loaded once). Deep-Reporter
(ReasoningOpenAI -> openai SDK) and the L1 episodic filter call it like any OpenAI
endpoint. Clients only depend on the endpoint contract, so a vLLM server can replace
this process later on the same host/port with no client change, e.g.
    vllm serve Qwen/Qwen3-VL-8B-Instruct --served-model-name qwen3vl-8b --port 8010
and set `llm.local.endpoint.server: vllm` in config.yaml.

Contract implemented (what Deep-Reporter reads): choices[0].message.content,
choices[0].finish_reason, usage.{prompt,completion,total}_tokens.
Non-streaming only. Requests are served one at a time (single GPU model).
Ignored request fields: chat_template_kwargs / enable_thinking (Qwen3-VL-Instruct has
no thinking mode), n, stop, tools.

Usage:
  python local_llm_server.py --config config.yaml --gpu 0
"""

import argparse
import base64
import io
import logging
import os
import threading
import time
import uuid
from typing import Any, Dict, List, Optional

from rf_config import load_config

logger = logging.getLogger("local_llm_server")


def load_image(url: str):
    """OpenAI image_url -> PIL image. Supports data: URLs and local paths (no network fetch)."""
    from PIL import Image
    if url.startswith("data:"):
        return Image.open(io.BytesIO(base64.b64decode(url.split(",", 1)[1]))).convert("RGB")
    path = url[len("file://"):] if url.startswith("file://") else url
    if not os.path.isabs(path):
        raise ValueError(f"Unsupported image_url (only data: URLs or absolute local paths): {url[:80]}")
    return Image.open(path).convert("RGB")


def to_qwen_messages(messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """OpenAI chat messages -> Qwen3VLModel messages (text parts kept, image_url -> PIL image)."""
    converted = []
    for message in messages:
        role, content = message.get("role"), message.get("content")
        if role not in ("system", "user", "assistant"):
            raise ValueError(f"Unsupported role: {role}")
        if content is None or isinstance(content, str):
            converted.append({"role": role, "content": content or ""})
            continue
        parts = []
        for part in content:
            if part.get("type") == "text":
                parts.append({"type": "text", "text": part["text"]})
            elif part.get("type") == "image_url":
                image_url = part["image_url"]
                parts.append({"type": "image", "image": load_image(image_url["url"] if isinstance(image_url, dict) else image_url)})
            else:
                raise ValueError(f"Unsupported content part type: {part.get('type')}")
        converted.append({"role": role, "content": parts})
    return converted


def count_tokens(processor, messages: List[Dict[str, Any]], completion: str) -> Dict[str, int]:
    """Text-token usage for logging (image tokens are not counted)."""
    try:
        text_only = [{"role": m["role"], "content": m["content"] if isinstance(m["content"], str) else
                      [p for p in m["content"] if p["type"] == "text"]} for m in messages]
        prompt_text = processor.apply_chat_template(text_only, tokenize=False, add_generation_prompt=True)
        prompt_tokens = len(processor.tokenizer(prompt_text).input_ids)
        completion_tokens = len(processor.tokenizer(completion, add_special_tokens=False).input_ids)
    except Exception as e:
        logger.warning(f"Token counting failed: {e}")
        prompt_tokens = completion_tokens = 0
    return {"prompt_tokens": prompt_tokens, "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens}


def error_response(message: str, status: int, error_type: str = "invalid_request_error"):
    from flask import jsonify
    return jsonify({"error": {"message": message, "type": error_type}}), status


def create_app(llm, served_model: str, default_max_tokens: int, max_tokens_cap: Optional[int] = None):
    from flask import Flask, jsonify, request

    app = Flask(__name__)
    generate_lock = threading.Lock()
    processor = llm.model.processor

    @app.get("/health")
    def health():
        return jsonify({"status": "ok", "model": served_model})

    @app.get("/v1/models")
    def models():
        return jsonify({"object": "list", "data": [{"id": served_model, "object": "model", "owned_by": "local"}]})

    @app.post("/v1/chat/completions")
    def chat_completions():
        body = request.get_json(force=True, silent=True) or {}
        if body.get("stream"):
            return error_response("stream=true is not supported by this server", 400)
        if not body.get("messages"):
            return error_response("messages is required", 400)
        try:
            messages = to_qwen_messages(body["messages"])
        except (ValueError, KeyError, OSError) as e:
            return error_response(str(e), 400)

        max_tokens = int(body.get("max_tokens") or body.get("max_completion_tokens") or default_max_tokens)
        if max_tokens_cap:
            # P9: a writer repetition loop runs to the requested limit (Deep-Reporter always asks for 8192);
            # the cap bounds the time such a loop can take. Normal outputs measured on 2026-10-25 stayed <= 2,182.
            max_tokens = min(max_tokens, max_tokens_cap)
        gen_kwargs: Dict[str, Any] = {"max_new_tokens": max_tokens}
        if body.get("temperature") is not None:
            temperature = float(body["temperature"])
            gen_kwargs.update({"do_sample": False} if temperature == 0 else {"do_sample": True, "temperature": temperature})
        if body.get("top_p") is not None:
            gen_kwargs["top_p"] = float(body["top_p"])

        start = time.time()
        try:
            with generate_lock:
                content = llm.generate(messages, **gen_kwargs)
                # I28: the tokenizer is not thread-safe; counting outside the lock collided with the next
                # request's tokenization ("Already borrowed", retried inside WorldMM).
                usage = count_tokens(processor, messages, content)
        except Exception as e:
            logger.exception("Generation failed")
            return error_response(f"Generation failed: {e}", 500, "server_error")

        finish_reason = "length" if usage["completion_tokens"] >= max_tokens else "stop"
        logger.info(f"chat.completions: prompt={usage['prompt_tokens']} completion={usage['completion_tokens']} "
                    f"finish={finish_reason} {time.time() - start:.1f}s")
        return jsonify({
            "id": f"chatcmpl-{uuid.uuid4().hex}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": served_model,
            "choices": [{"index": 0, "message": {"role": "assistant", "content": content},
                         "finish_reason": finish_reason}],
            "usage": usage,
        })

    return app


def main() -> None:
    parser = argparse.ArgumentParser(description="Local OpenAI-compatible chat server (Qwen3-VL via transformers)")
    parser.add_argument("--config", required=True)
    parser.add_argument("--gpu", default=None, help="CUDA_VISIBLE_DEVICES for this process (set before torch import)")
    parser.add_argument("--port", type=int, default=None, help="Override llm.local.endpoint.port")
    args = parser.parse_args()

    cfg = load_config(args.config)
    endpoint = cfg["llm"]["local"]["endpoint"]
    if endpoint["server"] != "hf":
        raise SystemExit(f"config llm.local.endpoint.server={endpoint['server']}: this script serves only 'hf'")

    # Must be set before importing torch/transformers (via worldmm).
    os.environ["HF_HOME"] = cfg["paths"]["hf_home"]
    if args.gpu is not None:
        os.environ["CUDA_VISIBLE_DEVICES"] = args.gpu
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")

    from worldmm.llm import LLMModel

    served_model = endpoint["model"]
    logger.info(f"Loading {served_model} (HF_HOME={os.environ['HF_HOME']}, GPU={os.environ.get('CUDA_VISIBLE_DEVICES')})")
    llm = LLMModel(model_name=served_model)

    cap = endpoint.get("max_tokens_cap")
    app = create_app(llm, served_model, int(endpoint["default_max_tokens"]), int(cap) if cap else None)
    logger.info(f"max_tokens cap: {cap or 'none'}")
    port = args.port or int(endpoint["port"])
    logger.info(f"Serving OpenAI-compatible API at http://{endpoint['host']}:{port}/v1")
    app.run(host=endpoint["host"], port=port, threaded=True)


if __name__ == "__main__":
    main()
