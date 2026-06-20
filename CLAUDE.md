# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

ComfyUI custom node pack for generating prompts via LLM APIs and local models. Supports text generation, image/video reverse-prompting, audio/music tagging, and image captioning.

## Architecture

- `nodes.py` — Central node registry. All node classes are imported here and mapped in `NODE_CLASS_MAPPINGS` / `NODE_DISPLAY_NAME_MAPPINGS`. Add new nodes here.
- `deepseek.py` — DeepSeek V4 Flash/Pro via OpenAI-compatible API (`DEEPSEEK_API_KEY` env var).
- `qwen.py` — Qwen/Alibaba Cloud Bailian API nodes: text gen, image-to-text, video-to-text, audio-to-text (`DASHSCOPE_API_KEY` env var). Also contains `imgtensor_to_base64()` and `audio_tensor_to_mp3_base64()` helpers used only within this module.
- `gemini.py` — Google Gemini API nodes: text gen, multimodal (image/audio/video)-to-text, image generation, text file understanding (`GOOGLE_API_KEY` env var). Supports HTTP proxy. Also contains `imgtensor_to_bytes()` and `audio_tensor_to_mp3_bytes()` helpers.
- `ollama_prompt_gen.py` — Local Ollama models for prompt generation and image/video reverse-prompting. Dynamically lists installed Ollama models. Has its own `tensor_to_pil_image()`, `tensor_to_base64()`, `sample_video_frames()` helpers.
- `joycaption.py` — Local JoyCaption (LLaVA-based) image captioning with NF4 support. Supports single image input or batch directory processing. Global `MODEL_CACHE` singleton.
- `audio_to_prompt.py` — Ke-Omni-R local model for audio analysis/tagging (6 description variants + JSON output). Global `MODEL_CACHE` / `PROCESSOR_CACHE` singletons. `MultiLinePromptKOR` is a utility node for multiline prompt input.

## ComfyUI node conventions

Every node class follows this pattern:
- `INPUT_TYPES` classmethod — defines required/optional inputs with ComfyUI widget types (`STRING`, `IMAGE`, `AUDIO`, `INT`, `FLOAT`, `BOOLEAN`)
- `RETURN_TYPES` / `RETURN_NAMES` — output tuple definition
- `FUNCTION` — name of the method that does the work
- `CATEGORY` — always `"🎤MW/MW-Prompt-All-In-One"`

## API keys

Three environment variables for cloud APIs, checked in this priority order:
- `DEEPSEEK_API_KEY` → DeepSeek nodes (also accepts direct `api_key` input)
- `DASHSCOPE_API_KEY` → Qwen/Alibaba Cloud nodes (also accepts direct `api_key` input)
- `GOOGLE_API_KEY` → Gemini nodes (also accepts direct `api_key` input)

On Windows, a system restart may be needed for new env vars to take effect.

## Local models

Local models (JoyCaption, Ke-Omni-R) are loaded from `<ComfyUI models dir>/LLM/<model-name>/`. This path is derived from `folder_paths.models_dir`. Models must be downloaded manually — see README for HuggingFace links.

## No build/test/lint infrastructure

This is a ComfyUI plugin loaded at runtime by ComfyUI. There is no build step, test suite, or linter configuration. Installing dependencies is done via `pip install -r requirements.txt`.
