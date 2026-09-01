# Grathon — Agent Instructions

When working with this project, **always read the `.ai-context/` directory first** for comprehensive project documentation.

## Required Reading Order

1. `.ai-context/README.md` — Project overview, structure, and key concepts
2. `.ai-context/API.md` — Full API reference for all classes and methods
3. `.ai-context/ARCHITECTURE.md` — Architecture layers and data flow
4. `.ai-context/RULES.md` — Coding rules and conventions (must follow)
5. `.ai-context/FAQ.md` — Common questions and troubleshooting
6. `.ai-context/EXAMPLES.md` — Usage examples

## Why `.ai-context/`?

This directory contains the **authoritative, up-to-date documentation** for the Grathon framework. It is maintained alongside the source code and reflects the current state of the project. Do not rely on scattered README files or inline comments alone.

## Project Overview

Grathon is a Python Telegram bot framework built on TDLib (via `tdjson`). It provides an async-first API with plugin-based architecture, filter DSL, and high-level helpers.

## Key Entry Points

- `grathon/__init__.py` — Public exports (`GrathonBot`, `F`, `RateLimitManager`, etc.)
- `grathon/grathon_bot.py` — Main bot class
- `grathon/high_level/` — High-level helpers (filters, keyboards, plugin manager, scheduler, etc.)
- `grathon/core/` — Core TDLib communication layer

## Important Rules

- Always use `ctx.match` (not `match_callback`) for callback query regex matching — `CallbackQueryCtx` exposes `match`
- Never use `F.from_user(*config.ADMINS)` for admin checks — use `F.from_user(user_ids_fn=lambda: config.ADMINS)` for live lookups
- Always use `edit_message_caption` for media messages, not `edit_message_text`
- Always use `KeyboardBuilder.button()` for callback data > 64 bytes (auto-compresses via `CallbackStore`)
- Never import from `utils/` — that module belongs to external projects (Babone/FileHolder), not Grathon itself

## Running the Bot

See the "Running the Bot" section in `.ai-context/README.md` for the full `main.py` pattern including middleware installation, plugin manager setup, scheduler, and graceful shutdown.