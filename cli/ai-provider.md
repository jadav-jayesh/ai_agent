# AI Provider Interface

## Purpose

Defines how the framework talks to language model providers.

## Supported providers

- OpenAI
- Groq
- OpenRouter
- Ollama

## Environment variables

Create a `.env` file in the project root to store your keys.

```bash
OPENAI_API_KEY=
GROQ_API_KEY=
OPENROUTER_API_KEY=
```

## Provider contract

Each provider implementation should accept:

- `systemPrompt`
- `userPrompt`
- `model`
- `temperature`

Each provider implementation should return:

- plain text containing a structured JSON response

## Notes

- Ollama is local-first and may not require an API key
- OpenAI-compatible providers should reuse one shared request shape where possible
