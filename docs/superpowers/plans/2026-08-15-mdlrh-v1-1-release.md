# MldrH v1.1 Release Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish the current MldrH Transformers/PEFT system as an additive GitHub v1.1.0 update.

**Architecture:** Create a portable release directory with config-based paths, bundle only the two adapters and terminal sources, and distribute the PT-only Chroma database as a separate Release ZIP. The setup script downloads public base models and the matching database asset, then validates the local configuration.

**Tech Stack:** Python 3.11, PyTorch CUDA BF16, Transformers, PEFT, SentenceTransformers, ChromaDB, prompt_toolkit, PowerShell, GitHub Releases.

## Global Constraints

- Preserve v1.0.0 and repository history.
- Do not publish base weights, raw corpora, staged conversational SFT vectors, paths, config, tokens, logs, or chats.
- Bundle Mdlr1.1-think and Mdlr-theory-embed-v1 adapters.
- Database asset must contain exactly 5089 `pt` records in collection `theory_knowledge`.
- Setup must not use Ollama, GGUF, or quantization.
- Verify package contents, hashes, tests, database metadata, Git status, and remote update before release creation.
