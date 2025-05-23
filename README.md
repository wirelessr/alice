# Alice

Alice (“A**I**-powered **I**ntegration **C**ommand **E**ngine”) is a terminal-based tool that automatically generates and runs shell commands using AI agents. Built with PyInstaller and driven by a trio of collaborating AI agents (planning, execution, and verification), Alice takes your natural-language request, plans the appropriate command, executes it, and returns the results — all in one seamless flow.

---

## Features

- **Natural-language command generation**
  Ask Alice in plain English (or Chinese!) and let it figure out the right shell command for you.
- **Multi-agent architecture**
  Uses Autogen to coordinate a Planning Agent (to decide which command to run), an Execution Agent (to run it), and a Verification Agent (to check the result).
- **Configurable AI backend**
  Works out of the box with any OpenAI-compatible service (e.g. OpenRouter).
- **Portable single executable**
  Packaged via PyInstaller; no Python runtime required on the target machine.
- **Environment file / env-var support**
  Reads API keys and settings from `~/.alice/.env` or from environment variables.

---

## Installation

1. **Download the binary**
   Download the latest release for your OS from the GitHub Releases page.

2. **Make it executable**

   ```bash
   chmod +x alice
   ```

3. **Place it in your PATH**

   ```bash
   mv alice /usr/local/bin/
   ```

---

## Configuration

Alice needs your AI service credentials and optional settings. You can set them via:

1. **Environment file**
   Create `~/.alice/.env` with contents like:

   ```ini
   ALICE_MODEL=meta-llama/llama-4-scout:free
   ALICE_API_KEY=sk-...
   ALICE_BASE_URL=https://openrouter.ai/api/v1
   ```

2. **Environment variables**

   ```bash
   export ALICE_API_KEY="sk-…"
   export ALICE_BASE_URL="https://api.openrouter.ai/v1"
   export ALICE_MODEL="gpt-4"
   ```

Supported variables:

| Variable            | Description                                                                       |
| ------------------- | --------------------------------------------------------------------------------- |
| `ALICE_API_KEY`     | Your OpenAI or compatible API key                                                 |
| `ALICE_BASE_URL`    | Endpoint URL for your AI service (optional)                                       |
| `ALICE_MODEL`       | Model name to use (e.g. `gpt-4`)                                                  |
| `ALICE_LOG_LEVEL`   | (optional) `DEBUG`, `INFO`, `WARN`, `ERROR`                                       |
| `ALICE_SILENT_MODE` | (optional) `true`/`false` - Hide agent interactions, only show command and result |
| `ALICE_LANGUAGE`    | (optional) Response language code (e.g. "zh-TW", "en-US") - Default: "zh-TW"      |
| `ALICE_DEVICE_TYPE` | (optional) Device type (e.g. "macos", "windows", "linux") - Default: "macos"      |
| `ALICE_INTERACTIVE_MODE` | (optional) true/false - Enable interactive (human-in-the-loop) mode |
| `ALICE_PERSISTENT_MODE` | (optional) true/false - Enable persistent mode (cache results) |
| `ALICE_CACHE_SIZE` | (optional) int (MB) - Persistent cache size in MB (default: 500) |

### Command line options

| Option            | Env Variable         | Type    | Description                                      |
|-------------------|---------------------|---------|--------------------------------------------------|
| `-s`, `--silent`  | `ALICE_SILENT_MODE` | boolean | Enable silent mode (hide agent interaction)       |
| `-i`, `--interactive` | `ALICE_INTERACTIVE_MODE` | boolean | Enable interactive (human-in-the-loop) mode |
| `-v`, `--verbose` |  | boolean | Enable verbose mode (force disable silent mode) |
| `-p`, `--persistent` | `ALICE_PERSISTENT_MODE` | boolean | Enable persistent mode (cache results) |

---

## Using Ollama Models

Alice supports running local LLMs via [Ollama](https://ollama.com/). To use an Ollama model, simply set the `ALICE_MODEL` variable to a value prefixed with `ollama:` followed by your model name. For example:

```ini
ALICE_MODEL=ollama:llama3
```

This tells Alice to use the local Ollama server and the specified model (e.g., `llama3`).

**Requirements:**
- Make sure you have [Ollama](https://ollama.com/) installed and running on your machine.
- The Python dependency `autogen-ext[ollama]` must be installed (already included if you follow the default setup).

**Example:**

```ini
ALICE_MODEL=ollama:llama3
```

No API key or base URL is required for Ollama models.

---

## Usage

Run Alice with a natural-language instruction. For example:

```bash
alice Find the largest file in the current directory
```

You can also use command line options to override config. For example, to enable silent mode:

```bash
alice -s Find the largest file in the current directory
```

Alice will then:

1. **Plan** the shell command:

   ```
   du -h * | sort -hr | head -1
   ```

2. **Execute** it in your shell environment.
3. **Verify** the output for correctness.
4. **Return** the result to your terminal.

---

## Architecture

Alice leverages three cooperating AI agents via Autogen:

1. **Planning Agent**

   - Parses your request
   - Chooses or composes the shell command to achieve the goal

2. **Execution Agent**

   - Runs the generated command in a safe subprocess
   - Captures stdout/stderr

3. **Verification Agent**

   - Analyzes the output
   - Ensures it matches the original intent (re-asks Planning if needed)

---

## Example

```bash
$ alice "Count all `.py` files in this directory and its subdirectories"
Counting `.py` files in `/home/user/project`...

> Planning: `find . -name '*.py' | wc -l`
> Executing…
> Verification: Output is a number ✅

Result:
```

125

---

## Troubleshooting

- **"API key not found"**
  Ensure `ALICE_API_KEY` is set in `~/.alice/.env` or as an env var.

- **"Model not available"**
  Verify that your `ALICE_MODEL` are correctly configured.

- **Logging**
  Set `ALICE_LOG_LEVEL=DEBUG` for verbose logs:

```bash
export ALICE_LOG_LEVEL=DEBUG
alice "…"
```

- **macOS: "Apple cannot check for malicious software"**
  If you see a Gatekeeper warning when running the binary, run:
  ```bash
  xattr -d com.apple.quarantine ./alice
  ```
  This will remove the quarantine flag and allow execution.

---

## Contributing

1. Fork the repo
2. Make your changes in a feature branch
3. Submit a pull request

Please adhere to the existing code style and write tests for new features.

---

## License

MIT License
© 2025 CT Wu
