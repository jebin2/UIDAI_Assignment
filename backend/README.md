---
title: UIDAI Assignment HF Header
emoji: 🔐
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---

# UIDAI Sandbox - Secure Payload API

Backend for the UIDAI Sandbox E2EE Payload Simulator assignment.

## Environment Variables

Set these as Secrets in the Hugging Face Space settings:

| Variable | Description |
|---|---|
| `ALLOWED_ORIGINS` | Frontend URL e.g. `["https://jebin2.github.io"]` |
| `RSA_PRIVATE_KEY_PEM` | PEM private key (leave empty to use mock key) |
| `LOG_FILE_PATH` | Log file path (leave empty for console only) |
